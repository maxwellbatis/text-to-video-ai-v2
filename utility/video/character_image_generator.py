import os
import requests
import json
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus
import time
try:
    from .globo_actor_scraper import GloboActorScraper
except ImportError:
    from globo_actor_scraper import GloboActorScraper

class CharacterImageGenerator:
    def __init__(self):
        self.pexels_key = os.environ.get('PEXELS_KEY')
        self.unsplash_key = os.environ.get('UNSPLASH_KEY')
        self.globo_scraper = GloboActorScraper()
        
        # Mapeamento de atores/atrizes reais por novela - Baseado no site oficial da Globo
        self.actor_database = {
            "dona de mim": {
                # Personagens principais mencionados no resumo
                "luana": ["Giulia Gayoso", "Giulia Gayoso atriz", "Giulia Gayoso novela"],
                "marina": ["Sheron Menezzes", "Sheron Menezzes atriz", "Sheron Menezzes novela"],
                "marina silva": ["Sheron Menezzes", "Sheron Menezzes atriz", "Sheron Menezzes novela"],
                "marina ricardo": ["Sheron Menezzes", "Sheron Menezzes atriz", "Sheron Menezzes novela"],
                "ricardo": ["Marcos Pasquim", "Marcos Pasquim ator", "Marcos Pasquim novela"],
                "ricardo cuba": ["Marcos Pasquim", "Marcos Pasquim ator", "Marcos Pasquim novela"],
                "ricardo cubba": ["Marcos Pasquim", "Marcos Pasquim ator", "Marcos Pasquim novela"],
                
                # Outros personagens importantes da novela
                "abel": ["Tony Ramos", "Tony Ramos ator", "Tony Ramos novela"],
                "alan": ["Hugo Resende", "Hugo Resende ator", "Hugo Resende novela"],
                "ayla": ["Bel Lima", "Bel Lima atriz", "Bel Lima novela"],
                "bárbara": ["Giovana Cordeiro", "Giovana Cordeiro atriz", "Giovana Cordeiro novela"],
                "breno": ["Gabriel Sanches", "Gabriel Sanches ator", "Gabriel Sanches novela"],
                "caco": ["Pedro Alves", "Pedro Alves ator", "Pedro Alves novela"],
                "danilo": ["Felipe Simas", "Felipe Simas ator", "Felipe Simas novela"],
                "dara": ["Cecília Chancez", "Cecília Chancez atriz", "Cecília Chancez novela"],
                "davi": ["Rafael Vitti", "Rafael Vitti ator", "Rafael Vitti novela"],
                "dedé": ["Lorenzo Reis", "Lorenzo Reis ator", "Lorenzo Reis novela"],
                "denise": ["Cris Larin", "Cris Larin atriz", "Cris Larin novela"],
                "ellen": ["Camila Pitanga", "Camila Pitanga atriz", "Camila Pitanga novela"],
                "filipa": ["Cláudia Abreu", "Cláudia Abreu atriz", "Cláudia Abreu novela"],
                "gisele": ["Luana Tanaka", "Luana Tanaka atriz", "Luana Tanaka novela"],
                "isabela": ["Sylvia Bandeira", "Sylvia Bandeira atriz", "Sylvia Bandeira novela"],
                "jaques": ["Marcello Novaes", "Marcello Novaes ator", "Marcello Novaes novela"],
                "jeff": ["Faíska Alves", "Faíska Alves ator", "Faíska Alves novela"],
                "jussara": ["Vilma Melo", "Vilma Melo atriz", "Vilma Melo novela"],
                "kamila": ["Giovanna Lancellotti", "Giovanna Lancellotti atriz", "Giovanna Lancellotti novela"],
                "leona": ["Clara Moneke", "Clara Moneke atriz", "Clara Moneke novela"],
                "lucas": ["Pedro Henrique Ferreira", "Pedro Henrique Ferreira ator", "Pedro Henrique Ferreira novela"],
                "luisão": ["Adélio Lima", "Adélio Lima ator", "Adélio Lima novela"],
                "marlon": ["Humberto Morais", "Humberto Morais ator", "Humberto Morais novela"],
                "natara": ["Carol Marra", "Carol Marra atriz", "Carol Marra novela"],
                "nina": ["Flora Camolese", "Flora Camolese atriz", "Flora Camolese novela"],
                "pam": ["Haonê Thinar", "Haonê Thinar atriz", "Haonê Thinar novela"],
                "peter": ["Pedro Fernandes", "Pedro Fernandes ator", "Pedro Fernandes novela"],
                "rosa": ["Suely Franco", "Suely Franco atriz", "Suely Franco novela"],
                "ryan": ["L7nnon", "L7nnon ator", "L7nnon novela"],
                "samuel": ["Juan Paiva", "Juan Paiva ator", "Juan Paiva novela"],
                "seu manuel": ["Ernani Moraes", "Ernani Moraes ator", "Ernani Moraes novela"],
                "sofia": ["Elis Cabral", "Elis Cabral atriz", "Elis Cabral novela"],
                "stephany": ["Nikolly Fernandes", "Nikolly Fernandes atriz", "Nikolly Fernandes novela"],
                "tânia": ["Aline Borges", "Aline Borges atriz", "Aline Borges novela"],
                "vanderson": ["Armando Babaioff", "Armando Babaioff ator", "Armando Babaioff novela"],
                "yara": ["Cyda Moreno", "Cyda Moreno atriz", "Cyda Moreno novela"],
                
                # Mapeamentos genéricos para fallback
                "maria": ["Giulia Gayoso", "Giulia Gayoso atriz", "Giulia Gayoso novela"],
                "joão": ["Marcos Pasquim", "Marcos Pasquim ator", "Marcos Pasquim novela"],
                "vilão": ["Tony Ramos", "Tony Ramos ator", "Tony Ramos novela"],
                "mocinha": ["Giulia Gayoso", "Giulia Gayoso atriz", "Giulia Gayoso novela"],
                "mocinho": ["Marcos Pasquim", "Marcos Pasquim ator", "Marcos Pasquim novela"]
            },
            "fuzuê": {
                "luna": ["Larissa Manoela", "Larissa Manoela atriz", "Larissa Manoela novela"],
                "dante": ["João Guilherme", "João Guilherme ator", "João Guilherme novela"],
                "vilão": ["Marcos Palmeira", "Marcos Palmeira ator", "Marcos Palmeira novela"],
                "mocinha": ["Larissa Manoela", "Larissa Manoela atriz", "Larissa Manoela novela"],
                "mocinho": ["João Guilherme", "João Guilherme ator", "João Guilherme novela"]
            },
            "vai na fé": {
                "sol": ["Sheron Menezzes", "Sheron Menezzes atriz", "Sheron Menezzes novela"],
                "daniel": ["Emilio Dantas", "Emilio Dantas ator", "Emilio Dantas novela"],
                "vilão": ["Marcos Palmeira", "Marcos Palmeira ator", "Marcos Palmeira novela"],
                "mocinha": ["Sheron Menezzes", "Sheron Menezzes atriz", "Sheron Menezzes novela"],
                "mocinho": ["Emilio Dantas", "Emilio Dantas ator", "Emilio Dantas novela"]
            },
            "terra e paixão": {
                "alice": ["Bárbara Reis", "Bárbara Reis atriz", "Bárbara Reis novela"],
                "caio": ["Cauã Reymond", "Cauã Reymond ator", "Cauã Reymond novela"],
                "vilão": ["Tony Ramos", "Tony Ramos ator", "Tony Ramos novela"],
                "mocinha": ["Bárbara Reis", "Bárbara Reis atriz", "Bárbara Reis novela"],
                "mocinho": ["Cauã Reymond", "Cauã Reymond ator", "Cauã Reymond novela"]
            }
        }
    
    def extract_character_info(self, text: str) -> Dict[str, str]:
        """
        Extrai informações sobre personagens do texto
        """
        text_lower = text.lower()
        
        # Detectar novela
        novela_name = None
        for novela in self.actor_database.keys():
            if novela in text_lower:
                novela_name = novela
                break
        
        if not novela_name:
            return {"novela": "geral", "personagem": "personagem", "tipo": "genérico"}
        
        # Detectar personagem
        personagem = "personagem"
        tipo = "genérico"
        
        # Buscar por nomes específicos de atores
        for char_name, actor_names in self.actor_database[novela_name].items():
            if char_name in text_lower:
                personagem = actor_names[0]  # Nome real do ator
                tipo = char_name
                break
        
        # Buscar por padrões específicos no texto
        if "marina" in text_lower and "continuou" in text_lower:
            personagem = "Sheron Menezzes"
            tipo = "marina"
        elif "ricardo" in text_lower and ("cuba" in text_lower or "cubba" in text_lower):
            personagem = "Marcos Pasquim"
            tipo = "ricardo"
        
        # Buscar por tipos genéricos
        if "protagonista" in text_lower or "principal" in text_lower:
            personagem = "protagonista"
            tipo = "protagonista"
        elif "vilão" in text_lower or "antagonista" in text_lower:
            personagem = "vilão"
            tipo = "antagonista"
        elif "mocinha" in text_lower or "heroína" in text_lower:
            personagem = "mocinha"
            tipo = "mocinha"
        elif "mocinho" in text_lower or "herói" in text_lower:
            personagem = "mocinho"
            tipo = "mocinho"
        
        return {
            "novela": novela_name,
            "personagem": personagem,
            "tipo": tipo
        }
    
    def extract_all_characters_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extrai TODOS os personagens mencionados no texto
        """
        text_lower = text.lower()
        characters_found = []
        
        # Detectar novela
        novela_name = None
        for novela in self.actor_database.keys():
            if novela in text_lower:
                novela_name = novela
                break
        
        if not novela_name:
            return [{"novela": "geral", "personagem": "personagem", "tipo": "genérico"}]
        
        # Buscar TODOS os personagens mencionados no texto
        for char_name, actor_names in self.actor_database[novela_name].items():
            if char_name in text_lower:
                characters_found.append({
                    "novela": novela_name,
                    "personagem": actor_names[0],  # Nome real do ator
                    "tipo": char_name,
                    "original_name": char_name
                })
        
        # Buscar por padrões específicos no texto
        if "marina" in text_lower and "continuou" in text_lower:
            # Verificar se já não foi adicionado
            if not any(c["tipo"] == "marina" for c in characters_found):
                characters_found.append({
                    "novela": novela_name,
                    "personagem": "Sheron Menezzes",
                    "tipo": "marina",
                    "original_name": "marina"
                })
        
        if "ricardo" in text_lower and ("cuba" in text_lower or "cubba" in text_lower):
            # Verificar se já não foi adicionado
            if not any(c["tipo"] == "ricardo" for c in characters_found):
                characters_found.append({
                    "novela": novela_name,
                    "personagem": "Marcos Pasquim",
                    "tipo": "ricardo",
                    "original_name": "ricardo"
                })
        
        # Se não encontrou nenhum personagem específico, usar genéricos
        if not characters_found:
            characters_found.append({
                "novela": novela_name,
                "personagem": "personagem",
                "tipo": "genérico",
                "original_name": "personagem"
            })
        
        return characters_found
    
    def search_character_image_google(self, query: str) -> Optional[str]:
        """
        Busca imagem de personagem no Google Images
        """
        try:
            # Construir consultas mais específicas para atores
            search_queries = [
                f"{query} ator atriz novela globo",
                f"{query} ator atriz novela 2024",
                f"{query} ator atriz novela",
                f"{query} ator atriz",
                f"{query} novela",
                f"{query} foto",
                f"{query} imagem"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            for search_query in search_queries:
                try:
                    # Construir URL do Google Images
                    encoded_query = quote_plus(search_query)
                    url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&tbs=isz:l"
                    
                    response = requests.get(url, headers=headers, timeout=20)
                    
                    if response.status_code == 200:
                        # Extrair URLs de imagens da resposta HTML
                        import re
                        # Padrões mais abrangentes para imagens
                        img_patterns = [
                            r'https://[^"]*\.(?:jpg|jpeg|png|webp)(?:\?[^"]*)?',
                            r'https://[^"]*\.googleusercontent\.com/[^"]*',
                            r'https://[^"]*\.gstatic\.com/[^"]*',
                            r'https://[^"]*\.(?:com|org|net)/[^"]*\.(?:jpg|jpeg|png|webp)',
                            r'https://[^"]*\.(?:com|org|net)/[^"]*\.(?:jpg|jpeg|png|webp)(?:\?[^"]*)?'
                        ]
                        
                        for pattern in img_patterns:
                            img_urls = re.findall(pattern, response.text)
                            if img_urls:
                                # Filtrar URLs válidas
                                valid_urls = []
                                for url in img_urls:
                                    if ('http' in url and 
                                        not url.endswith('.js') and 
                                        not url.endswith('.css') and
                                        not url.endswith('.html') and
                                        len(url) > 20):
                                        valid_urls.append(url)
                                
                                if valid_urls:
                                    print(f"🔍 Encontradas {len(valid_urls)} imagens para: {search_query}")
                                    # Retornar a primeira URL válida
                                    return valid_urls[0]
                    
                    # Pequena pausa entre requisições
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"⚠️ Erro na busca específica '{search_query}': {e}")
                    continue
            
            return None
            
        except Exception as e:
            print(f"⚠️ Erro geral na busca Google: {e}")
            return None

    def search_character_image_pexels(self, query: str, orientation: str = "portrait") -> Optional[str]:
        """
        Busca imagem de personagem no Pexels
        """
        if not self.pexels_key:
            return None
        
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {
                "Authorization": self.pexels_key,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            params = {
                "query": query,
                "orientation": orientation,
                "per_page": 10,
                "size": "large"
            }
            
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if data.get('photos') and len(data['photos']) > 0:
                # Escolher a primeira imagem de alta qualidade
                photo = data['photos'][0]
                return photo['src']['large']
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar no Pexels: {e}")
            return None
    
    def search_character_image_unsplash(self, query: str) -> Optional[str]:
        """
        Busca imagem de personagem no Unsplash
        """
        if not self.unsplash_key:
            return None
        
        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {
                "Authorization": f"Client-ID {self.unsplash_key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            params = {
                "query": query,
                "orientation": "portrait",
                "per_page": 10
            }
            
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                # Escolher a primeira imagem
                photo = data['results'][0]
                return photo['urls']['regular']
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar no Unsplash: {e}")
            return None
    
    def generate_character_search_queries(self, character_info: Dict[str, str]) -> List[str]:
        """
        Gera consultas de busca para personagens
        """
        novela = character_info["novela"]
        personagem = character_info["personagem"]
        tipo = character_info["tipo"]
        
        queries = []
        
        # Consultas específicas para o ator/atriz
        if personagem != "personagem":
            queries.extend([
                f"{personagem} ator",
                f"{personagem} atriz", 
                f"{personagem} {novela}",
                f"{personagem} globo",
                f"{personagem} novela"
            ])
        
        # Consultas por tipo
        if tipo == "protagonista":
            queries.extend([
                "protagonista novela",
                "personagem principal",
                "heroi heroina"
            ])
        elif tipo == "antagonista":
            queries.extend([
                "vilão novela",
                "antagonista",
                "personagem malvado"
            ])
        elif tipo == "mocinha":
            queries.extend([
                "mocinha novela",
                "jovem mulher",
                "heroina"
            ])
        elif tipo == "mocinho":
            queries.extend([
                "mocinho novela",
                "jovem homem",
                "heroi"
            ])
        
        # Consultas genéricas
        queries.extend([
            "ator atriz novela",
            "personagem televisão",
            "rosto expressivo"
        ])
        
        return queries
    
    def get_character_image(self, text: str) -> Optional[str]:
        """
        Obtém imagem de personagem baseada no texto
        """
        character_info = self.extract_character_info(text)
        queries = self.generate_character_search_queries(character_info)
        
        print(f"🎭 Buscando imagem para: {character_info['personagem']} ({character_info['tipo']})")
        
        # Para atores reais, usar PRIMEIRO o site da Globo, depois Google Images
        if character_info['personagem'] != "personagem":
            print(f"🔍 Buscando ator real: {character_info['personagem']}")
            
            # 1. Tentar primeiro no site oficial da Globo
            globo_image = self.globo_scraper.get_actor_image_from_globo(character_info['personagem'])
            if globo_image:
                print(f"✅ Imagem encontrada no site da Globo: {character_info['personagem']}")
                return globo_image
            
            # 2. Se não encontrou na Globo, tentar Google Images
            for query in queries[:5]:  # Mais consultas para atores reais
                image_url = self.search_character_image_google(query)
                if image_url:
                    print(f"✅ Imagem encontrada no Google: {query}")
                    return image_url
            
            # Se não encontrou em nenhum lugar, não usar Pexels/Unsplash para atores reais
            print(f"❌ Nenhuma imagem encontrada para: {character_info['personagem']}")
            return None
        
        # Para personagens genéricos, usar Pexels/Unsplash
        print(f"🔍 Buscando personagem genérico")
        for query in queries:
            image_url = self.search_character_image_pexels(query)
            if image_url:
                print(f"✅ Imagem encontrada no Pexels: {query}")
                return image_url
        
        for query in queries:
            image_url = self.search_character_image_unsplash(query)
            if image_url:
                print(f"✅ Imagem encontrada no Unsplash: {query}")
                return image_url
        
        print(f"❌ Nenhuma imagem encontrada para: {character_info['personagem']}")
        return None
    
    def get_all_character_images_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Obtém imagens de TODOS os personagens mencionados no texto
        """
        characters = self.extract_all_characters_from_text(text)
        results = []
        
        print(f"🎭 Encontrados {len(characters)} personagens no texto")
        
        for character in characters:
            print(f"\n🔍 Processando: {character['personagem']} ({character['tipo']})")
            
            # Buscar imagem para este personagem
            image_url = None
            
            if character['personagem'] != "personagem":
                # Para atores reais, usar Globo primeiro
                image_url = self.globo_scraper.get_actor_image_from_globo(character['personagem'])
                if image_url:
                    print(f"✅ Imagem encontrada no site da Globo: {character['personagem']}")
                else:
                    # Tentar Google Images
                    queries = self.generate_character_search_queries(character)
                    for query in queries[:3]:
                        image_url = self.search_character_image_google(query)
                        if image_url:
                            print(f"✅ Imagem encontrada no Google: {query}")
                            break
            else:
                # Para personagens genéricos, usar Pexels/Unsplash
                queries = self.generate_character_search_queries(character)
                for query in queries:
                    image_url = self.search_character_image_pexels(query)
                    if image_url:
                        print(f"✅ Imagem encontrada no Pexels: {query}")
                        break
                
                if not image_url:
                    for query in queries:
                        image_url = self.search_character_image_unsplash(query)
                        if image_url:
                            print(f"✅ Imagem encontrada no Unsplash: {query}")
                            break
            
            # Adicionar resultado
            result = character.copy()
            result['image_url'] = image_url
            results.append(result)
            
            if image_url:
                print(f"✅ Imagem encontrada para {character['personagem']}")
            else:
                print(f"❌ Nenhuma imagem encontrada para {character['personagem']}")
        
        return results
    
    def get_multiple_character_images(self, text: str, count: int = 3) -> List[str]:
        """
        Obtém múltiplas imagens de personagens
        """
        character_info = self.extract_character_info(text)
        queries = self.generate_character_search_queries(character_info)
        
        images = []
        
        # Buscar no Pexels
        if self.pexels_key:
            for query in queries[:count]:
                image_url = self.search_character_image_pexels(query)
                if image_url and image_url not in images:
                    images.append(image_url)
                    if len(images) >= count:
                        break
        
        # Completar com Unsplash se necessário
        if len(images) < count and self.unsplash_key:
            for query in queries[:count]:
                image_url = self.search_character_image_unsplash(query)
                if image_url and image_url not in images:
                    images.append(image_url)
                    if len(images) >= count:
                        break
        
        return images
    
    def download_character_image(self, image_url: str, filename: str) -> Optional[str]:
        """
        Baixa imagem de personagem
        """
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Criar diretório se não existir
            os.makedirs("character_images", exist_ok=True)
            
            filepath = f"character_images/{filename}.jpg"
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Imagem baixada: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro ao baixar imagem: {e}")
            return None

# Função para testar o gerador
def test_character_image_generator():
    """
    Testa o gerador de imagens de personagens
    """
    generator = CharacterImageGenerator()
    
    test_texts = [
        "Maria é a protagonista de Dona de Mim",
        "O vilão de Fuzuê está causando problemas",
        "A mocinha de Vai na Fé está apaixonada",
        "O mocinho de Terra e Paixão é muito bonito"
    ]
    
    print("🎭 Testando Gerador de Imagens de Personagens")
    print("=" * 50)
    
    for text in test_texts:
        print(f"\n📝 Texto: {text}")
        print("-" * 30)
        
        character_info = generator.extract_character_info(text)
        print(f"🎭 Personagem: {character_info['personagem']}")
        print(f"📺 Novela: {character_info['novela']}")
        print(f"🏷️ Tipo: {character_info['tipo']}")
        
        # Buscar imagem
        image_url = generator.get_character_image(text)
        if image_url:
            print(f"🖼️ Imagem: {image_url}")
        else:
            print("❌ Nenhuma imagem encontrada")
        
        print()

if __name__ == "__main__":
    test_character_image_generator() 