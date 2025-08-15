#!/usr/bin/env python3
"""
Teste do Sistema de Imagens de Personagens para Novelas
"""

import os
import asyncio
from utility.video.character_image_generator import CharacterImageGenerator

async def test_character_images():
    """
    Testa o sistema de imagens de personagens
    """
    print("🎭 Teste do Sistema de Imagens de Personagens")
    print("=" * 60)
    
    # Verificar APIs
    if not os.environ.get("PEXELS_KEY"):
        print("⚠️ PEXELS_KEY não configurada")
        print("💡 Configure: $env:PEXELS_KEY='sua_chave_pexels'")
        return
    
    if not os.environ.get("UNSPLASH_KEY"):
        print("⚠️ UNSPLASH_KEY não configurada (opcional)")
        print("💡 Configure: $env:UNSPLASH_KEY='sua_chave_unsplash'")
    
    # Inicializar gerador
    generator = CharacterImageGenerator()
    
    # Testes de personagens
    test_cases = [
        {
            "text": "Maria é a protagonista de Dona de Mim e está enfrentando muitos desafios",
            "expected": "maria protagonista"
        },
        {
            "text": "O vilão de Fuzuê está causando problemas para Luna",
            "expected": "vilão antagonista"
        },
        {
            "text": "A mocinha de Vai na Fé está apaixonada pelo mocinho",
            "expected": "mocinha mocinho"
        },
        {
            "text": "Alice e Caio de Terra e Paixão estão vivendo um romance intenso",
            "expected": "alice caio protagonistas"
        },
        {
            "text": "O personagem principal da novela está sofrendo muito",
            "expected": "protagonista genérico"
        }
    ]
    
    print("\n🎬 Testando Detecção de Personagens:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Teste {i}: {test_case['text']}")
        print("-" * 30)
        
        # Extrair informações do personagem
        character_info = generator.extract_character_info(test_case['text'])
        print(f"🎭 Personagem: {character_info['personagem']}")
        print(f"📺 Novela: {character_info['novela']}")
        print(f"🏷️ Tipo: {character_info['tipo']}")
        
        # Gerar consultas de busca
        queries = generator.generate_character_search_queries(character_info)
        print(f"🔍 Consultas geradas: {len(queries)}")
        for j, query in enumerate(queries[:3], 1):
            print(f"   {j}. {query}")
        
        # Buscar imagem
        print("🖼️ Buscando imagem...")
        image_url = generator.get_character_image(test_case['text'])
        
        if image_url:
            print(f"✅ Imagem encontrada: {image_url[:80]}...")
            
            # Opcional: baixar imagem
            filename = f"teste_{i}_{character_info['personagem']}"
            filepath = generator.download_character_image(image_url, filename)
            if filepath:
                print(f"💾 Imagem salva: {filepath}")
        else:
            print("❌ Nenhuma imagem encontrada")
        
        print()

def show_character_database():
    """
    Mostra o banco de dados de personagens
    """
    print("\n📚 Banco de Dados de Personagens:")
    print("=" * 40)
    
    generator = CharacterImageGenerator()
    
    for novela, data in generator.character_database.items():
        print(f"\n📺 {novela.upper()}:")
        for personagem, keywords in data["personagens"].items():
            print(f"   🎭 {personagem}: {', '.join(keywords)}")

def show_usage_examples():
    """
    Mostra exemplos de uso
    """
    print("\n💡 Exemplos de Uso:")
    print("=" * 30)
    
    examples = [
        "Maria protagonista Dona de Mim",
        "Vilão Fuzuê antagonista",
        "Mocinha Vai na Fé jovem",
        "Mocinho Terra e Paixão herói",
        "Personagem principal novela"
    ]
    
    for example in examples:
        print(f"   • {example}")

async def main():
    """
    Função principal
    """
    print("🎭 SISTEMA DE IMAGENS DE PERSONAGENS PARA NOVELAS")
    print("=" * 60)
    
    # Mostrar informações do banco de dados
    show_character_database()
    
    # Mostrar exemplos de uso
    show_usage_examples()
    
    # Executar testes
    await test_character_images()
    
    print("\n🎉 Teste concluído!")
    print("💡 Configure as APIs e teste com personagens reais!")

if __name__ == "__main__":
    asyncio.run(main()) 