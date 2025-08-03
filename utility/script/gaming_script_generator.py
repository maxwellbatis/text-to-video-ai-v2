#!/usr/bin/env python3
"""
Gerador de Scripts para Gaming
Gera scripts específicos para tutoriais e highlights de jogos
"""

import json
import random
from typing import Dict, List, Optional

class GamingScriptGenerator:
    def __init__(self):
        self.tutorial_templates = {
            "fps": {
                "intro": "Aprenda como fazer {técnica} em {jogo}",
                "steps": [
                    "Passo 1: Posicione-se corretamente",
                    "Passo 2: Ajuste sua mira",
                    "Passo 3: Controle o recuo",
                    "Passo 4: Pratique o timing"
                ],
                "tip": "Dica: Mantenha a calma e respire fundo",
                "outro": "Pratique diariamente para melhorar!"
            },
            "moba": {
                "intro": "Domine {técnica} em {jogo}",
                "steps": [
                    "Passo 1: Entenda o mapa",
                    "Passo 2: Posicione-se estrategicamente",
                    "Passo 3: Use suas habilidades no momento certo",
                    "Passo 4: Trabalhe em equipe"
                ],
                "tip": "Dica: Comunicação é fundamental",
                "outro": "Continue praticando e evoluindo!"
            },
            "battle_royale": {
                "intro": "Sobreviva e vença em {jogo}",
                "steps": [
                    "Passo 1: Escolha o local de pouso",
                    "Passo 2: Colete equipamentos rapidamente",
                    "Passo 3: Mantenha-se em movimento",
                    "Passo 4: Use a cobertura a seu favor"
                ],
                "tip": "Dica: Sempre tenha um plano de fuga",
                "outro": "Seja paciente e estratégico!"
            }
        }
        
        self.highlights_templates = {
            "fps": [
                "HEADSHOT PERFEITO!",
                "CLUTCH INCRÍVEL!",
                "PLAY MORTAL!",
                "VICTORY ROYALE!"
            ],
            "moba": [
                "PENTAKILL ÉPICO!",
                "PLAY PERFEITO!",
                "VICTORY INCRÍVEL!",
                "DOMINAÇÃO TOTAL!"
            ],
            "battle_royale": [
                "VICTORY ROYALE!",
                "PLAY INCRÍVEL!",
                "SURVIVAL MASTER!",
                "CHAMPION!"
            ]
        }
    
    def generate_tutorial_script(self, topic: str, game_type: str = "fps") -> str:
        """Gera script para tutorial de gaming"""
        try:
            # Extrair técnica e jogo do tópico
            words = topic.split()
            if len(words) >= 3:
                técnica = " ".join(words[2:])  # "fazer headshot"
                jogo = words[0]  # "CS2"
            else:
                técnica = "melhorar no jogo"
                jogo = "seu jogo favorito"
            
            template = self.tutorial_templates.get(game_type, self.tutorial_templates["fps"])
            
            # Gerar script estruturado
            script = f"{template['intro'].format(técnica=técnica, jogo=jogo)}\n\n"
            
            for step in template["steps"]:
                script += f"{step}\n"
            
            script += f"\n{template['tip']}\n\n"
            script += template["outro"]
            
            return script
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar tutorial: {e}")
            return f"Aprenda como melhorar em {topic}. Pratique diariamente e você verá resultados!"
    
    def generate_highlights_script(self, topic: str, game_type: str = "fps") -> str:
        """Gera script para highlights de gaming"""
        try:
            highlights = self.highlights_templates.get(game_type, self.highlights_templates["fps"])
            
            # Gerar script dramático
            script = "MOMENTOS ÉPICOS\n\n"
            
            for i, highlight in enumerate(highlights[:3]):  # Máximo 3 highlights
                script += f"{highlight}\n"
            
            script += "\nINSCREVA-SE PARA MAIS!"
            
            return script
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar highlights: {e}")
            return "MOMENTOS ÉPICOS!\nPLAY INCRÍVEL!\nVICTORY ROYALE!\nINSCREVA-SE PARA MAIS!"
    
    def detect_game_type(self, topic: str) -> str:
        """Detecta o tipo de jogo baseado no tópico"""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["cs", "valorant", "cod", "fps", "shooter"]):
            return "fps"
        elif any(word in topic_lower for word in ["lol", "dota", "moba", "league", "dota"]):
            return "moba"
        elif any(word in topic_lower for word in ["fortnite", "pubg", "apex", "battle royale"]):
            return "battle_royale"
        else:
            return "fps"  # Padrão

# Funções de conveniência
def generate_gaming_tutorial(topic: str) -> str:
    """Gera tutorial de gaming"""
    generator = GamingScriptGenerator()
    game_type = generator.detect_game_type(topic)
    return generator.generate_tutorial_script(topic, game_type)

def generate_gaming_highlights(topic: str) -> str:
    """Gera highlights de gaming"""
    generator = GamingScriptGenerator()
    game_type = generator.detect_game_type(topic)
    return generator.generate_highlights_script(topic, game_type) 