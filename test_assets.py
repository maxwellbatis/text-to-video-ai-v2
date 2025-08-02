#!/usr/bin/env python3
"""
Script para testar se os assets estão sendo encontrados corretamente
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(".")

try:
    from utility.assets.asset_manager import asset_manager
    print("✅ AssetManager importado com sucesso")
    
    # Listar todos os assets disponíveis
    print("\n📋 ASSETS DISPONÍVEIS:")
    assets = asset_manager.list_available_assets()
    
    for category, category_assets in assets.items():
        print(f"\n🎵 {category.upper()}:")
        if category_assets and isinstance(category_assets, dict):
            for subcategory, files in category_assets.items():
                if files and len(files) > 0:
                    print(f"   📁 {subcategory}: {len(files)} arquivos")
                    for i, file in enumerate(files[:3]):  # Mostrar apenas os primeiros 3
                        print(f"      {i+1}. {os.path.basename(file)}")
                    if len(files) > 3:
                        print(f"      ... e mais {len(files) - 3} arquivos")
                else:
                    print(f"   📁 {subcategory}: ❌ Nenhum arquivo encontrado")
        else:
            print("   ❌ Estrutura inválida")
    
    # Testar assets para template específico
    print(f"\n🎬 ASSETS PARA TEMPLATE 'cinematic_religious':")
    template_assets = asset_manager.get_assets_for_template("cinematic_religious")
    
    for asset_type, asset_path in template_assets.items():
        if asset_path:
            exists = "✅" if os.path.exists(asset_path) else "❌"
            print(f"   {exists} {asset_type}: {os.path.basename(asset_path)}")
        else:
            print(f"   ❌ {asset_type}: Não encontrado")
    
    # Verificar estrutura de diretórios
    print(f"\n📁 ESTRUTURA DE DIRETÓRIOS:")
    assets_root = Path("assets")
    if assets_root.exists():
        print(f"✅ Diretório assets existe: {assets_root}")
        
        for subdir in ["EFEITOS SONOROS", "EFEITOS DE VÍDEO", "TRILHA SONORA"]:
            subdir_path = assets_root / subdir
            if subdir_path.exists():
                print(f"✅ {subdir}: {subdir_path}")
                # Listar alguns arquivos
                files = list(subdir_path.rglob("*"))[:3]
                for file in files:
                    if file.is_file():
                        print(f"   📄 {file.name}")
            else:
                print(f"❌ {subdir}: Não encontrado")
    else:
        print(f"❌ Diretório assets não existe: {assets_root}")

except Exception as e:
    print(f"❌ Erro ao testar assets: {e}")
    import traceback
    traceback.print_exc() 