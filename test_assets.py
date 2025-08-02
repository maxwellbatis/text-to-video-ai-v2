#!/usr/bin/env python3
"""
Teste do AssetManager
Verifica se os assets estão sendo carregados corretamente
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utility.assets.asset_manager import asset_manager
    
    print("🎵 TESTE DO ASSET MANAGER")
    print("=" * 50)
    
    # Listar todos os assets disponíveis
    assets = asset_manager.list_available_assets()
    
    print("\n📁 ASSETS DISPONÍVEIS:")
    print("-" * 30)
    
    # Efeitos sonoros
    print("\n🎵 EFEITOS SONOROS:")
    for category, files in assets['audio_effects'].items():
        print(f"  {category}: {len(files)} arquivos")
        for i, file in enumerate(files[:3]):  # Mostrar apenas os 3 primeiros
            print(f"    {i+1}. {os.path.basename(file)}")
        if len(files) > 3:
            print(f"    ... e mais {len(files) - 3} arquivos")
    
    # Efeitos visuais
    print("\n🎬 EFEITOS VISUAIS:")
    for category, files in assets['video_effects'].items():
        print(f"  {category}: {len(files)} arquivos")
        for i, file in enumerate(files[:3]):  # Mostrar apenas os 3 primeiros
            print(f"    {i+1}. {os.path.basename(file)}")
        if len(files) > 3:
            print(f"    ... e mais {len(files) - 3} arquivos")
    
    # Trilhas sonoras
    print("\n🎼 TRILHAS SONORAS:")
    for category, files in assets['music_tracks'].items():
        print(f"  {category}: {len(files)} arquivos")
        for i, file in enumerate(files[:3]):  # Mostrar apenas os 3 primeiros
            print(f"    {i+1}. {os.path.basename(file)}")
        if len(files) > 3:
            print(f"    ... e mais {len(files) - 3} arquivos")
    
    # Testar assets para template religioso
    print("\n🎯 ASSETS PARA TEMPLATE RELIGIOSO:")
    print("-" * 40)
    religious_assets = asset_manager.get_assets_for_template("cinematic_religious")
    
    for asset_type, asset_path in religious_assets.items():
        if asset_path:
            exists = "✅" if os.path.exists(asset_path) else "❌"
            print(f"{exists} {asset_type}: {os.path.basename(asset_path)}")
        else:
            print(f"❌ {asset_type}: Não encontrado")
    
    print("\n✅ TESTE CONCLUÍDO!")
    
except ImportError as e:
    print(f"❌ Erro ao importar AssetManager: {e}")
except Exception as e:
    print(f"❌ Erro durante o teste: {e}") 