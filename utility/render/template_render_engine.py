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

# Importar AssetManager
try:
    from utility.assets.asset_manager import asset_manager
    ASSETS_AVAILABLE = True
except ImportError:
    print("⚠️ AssetManager não disponível - usando configurações padrão")
    ASSETS_AVAILABLE = False

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
            
            # Aplicar configurações de áudio com assets
            if audio_path and os.path.exists(audio_path):
                video = self._apply_audio_settings_with_assets(video, audio_path, template_config)
            
            # Aplicar efeitos visuais com assets
            video = self._apply_effects_with_assets(video, template_config)
            
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
                # Usar método de redimensionamento compatível
                try:
                    video = video.resize((width, height))
                except AttributeError:
                    # Fallback para versões mais antigas do PIL
                    video = video.resize((width, height), resample='bicubic')
            
            # Aplicar efeitos de transição
            if 'transition_effects' in visual_settings:
                video = self._apply_transitions(video, visual_settings['transition_effects'])
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar configurações visuais: {e}")
            return video
    
    def _apply_audio_settings_with_assets(self, video: VideoFileClip, audio_path: str, template_config: Dict) -> VideoFileClip:
        """Aplica configurações de áudio com assets do template"""
        try:
            # Carregar áudio principal
            audio = AudioFileClip(audio_path)
            print(f"🎵 Áudio principal carregado: {os.path.basename(audio_path)}")
            
            # Obter assets para o template
            template_id = template_config.get('template_id', 'default')
            print(f"🎵 Aplicando áudio para template: {template_id}")
            
            if ASSETS_AVAILABLE:
                assets = asset_manager.get_assets_for_template(template_id)
                print(f"🎵 Assets de áudio encontrados: {list(assets.keys())}")
                
                # Adicionar música de fundo
                if assets.get('background_music') and os.path.exists(assets['background_music']):
                    print(f"🎵 Tentando aplicar música de fundo: {assets['background_music']}")
                    try:
                        bg_music = AudioFileClip(assets['background_music'])
                        # Loop da música de fundo para cobrir toda a duração
                        bg_music = audio_loop(bg_music, duration=audio.duration)
                        # Volume reduzido para não competir com a narração
                        bg_music = bg_music.volumex(0.1)
                        
                        # Combinar áudio principal com música de fundo
                        audio = CompositeAudioClip([audio, bg_music])
                        print(f"✅ Música de fundo aplicada: {os.path.basename(assets['background_music'])}")
                    except Exception as e:
                        print(f"❌ Erro ao aplicar música de fundo: {e}")
                else:
                    print(f"⚠️ Música de fundo não encontrada ou não existe")
                
                # Adicionar efeitos sonoros
                audio_clips = [audio]
                
                # Efeito de tensão
                if assets.get('tension_effect') and os.path.exists(assets['tension_effect']):
                    print(f"🎵 Tentando aplicar efeito de tensão: {assets['tension_effect']}")
                    try:
                        tension = AudioFileClip(assets['tension_effect'])
                        tension = tension.volumex(0.3)
                        audio_clips.append(tension)
                        print(f"✅ Efeito de tensão aplicado: {os.path.basename(assets['tension_effect'])}")
                    except Exception as e:
                        print(f"❌ Erro ao aplicar efeito de tensão: {e}")
                else:
                    print(f"⚠️ Efeito de tensão não encontrado ou não existe")
                
                # Efeito de impacto
                if assets.get('impact_effect') and os.path.exists(assets['impact_effect']):
                    print(f"🎵 Tentando aplicar efeito de impacto: {assets['impact_effect']}")
                    try:
                        impact = AudioFileClip(assets['impact_effect'])
                        impact = impact.volumex(0.2)
                        audio_clips.append(impact)
                        print(f"✅ Efeito de impacto aplicado: {os.path.basename(assets['impact_effect'])}")
                    except Exception as e:
                        print(f"❌ Erro ao aplicar efeito de impacto: {e}")
                else:
                    print(f"⚠️ Efeito de impacto não encontrado ou não existe")
                
                if len(audio_clips) > 1:
                    print(f"🎵 Combinando {len(audio_clips)} clips de áudio")
                    audio = CompositeAudioClip(audio_clips)
                else:
                    print(f"⚠️ Nenhum efeito de áudio aplicado")
            else:
                print(f"⚠️ AssetManager não disponível")
            
            # Normalizar áudio final
            try:
                audio = audio_normalize(audio)
            except AttributeError:
                # CompositeAudioClip não tem atributo fps, pular normalização
                print("⚠️ Pulando normalização do áudio (CompositeAudioClip)")
            
            # Combinar áudio com vídeo
            video = video.set_audio(audio)
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar configurações de áudio com assets: {e}")
            import traceback
            traceback.print_exc()
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
    
    def _apply_effects_with_assets(self, video: VideoFileClip, template_config: Dict) -> VideoFileClip:
        """Aplica efeitos visuais com assets do template"""
        try:
            template_id = template_config.get('template_id', 'default')
            print(f"🎬 Aplicando efeitos visuais para template: {template_id}")
            
            if ASSETS_AVAILABLE:
                assets = asset_manager.get_assets_for_template(template_id)
                print(f"📋 Assets encontrados: {list(assets.keys())}")
                video_clips = [video]
                
                # Adicionar overlay de filme antigo
                if assets.get('film_overlay') and os.path.exists(assets['film_overlay']):
                    print(f"🎬 Tentando aplicar overlay de filme: {assets['film_overlay']}")
                    try:
                        overlay = VideoFileClip(assets['film_overlay'])
                        overlay = overlay.resize(video.size)
                        overlay = overlay.set_duration(video.duration)
                        overlay = overlay.set_opacity(0.3)  # 30% de opacidade
                        video_clips.append(overlay)
                        print(f"✅ Overlay de filme aplicado: {os.path.basename(assets['film_overlay'])}")
                    except Exception as e:
                        print(f"❌ Erro ao aplicar overlay de filme: {e}")
                else:
                    print(f"⚠️ Overlay de filme não encontrado ou não existe")
                
                # Adicionar light leak
                if assets.get('light_leak') and os.path.exists(assets['light_leak']):
                    print(f"🎬 Tentando aplicar light leak: {assets['light_leak']}")
                    try:
                        light_leak = VideoFileClip(assets['light_leak'])
                        light_leak = light_leak.resize(video.size)
                        light_leak = light_leak.set_duration(video.duration)
                        light_leak = light_leak.set_opacity(0.2)  # 20% de opacidade
                        video_clips.append(light_leak)
                        print(f"✅ Light leak aplicado: {os.path.basename(assets['light_leak'])}")
                    except Exception as e:
                        print(f"❌ Erro ao aplicar light leak: {e}")
                else:
                    print(f"⚠️ Light leak não encontrado ou não existe")
                
                if len(video_clips) > 1:
                    print(f"🎬 Combinando {len(video_clips)} clips de vídeo")
                    video = CompositeVideoClip(video_clips)
                else:
                    print(f"⚠️ Nenhum efeito visual aplicado")
            else:
                print(f"⚠️ AssetManager não disponível")
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar efeitos visuais com assets: {e}")
            import traceback
            traceback.print_exc()
            return video
    
    def apply_strategic_pauses(self, audio_path: str, pauses_config: Dict) -> str:
        """Aplica pausas estratégicas ao áudio de forma mais suave"""
        try:
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Verificar se há pausas configuradas
            impact_pauses = pauses_config.get('impact_pauses', [])
            if not impact_pauses:
                print("⚠️ Nenhuma pausa estratégica configurada")
                return audio_path
            
            # Criar segmentos de áudio com pausas mais suaves
            segments = []
            current_time = 0
            
            for pause in impact_pauses:
                pause_time = duration * pause['position']
                pause_duration = pause['duration']
                
                # Verificar se a pausa está dentro dos limites
                if pause_time >= duration:
                    continue
                
                # Adicionar segmento antes da pausa
                if pause_time > current_time:
                    segment = audio.subclip(current_time, pause_time)
                    segments.append(segment)
                
                # Criar silêncio mais suave
                try:
                    import numpy as np
                    sample_rate = int(audio.fps)
                    silence_samples = int(pause_duration * sample_rate)
                    silence_array = np.zeros(silence_samples)
                    
                    # Criar AudioClip do silêncio
                    from moviepy.audio.AudioClip import AudioArrayClip
                    silence = AudioArrayClip(silence_array.reshape(-1, 1), fps=sample_rate)
                    segments.append(silence)
                    
                    current_time = pause_time + pause_duration
                except Exception as e:
                    print(f"⚠️ Erro ao criar pausa: {e}")
                    continue
            
            # Adicionar segmento final
            if current_time < duration:
                final_segment = audio.subclip(current_time, duration)
                segments.append(final_segment)
            
            # Combinar segmentos apenas se houver segmentos válidos
            if segments and len(segments) > 1:
                try:
                    final_audio = CompositeAudioClip(segments)
                    output_path = f"paused_{os.path.basename(audio_path)}"
                    final_audio.write_audiofile(output_path)
                    print(f"✅ Pausas estratégicas aplicadas com sucesso")
                    return output_path
                except Exception as e:
                    print(f"⚠️ Erro ao combinar segmentos: {e}")
                    return audio_path
            
            return audio_path
            
        except Exception as e:
            print(f"❌ Erro ao aplicar pausas estratégicas: {e}")
            return audio_path 