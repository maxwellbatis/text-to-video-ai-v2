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

# Patch para compatibilidade com Pillow 10.x (ANTIALIAS foi removido)
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
except ImportError:
    pass

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
            
            # Aplicar configurações específicas do template
            template_id = template_config.get('template_id', 'default')
            
            if template_id == "vsl_magnetic":
                video = self._apply_vsl_magnetic_settings(video, template_config)
            else:
                # Aplicar configurações visuais padrão
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
    
    def _apply_vsl_magnetic_settings(self, video: VideoFileClip, template_config: Dict) -> VideoFileClip:
        """Aplica configurações específicas do template VSL magnético"""
        try:
            print("🎬 Aplicando configurações VSL Magnético...")
            
            # Configurações do template VSL
            visual_settings = template_config.get('visual_settings', {})
            
            # Redimensionar para formato vertical (720x1280)
            target_width = 720
            target_height = 1280
            
            # Calcular proporção para manter aspecto
            current_width, current_height = video.size
            aspect_ratio = current_width / current_height
            
            if aspect_ratio > 1:  # Vídeo horizontal
                # Cortar para formato vertical
                new_width = int(current_height * (9/16))  # Proporção 9:16
                crop_x = (current_width - new_width) // 2
                video = video.crop(x1=crop_x, y1=0, x2=crop_x + new_width, y2=current_height)
            
            # Redimensionar para 720x1280
            video = video.resize((target_width, target_height))
            
            print(f"✅ Vídeo redimensionado para {target_width}x{target_height}")
            
            # Aplicar efeitos visuais específicos do VSL
            video = self._apply_vsl_visual_effects(video, visual_settings)
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar configurações VSL: {e}")
            return video
    
    def _apply_vsl_visual_effects(self, video: VideoFileClip, visual_settings: Dict) -> VideoFileClip:
        """Aplica efeitos visuais específicos do VSL"""
        try:
            # Aplicar efeitos de transição dinâmicos
            if visual_settings.get('transition_effects'):
                video = self._apply_vsl_transitions(video, visual_settings['transition_effects'])
            
            # Aplicar efeitos de texto se especificados
            text_style = visual_settings.get('text_style', {})
            if text_style:
                video = self._apply_vsl_text_effects(video, text_style)
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar efeitos visuais VSL: {e}")
            return video
    
    def _apply_vsl_transitions(self, video: VideoFileClip, transitions: List[str]) -> VideoFileClip:
        """Aplica transições específicas do VSL"""
        try:
            # Transições rápidas e dinâmicas para VSL
            if 'fast_cuts' in transitions:
                # Implementar cortes rápidos
                print("🎬 Aplicando cortes rápidos VSL")
            
            if 'zoom_effects' in transitions:
                # Implementar efeitos de zoom
                print("🎬 Aplicando efeitos de zoom VSL")
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar transições VSL: {e}")
            return video
    
    def _apply_vsl_text_effects(self, video: VideoFileClip, text_style: Dict) -> VideoFileClip:
        """Aplica efeitos de texto específicos do VSL"""
        try:
            # Efeitos de texto para VSL (palavras-chave destacadas, etc.)
            font = text_style.get('font', 'Impact')
            font_size = text_style.get('font_size', 120)
            stroke_width = text_style.get('stroke_width', 10)
            
            print(f"🎬 Configurações de texto VSL: {font}, {font_size}px, stroke {stroke_width}")
            
            return video
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar efeitos de texto VSL: {e}")
            return video
    
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
            background_music_choice = template_config.get('background_music')
            print(f"🎵 Aplicando áudio para template: {template_id}")
            if background_music_choice:
                print(f"🎵 Música de fundo escolhida: {background_music_choice}")
            
            if ASSETS_AVAILABLE:
                assets = asset_manager.get_assets_for_template(template_id, background_music_choice)
                print(f"🎵 Assets de áudio encontrados: {list(assets.keys())}")
                
                # Adicionar música de fundo
                if assets.get('background_music') and os.path.exists(assets['background_music']):
                    print(f"🎵 Tentando aplicar música de fundo: {assets['background_music']}")
                    try:
                        bg_music = AudioFileClip(assets['background_music'])
                        # Loop da música de fundo para cobrir toda a duração
                        bg_music = audio_loop(bg_music, duration=audio.duration)
                        # Volume aumentado para melhor audibilidade
                        bg_music = bg_music.volumex(0.3)
                        
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
                        tension = tension.volumex(0.5)
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
                        impact = impact.volumex(0.4)
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
    
    def apply_strategic_pauses(self, audio_file_path: str, pauses_config: Dict) -> str:
        """Aplica pausas estratégicas ao áudio"""
        try:
            # Carregar áudio
            audio = AudioFileClip(audio_file_path)
            
            # Configurações de pausas
            pause_duration = pauses_config.get('duration', 2.0)
            pause_count = pauses_config.get('count', 3)
            
            # Dividir áudio em segmentos
            total_duration = audio.duration
            segment_duration = total_duration / (pause_count + 1)
            
            # Criar segmentos de áudio
            audio_segments = []
            for i in range(pause_count + 1):
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration
                
                segment = audio.subclip(start_time, end_time)
                audio_segments.append(segment)
                
                # Adicionar pausa (exceto após o último segmento)
                if i < pause_count:
                    silence = AudioFileClip(audio_file_path).subclip(0, pause_duration).volumex(0)
                    audio_segments.append(silence)
            
            # Combinar segmentos
            from moviepy.editor import concatenate_audioclips
            final_audio = concatenate_audioclips(audio_segments)
            
            # Salvar áudio com pausas
            output_path = f"paused_{audio_file_path}"
            final_audio.write_audiofile(output_path, verbose=False, logger=None)
            
            return output_path
            
        except Exception as e:
            print(f"❌ Erro ao aplicar pausas estratégicas: {e}")
            return audio_file_path 