#!/usr/bin/env python3
"""
Script para testar a aplicação de efeitos do template
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(".")

try:
    from utility.assets.asset_manager import asset_manager
    from utility.render.template_render_engine import TemplateRenderEngine
    
    print("✅ Módulos importados com sucesso")
    
    # Testar assets para template
    print(f"\n🎬 TESTANDO ASSETS PARA TEMPLATE:")
    template_assets = asset_manager.get_assets_for_template("cinematic_religious")
    
    for asset_type, asset_path in template_assets.items():
        if asset_path:
            exists = "✅" if os.path.exists(asset_path) else "❌"
            print(f"   {exists} {asset_type}: {os.path.basename(asset_path)}")
            if os.path.exists(asset_path):
                file_size = os.path.getsize(asset_path)
                print(f"      Tamanho: {file_size} bytes")
        else:
            print(f"   ❌ {asset_type}: Não encontrado")
    
    # Testar render engine
    print(f"\n🎬 TESTANDO TEMPLATE RENDER ENGINE:")
    render_engine = TemplateRenderEngine()
    
    # Simular configuração de template
    template_config = {
        'template_id': 'cinematic_religious',
        'visual_settings': {
            'resolution': '1920x1080'
        }
    }
    
    # Verificar se existe um vídeo de teste
    test_video = "rendered_video.mp4"
    if os.path.exists(test_video):
        print(f"✅ Vídeo de teste encontrado: {test_video}")
        
        # Testar aplicação do template
        try:
            output_video = render_engine.apply_template_to_video(test_video, template_config)
            print(f"✅ Template aplicado com sucesso: {output_video}")
        except Exception as e:
            print(f"❌ Erro ao aplicar template: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Vídeo de teste não encontrado: {test_video}")
        print("   Execute primeiro a geração de um vídeo para testar")

except Exception as e:
    print(f"❌ Erro ao testar efeitos: {e}")
    import traceback
    traceback.print_exc() 