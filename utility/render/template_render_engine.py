#!/usr/bin/env python3
"""
Motor de Renderização de Templates
Aplica configurações de template ao vídeo final
"""

import os
import json
from typing import Dict, List, Optional
from moviepy.editor import AudioFileClip, CompositeVideoClip, CompositeAudioClip, VideoFileClip, TextClip
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.audio_loop import audio_loop

class TemplateRenderEngine:
    def __init__(self):
        self.templates = {}
    
    def apply_template_to_video(self, video_path: str, template_config: Dict, audio_path: str = None) -> str:
        """Aplica configurações de template ao vídeo"""
        try:
            # Carregar vídeo
            video = VideoFileClip(video_path)
            
            # Aplicar configurações visuais
            video = self._apply_visual_settings(video, template_config.get('visual_settings', {}))
            
            # Aplicar configurações de áudio
            if audio_path and os.path.exists(audio_path):
                video = self._apply_audio_settings(video, audio_path, template_config.get('audio_settings', {}))
            
            # Aplicar efeitos
            video = self._apply_effects(video, template_config.get('effects', {}))
            
            # Salvar vídeo processado
            output_path = f"template_processed_{os.path.basename(video_path)}"
            video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            return output_path
            
        except Exception as e:
            print(f"❌ Erro ao aplicar template: {e}")
            return video_path
    
    def _apply_visual_settings(self, video: VideoFileClip, visual_settings: Dict) -> VideoFileClip:
        """Aplica configurações visuais do template"""
        try:
            # Aplicar resolução se especificada
            if 'resolution' in visual_settings:
                width, height = map(int, visual_settings['resolution'].split('x'))
                video = video.resize((width, height))
            
            # Aplicar efeitos de transição
            if 'transition_effects' in visual_settings:
                video = self._apply_transitions(video, visual_settings['transition_effects'])
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar configurações visuais: {e}")
            return video
    
    def _apply_audio_settings(self, video: VideoFileClip, audio_path: str, audio_settings: Dict) -> VideoFileClip:
        """Aplica configurações de áudio do template"""
        try:
            # Carregar áudio
            audio = AudioFileClip(audio_path)
            
            # Normalizar áudio se especificado
            if audio_settings.get('voice_processing', {}).get('normalize', False):
                audio = audio_normalize(audio)
            
            # Aplicar volume de música de fundo
            if 'background_music' in audio_settings:
                bg_volume = audio_settings['background_music'].get('volume', 0.15)
                # Reduzir volume do áudio principal para dar espaço à música
                audio = audio.volumex(1.0 - bg_volume)
            
            # Aplicar efeitos de áudio
            if 'sound_effects' in audio_settings:
                audio = self._apply_audio_effects(audio, audio_settings['sound_effects'])
            
            # Combinar áudio com vídeo
            video = video.set_audio(audio)
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar configurações de áudio: {e}")
            return video
    
    def _apply_transitions(self, video: VideoFileClip, transitions: List[str]) -> VideoFileClip:
        """Aplica efeitos de transição"""
        try:
            # Implementar transições básicas
            if 'fade_in' in transitions:
                video = video.fadein(1.0)
            if 'fade_out' in transitions:
                video = video.fadeout(1.0)
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar transições: {e}")
            return video
    
    def _apply_audio_effects(self, audio: AudioFileClip, effects_config: Dict) -> AudioFileClip:
        """Aplica efeitos de áudio"""
        try:
            # Aplicar volume de efeitos
            if 'volume' in effects_config:
                audio = audio.volumex(effects_config['volume'])
            
            return audio
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar efeitos de áudio: {e}")
            return audio
    
    def _apply_effects(self, video: VideoFileClip, effects: Dict) -> VideoFileClip:
        """Aplica efeitos visuais e de áudio"""
        try:
            # Implementar efeitos visuais básicos
            if 'visual' in effects:
                for effect in effects['visual']:
                    if effect == 'slow_motion':
                        video = video.speedx(0.5)
                    elif effect == 'color_grading':
                        # Implementar gradiente de cores básico
                        pass
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar efeitos: {e}")
            return video
    
    def apply_strategic_pauses(self, audio_path: str, pauses_config: Dict) -> str:
        """Aplica pausas estratégicas ao áudio"""
        try:
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Criar segmentos de áudio com pausas
            segments = []
            current_time = 0
            
            # Aplicar pausas de impacto
            impact_pauses = pauses_config.get('impact_pauses', [])
            for pause in impact_pauses:
                pause_time = duration * pause['position']
                pause_duration = pause['duration']
                
                # Adicionar segmento antes da pausa
                if pause_time > current_time:
                    segment = audio.subclip(current_time, pause_time)
                    segments.append(segment)
                
                # Adicionar silêncio (pausa)
                silence = AudioFileClip(audio_path).subclip(0, pause_duration).volumex(0)
                # Definir fps para evitar erro
                silence.fps = audio.fps
                segments.append(silence)
                
                current_time = pause_time + pause_duration
            
            # Adicionar segmento final
            if current_time < duration:
                final_segment = audio.subclip(current_time, duration)
                segments.append(final_segment)
            
            # Combinar segmentos
            if segments:
                final_audio = CompositeAudioClip(segments)
                output_path = f"paused_{os.path.basename(audio_path)}"
                final_audio.write_audiofile(output_path)
                return output_path
            
            return audio_path
            
        except Exception as e:
            print(f"❌ Erro ao aplicar pausas estratégicas: {e}")
            return audio_path 