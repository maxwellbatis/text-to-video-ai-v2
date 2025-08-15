#!/usr/bin/env python3
"""
Exemplo de uso do Gerador de Vídeos de Resumos de Novelas
"""

import asyncio
import os
from utility.script.novela_script_generator import generate_novela_script, extract_novela_info

async def exemplo_novela():
    """
    Exemplo de como usar o gerador de novelas
    """
    print("🎬 Exemplo do Gerador de Vídeos de Resumos de Novelas")
    print("=" * 60)
    
    # Exemplos de tópicos
    exemplos = [
        "Resumo da semana de Dona de Mim",
        "Análise do personagem principal de Fuzuê",
        "Previsões para próximos capítulos de Vai na Fé",
        "Curiosidades sobre Terra e Paixão"
    ]
    
    for i, topico in enumerate(exemplos, 1):
        print(f"\n📺 Exemplo {i}: {topico}")
        print("-" * 40)
        
        # Extrair informações da novela
        novela_info = extract_novela_info(topico)
        print(f"🎭 Novela detectada: {novela_info['novela_name']}")
        print(f"📝 Tipo de conteúdo: {novela_info['content_type']}")
        
        # Simular geração de script (sem API)
        print("📝 Script seria gerado aqui...")
        print("🎙️ Áudio seria gerado aqui...")
        print("🎬 Vídeo seria renderizado aqui...")
        print("✅ Vídeo finalizado!")
        
        print()

def mostrar_estrutura():
    """
    Mostra a estrutura do projeto
    """
    print("\n📁 Estrutura do Projeto:")
    print("=" * 40)
    print("Text-To-Video-AI/")
    print("├── novela_video_generator.py          # Script principal")
    print("├── utility/")
    print("│   ├── script/")
    print("│   │   └── novela_script_generator.py # Gerador de scripts")
    print("│   └── templates/")
    print("│       └── novela_resumo.json         # Template de novela")
    print("├── assets/")
    print("│   ├── TRILHA SONORA/CINEMATIC/       # Músicas dramáticas")
    print("│   └── EFEITOS SONOROS/")
    print("│       ├── CINEMATIC/                 # Efeitos dramáticos")
    print("│       └── IMPACTOS/                  # Efeitos de impacto")
    print("└── database/                          # Sistema de banco de dados")

def mostrar_configuracao():
    """
    Mostra como configurar o sistema
    """
    print("\n🔧 Configuração Necessária:")
    print("=" * 40)
    print("1. APIs Obrigatórias:")
    print("   - GROQ_API_KEY ou OPENAI_KEY (para scripts)")
    print("   - PEXELS_KEY (para vídeos de fundo)")
    print()
    print("2. APIs Opcionais:")
    print("   - ELEVENLABS_API_KEY (para vozes profissionais)")
    print()
    print("3. Exemplo de configuração (Windows):")
    print("   $env:GROQ_API_KEY='sua_chave_groq'")
    print("   $env:PEXELS_KEY='sua_chave_pexels'")
    print()
    print("4. Exemplo de uso:")
    print("   py -3 novela_video_generator.py 'Resumo da semana de Dona de Mim'")

def mostrar_caracteristicas():
    """
    Mostra as características do sistema
    """
    print("\n🎯 Características do Sistema:")
    print("=" * 40)
    print("✅ Scripts especializados para novelas")
    print("✅ Detecção automática de novela e tipo")
    print("✅ Template visual dramático")
    print("✅ Vozes apropriadas para entretenimento")
    print("✅ Banco de dados para histórico")
    print("✅ Suporte a múltiplas novelas")
    print("✅ Estrutura otimizada para redes sociais")
    print("✅ Fallback automático para APIs")

def main():
    """
    Função principal do exemplo
    """
    print("🎬 GERADOR DE VÍDEOS DE RESUMOS DE NOVELAS")
    print("=" * 60)
    
    # Executar exemplo
    asyncio.run(exemplo_novela())
    
    # Mostrar informações adicionais
    mostrar_estrutura()
    mostrar_configuracao()
    mostrar_caracteristicas()
    
    print("\n🎉 Sistema pronto para uso!")
    print("💡 Configure as APIs e comece a gerar vídeos!")

if __name__ == "__main__":
    main() 