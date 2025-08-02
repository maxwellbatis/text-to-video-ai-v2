#!/usr/bin/env python3
"""
Gerenciador de Templates para Text-to-Video AI
Carrega e gerencia templates de vídeo com configurações específicas
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path

class TemplateManager:
    def __init__(self, templates_dir: str = "utility/templates"):
        self.templates_dir = Path(templates_dir)
        self.templates = {}
        self.load_templates()
    
    def load_templates(self):
        """Carrega todos os templates disponíveis"""
        if not self.templates_dir.exists():
            print(f"⚠️ Diretório de templates não encontrado: {self.templates_dir}")
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template_id = template_file.stem
                    template_data['id'] = template_id
                    self.templates[template_id] = template_data
                    print(f"✅ Template carregado: {template_data.get('name', template_id)}")
            except Exception as e:
                print(f"❌ Erro ao carregar template {template_file}: {e}")
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Obtém um template específico"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[Dict]:
        """Lista todos os templates disponíveis"""
        return [
            {
                'id': template_id,
                'name': template.get('name', template_id),
                'description': template.get('description', ''),
                'category': template.get('category', 'geral')
            }
            for template_id, template in self.templates.items()
        ]
    
    def get_template_by_category(self, category: str) -> List[Dict]:
        """Obtém templates por categoria"""
        return [
            {
                'id': template_id,
                'name': template.get('name', template_id),
                'description': template.get('description', ''),
                'category': template.get('category', 'geral')
            }
            for template_id, template in self.templates.items()
            if template.get('category', 'geral') == category
        ] 