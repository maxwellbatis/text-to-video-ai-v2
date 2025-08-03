#!/usr/bin/env python3
"""
Gerador de Script para VSL Magnética
- Estrutura de 5 blocos
- Estilo criativo e energético
- Otimizado para Reels/TikTok
"""

import json
import random
from typing import Dict, List

class VSLScriptGenerator:
    def __init__(self):
        self.template = self._load_template()
    
    def _load_template(self) -> Dict:
        """Carrega o template VSL magnética"""
        try:
            with open('utility/templates/vsl_magnetic.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_template()
    
    def _get_default_template(self) -> Dict:
        """Template padrão caso arquivo não seja encontrado"""
        return {
            "text_templates": {
                "hook": [
                    "Você também sente que está tentando de tudo e nada funciona?",
                    "Já tentou de tudo e continua no mesmo lugar?",
                    "Cansada de tentar e não ver resultado?",
                    "Frustrada porque nada parece dar certo?"
                ],
                "problem": [
                    "Frustração. Cansaço. Dúvida. Medo.",
                    "É difícil continuar quando nada parece dar resultado.",
                    "Você não está sozinha nessa situação.",
                    "Muitas pessoas passam por isso."
                ],
                "solution": [
                    "✅ Existe um jeito diferente.\n🧠 Com foco, clareza e resultado.\n💥 Sem complicação, sem enrolação.",
                    "A diferença está em parar de tentar tudo…\ne focar no que realmente transforma.",
                    "Não é mágica. É método.\nSimples, direto e eficaz."
                ],
                "proof": [
                    "\"Em poucos dias, comecei a ver mudanças reais.\"\n\"Era o que eu precisava — simples e direto.\"",
                    "Você não precisa de mágica.\nSó de direção certa.",
                    "Muitas pessoas já transformaram suas vidas.\nVocê pode ser a próxima."
                ],
                "cta": [
                    "A decisão está nas suas mãos.\n👉 Toque agora e veja o que pode mudar.",
                    "Você já viu o que não funciona.\nAgora veja o que funciona.",
                    "Não perca mais tempo.\nClique agora e transforme sua vida."
                ]
            }
        }
    
    def generate_vsl_script(self, topic: str, niche: str = "general", template_config: Dict = None) -> str:
        """
        Gera script VSL magnética com estrutura de 5 blocos
        
        Args:
            topic: Tópico principal
            niche: Nicho (saas, maternity, fitness, etc.)
            template_config: Configuração do template (opcional)
        
        Returns:
            String com script completo
        """
        
        # Selecionar templates baseado no nicho
        templates = self.template.get("text_templates", {})
        
        # Gerar script estruturado
        script_structure = {
            "topic": topic,
            "niche": niche,
            "duration_target": 30,
            "blocks": {
                "hook": {
                    "text": self._select_template(templates.get("hook", [])),
                    "duration": "0-5s",
                    "emotion": "frustration",
                    "style": "impact"
                },
                "problem": {
                    "text": self._select_template(templates.get("problem", [])),
                    "duration": "5-10s",
                    "emotion": "struggle",
                    "style": "empathy"
                },
                "solution": {
                    "text": self._select_template(templates.get("solution", [])),
                    "duration": "10-20s",
                    "emotion": "relief",
                    "style": "hope"
                },
                "proof": {
                    "text": self._select_template(templates.get("proof", [])),
                    "duration": "20-25s",
                    "emotion": "confidence",
                    "style": "social_proof"
                },
                "cta": {
                    "text": self._select_template(templates.get("cta", [])),
                    "duration": "25-30s",
                    "emotion": "urgency",
                    "style": "action"
                }
            }
        }
        
        # Combinar blocos em texto contínuo
        combined_text = self._combine_blocks(script_structure["blocks"])
        
        # Adicionar contexto do tópico se fornecido
        if topic and len(topic) > 10:
            # Inserir o tópico no início do script
            combined_text = f"Fatos surpreendentes sobre {topic}: {combined_text}"
        
        return combined_text
    
    def _select_template(self, templates: List[str]) -> str:
        """Seleciona template aleatório"""
        if not templates:
            return "Texto padrão"
        return random.choice(templates)
    
    def _combine_blocks(self, templates: Dict) -> str:
        """Combina todos os blocos em um script completo"""
        blocks = []
        
        for block_name in ["hook", "problem", "solution", "proof", "cta"]:
            if block_name in templates:
                text = self._select_template(templates[block_name])
                blocks.append(text)
        
        return "\n\n".join(blocks)
    
    def _get_visual_instructions(self) -> Dict:
        """Retorna instruções visuais para o template"""
        return {
            "format": "vertical",
            "resolution": "720x1280",
            "font": "Impact",
            "font_size": 120,
            "effects": [
                "zoom_in",
                "shake",
                "flash",
                "bounce",
                "glow"
            ],
            "colors": {
                "primary": "white",
                "stroke": "black",
                "accent": "yellow"
            }
        }
    
    def _get_audio_instructions(self) -> Dict:
        """Retorna instruções de áudio para o template"""
        return {
            "voice": "pt-BR-AntonioNeural",
            "rate": "fast",
            "pitch": "high",
            "music": "energetic",
            "sound_effects": [
                "whoosh",
                "pop",
                "typing",
                "impact",
                "bell"
            ]
        }
    
    def generate_custom_vsl(self, topic: str, pain_point: str, solution: str, benefit: str) -> Dict:
        """
        Gera VSL customizada com elementos específicos
        
        Args:
            topic: Tópico principal
            pain_point: Ponto de dor específico
            solution: Solução oferecida
            benefit: Benefício principal
        """
        
        # Criar templates customizados
        custom_templates = {
            "hook": [
                f"Você também {pain_point.lower()}?",
                f"Já tentou de tudo para {pain_point.lower()}?",
                f"Cansada de {pain_point.lower()} sem resultado?",
                f"Frustrada porque {pain_point.lower()} não funciona?"
            ],
            "problem": [
                f"{pain_point}. Dúvida. Medo.",
                f"É difícil continuar quando {pain_point.lower()}.",
                f"Você não está sozinha nessa situação.",
                f"Muitas pessoas passam por isso."
            ],
            "solution": [
                f"✅ {solution}.\n🧠 {benefit}.\n💥 Sem complicação.",
                f"A diferença está em {solution.lower()}.",
                f"Não é mágica. É método.\nSimples, direto e eficaz."
            ],
            "proof": [
                f"\"Em poucos dias, {benefit.lower()}.\"\n\"Era o que eu precisava — simples e direto.\"",
                f"Você não precisa de mágica.\nSó de {solution.lower()}.",
                f"Muitas pessoas já {benefit.lower()}.\nVocê pode ser a próxima."
            ],
            "cta": [
                f"A decisão está nas suas mãos.\n👉 {solution} agora.",
                f"Você já viu o que não funciona.\nAgora veja {solution.lower()}.",
                f"Não perca mais tempo.\n{benefit} agora."
            ]
        }
        
        # Atualizar template temporariamente
        original_templates = self.template.get("text_templates", {})
        self.template["text_templates"] = custom_templates
        
        # Gerar script
        script = self.generate_vsl_script(topic)
        
        # Restaurar template original
        self.template["text_templates"] = original_templates
        
        return script

def generate_vsl_script(topic: str, niche: str = "general") -> Dict:
    """
    Função principal para gerar script VSL magnética
    
    Args:
        topic: Tópico principal
        niche: Nicho específico
    
    Returns:
        Dict com script estruturado
    """
    generator = VSLScriptGenerator()
    return generator.generate_vsl_script(topic, niche)

def generate_custom_vsl(topic: str, pain_point: str, solution: str, benefit: str) -> Dict:
    """
    Função para gerar VSL customizada
    
    Args:
        topic: Tópico principal
        pain_point: Ponto de dor
        solution: Solução
        benefit: Benefício
    
    Returns:
        Dict com script customizado
    """
    generator = VSLScriptGenerator()
    return generator.generate_custom_vsl(topic, pain_point, solution, benefit)

if __name__ == "__main__":
    # Teste do gerador
    generator = VSLScriptGenerator()
    
    # Teste básico
    script = generator.generate_vsl_script("Marketing Digital", "saas")
    print("🎬 VSL MAGNÉTICA GERADA:")
    print("=" * 50)
    print(f"Tópico: {script['topic']}")
    print(f"Nicho: {script['niche']}")
    print(f"Duração: {script['duration_target']}s")
    print("\n📝 BLOCOS:")
    for block_name, block_data in script['blocks'].items():
        print(f"\n{block_name.upper()}:")
        print(f"  Texto: {block_data['text']}")
        print(f"  Duração: {block_data['duration']}")
        print(f"  Emoção: {block_data['emotion']}")
    
    print("\n🎨 INSTRUÇÕES VISUAIS:")
    for key, value in script['visual_instructions'].items():
        print(f"  {key}: {value}")
    
    print("\n🎵 INSTRUÇÕES DE ÁUDIO:")
    for key, value in script['audio_instructions'].items():
        print(f"  {key}: {value}") 