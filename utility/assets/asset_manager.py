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
            "explosions": []
        }
        
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
                else:
                    effects["cinematic"].append(str(file))
        
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
            "atmospheric": []
        }
        
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
    
    def list_available_assets(self) -> Dict:
        """Lista todos os assets disponíveis"""
        return {
            "audio_effects": self.audio_effects,
            "video_effects": self.video_effects,
            "music_tracks": self.music_tracks
        }
    
    def get_assets_for_template(self, template_id: str) -> Dict:
        """Obtém assets recomendados para um template específico"""
        if template_id == "cinematic_religious":
            return {
                "background_music": self.get_music_track("cinematic", 0),  # Cinematic_principal.mp3
                "tension_effect": self.get_audio_effect("tension", 0),      # Cinematic_Tension_coração.wav
                "impact_effect": self.get_audio_effect("impacts", 0),       # Cinematic_impact02.wav
                "film_overlay": self.get_video_effect("overlays", 0),       # OverlayFilm_sfx15.mp4
                "light_leak": self.get_video_effect("light_leaks", 0)       # LightLeak02_sfx18.mp4
            }
        elif template_id == "dramatic":
            return {
                "background_music": self.get_music_track("suspense", 0),    # cinematic_suspense01.mp3
                "explosion_effect": self.get_audio_effect("explosions", 0), # Explosion_Debris.wav
                "glitch_effect": self.get_audio_effect("glitch", 0),        # Cinematic_Glitch04.wav
                "vibrant_overlay": self.get_video_effect("overlays", 2)     # Overlay_vibrante_sfx16.mp4
            }
        else:
            return {
                "background_music": self.get_music_track("cinematic", 0),
                "tension_effect": self.get_audio_effect("tension", 0)
            }

# Instância global do asset manager
asset_manager = AssetManager() 