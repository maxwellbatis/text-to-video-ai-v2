import os
import requests
import json
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus
import time

class CharacterImageGenerator:
    def __init__(self):
        self.pexels_key = os.environ.get('PEXELS_KEY')
        self.unsplash_key = os.environ.get('UNSPLASH_KEY')
        
        # Mapeamento de atores/atrizes reais por novela
        self.actor_database = {
            "dona de mim": {
                "luana": ["Giulia Gayoso", "Giulia Gayoso atriz", "Giulia Gayoso novela"],
                "marina": ["Sheron Menezzes", "Sheron Menezzes atriz", "Sheron Menezzes novela"],
                "ricardo": ["Gabriel Leone", "Gabriel Leone ator", "Gabriel Leone novela"],
                "ricardo cuba": ["Gabriel Leone", "Gabriel Leone ator", "Gabriel Leone novela"],
                "ricardo cubba": ["Gabriel Leone", "Gabriel Leone ator", "Gabriel Leone novela"],
                "maria": ["Giulia Gayoso", "Giulia Gayoso atriz", "Giulia Gayoso novela"],
                "joão": ["Gabriel Leone", "Gabriel Leone ator", "Gabriel Leone novela"],
                "vilão": ["Marcos Palmeira", "Marcos Palmeira ator", "Marcos Palmeira novela"],
                "mocinha": ["Giulia Gayoso", "Giulia Gayoso atriz", "Giulia Gayoso novela"],
                "mocinho": ["Gabriel Leone", "Gabriel Leone ator", "Gabriel Leone novela"]
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
    
    def search_character_image_google(self, query: str) -> Optional[str]:
        """
        Busca imagem de personagem no Google Images
        """
        try:
            # Usar a API do Google Custom Search para imagens
            # Primeiro, vamos usar uma abordagem alternativa com requests
            search_query = f"{query} ator atriz novela"
            
            # Construir URL do Google Images
            encoded_query = quote_plus(search_query)
            url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&tbs=isz:l"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Extrair URLs de imagens da resposta HTML
                import re
                img_pattern = r'https://[^"]*\.(?:jpg|jpeg|png|webp)'
                img_urls = re.findall(img_pattern, response.text)
                
                if img_urls:
                    # Retornar a primeira imagem encontrada
                    return img_urls[0]
            
            return None
            
        except Exception as e:
            print(f"⚠️ Erro na busca Google: {e}")
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
        
        # Tentar Google Images primeiro (para atores reais)
        if character_info['personagem'] != "personagem":
            for query in queries[:3]:  # Primeiras 3 consultas mais específicas
                image_url = self.search_character_image_google(query)
                if image_url:
                    print(f"✅ Imagem encontrada no Google: {query}")
                    return image_url
        
        # Tentar Pexels como fallback
        for query in queries:
            image_url = self.search_character_image_pexels(query)
            if image_url:
                print(f"✅ Imagem encontrada no Pexels: {query}")
                return image_url
        
        # Tentar Unsplash como último recurso
        for query in queries:
            image_url = self.search_character_image_unsplash(query)
            if image_url:
                print(f"✅ Imagem encontrada no Unsplash: {query}")
                return image_url
        
        print(f"❌ Nenhuma imagem encontrada para: {character_info['personagem']}")
        return None
    
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