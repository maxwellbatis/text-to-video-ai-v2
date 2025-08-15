import os
import requests
import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class GloboActorScraper:
    def __init__(self):
        self.base_url = "https://gshow.globo.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Cache de imagens já encontradas
        self.image_cache = {}
        
    def get_actor_image_from_globo(self, actor_name: str, novela_name: str = "dona de mim") -> Optional[str]:
        """
        Busca imagem do ator diretamente no site da Globo
        """
        try:
            # URL da página de personagens da novela
            novela_url = f"https://gshow.globo.com/novelas/{novela_name.replace(' ', '-')}/personagem/"
            
            print(f"🔍 Buscando ator '{actor_name}' em: {novela_url}")
            
            # Fazer requisição para a página
            response = self.session.get(novela_url, timeout=15)
            response.raise_for_status()
            
            # Parsear HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar por cards de personagens
            character_cards = soup.find_all('div', class_=re.compile(r'card|personagem|ator'))
            
            # Se não encontrar cards específicos, buscar por qualquer div com imagens
            if not character_cards:
                character_cards = soup.find_all('div', class_=re.compile(r'content|item|box'))
            
            # Buscar por imagens de atores
            for card in character_cards:
                # Buscar por texto que contenha o nome do ator
                card_text = card.get_text().lower()
                if actor_name.lower() in card_text:
                    # Encontrar imagem neste card
                    img_tag = card.find('img')
                    if img_tag:
                        img_src = img_tag.get('src') or img_tag.get('data-src')
                        if img_src:
                            # Converter para URL completa
                            full_url = urljoin(self.base_url, img_src)
                            print(f"✅ Imagem encontrada para {actor_name}: {full_url}")
                            return full_url
            
            # Buscar por imagens com alt text contendo o nome do ator
            img_tags = soup.find_all('img', alt=re.compile(actor_name, re.IGNORECASE))
            for img in img_tags:
                img_src = img.get('src') or img.get('data-src')
                if img_src:
                    full_url = urljoin(self.base_url, img_src)
                    print(f"✅ Imagem encontrada por alt text para {actor_name}: {full_url}")
                    return full_url
            
            # Buscar por qualquer imagem que possa ser do ator
            all_images = soup.find_all('img')
            for img in all_images:
                img_src = img.get('src') or img.get('data-src')
                if img_src and any(keyword in img_src.lower() for keyword in ['ator', 'atriz', 'personagem', 'foto']):
                    # Verificar se o contexto ao redor da imagem menciona o ator
                    parent_text = img.parent.get_text().lower() if img.parent else ""
                    if actor_name.lower() in parent_text:
                        full_url = urljoin(self.base_url, img_src)
                        print(f"✅ Imagem encontrada por contexto para {actor_name}: {full_url}")
                        return full_url
            
            print(f"❌ Nenhuma imagem encontrada para {actor_name} no site da Globo")
            return None
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar imagem de {actor_name} no site da Globo: {e}")
            return None
    
    def get_all_actor_images(self, novela_name: str = "dona de mim") -> Dict[str, str]:
        """
        Busca imagens de todos os atores da novela
        """
        try:
            novela_url = f"https://gshow.globo.com/novelas/{novela_name.replace(' ', '-')}/personagem/"
            
            print(f"🔍 Buscando todos os atores em: {novela_url}")
            
            response = self.session.get(novela_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            actor_images = {}
            
            # Buscar por todas as imagens de personagens
            img_tags = soup.find_all('img')
            
            for img in img_tags:
                img_src = img.get('src') or img.get('data-src')
                if img_src:
                    # Verificar se é uma imagem de ator
                    alt_text = img.get('alt', '').lower()
                    parent_text = img.parent.get_text().lower() if img.parent else ""
                    
                    # Procurar por nomes de atores conhecidos
                    known_actors = [
                        "giulia gayoso", "marcos pasquim", "sheron menezzes", "tony ramos",
                        "hugo resende", "bel lima", "giovana cordeiro", "gabriel sanches",
                        "pedro alves", "felipe simas", "cecília chancez", "rafael vitti"
                    ]
                    
                    for actor in known_actors:
                        if actor in alt_text or actor in parent_text:
                            full_url = urljoin(self.base_url, img_src)
                            actor_images[actor] = full_url
                            print(f"✅ Imagem encontrada para {actor}: {full_url}")
                            break
            
            return actor_images
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar imagens de atores: {e}")
            return {}
    
    def search_actor_by_name(self, actor_name: str) -> Optional[str]:
        """
        Busca ator por nome em diferentes páginas da Globo
        """
        # Tentar diferentes variações do nome
        name_variations = [
            actor_name,
            actor_name.replace(' ', '-'),
            actor_name.replace(' ', ''),
            actor_name.split()[0] if ' ' in actor_name else actor_name
        ]
        
        for name_var in name_variations:
            # Tentar buscar na página de busca da Globo
            search_url = f"https://gshow.globo.com/busca/?q={name_var}"
            
            try:
                response = self.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar por imagens nos resultados
                    img_tags = soup.find_all('img')
                    for img in img_tags:
                        img_src = img.get('src') or img.get('data-src')
                        if img_src and any(keyword in img_src.lower() for keyword in ['ator', 'atriz', 'foto']):
                            full_url = urljoin(self.base_url, img_src)
                            print(f"✅ Imagem encontrada para {actor_name} via busca: {full_url}")
                            return full_url
                            
            except Exception as e:
                print(f"⚠️ Erro na busca por {name_var}: {e}")
                continue
        
        return None

# Função para testar o scraper
def test_globo_scraper():
    """
    Testa o scraper da Globo
    """
    scraper = GloboActorScraper()
    
    # Testar busca de atores específicos
    test_actors = [
        "Giulia Gayoso",
        "Marcos Pasquim", 
        "Sheron Menezzes",
        "Tony Ramos"
    ]
    
    print("🎭 Testando Scraper da Globo")
    print("=" * 50)
    
    for actor in test_actors:
        print(f"\n🔍 Buscando: {actor}")
        image_url = scraper.get_actor_image_from_globo(actor)
        if image_url:
            print(f"✅ Encontrado: {image_url}")
        else:
            print("❌ Não encontrado")
    
    # Buscar todas as imagens
    print(f"\n🔍 Buscando todas as imagens de atores...")
    all_images = scraper.get_all_actor_images()
    print(f"✅ Encontradas {len(all_images)} imagens de atores")

if __name__ == "__main__":
    test_globo_scraper() 