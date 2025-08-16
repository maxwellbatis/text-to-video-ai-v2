import requests
import re
import json
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

class NovelaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # URLs das novelas
        self.novela_urls = {
            "dona de mim": "https://gshow.globo.com/novelas/dona-de-mim/resumo/",
            "fuzuê": "https://gshow.globo.com/novelas/fuzue/resumo/",
            "vai na fé": "https://gshow.globo.com/novelas/vai-na-fe/resumo/",
            "terra e paixão": "https://gshow.globo.com/novelas/terra-e-paixao/resumo/"
        }
        
        # Mapeamento de atores/atrizes conhecidos
        self.actor_database = {
            "dona de mim": {
                "maria": ["Giulia Gayoso", "Giulia", "Gayoso"],
                "joão": ["Gabriel Leone", "Gabriel", "Leone"],
                "vilão": ["Marcos Palmeira", "Marcos", "Palmeira"],
                "mocinha": ["Giulia Gayoso", "Giulia", "Gayoso"],
                "mocinho": ["Gabriel Leone", "Gabriel", "Leone"]
            },
            "fuzuê": {
                "luna": ["Larissa Manoela", "Larissa", "Manoela"],
                "dante": ["João Guilherme", "João", "Guilherme"],
                "vilão": ["Marcos Palmeira", "Marcos", "Palmeira"],
                "mocinha": ["Larissa Manoela", "Larissa", "Manoela"],
                "mocinho": ["João Guilherme", "João", "Guilherme"]
            },
            "vai na fé": {
                "sol": ["Sheron Menezzes", "Sheron", "Menezzes"],
                "daniel": ["Emilio Dantas", "Emilio", "Dantas"],
                "vilão": ["Marcos Palmeira", "Marcos", "Palmeira"],
                "mocinha": ["Sheron Menezzes", "Sheron", "Menezzes"],
                "mocinho": ["Emilio Dantas", "Emilio", "Dantas"]
            },
            "terra e paixão": {
                "alice": ["Bárbara Reis", "Bárbara", "Reis"],
                "caio": ["Cauã Reymond", "Cauã", "Reymond"],
                "vilão": ["Tony Ramos", "Tony", "Ramos"],
                "mocinha": ["Bárbara Reis", "Bárbara", "Reis"],
                "mocinho": ["Cauã Reymond", "Cauã", "Reymond"]
            }
        }
    
    def get_novela_resumo(self, novela_name: str) -> Optional[Dict]:
        """
        Busca resumo real da novela
        """
        novela_lower = novela_name.lower()
        
        if novela_lower not in self.novela_urls:
            print(f"❌ Novela '{novela_name}' não suportada")
            return None
        
        url = self.novela_urls[novela_lower]
        
        try:
            print(f"🔍 Buscando resumo de {novela_name} em: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair título
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else f"Resumo de {novela_name}"
            
            # Extrair conteúdo do resumo
            content = ""
            
            # Tentar diferentes seletores para encontrar o conteúdo
            selectors = [
                '.content-text__container',
                '.content-text',
                '.post-content',
                '.entry-content',
                'article',
                '.resumo-content'
            ]
            
            for selector in selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text().strip()
                    break
            
            if not content:
                # Fallback: buscar parágrafos
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            # Extrair personagens mencionados
            characters = self.extract_characters_from_text(content, novela_lower)
            
            return {
                "novela": novela_name,
                "title": title_text,
                "content": content,
                "characters": characters,
                "url": url
            }
            
        except Exception as e:
            print(f"❌ Erro ao buscar resumo de {novela_name}: {e}")
            return None
    
    def extract_characters_from_text(self, text: str, novela_name: str) -> List[Dict]:
        """
        Extrai personagens reais do texto
        """
        characters = []
        
        # Buscar por nomes de atores conhecidos
        if novela_name in self.actor_database:
            for character_type, actor_names in self.actor_database[novela_name].items():
                for actor_name in actor_names:
                    if actor_name.lower() in text.lower():
                        characters.append({
                            "name": actor_name,
                            "character_type": character_type,
                            "novela": novela_name,
                            "search_terms": [actor_name, f"{actor_name} ator", f"{actor_name} atriz"]
                        })
                        break
        
        # Buscar por nomes de personagens mencionados no texto
        character_patterns = [
            r'([A-Z][a-z]+)\s+(?:é|está|estava|foi|será)',
            r'(?:personagem|protagonista|vilão|mocinha|mocinho)\s+([A-Z][a-z]+)',
            r'([A-Z][a-z]+)\s+(?:de|da|do)\s+[A-Z][a-z]+'
        ]
        
        for pattern in character_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 2 and match not in [char["name"] for char in characters]:
                    characters.append({
                        "name": match,
                        "character_type": "mencionado",
                        "novela": novela_name,
                        "search_terms": [match, f"{match} ator", f"{match} atriz"]
                    })
        
        return characters
    
    def search_actor_images(self, actor_name: str, novela_name: str) -> List[str]:
        """
        Busca imagens do ator/atriz real
        """
        search_queries = [
            f"{actor_name} ator",
            f"{actor_name} atriz",
            f"{actor_name} {novela_name}",
            f"{actor_name} globo",
            f"{actor_name} novela"
        ]
        
        image_urls = []
        
        # Aqui você pode integrar com APIs de busca de imagens
        # Por enquanto, retornamos as queries para uso posterior
        return search_queries
    
    def get_complete_novela_info(self, novela_name: str) -> Optional[Dict]:
        """
        Obtém informações completas da novela: resumo + personagens + imagens
        """
        print(f"🎬 Buscando informações completas de {novela_name}")
        
        # Buscar resumo
        resumo = self.get_novela_resumo(novela_name)
        if not resumo:
            return None
        
        # Buscar imagens dos personagens
        for character in resumo["characters"]:
            character["image_queries"] = self.search_actor_images(
                character["name"], 
                novela_name
            )
        
        return resumo

# Função para testar o scraper
def test_novela_scraper():
    """
    Testa o scraper de novelas
    """
    scraper = NovelaScraper()
    
    novelas = ["Dona de Mim", "Fuzuê", "Vai na Fé", "Terra e Paixão"]
    
    print("🎬 Testando Scraper de Novelas")
    print("=" * 50)
    
    for novela in novelas:
        print(f"\n📺 Buscando: {novela}")
        print("-" * 30)
        
        info = scraper.get_complete_novela_info(novela)
        
        if info:
            print(f"✅ Título: {info['title']}")
            print(f"📝 Conteúdo: {info['content'][:200]}...")
            print(f"🎭 Personagens encontrados: {len(info['characters'])}")
            
            for char in info['characters']:
                print(f"   • {char['name']} ({char['character_type']})")
                print(f"     Busca: {char['image_queries'][:2]}")
        else:
            print("❌ Erro ao buscar informações")
        
        print()

if __name__ == "__main__":
    test_novela_scraper() 