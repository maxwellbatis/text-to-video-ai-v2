#!/usr/bin/env python3
"""
Análise do Vídeo VSL Cinematográfico de Referência
Analisa visual, áudio, narração, roteiro e estrutura
"""

import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper
import json
from datetime import datetime

def analyze_video_structure(video_path):
    """Analisa a estrutura básica do vídeo"""
    print("🎬 ANÁLISE ESTRUTURAL DO VÍDEO")
    print("=" * 50)
    
    try:
        video = VideoFileClip(video_path)
        
        # Informações básicas
        duration = video.duration
        fps = video.fps
        size = video.size
        has_audio = video.audio is not None
        
        print(f"📊 DURAÇÃO: {duration:.2f} segundos ({duration/60:.2f} minutos)")
        print(f"🎞️ FPS: {fps}")
        print(f"📐 RESOLUÇÃO: {size[0]}x{size[1]}")
        print(f"🔊 ÁUDIO: {'Sim' if has_audio else 'Não'}")
        
        if has_audio:
            audio = video.audio
            print(f"🎵 DURAÇÃO DO ÁUDIO: {audio.duration:.2f} segundos")
        
        return {
            'duration': duration,
            'fps': fps,
            'size': size,
            'has_audio': has_audio
        }
        
    except Exception as e:
        print(f"❌ Erro ao analisar estrutura: {e}")
        return None

def analyze_audio_quality(video_path):
    """Analisa a qualidade do áudio"""
    print("\n🎵 ANÁLISE DE ÁUDIO")
    print("=" * 50)
    
    try:
        video = VideoFileClip(video_path)
        if video.audio is None:
            print("⚠️ Vídeo não possui áudio")
            return None
        
        audio = video.audio
        
        # Extrair áudio para análise
        temp_audio = "temp_audio.wav"
        audio.write_audiofile(temp_audio, verbose=False, logger=None)
        
        # Carregar áudio para análise
        audio_clip = AudioFileClip(temp_audio)
        
        print(f"🎵 DURAÇÃO: {audio_clip.duration:.2f} segundos")
        print(f"🔊 FREQUÊNCIA: {audio_clip.fps} Hz")
        
        # Analisar níveis de áudio
        audio_array = audio_clip.to_soundarray()
        max_volume = audio_array.max()
        min_volume = audio_array.min()
        avg_volume = audio_array.mean()
        
        print(f"📊 VOLUME MÁXIMO: {max_volume:.3f}")
        print(f"📊 VOLUME MÍNIMO: {min_volume:.3f}")
        print(f"📊 VOLUME MÉDIO: {avg_volume:.3f}")
        
        # Limpar arquivo temporário
        os.remove(temp_audio)
        
        return {
            'duration': audio_clip.duration,
            'fps': audio_clip.fps,
            'max_volume': max_volume,
            'min_volume': min_volume,
            'avg_volume': avg_volume
        }
        
    except Exception as e:
        print(f"❌ Erro ao analisar áudio: {e}")
        return None

def transcribe_audio(video_path):
    """Transcreve o áudio do vídeo"""
    print("\n📝 TRANSCRIÇÃO DO ÁUDIO")
    print("=" * 50)
    
    try:
        # Extrair áudio
        video = VideoFileClip(video_path)
        if video.audio is None:
            print("⚠️ Vídeo não possui áudio para transcrição")
            return None
        
        temp_audio = "temp_audio.wav"
        video.audio.write_audiofile(temp_audio, verbose=False, logger=None)
        
        # Carregar modelo Whisper
        print("🤖 Carregando modelo Whisper...")
        model = whisper.load_model("base")
        
        # Transcrever
        print("📝 Transcrevendo áudio...")
        result = model.transcribe(temp_audio, language="pt")
        
        # Limpar arquivo temporário
        os.remove(temp_audio)
        
        # Analisar transcrição
        text = result["text"]
        segments = result["segments"]
        
        print(f"📄 TEXTO COMPLETO:")
        print("-" * 30)
        print(text)
        print("-" * 30)
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"📝 PALAVRAS: {len(text.split())}")
        print(f"📝 CARACTERES: {len(text)}")
        print(f"⏱️ SEGMENTOS: {len(segments)}")
        
        # Analisar segmentos
        print(f"\n📋 SEGMENTOS DETALHADOS:")
        for i, segment in enumerate(segments[:10]):  # Primeiros 10 segmentos
            start = segment["start"]
            end = segment["end"]
            text_seg = segment["text"].strip()
            print(f"  {i+1:2d}. [{start:6.2f}s - {end:6.2f}s] {text_seg}")
        
        if len(segments) > 10:
            print(f"  ... e mais {len(segments) - 10} segmentos")
        
        return {
            'text': text,
            'segments': segments,
            'word_count': len(text.split()),
            'char_count': len(text)
        }
        
    except Exception as e:
        print(f"❌ Erro na transcrição: {e}")
        return None

def analyze_visual_elements(video_path):
    """Analisa elementos visuais do vídeo"""
    print("\n🎨 ANÁLISE VISUAL")
    print("=" * 50)
    
    try:
        video = VideoFileClip(video_path)
        
        # Analisar frames
        total_frames = int(video.duration * video.fps)
        print(f"🎞️ TOTAL DE FRAMES: {total_frames}")
        
        # Analisar alguns frames para detectar padrões
        sample_frames = 10
        frame_interval = total_frames // sample_frames
        
        print(f"🔍 ANALISANDO {sample_frames} FRAMES DE REFERÊNCIA:")
        
        for i in range(sample_frames):
            frame_time = (i * frame_interval) / video.fps
            frame = video.get_frame(frame_time)
            
            # Análise básica do frame
            brightness = frame.mean()
            contrast = frame.std()
            
            print(f"  Frame {i+1:2d} ({frame_time:6.2f}s): Brilho={brightness:6.1f}, Contraste={contrast:6.1f}")
        
        # Detectar mudanças de cena (simplificado)
        print(f"\n🎬 DETECÇÃO DE MUDANÇAS DE CENA:")
        scene_changes = []
        prev_frame = None
        
        for i in range(0, min(total_frames, 100), 10):  # Analisar primeiros 100 frames
            frame_time = i / video.fps
            frame = video.get_frame(frame_time)
            
            if prev_frame is not None:
                # Calcular diferença entre frames
                diff = abs(frame - prev_frame).mean()
                if diff > 30:  # Threshold para mudança de cena
                    scene_changes.append(frame_time)
            
            prev_frame = frame
        
        print(f"  Mudanças detectadas: {len(scene_changes)}")
        for i, time in enumerate(scene_changes[:5]):
            print(f"    {i+1}. {time:.2f}s")
        
        return {
            'total_frames': total_frames,
            'scene_changes': scene_changes
        }
        
    except Exception as e:
        print(f"❌ Erro na análise visual: {e}")
        return None

def analyze_script_structure(transcription_data):
    """Analisa a estrutura do roteiro"""
    print("\n📖 ANÁLISE DO ROTEIRO")
    print("=" * 50)
    
    if not transcription_data:
        print("⚠️ Sem dados de transcrição para análise")
        return None
    
    text = transcription_data['text']
    segments = transcription_data['segments']
    
    # Análise de palavras
    words = text.split()
    unique_words = set(words)
    
    print(f"📊 ESTATÍSTICAS DE TEXTO:")
    print(f"  📝 Total de palavras: {len(words)}")
    print(f"  📝 Palavras únicas: {len(unique_words)}")
    print(f"  📝 Palavras por minuto: {len(words) / (segments[-1]['end'] / 60):.1f}")
    
    # Análise de frases
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    print(f"\n📋 ANÁLISE DE FRASES:")
    print(f"  📝 Total de frases: {len(sentences)}")
    print(f"  📝 Média de palavras por frase: {len(words) / len(sentences):.1f}")
    
    # Palavras mais frequentes
    word_count = {}
    for word in words:
        word_lower = word.lower().strip('.,!?;:')
        if len(word_lower) > 3:  # Ignorar palavras muito curtas
            word_count[word_lower] = word_count.get(word_lower, 0) + 1
    
    # Top 10 palavras mais frequentes
    top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"\n🔤 PALAVRAS MAIS FREQUENTES:")
    for i, (word, count) in enumerate(top_words):
        print(f"  {i+1:2d}. '{word}': {count} vezes")
    
    # Análise de estrutura temporal
    print(f"\n⏱️ ESTRUTURA TEMPORAL:")
    total_duration = segments[-1]['end']
    
    # Dividir em terços
    third = total_duration / 3
    print(f"  📊 Duração total: {total_duration:.2f}s")
    print(f"  📊 Primeiro terço: 0.00s - {third:.2f}s")
    print(f"  📊 Segundo terço: {third:.2f}s - {third*2:.2f}s")
    print(f"  📊 Terceiro terço: {third*2:.2f}s - {total_duration:.2f}s")
    
    return {
        'word_count': len(words),
        'unique_words': len(unique_words),
        'sentence_count': len(sentences),
        'words_per_minute': len(words) / (total_duration / 60),
        'top_words': top_words,
        'duration': total_duration
    }

def generate_vsl_recommendations(analysis_data):
    """Gera recomendações baseadas na análise"""
    print("\n💡 RECOMENDAÇÕES PARA VSL")
    print("=" * 50)
    
    if not analysis_data:
        print("⚠️ Sem dados suficientes para recomendações")
        return
    
    # Recomendações baseadas na duração
    duration = analysis_data.get('duration', 0)
    if duration < 30:
        print("🎯 DURAÇÃO: Vídeo muito curto para VSL")
        print("   💡 Recomendação: Aumentar para 60-90 segundos")
    elif duration > 120:
        print("🎯 DURAÇÃO: Vídeo muito longo para VSL")
        print("   💡 Recomendação: Reduzir para 60-90 segundos")
    else:
        print("🎯 DURAÇÃO: Perfeita para VSL (60-90 segundos)")
    
    # Recomendações baseadas na estrutura
    script_data = analysis_data.get('script_analysis')
    if script_data:
        wpm = script_data.get('words_per_minute', 0)
        if wpm > 200:
            print("🎯 VELOCIDADE: Narração muito rápida")
            print("   💡 Recomendação: Reduzir velocidade para 150-180 WPM")
        elif wpm < 120:
            print("🎯 VELOCIDADE: Narração muito lenta")
            print("   💡 Recomendação: Aumentar velocidade para 150-180 WPM")
        else:
            print("🎯 VELOCIDADE: Perfeita para VSL (150-180 WPM)")
    
    # Recomendações visuais
    visual_data = analysis_data.get('visual_analysis')
    if visual_data and visual_data.get('scene_changes'):
        scene_count = len(visual_data['scene_changes'])
        if scene_count < 5:
            print("🎯 VISUAL: Poucas mudanças de cena")
            print("   💡 Recomendação: Adicionar mais transições visuais")
        elif scene_count > 20:
            print("🎯 VISUAL: Muitas mudanças de cena")
            print("   💡 Recomendação: Reduzir para manter foco")
        else:
            print("🎯 VISUAL: Mudanças de cena equilibradas")
    
    print("\n🎬 ELEMENTOS CINEMATOGRÁFICOS RECOMENDADOS:")
    print("   🎨 Gradientes e overlays dramáticos")
    print("   🎵 Trilha sonora épica/cinematográfica")
    print("   📝 Tipografia impactante e legível")
    print("   ⚡ Transições suaves e dinâmicas")
    print("   🎭 Pausas estratégicas para impacto")

def main():
    """Função principal de análise"""
    video_path = "referencia vsl 3.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Arquivo não encontrado: {video_path}")
        return
    
    print("🎬 ANÁLISE COMPLETA DO VSL CINEMATOGRÁFICO #3")
    print("=" * 60)
    print(f"📁 Arquivo: {video_path}")
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Análises
    structure_data = analyze_video_structure(video_path)
    audio_data = analyze_audio_quality(video_path)
    transcription_data = transcribe_audio(video_path)
    visual_data = analyze_visual_elements(video_path)
    
    # Análise do roteiro
    script_data = None
    if transcription_data:
        script_data = analyze_script_structure(transcription_data)
    
    # Consolidar dados
    analysis_data = {
        'structure': structure_data,
        'audio': audio_data,
        'transcription': transcription_data,
        'visual': visual_data,
        'script_analysis': script_data,
        'duration': structure_data['duration'] if structure_data else 0
    }
    
    # Gerar recomendações
    generate_vsl_recommendations(analysis_data)
    
    print("\n" + "=" * 60)
    print(f"✅ ANÁLISE CONCLUÍDA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main() 