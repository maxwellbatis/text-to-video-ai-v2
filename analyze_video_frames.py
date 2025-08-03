#!/usr/bin/env python3
"""
Análise de Frames do Vídeo
Extrai e analisa frames para verificar legendas
"""

import os
import sys
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
from datetime import datetime

def extract_frames_for_analysis(video_path, num_frames=20):
    """Extrai frames para análise detalhada"""
    print(f"🎬 ANALISANDO FRAMES DO VÍDEO: {os.path.basename(video_path)}")
    print("=" * 80)
    
    try:
        video = VideoFileClip(video_path)
        duration = video.duration
        
        print(f"📊 INFORMAÇÕES DO VÍDEO:")
        print(f"  ⏱️ Duração: {duration:.2f} segundos")
        print(f"  🎞️ FPS: {video.fps}")
        print(f"  📐 Resolução: {video.size[0]}x{video.size[1]}")
        print(f"  🎵 Áudio: {'Sim' if video.audio else 'Não'}")
        print()
        
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
            
            # Detectar se há texto (áreas brancas na parte inferior)
            height, width = frame.shape[:2]
            bottom_region = frame[int(height*0.7):height, :, :]  # Região inferior
            white_pixels = np.sum(bottom_region > 200)  # Pixels claros
            total_pixels = bottom_region.shape[0] * bottom_region.shape[1]
            text_ratio = white_pixels / total_pixels
            text_detected = text_ratio > 0.05  # 5% de pixels claros
            
            # Análise adicional de contraste na região inferior
            bottom_contrast = bottom_region.std()
            high_contrast = bottom_contrast > 30  # Alto contraste indica texto
            
            frame_info = {
                'time': time,
                'brightness': brightness,
                'contrast': contrast,
                'red': red_channel,
                'green': green_channel,
                'blue': blue_channel,
                'text_detected': text_detected,
                'text_ratio': text_ratio,
                'bottom_contrast': bottom_contrast,
                'high_contrast': high_contrast,
                'frame': frame
            }
            
            frames_data.append(frame_info)
            
            print(f"  Frame {i+1:2d} ({time:6.2f}s):")
            print(f"    🎨 Brilho: {brightness:6.1f}, Contraste: {contrast:6.1f}")
            print(f"    🎨 RGB: ({red_channel:5.1f},{green_channel:5.1f},{blue_channel:5.1f})")
            print(f"    📝 Texto detectado: {'✅ Sim' if text_detected else '❌ Não'}")
            print()
        
        return frames_data
        
    except Exception as e:
        print(f"❌ Erro ao analisar frames: {e}")
        return None

def analyze_legend_quality(frames_data):
    """Analisa a qualidade das legendas"""
    if not frames_data:
        return
    
    print(f"📝 ANÁLISE DE QUALIDADE DAS LEGENDAS")
    print("=" * 80)
    
    # Estatísticas de texto
    frames_with_text = sum(1 for f in frames_data if f['text_detected'])
    total_frames = len(frames_data)
    
    print(f"📊 ESTATÍSTICAS DE LEGENDAS:")
    print(f"  📝 Frames com texto: {frames_with_text}/{total_frames} ({frames_with_text/total_frames*100:.1f}%)")
    print(f"  📝 Frames sem texto: {total_frames-frames_with_text}/{total_frames} ({(total_frames-frames_with_text)/total_frames*100:.1f}%)")
    
    # Análise de distribuição temporal
    text_frames = [f for f in frames_data if f['text_detected']]
    no_text_frames = [f for f in frames_data if not f['text_detected']]
    
    if text_frames:
        avg_text_time = np.mean([f['time'] for f in text_frames])
        print(f"  ⏱️ Tempo médio com texto: {avg_text_time:.2f}s")
    
    if no_text_frames:
        avg_no_text_time = np.mean([f['time'] for f in no_text_frames])
        print(f"  ⏱️ Tempo médio sem texto: {avg_no_text_time:.2f}s")
    
    # Análise de contraste para legibilidade
    text_frame_contrasts = [f['contrast'] for f in text_frames]
    if text_frame_contrasts:
        avg_contrast = np.mean(text_frame_contrasts)
        print(f"  🎨 Contraste médio com texto: {avg_contrast:.1f}")
        
        if avg_contrast > 50:
            print(f"    ✅ Contraste adequado para legibilidade")
        else:
            print(f"    ⚠️ Contraste baixo - pode afetar legibilidade")

def generate_recommendations(frames_data, video_name):
    """Gera recomendações baseadas na análise"""
    if not frames_data:
        return
    
    print(f"\n💡 RECOMENDAÇÕES PARA {video_name}")
    print("=" * 80)
    
    frames_with_text = sum(1 for f in frames_data if f['text_detected'])
    total_frames = len(frames_data)
    text_percentage = frames_with_text / total_frames * 100
    
    # Análise de distribuição de texto
    if text_percentage > 80:
        print(f"📝 DISTRIBUIÇÃO: Muito texto na tela ({text_percentage:.1f}%)")
        print(f"   💡 Recomendação: Reduzir quantidade de texto para melhor visualização")
    elif text_percentage < 20:
        print(f"📝 DISTRIBUIÇÃO: Pouco texto na tela ({text_percentage:.1f}%)")
        print(f"   💡 Recomendação: Aumentar presença de legendas")
    else:
        print(f"📝 DISTRIBUIÇÃO: Equilibrada ({text_percentage:.1f}%)")
        print(f"   💡 Recomendação: Manter distribuição atual")
    
    # Análise de contraste
    text_frames = [f for f in frames_data if f['text_detected']]
    if text_frames:
        avg_contrast = np.mean([f['contrast'] for f in text_frames])
        if avg_contrast < 40:
            print(f"🎨 CONTRASTE: Baixo ({avg_contrast:.1f})")
            print(f"   💡 Recomendação: Aumentar contraste das legendas")
        else:
            print(f"🎨 CONTRASTE: Adequado ({avg_contrast:.1f})")
    
    print(f"\n🎬 RECOMENDAÇÕES GERAIS:")
    print(f"   📱 Verificar tamanho das legendas para vídeo vertical")
    print(f"   🎨 Garantir contraste adequado (branco com contorno preto)")
    print(f"   ⏱️ Distribuir texto ao longo do vídeo")
    print(f"   📝 Manter legibilidade em diferentes dispositivos")

def main():
    """Função principal"""
    video_path = "referencialegendas.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Arquivo não encontrado: {video_path}")
        return
    
    print("🎬 ANÁLISE COMPLETA DE FRAMES DO VÍDEO")
    print("=" * 80)
    print(f"📁 Arquivo: {video_path}")
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    # Análise de frames
    frames_data = extract_frames_for_analysis(video_path, num_frames=15)
    
    if frames_data:
        # Análise de qualidade
        analyze_legend_quality(frames_data)
        
        # Recomendações
        generate_recommendations(frames_data, os.path.basename(video_path))
    
    print("\n" + "=" * 80)
    print(f"✅ ANÁLISE CONCLUÍDA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main() 