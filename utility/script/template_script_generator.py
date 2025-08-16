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
from utility.script.script_generator import generate_script, generate_prayer_script

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
    
    def generate_script_for_template(self, topic: str, template_id: str, duration_minutes: int = 1) -> Dict:
        """Gera script baseado no template selecionado"""
        try:
            # Carregar template
            template = self.load_template(template_id)
            if not template:
                raise Exception(f"Template '{template_id}' não encontrado")
            
            # Gerar script base baseado no template
            if template_id == "prayer_extended":
                script = generate_prayer_script(topic, duration_minutes)
            else:
                script = generate_script(topic, duration_minutes)
            
            # Aplicar adaptações específicas do template
            if template_id == "cinematic_religious":
                script = self._adapt_for_religious_template(script, template)
            elif template_id == "prayer_extended":
                script = self._adapt_for_prayer_template(script, template, duration_minutes)
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
                'script': generate_script(topic, duration_minutes),
                'template': None
            }
    
    def _generate_script_with_ai(self, topic: str, template: Dict, duration_minutes: int = 1) -> str:
        """Gera script usando IA com base no template"""
        try:
            from utility.script.script_generator import generate_script
            
            # Adicionar contexto do template ao tópico
            template_context = template.get('content_guidelines', {})
            enhanced_topic = f"{topic} - {template.get('name', '')} - {template_context.get('tone', '')}"
            
            # Gerar script base
            base_script = generate_script(enhanced_topic, duration_minutes)
            
            return base_script
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar script com IA: {e}")
            # Fallback para script padrão
            return f"Fatos interessantes sobre {topic}. Este é um conteúdo gerado automaticamente seguindo o estilo {template.get('name', '')}."
    
    def _adapt_for_prayer_template(self, script: str, template: Dict, duration_minutes: int) -> str:
        """Adapta script para template de oração estendida"""
        try:
            # Extrair diretrizes do template
            structure_guidelines = template.get('script_pattern', {}).get('video_structure', {})
            content_types = template.get('script_pattern', {}).get('content_types', {})
            tone_guidelines = template.get('script_pattern', {}).get('tone_guidelines', {})
            
            # Estrutura específica para orações
            prayer_elements = {
                "adoration": [
                    "Senhor, nós Te adoramos e Te louvamos por quem Tu és",
                    "Pai, Tu és digno de toda honra e glória",
                    "Deus, nós Te exaltamos acima de tudo",
                    "Senhor, Te bendizemos por Tua bondade e misericórdia"
                ],
                "thanksgiving": [
                    "Agradecemos por Tua presença em nossas vidas",
                    "Obrigado por Tua graça e amor incondicional",
                    "Senhor, Te agradecemos por todas as bênçãos",
                    "Pai, somos gratos por Tua fidelidade"
                ],
                "supplication": [
                    "Senhor, Te pedimos que [petição específica]",
                    "Pai, imploramos Tua ajuda para [necessidade]",
                    "Deus, Te rogamos que [intercessão]",
                    "Senhor, Te suplicamos que [pedido]"
                ]
            }
            
            # Adicionar momentos de silêncio estratégicos
            silence_markers = ["[...]", "[pausa]", "[contemplação]", "[reflexão]"]
            
            # Estruturar o script com elementos de oração
            enhanced_script = script
            
            # Adicionar elementos de oração se não estiverem presentes
            if "adoração" not in script.lower() and "louvor" not in script.lower():
                adoration = prayer_elements["adoration"][0]
                enhanced_script = f"{adoration}. [...] {enhanced_script}"
            
            if "agradecemos" not in script.lower() and "obrigado" not in script.lower():
                thanksgiving = prayer_elements["thanksgiving"][0]
                enhanced_script = f"{enhanced_script} {thanksgiving}. [...]"
            
            # Garantir que termine com "Amém"
            if not enhanced_script.strip().endswith("Amém"):
                enhanced_script = f"{enhanced_script} Amém."
            
            # Adicionar pausas estratégicas baseadas na duração
            if duration_minutes >= 3:
                # Dividir o script em seções com pausas
                sentences = enhanced_script.split('. ')
                enhanced_sections = []
                for i, sentence in enumerate(sentences):
                    enhanced_sections.append(sentence)
                    if i % 3 == 2 and i < len(sentences) - 1:  # Pausa a cada 3 frases
                        enhanced_sections.append("[...]")
                
                enhanced_script = '. '.join(enhanced_sections)
            
            return enhanced_script
            
        except Exception as e:
            print(f"⚠️ Erro ao adaptar para template de oração: {e}")
            return script
    
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
                "Conhece o poder transformador do amor de Deus?",
                "Sabe como encontrar paz em meio às tempestades da vida?"
            ]
            
            # Conclusões inspiradoras
            inspiring_conclusions = [
                "Lembre-se: Deus não prometeu uma vida sem problemas, mas prometeu estar conosco em todos os momentos.",
                "Que a paz de Deus, que excede todo entendimento, guarde seu coração e sua mente.",
                "Deus tem um plano perfeito para sua vida. Confie Nele e siga em frente com fé.",
                "Que o Senhor te abençoe e te guarde, que Ele faça resplandecer o Seu rosto sobre ti.",
                "Em Cristo, você é mais que vencedor. Mantenha a fé e persevere!"
            ]
            
            # Adaptar abertura se necessário
            if not any(opening in script for opening in opening_elements):
                import random
                opening = random.choice(opening_elements)
                question = random.choice(impact_questions)
                script = f"{opening} {question} {script}"
            
            # Adaptar conclusão se necessário
            if not any(conclusion in script for conclusion in inspiring_conclusions):
                import random
                conclusion = random.choice(inspiring_conclusions)
                script = f"{script} {conclusion}"
            
            # Garantir chamada à ação
            if "deixe seu comentário" not in script.lower():
                script = f"{script} Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"
            
            return script
            
        except Exception as e:
            print(f"⚠️ Erro ao adaptar para template religioso: {e}")
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