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
    
    def apply_strategic_pauses(self, audio_path: str, pauses_config: Dict) -> str:
        """Aplica pausas estratégicas ao áudio"""
        try:
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Aplicar pausas baseadas na configuração
            impact_pauses = pauses_config.get('impact_pauses', [])
            
            for pause in impact_pauses:
                position = pause['position']
                pause_duration = pause['duration']
                purpose = pause.get('purpose', 'drama')
                
                # Calcular tempo real da pausa
                pause_time = duration * position
                
                # Criar silêncio para a pausa
                silence = AudioFileClip(audio_path).set_duration(pause_duration)
                silence = silence.volumex(0)  # Silêncio total
                
                # Inserir pausa no áudio
                audio = audio.set_start(0)
                audio = audio.set_end(pause_time)
                
                # Combinar com silêncio
                from moviepy.editor import concatenate_audioclips
                audio = concatenate_audioclips([audio, silence])
            
            # Salvar áudio com pausas
            output_path = f"paused_{os.path.basename(audio_path)}"
            audio.write_audiofile(output_path)
            
            return output_path
            
        except Exception as e:
            print(f"❌ Erro ao aplicar pausas estratégicas: {e}")
            return audio_path
    
    def generate_vsl_text_overlays(self, script: str, template_config: Dict) -> List[Dict]:
        """Gera overlays de texto para VSL baseado no script e template"""
        try:
            # Estrutura VSL: Hook → Problema → Solução → Oferta → CTA
            vsl_structure = template_config.get('script_pattern', {}).get('structure', {})
            text_settings = template_config.get('text_display', {})
            
            # Dividir script em frases
            sentences = script.split('. ')
            overlays = []
            
            # Configurações de texto
            typography = text_settings.get('typography', {})
            animations = text_settings.get('animations', {})
            timing = text_settings.get('timing', {})
            
            # Duração total estimada (45-60 segundos para VSL)
            total_duration = 50  # segundos
            segment_duration = total_duration / len(sentences) if sentences else 10
            
            for i, sentence in enumerate(sentences):
                if not sentence.strip():
                    continue
                
                # Calcular timing
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration
                
                # Determinar tipo de texto baseado na posição
                text_type = self._determine_vsl_text_type(i, len(sentences))
                
                # Criar overlay de texto
                overlay = {
                    'text': sentence.strip(),
                    'start_time': start_time,
                    'end_time': end_time,
                    'type': text_type,
                    'style': self._get_vsl_text_style(text_type, typography),
                    'animation': self._get_vsl_animation(text_type, animations),
                    'position': self._get_vsl_position(text_type, text_settings)
                }
                
                overlays.append(overlay)
            
            return overlays
            
        except Exception as e:
            print(f"❌ Erro ao gerar overlays VSL: {e}")
            return []
    
    def _determine_vsl_text_type(self, index: int, total_sentences: int) -> str:
        """Determina o tipo de texto baseado na posição na estrutura VSL"""
        if index == 0:
            return 'hook'  # Primeira frase - Hook
        elif index < total_sentences * 0.2:
            return 'problem'  # 20% - Problema
        elif index < total_sentences * 0.4:
            return 'solution'  # 40% - Solução
        elif index < total_sentences * 0.8:
            return 'offer'  # 80% - Oferta
        else:
            return 'cta'  # Últimas frases - CTA
    
    def _get_vsl_text_style(self, text_type: str, typography: Dict) -> Dict:
        """Retorna estilo de texto baseado no tipo VSL"""
        base_style = {
            'font': typography.get('font', 'Arial-Bold'),
            'size': typography.get('size', '120-150'),
            'color': typography.get('color', 'white'),
            'stroke': typography.get('stroke', 'black'),
            'stroke_width': typography.get('stroke_width', 6)
        }
        
        # Personalizar baseado no tipo
        if text_type == 'hook':
            base_style['size'] = '150-180'  # Maior para impacto
            base_style['color'] = '#FFD700'  # Dourado para chamar atenção
        elif text_type == 'cta':
            base_style['size'] = '140-160'
            base_style['color'] = '#FF4444'  # Vermelho para urgência
        elif text_type == 'offer':
            base_style['color'] = '#00FF00'  # Verde para benefícios
        
        return base_style
    
    def _get_vsl_animation(self, text_type: str, animations: Dict) -> str:
        """Retorna tipo de animação baseado no tipo VSL"""
        if text_type == 'hook':
            return 'fade_in_zoom'  # Entrada dramática
        elif text_type == 'cta':
            return 'pulse_glow'  # Pulsação para urgência
        else:
            return 'fade_in_slide'  # Entrada suave
    
    def _get_vsl_position(self, text_type: str, text_settings: Dict) -> str:
        """Retorna posição do texto baseado no tipo VSL"""
        positioning = text_settings.get('positioning', {})
        
        if text_type == 'hook':
            return positioning.get('primary', 'center')  # Centro para hook
        elif text_type == 'cta':
            return positioning.get('secondary', 'bottom')  # Baixo para CTA
        else:
            return positioning.get('primary', 'center')  # Centro para outros 