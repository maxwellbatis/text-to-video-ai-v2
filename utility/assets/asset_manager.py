import os
import json
from pathlib import Path
from typing import Dict, List, Optional

class AssetManager:
    """Gerenciador de assets para efeitos, músicas e transições"""
    
    def __init__(self):
        self.assets_root = Path("assets")
        self.audio_effects = self._load_audio_effects()
        self.video_effects = self._load_video_effects()
        self.music_tracks = self._load_music_tracks()
        
    def _load_audio_effects(self) -> Dict[str, List[str]]:
        """Carrega efeitos sonoros organizados por categoria"""
        effects = {
            "cinematic": [],
            "impacts": [],
            "tension": [],
            "glitch": [],
            "heartbeat": [],
            "explosions": [],
            "drones": [],
            "reverse": []
        }
        
        # Diretório CINEMATIC
        cinematic_dir = self.assets_root / "EFEITOS SONOROS" / "CINEMATIC"
        if cinematic_dir.exists():
            for file in cinematic_dir.glob("*.wav"):
                if "tension" in file.name.lower():
                    effects["tension"].append(str(file))
                elif "impact" in file.name.lower():
                    effects["impacts"].append(str(file))
                elif "glitch" in file.name.lower():
                    effects["glitch"].append(str(file))
                elif "heartbeat" in file.name.lower():
                    effects["heartbeat"].append(str(file))
                elif "explosion" in file.name.lower():
                    effects["explosions"].append(str(file))
                elif "drone" in file.name.lower():
                    effects["drones"].append(str(file))
                elif "reverse" in file.name.lower():
                    effects["reverse"].append(str(file))
                else:
                    effects["cinematic"].append(str(file))
            
            # Incluir arquivos .mp3 também
            for file in cinematic_dir.glob("*.mp3"):
                if "heartbeat" in file.name.lower():
                    effects["heartbeat"].append(str(file))
                elif "orchestra" in file.name.lower():
                    effects["cinematic"].append(str(file))
                elif "radio" in file.name.lower():
                    effects["cinematic"].append(str(file))
                elif "wind" in file.name.lower():
                    effects["cinematic"].append(str(file))
                elif "weird" in file.name.lower():
                    effects["glitch"].append(str(file))
        
        # Diretório IMPACTOS
        impactos_dir = self.assets_root / "EFEITOS SONOROS" / "IMPACTOS"
        if impactos_dir.exists():
            for file in impactos_dir.glob("*.mp3"):
                effects["impacts"].append(str(file))
        
        return effects
    
    def _load_video_effects(self) -> Dict[str, List[str]]:
        """Carrega efeitos visuais organizados por categoria"""
        effects = {
            "fire": [],
            "film_old": [],
            "transitions": [],
            "overlays": [],
            "light_leaks": []
        }
        
        # Efeitos de fogo
        efeitos_dir = self.assets_root / "EFEITOS DE VÍDEO" / "EFEITOS_AMOSTRA"
        if efeitos_dir.exists():
            for file in efeitos_dir.glob("*.mp4"):
                if "fire" in file.name.lower():
                    effects["fire"].append(str(file))
                elif "filme" in file.name.lower():
                    effects["film_old"].append(str(file))
        
        # Transições e overlays
        transicoes_dir = self.assets_root / "EFEITOS DE VÍDEO" / "TRANSIÇÕES_AMOSTRA"
        if transicoes_dir.exists():
            for file in transicoes_dir.glob("*.mp4"):
                if "overlay" in file.name.lower():
                    effects["overlays"].append(str(file))
                elif "light" in file.name.lower():
                    effects["light_leaks"].append(str(file))
                else:
                    effects["transitions"].append(str(file))
        
        return effects
    
    def _load_music_tracks(self) -> Dict[str, List[str]]:
        """Carrega trilhas sonoras organizadas por categoria"""
        tracks = {
            "cinematic": [],
            "suspense": [],
            "atmospheric": [],
            "religious": []
        }
        
        # Músicas cinematográficas
        music_dir = self.assets_root / "TRILHA SONORA" / "CINEMATIC"
        if music_dir.exists():
            for file in music_dir.glob("*.mp3"):
                if "suspense" in file.name.lower():
                    tracks["suspense"].append(str(file))
                elif "atmosphera" in file.name.lower():
                    tracks["atmospheric"].append(str(file))
                else:
                    tracks["cinematic"].append(str(file))
            
            # Incluir arquivos .aac também
            for file in music_dir.glob("*.aac"):
                if "suspense" in file.name.lower():
                    tracks["suspense"].append(str(file))
        
        # Músicas religiosas
        religious_dir = self.assets_root / "TRILHA SONORA" / "Biblic"
        if religious_dir.exists():
            for file in religious_dir.glob("*.mp3"):
                tracks["religious"].append(str(file))
        
        return tracks
    
    def get_audio_effect(self, category: str, index: int = 0) -> Optional[str]:
        """Obtém um efeito sonoro específico"""
        if category in self.audio_effects and self.audio_effects[category]:
            effects = self.audio_effects[category]
            if 0 <= index < len(effects):
                return effects[index]
        return None
    
    def get_video_effect(self, category: str, index: int = 0) -> Optional[str]:
        """Obtém um efeito visual específico"""
        if category in self.video_effects and self.video_effects[category]:
            effects = self.video_effects[category]
            if 0 <= index < len(effects):
                return effects[index]
        return None
    
    def get_music_track(self, category: str, index: int = 0) -> Optional[str]:
        """Obtém uma trilha sonora específica"""
        if category in self.music_tracks and self.music_tracks[category]:
            tracks = self.music_tracks[category]
            if 0 <= index < len(tracks):
                return tracks[index]
        return None
    
    def get_religious_music_by_name(self, music_name: str) -> Optional[str]:
        """Obtém uma música religiosa específica pelo nome"""
        religious_tracks = self.music_tracks.get("religious", [])
        
        # Mapeamento de nomes para arquivos
        music_mapping = {
            "piano-worship": "piano-worship-184108.mp3",
            "worship-piano": "worship-piano-instrumental-peaceful-prayer-music-223373.mp3",
            "guitar-worship": "instrumental-guitar-worship-to-jesus-301253.mp3",
            "piano-christian": "instrumental-piano-christian-worship-of-jesus-301250.mp3",
            "cherry-blossom": "cherry-blossom-christian-worship-music-for-jesus-christ-312719.mp3",
            "morning-light": "morningx27s-first-light-worship-music-to-jesus-christ-our-god-312717.mp3",
            "peaceful-piano": "peaceful-piano-soaking-instrumental-worship-track-loops-223094.mp3",
            "gospel-worship": "gospel-worship-church-prayer-music-343269.mp3",
            "christian-piano": "christian-instrumental-piano-worship-calm-emotional-soaking-prayer-249459.mp3",
            "worship-gospel": "worship-gospel-christian-church-music-351228.mp3"
        }
        
        target_file = music_mapping.get(music_name)
        if target_file:
            for track in religious_tracks:
                if target_file in track:
                    return track
        
        # Se não encontrar, retornar a primeira música religiosa disponível
        return religious_tracks[0] if religious_tracks else None
    
    def list_available_assets(self) -> Dict:
        """Lista todos os assets disponíveis"""
        return {
            "audio_effects": self.audio_effects,
            "video_effects": self.video_effects,
            "music_tracks": self.music_tracks
        }
    
    def get_assets_for_template(self, template_id: str, background_music_choice: str = None) -> Dict:
        """Obtém assets recomendados para um template específico"""
        if template_id == "cinematic_religious" or template_id == "prayer_extended":
            # Para templates religiosos, usar música religiosa se especificada
            if background_music_choice:
                background_music = self.get_religious_music_by_name(background_music_choice)
            else:
                # Usar música religiosa aleatória
                import random
                religious_tracks = self.music_tracks["religious"]
                background_music = random.choice(religious_tracks) if religious_tracks else self.get_music_track("cinematic", 0)
            
            return {
                "background_music": background_music,
                "tension_effect": self.get_audio_effect("cinematic", 0),    # Orchestra build up 01.mp3
                "impact_effect": self.get_audio_effect("impacts", 0),       # Primeiro impacto disponível
                "film_overlay": self.get_video_effect("film_old", 0),       # Filme antigo
                "light_leak": self.get_video_effect("light_leaks", 0),      # Light leak
                "drones": None,        # Não disponível no VPS
                "reverse": None        # Não disponível no VPS
            }
        elif template_id == "dramatic":
            return {
                "background_music": self.get_music_track("suspense", 0),    # cinematic_suspense01.mp3
                "explosion_effect": self.get_audio_effect("impacts", 0),     # Primeiro impacto disponível
                "glitch_effect": self.get_audio_effect("glitch", 0),        # Weird noise.mp3
                "vibrant_overlay": None,  # Não disponível no VPS
                "heartbeat": self.get_audio_effect("heartbeat", 0),         # Heartbeat.mp3
                "tension": self.get_audio_effect("cinematic", 1)            # Radio station search.mp3
            }
        else:
            return {
                "background_music": self.get_music_track("cinematic", 0),
                "tension_effect": self.get_audio_effect("cinematic", 0),
                "atmospheric": self.get_music_track("atmospheric", 0)        # cinematic_atmosphera.mp3
            }

# Instância global do asset manager
asset_manager = AssetManager() 