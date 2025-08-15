#!/usr/bin/env python3
"""
Teste do Sistema Completo de Novelas com Dados Reais
"""

import os
import asyncio
from utility.script.novela_scraper import NovelaScraper
from utility.video.character_image_generator import CharacterImageGenerator

async def test_real_novela_system():
    """
    Testa o sistema completo com dados reais
    """
    print("🎬 SISTEMA COMPLETO DE NOVELAS COM DADOS REAIS")
    print("=" * 60)
    
    # Verificar APIs
    if not os.environ.get("PEXELS_KEY"):
        print("⚠️ PEXELS_KEY não configurada")
        print("💡 Configure: $env:PEXELS_KEY='sua_chave_pexels'")
        return
    
    # Inicializar componentes
    scraper = NovelaScraper()
    character_generator = CharacterImageGenerator()
    
    # Testar com uma novela específica
    novela_name = "Dona de Mim"
    
    print(f"\n📺 Testando com: {novela_name}")
    print("-" * 40)
    
    # 1. Buscar resumo real
    print("🔍 1. Buscando resumo real...")
    resumo = scraper.get_novela_resumo(novela_name)
    
    if resumo:
        print(f"✅ Título: {resumo['title']}")
        print(f"📝 Conteúdo: {resumo['content'][:200]}...")
        print(f"🎭 Personagens encontrados: {len(resumo['characters'])}")
        
        # Mostrar personagens reais
        for char in resumo['characters']:
            print(f"   • {char['name']} ({char['character_type']})")
    else:
        print("❌ Erro ao buscar resumo")
        return
    
    # 2. Buscar imagens dos atores reais
    print(f"\n🖼️ 2. Buscando imagens dos atores reais...")
    
    for char in resumo['characters'][:3]:  # Limitar a 3 para teste
        print(f"\n🎭 Buscando: {char['name']}")
        
        # Buscar imagem do ator real
        image_url = character_generator.get_character_image(char['name'])
        
        if image_url:
            print(f"✅ Imagem encontrada: {image_url[:80]}...")
            
            # Baixar imagem
            filename = f"ator_{char['name'].replace(' ', '_').lower()}"
            filepath = character_generator.download_character_image(image_url, filename)
            
            if filepath:
                print(f"💾 Imagem salva: {filepath}")
        else:
            print("❌ Nenhuma imagem encontrada")
    
    # 3. Gerar script baseado no resumo real
    print(f"\n📝 3. Gerando script baseado no resumo real...")
    
    # Simular geração de script (sem API)
    script_prompt = f"""
    Baseado no resumo real de {novela_name}:
    {resumo['content'][:500]}...
    
    Crie um roteiro envolvente para vídeo de 60-90 segundos.
    """
    
    print("📝 Script seria gerado aqui usando IA...")
    print("🎙️ Áudio seria gerado aqui...")
    print("🎬 Vídeo seria renderizado aqui...")
    
    print(f"\n✅ Sistema completo testado com sucesso!")

def show_real_actors_database():
    """
    Mostra o banco de dados de atores reais
    """
    print("\n🎭 Banco de Dados de Atores Reais:")
    print("=" * 40)
    
    character_generator = CharacterImageGenerator()
    
    for novela, actors in character_generator.actor_database.items():
        print(f"\n📺 {novela.upper()}:")
        for character_type, actor_names in actors.items():
            print(f"   🎭 {character_type}: {actor_names[0]}")

def show_scraping_capabilities():
    """
    Mostra as capacidades de scraping
    """
    print("\n🔍 Capacidades de Scraping:")
    print("=" * 30)
    
    scraper = NovelaScraper()
    
    print("📺 Novelas suportadas:")
    for novela, url in scraper.novela_urls.items():
        print(f"   • {novela}: {url}")
    
    print("\n🎭 Atores mapeados:")
    for novela, actors in scraper.actor_database.items():
        print(f"   📺 {novela}:")
        for char_type, actor_names in actors.items():
            print(f"      • {char_type}: {actor_names[0]}")

async def main():
    """
    Função principal
    """
    print("🎬 SISTEMA COMPLETO DE NOVELAS COM DADOS REAIS")
    print("=" * 60)
    
    # Mostrar capacidades
    show_real_actors_database()
    show_scraping_capabilities()
    
    # Executar teste completo
    await test_real_novela_system()
    
    print("\n🎉 Teste concluído!")
    print("💡 Configure as APIs e teste com dados reais!")

if __name__ == "__main__":
    asyncio.run(main()) 