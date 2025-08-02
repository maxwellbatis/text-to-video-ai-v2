#!/usr/bin/env python3
"""
Análise Visual Detalhada dos Vídeos VSL
Extrai frames e analisa elementos visuais
"""

import os
import sys
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
from datetime import datetime

def extract_frames_for_analysis(video_path, num_frames=20):
    """Extrai frames para análise visual detalhada"""
    print(f"🎬 ANALISANDO VISUALMENTE: {os.path.basename(video_path)}")
    print("=" * 60)
    
    try:
        video = VideoFileClip(video_path)
        duration = video.duration
        
        # Calcular intervalos para extrair frames
        intervals = np.linspace(0, duration, num_frames)
        
        frames_data = []
        
        for i, time in enumerate(intervals):
            frame = video.get_frame(time)
            
            # Análise básica do frame
            brightness = frame.mean()
            contrast = frame.std()
            
            # Análise de cores
            red_channel = frame[:, :, 0].mean()
            green_channel = frame[:, :, 1].mean()
            blue_channel = frame[:, :, 2].mean()
            
            # Detectar se é claro ou escuro
            is_bright = brightness > 128
            is_high_contrast = contrast > 50
            
            frame_info = {
                'time': time,
                'brightness': brightness,
                'contrast': contrast,
                'red': red_channel,
                'green': green_channel,
                'blue': blue_channel,
                'is_bright': is_bright,
                'is_high_contrast': is_high_contrast,
                'frame': frame
            }
            
            frames_data.append(frame_info)
            
            print(f"  Frame {i+1:2d} ({time:6.2f}s): Brilho={brightness:6.1f}, Contraste={contrast:6.1f}, RGB=({red_channel:5.1f},{green_channel:5.1f},{blue_channel:5.1f})")
        
        return frames_data
        
    except Exception as e:
        print(f"❌ Erro ao analisar visualmente: {e}")
        return None

def analyze_visual_patterns(frames_data):
    """Analisa padrões visuais nos frames"""
    if not frames_data:
        return
    
    print(f"\n🎨 ANÁLISE DE PADRÕES VISUAIS")
    print("=" * 60)
    
    # Estatísticas gerais
    brightness_values = [f['brightness'] for f in frames_data]
    contrast_values = [f['contrast'] for f in frames_data]
    
    bright_frames = sum(1 for f in frames_data if f['is_bright'])
    high_contrast_frames = sum(1 for f in frames_data if f['is_high_contrast'])
    
    print(f"📊 ESTATÍSTICAS VISUAIS:")
    print(f"  🎨 Frames claros: {bright_frames}/{len(frames_data)} ({bright_frames/len(frames_data)*100:.1f}%)")
    print(f"  🎨 Frames escuros: {len(frames_data)-bright_frames}/{len(frames_data)} ({(len(frames_data)-bright_frames)/len(frames_data)*100:.1f}%)")
    print(f"  🎨 Alto contraste: {high_contrast_frames}/{len(frames_data)} ({high_contrast_frames/len(frames_data)*100:.1f}%)")
    print(f"  📊 Brilho médio: {np.mean(brightness_values):.1f}")
    print(f"  📊 Contraste médio: {np.mean(contrast_values):.1f}")
    
    # Análise de transições
    print(f"\n🎬 ANÁLISE DE TRANSIÇÕES:")
    transitions = []
    for i in range(1, len(frames_data)):
        prev_bright = frames_data[i-1]['is_bright']
        curr_bright = frames_data[i]['is_bright']
        
        if prev_bright != curr_bright:
            transition_type = "Claro → Escuro" if prev_bright else "Escuro → Claro"
            transitions.append({
                'time': frames_data[i]['time'],
                'type': transition_type
            })
    
    print(f"  ⚡ Transições detectadas: {len(transitions)}")
    for i, trans in enumerate(transitions[:5]):
        print(f"    {i+1}. {trans['time']:.2f}s: {trans['type']}")
    
    # Análise de cores dominantes
    print(f"\n🎨 ANÁLISE DE CORES:")
    red_avg = np.mean([f['red'] for f in frames_data])
    green_avg = np.mean([f['green'] for f in frames_data])
    blue_avg = np.mean([f['blue'] for f in frames_data])
    
    print(f"  🔴 Vermelho médio: {red_avg:.1f}")
    print(f"  🟢 Verde médio: {green_avg:.1f}")
    print(f"  🔵 Azul médio: {blue_avg:.1f}")
    
    # Determinar paleta dominante
    if red_avg > green_avg and red_avg > blue_avg:
        dominant_color = "Vermelho/Quente"
    elif green_avg > red_avg and green_avg > blue_avg:
        dominant_color = "Verde/Natural"
    elif blue_avg > red_avg and blue_avg > green_avg:
        dominant_color = "Azul/Frio"
    else:
        dominant_color = "Equilibrada"
    
    print(f"  🎨 Paleta dominante: {dominant_color}")

def generate_visual_recommendations(frames_data, video_name):
    """Gera recomendações visuais baseadas na análise"""
    if not frames_data:
        return
    
    print(f"\n💡 RECOMENDAÇÕES VISUAIS PARA {video_name}")
    print("=" * 60)
    
    bright_frames = sum(1 for f in frames_data if f['is_bright'])
    dark_frames = len(frames_data) - bright_frames
    high_contrast_frames = sum(1 for f in frames_data if f['is_high_contrast'])
    
    # Análise de padrões
    bright_percentage = bright_frames / len(frames_data) * 100
    contrast_percentage = high_contrast_frames / len(frames_data) * 100
    
    print(f"📊 ANÁLISE DE PADRÕES:")
    print(f"  🎨 Frames claros: {bright_percentage:.1f}%")
    print(f"  🎨 Frames escuros: {100-bright_percentage:.1f}%")
    print(f"  🎨 Alto contraste: {contrast_percentage:.1f}%")
    
    # Recomendações baseadas nos padrões
    if bright_percentage > 70:
        print(f"🎯 PADRÃO: Vídeo predominantemente claro")
        print(f"   💡 Recomendação: Adicionar mais contrastes escuros para drama")
    elif bright_percentage < 30:
        print(f"🎯 PADRÃO: Vídeo predominantemente escuro")
        print(f"   💡 Recomendação: Adicionar momentos de luz para impacto")
    else:
        print(f"🎯 PADRÃO: Vídeo com equilíbrio claro/escuro")
        print(f"   💡 Recomendação: Manter padrão, está ideal")
    
    if contrast_percentage > 60:
        print(f"🎯 CONTRASTE: Alto contraste detectado")
        print(f"   💡 Recomendação: Excelente para impacto visual")
    else:
        print(f"🎯 CONTRASTE: Contraste moderado")
        print(f"   💡 Recomendação: Aumentar contraste para mais impacto")
    
    print(f"\n🎬 ELEMENTOS CINEMATOGRÁFICOS RECOMENDADOS:")
    print(f"   🎨 Gradientes dramáticos")
    print(f"   ⚡ Transições suaves")
    print(f"   📝 Tipografia contrastante")
    print(f"   🎭 Overlays cinematográficos")

def analyze_all_vsl_videos():
    """Analisa todos os vídeos VSL visualmente"""
    videos = [
        "referencia vsl.mp4",
        "referencia vsl 2.mp4", 
        "referencia vsl 3.mp4"
    ]
    
    print("🎬 ANÁLISE VISUAL COMPLETA DOS VSLs")
    print("=" * 80)
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    all_analyses = {}
    
    for video_path in videos:
        if os.path.exists(video_path):
            frames_data = extract_frames_for_analysis(video_path)
            if frames_data:
                analyze_visual_patterns(frames_data)
                generate_visual_recommendations(frames_data, os.path.basename(video_path))
                all_analyses[video_path] = frames_data
            print("\n" + "="*80 + "\n")
        else:
            print(f"❌ Arquivo não encontrado: {video_path}")
    
    # Comparação entre vídeos
    if len(all_analyses) > 1:
        print("📊 COMPARAÇÃO VISUAL ENTRE VSLs")
        print("=" * 80)
        
        for video_path, frames_data in all_analyses.items():
            video_name = os.path.basename(video_path)
            brightness_values = [f['brightness'] for f in frames_data]
            contrast_values = [f['contrast'] for f in frames_data]
            
            bright_frames = sum(1 for f in frames_data if f['is_bright'])
            high_contrast_frames = sum(1 for f in frames_data if f['is_high_contrast'])
            
            print(f"📁 {video_name}:")
            print(f"  🎨 Brilho médio: {np.mean(brightness_values):.1f}")
            print(f"  🎨 Contraste médio: {np.mean(contrast_values):.1f}")
            print(f"  🎨 Frames claros: {bright_frames}/{len(frames_data)} ({bright_frames/len(frames_data)*100:.1f}%)")
            print(f"  🎨 Alto contraste: {high_contrast_frames}/{len(frames_data)} ({high_contrast_frames/len(frames_data)*100:.1f}%)")
            print()
    
    print("=" * 80)
    print(f"✅ ANÁLISE VISUAL CONCLUÍDA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    analyze_all_vsl_videos() 