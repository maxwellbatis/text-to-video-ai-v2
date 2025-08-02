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

class TemplateScriptGenerator:
    def __init__(self):
        self.template_manager = TemplateManager()
    
    def generate_script_for_template(self, topic: str, template_id: str) -> Dict:
        """Gera script baseado em um template específico"""
        template = self.template_manager.get_template(template_id)
        if not template:
            raise ValueError(f"Template '{template_id}' não encontrado")
        
        # Gerar script usando IA
        script = self._generate_script_with_ai(topic, template)
        
        # Aplicar adaptações específicas do template
        if template_id == "cinematic_religious":
            script = self._adapt_for_religious_template(script, template)
        elif template_id == "vsl_cinematographic":
            script = self._adapt_for_vsl_template(script, template)
        
        return {
            'script': script,
            'template': template,
            'pauses': template.get('script_pattern', {}).get('pauses_strategy', {}),
            'voice_settings': template.get('script_pattern', {}).get('voice_settings', {}),
            'visual_settings': template.get('visual_settings', {}),
            'audio_settings': template.get('audio_settings', {})
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
        """Adapta script para template religioso"""
        # Adicionar elementos religiosos ao script
        religious_elements = [
            "De acordo com as escrituras",
            "Como nos ensina a Bíblia",
            "Segundo a palavra de Deus",
            "Em nome da fé",
            "Através da graça divina"
        ]
        
        # Inserir elementos religiosos em pontos estratégicos
        sentences = script.split('. ')
        if len(sentences) > 2:
            # Inserir elemento religioso no meio
            mid_point = len(sentences) // 2
            sentences.insert(mid_point, f"{religious_elements[0]}, ")
        
        return '. '.join(sentences)
    
    def _adapt_for_vsl_template(self, script: str, template: Dict) -> str:
        """Adapta script para template VSL cinematográfico"""
        # Estrutura VSL: Hook → Problema → Solução → Oferta → CTA
        script_pattern = template.get('script_pattern', {})
        structure = script_pattern.get('structure', {})
        
        # Dividir script em frases
        sentences = script.split('. ')
        if len(sentences) < 5:
            # Se não há frases suficientes, criar estrutura VSL
            return self._create_vsl_structure(topic, template)
        
        # Adaptar para estrutura VSL
        vsl_script = []
        
        # Hook (primeira frase)
        if sentences:
            hook = sentences[0]
            vsl_script.append(f"Você sabe por que {hook.lower()}")
        
        # Problema (segunda frase)
        if len(sentences) > 1:
            problem = sentences[1]
            vsl_script.append(f"O problema é que {problem.lower()}")
        
        # Solução (terceira frase)
        if len(sentences) > 2:
            solution = sentences[2]
            vsl_script.append(f"Com nossa solução, {solution.lower()}")
        
        # Oferta (quarta frase)
        if len(sentences) > 3:
            offer = sentences[3]
            vsl_script.append(f"Por tempo limitado, {offer.lower()}")
        
        # CTA (última frase)
        if len(sentences) > 4:
            cta = sentences[4]
            vsl_script.append(f"Clique agora e {cta.lower()}")
        
        return '. '.join(vsl_script)
    
    def _create_vsl_structure(self, topic: str, template: Dict) -> str:
        """Cria estrutura VSL completa para um tópico"""
        vsl_elements = [
            f"Você sabe por que {topic} é um problema real?",
            f"O problema é que a maioria das pessoas não consegue resolver isso.",
            f"Com nossa solução exclusiva, você terá resultados imediatos.",
            f"Por tempo limitado, oferecemos um desconto especial.",
            f"Clique agora e descubra como transformar sua situação."
        ]
        
        return '. '.join(vsl_elements)
    
    def get_template_suggestions(self, topic: str) -> List[Dict]:
        """Sugere templates apropriados para um tópico"""
        templates = self.template_manager.list_templates()
        suggestions = []
        
        # Análise simples baseada em palavras-chave
        topic_lower = topic.lower()
        
        for template in templates:
            score = 0
            reasons = []
            
            # Verificar se é conteúdo religioso/bíblico
            if any(word in topic_lower for word in ['bíblico', 'religioso', 'profecia', 'apocalipse', 'deus', 'jesus', 'bíblia']):
                if 'religioso' in template['name'].lower() or 'cinematográfico' in template['name'].lower():
                    score += 3
                    reasons.append("Conteúdo religioso detectado")
            
            # Verificar se é conteúdo educativo/curioso
            if any(word in topic_lower for word in ['curioso', 'interessante', 'fato', 'descoberta', 'ciência', 'história']):
                if 'curioso' in template['name'].lower() or 'fatos' in template['name'].lower():
                    score += 2
                    reasons.append("Conteúdo educativo detectado")
            
            # Verificar se é conteúdo de vendas/VSL
            if any(word in topic_lower for word in ['venda', 'produto', 'serviço', 'oferta', 'desconto', 'solução', 'problema']):
                if 'vsl' in template['name'].lower() or 'cinematográfico' in template['name'].lower():
                    score += 3
                    reasons.append("Conteúdo de vendas detectado")
            
            # Verificar se é conteúdo empresarial/profissional
            if any(word in topic_lower for word in ['negócio', 'empresa', 'profissional', 'sucesso', 'resultado']):
                if 'vsl' in template['name'].lower() or 'cinematográfico' in template['name'].lower():
                    score += 2
                    reasons.append("Conteúdo empresarial detectado")
            
            if score > 0:
                suggestions.append({
                    'template_id': template['id'],
                    'name': template['name'],
                    'description': template['description'],
                    'score': score,
                    'reasons': reasons
                })
        
        # Ordenar por score
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        
        return suggestions
    
    def apply_pauses_to_script(self, script: str, pauses_config: Dict) -> str:
        """Aplica pausas estratégicas ao script"""
        # Esta função será implementada para sincronizar com o áudio
        # Por enquanto, retorna o script original
        return script 