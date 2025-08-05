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
            elif template_id == "gaming_tutorial":
                script = self._adapt_for_gaming_tutorial_template(topic, template)
            elif template_id == "gaming_highlights":
                script = self._adapt_for_gaming_highlights_template(topic, template)
            
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
        """Adapta script para template religioso cinematográfico seguindo estrutura profissional"""
        try:
            # Extrair diretrizes do template
            structure_guidelines = template.get('script_pattern', {}).get('video_structure', {})
            content_types = template.get('script_pattern', {}).get('content_types', {})
            
            # Estrutura profissional para vídeos religiosos
            opening_elements = [
                "A paz do Senhor! Que Deus abençoe sua vida!",
                "Que a graça de Deus esteja com você!",
                "Bem-vindo a mais um momento de reflexão espiritual!",
                "Que o amor de Cristo ilumine seu caminho!"
            ]
            
            # Perguntas impactantes para abertura
            impact_questions = [
                "Você já se perguntou por que Deus permite o sofrimento?",
                "Sabe qual é o verdadeiro significado da fé?",
                "Já parou para refletir sobre o propósito da sua vida?",
                "O que realmente significa confiar em Deus?"
            ]
            
            # Elementos de desenvolvimento
            development_elements = [
                "De acordo com as escrituras sagradas,",
                "Como revelado nas palavras de Jesus,",
                "Segundo a tradição cristã,",
                "Conforme ensinam os textos sagrados,"
            ]
            
            # Reflexões e exemplos práticos
            practical_examples = [
                "Assim como uma semente precisa de tempo para crescer, nossa fé também se desenvolve gradualmente.",
                "Assim como um pai cuida de seus filhos, Deus cuida de cada um de nós com amor infinito.",
                "Assim como a luz dissipa as trevas, a fé dissipa o medo e a dúvida.",
                "Assim como uma âncora mantém o navio firme, nossa fé nos mantém firmes nas tempestades da vida."
            ]
            
            # Conclusões inspiradoras
            inspiring_conclusions = [
                "Lembre-se: Deus não prometeu uma vida sem problemas, mas prometeu estar conosco em todos os momentos.",
                "A fé não remove todas as dificuldades, mas nos dá força para enfrentá-las com coragem.",
                "Deus não nos dá o que queremos, mas o que precisamos para crescer espiritualmente.",
                "A verdadeira paz não vem da ausência de problemas, mas da presença de Deus em nossa vida."
            ]
            
            # Chamadas à ação
            call_to_action = [
                "Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!",
                "Compartilhe este vídeo com quem precisa de esperança!",
                "Deixe seu 'Amém' se esta mensagem tocou seu coração!",
                "Compartilhe com alguém que precisa de força espiritual!"
            ]
            
            import random
            
            # Construir script estruturado
            structured_script = ""
            
            # ABERTURA (5-15 segundos)
            opening = random.choice(opening_elements)
            impact_question = random.choice(impact_questions)
            structured_script += f"{opening} {impact_question}\n\n"
            
            # DESENVOLVIMENTO (40-70 segundos)
            development_intro = random.choice(development_elements)
            structured_script += f"{development_intro} {script}\n\n"
            
            # Adicionar exemplo prático
            practical_example = random.choice(practical_examples)
            structured_script += f"{practical_example}\n\n"
            
            # FECHAMENTO (10-15 segundos)
            conclusion = random.choice(inspiring_conclusions)
            cta = random.choice(call_to_action)
            structured_script += f"{conclusion} {cta}"
            
            return structured_script
            
        except Exception as e:
            print(f"⚠️ Erro ao adaptar script religioso: {e}")
            # Fallback básico
            religious_elements = [
                "De acordo com as escrituras,",
                "Segundo a tradição sagrada,",
                "Como revelado nas escrituras,",
                "Conforme ensinam os textos sagrados,"
            ]
            
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
    
    def _adapt_for_gaming_tutorial_template(self, topic: str, template: Dict) -> str:
        """Adapta script para template de tutorial gaming"""
        try:
            from utility.script.gaming_script_generator import generate_gaming_tutorial
            
            tutorial_script = generate_gaming_tutorial(topic)
            return tutorial_script
            
        except Exception as e:
            print(f"⚠️ Erro no gerador de tutorial gaming: {e}, usando adaptação básica")
            
            # Fallback básico
            tutorial_elements = [
                "Aprenda como",
                "Domine a técnica de",
                "Descubra como",
                "Masterize"
            ]
            
            import random
            tutorial_intro = random.choice(tutorial_elements)
            script = f"{tutorial_intro} {topic}.\n\n"
            
            # Adicionar passos básicos
            steps = [
                "Passo 1: Entenda o básico",
                "Passo 2: Pratique regularmente", 
                "Passo 3: Analise seus erros",
                "Passo 4: Continue evoluindo"
            ]
            
            for step in steps:
                script += f"{step}\n"
            
            script += "\nDica: A prática leva à perfeição!\n"
            script += "Continue praticando e você verá resultados!"
            
            return script
    
    def _adapt_for_gaming_highlights_template(self, topic: str, template: Dict) -> str:
        """Adapta script para template de highlights gaming"""
        try:
            from utility.script.gaming_script_generator import generate_gaming_highlights
            
            highlights_script = generate_gaming_highlights(topic)
            return highlights_script
            
        except Exception as e:
            print(f"⚠️ Erro no gerador de highlights gaming: {e}, usando adaptação básica")
            
            # Fallback básico
            highlights_elements = [
                "MOMENTOS ÉPICOS!",
                "PLAY INCRÍVEL!",
                "VICTORY ROYALE!",
                "DOMINAÇÃO TOTAL!"
            ]
            
            import random
            script = "MOMENTOS ÉPICOS\n\n"
            
            for highlight in highlights_elements:
                script += f"{highlight}\n"
            
            script += "\nINSCREVA-SE PARA MAIS!"
            
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
        
        # Template Gaming Tutorial
        gaming_tutorial_keywords = ['tutorial', 'aprender', 'como fazer', 'dicas', 'passo a passo', 'técnica', 'melhorar', 'praticar']
        gaming_tutorial_score = sum(1 for keyword in gaming_tutorial_keywords if keyword in topic_lower)
        
        if gaming_tutorial_score > 0:
            suggestions.append({
                'template_id': 'gaming_tutorial',
                'name': 'Gaming Tutorial',
                'description': 'Template para tutoriais de jogos com passo a passo claro',
                'score': gaming_tutorial_score,
                'reasons': [f'Detectado conteúdo tutorial: {gaming_tutorial_score} palavras-chave']
            })
        
        # Template Gaming Highlights
        gaming_highlights_keywords = ['highlights', 'momentos', 'épico', 'incrível', 'play', 'victory', 'clutch', 'headshot']
        gaming_highlights_score = sum(1 for keyword in gaming_highlights_keywords if keyword in topic_lower)
        
        if gaming_highlights_score > 0:
            suggestions.append({
                'template_id': 'gaming_highlights',
                'name': 'Gaming Highlights',
                'description': 'Template para vídeos de highlights épicos de jogos',
                'score': gaming_highlights_score,
                'reasons': [f'Detectado conteúdo de highlights: {gaming_highlights_score} palavras-chave']
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