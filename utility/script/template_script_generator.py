#!/usr/bin/env python3
"""
Gerador de Scripts Baseado em Templates
Gera scripts específicos baseados em templates pré-definidos
"""

import os
import json
from typing import Dict, List, Optional
import sys
sys.path.append(".")

from utility.templates.template_manager import TemplateManager
from utility.script.script_generator import generate_script

class TemplateScriptGenerator:
    def __init__(self):
        self.template_manager = TemplateManager()
    
    def load_template(self, template_id: str) -> Optional[Dict]:
        """Carrega template pelo ID"""
        try:
            return self.template_manager.get_template(template_id)
        except Exception as e:
            print(f"❌ Erro ao carregar template '{template_id}': {e}")
            return None
    
    def generate_script_for_template(self, topic: str, template_id: str) -> Dict:
        """Gera script baseado no template selecionado"""
        try:
            # Carregar template
            template = self.load_template(template_id)
            if not template:
                raise Exception(f"Template '{template_id}' não encontrado")
            
            # Gerar script base
            script = generate_script(topic)
            
            # Aplicar adaptações específicas do template
            if template_id == "cinematic_religious":
                script = self._adapt_for_religious_template(script, template)
            elif template_id == "vsl_magnetic":
                script = self._adapt_for_vsl_magnetic_template(script, template)
            
            return {
                'script': script,
                'template': template
            }
            
        except Exception as e:
            print(f"❌ Erro ao gerar script para template: {e}")
            # Fallback para script normal
            return {
                'script': generate_script(topic),
                'template': None
            }
    
    def _generate_script_with_ai(self, topic: str, template: Dict) -> str:
        """Gera script usando IA com base no template"""
        try:
            from utility.script.script_generator import generate_script
            
            # Adicionar contexto do template ao tópico
            template_context = template.get('content_guidelines', {})
            enhanced_topic = f"{topic} - {template.get('name', '')} - {template_context.get('tone', '')}"
            
            # Gerar script base
            base_script = generate_script(enhanced_topic)
            
            return base_script
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar script com IA: {e}")
            # Fallback para script padrão
            return f"Fatos interessantes sobre {topic}. Este é um conteúdo gerado automaticamente seguindo o estilo {template.get('name', '')}."
    
    def _adapt_for_religious_template(self, script: str, template: Dict) -> str:
        """Adapta script para template religioso cinematográfico"""
        # Adicionar elementos religiosos e cinematográficos
        religious_elements = [
            "De acordo com as escrituras,",
            "Segundo a tradição sagrada,",
            "Como revelado nas escrituras,",
            "Conforme ensinam os textos sagrados,"
        ]
        
        # Inserir elemento religioso no início
        import random
        religious_intro = random.choice(religious_elements)
        script = f"{religious_intro} {script}"
        
        return script
    
    def _adapt_for_vsl_magnetic_template(self, script: str, template: Dict) -> str:
        """Adapta script para template VSL magnético"""
        try:
            # Usar o gerador específico de VSL se disponível
            from utility.script.vsl_script_generator import VSLScriptGenerator
            
            vsl_generator = VSLScriptGenerator()
            # Usar o script original completo em vez de truncar
            vsl_script = vsl_generator.generate_vsl_script(topic=script, template_config=template)
            
            return vsl_script
            
        except Exception as e:
            # Fallback se o gerador VSL não estiver disponível
            print(f"⚠️ Erro no gerador VSL: {e}, usando adaptação básica")
            
            # Adicionar elementos de VSL ao script
            vsl_elements = [
                "Você já se perguntou sobre",
                "Descubra agora",
                "A verdade sobre",
                "O que ninguém te conta sobre"
            ]
            
            import random
            vsl_intro = random.choice(vsl_elements)
            script = f"{vsl_intro} {script}"
            
            # Adicionar CTA no final
            cta_options = [
                "Clique agora e descubra mais!",
                "Veja o que você está perdendo!",
                "Não perca mais tempo, acesse agora!",
                "A decisão está nas suas mãos!"
            ]
            
            cta = random.choice(cta_options)
            script = f"{script} {cta}"
            
            return script
    
    def get_template_suggestions(self, topic: str) -> List[Dict]:
        """Sugere templates apropriados para um tópico"""
        suggestions = []
        
        # Análise de palavras-chave no tópico
        topic_lower = topic.lower()
        
        # Template Religioso Cinematográfico
        religious_keywords = ['religioso', 'bíblia', 'deus', 'fé', 'igreja', 'sagrado', 'espiritual', 'cristão', 'cristã']
        religious_score = sum(1 for keyword in religious_keywords if keyword in topic_lower)
        
        if religious_score > 0:
            suggestions.append({
                'template_id': 'cinematic_religious',
                'name': 'Cinematográfico Religioso',
                'description': 'Template para conteúdo religioso com elementos cinematográficos',
                'score': religious_score,
                'reasons': [f'Detectado conteúdo religioso: {religious_score} palavras-chave']
            })
        
        # Template VSL Magnético
        vsl_keywords = ['venda', 'vender', 'produto', 'serviço', 'oferta', 'promoção', 'desconto', 'negócio', 'empresa', 'marketing', 'vendas', 'comercial']
        vsl_score = sum(1 for keyword in vsl_keywords if keyword in topic_lower)
        
        if vsl_score > 0:
            suggestions.append({
                'template_id': 'vsl_magnetic',
                'name': 'VSL Magnético',
                'description': 'Template para vídeos de vendas magnéticos (formato vertical)',
                'score': vsl_score,
                'reasons': [f'Detectado conteúdo comercial: {vsl_score} palavras-chave']
            })
        
        # Template VSL para qualquer tópico (score baixo mas sempre disponível)
        suggestions.append({
            'template_id': 'vsl_magnetic',
            'name': 'VSL Magnético',
            'description': 'Template para vídeos de vendas magnéticos (formato vertical)',
            'score': 1,
            'reasons': ['Template versátil para qualquer tópico']
        })
        
        # Ordenar por score
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        
        return suggestions
    
    def apply_pauses_to_script(self, script: str, pauses_config: Dict) -> str:
        """Aplica pausas estratégicas ao script"""
        # Esta função será implementada para sincronizar com o áudio
        # Por enquanto, retorna o script original
        return script 