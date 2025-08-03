#!/usr/bin/env python3
"""
Visualização de Frames do Vídeo
Extrai e salva frames para análise visual
"""

import os
import sys
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

def extract_and_save_frames(video_path, num_frames=10, output_dir="frames_analysis"):
    """Extrai e salva frames para análise visual"""
    print(f"🎬 EXTRAINDO FRAMES DO VÍDEO: {os.path.basename(video_path)}")
    print("=" * 80)
    
    # Criar diretório de saída
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        video = VideoFileClip(video_path)
        duration = video.duration
        
        print(f"📊 INFORMAÇÕES DO VÍDEO:")
        print(f"  ⏱️ Duração: {duration:.2f} segundos")
        print(f"  🎞️ FPS: {video.fps}")
        print(f"  📐 Resolução: {video.size[0]}x{video.size[1]}")
        print(f"  📁 Diretório de saída: {output_dir}")
        print()
        
        # Calcular intervalos para extrair frames
        intervals = np.linspace(0, duration, num_frames)
        
        saved_frames = []
        
        for i, time in enumerate(intervals):
            frame = video.get_frame(time)
            
            # Converter para PIL Image
            frame_pil = Image.fromarray(frame.astype('uint8'))
            
            # Salvar frame
            frame_filename = f"frame_{i+1:02d}_{time:.2f}s.png"
            frame_path = os.path.join(output_dir, frame_filename)
            frame_pil.save(frame_path)
            
            # Análise básica do frame
            brightness = frame.mean()
            contrast = frame.std()
            
            # Análise de cores
            red_channel = frame[:, :, 0].mean()
            green_channel = frame[:, :, 1].mean()
            blue_channel = frame[:, :, 2].mean()
            
            # Detectar texto na região inferior
            height, width = frame.shape[:2]
            bottom_region = frame[int(height*0.7):height, :, :]
            white_pixels = np.sum(bottom_region > 200)
            total_pixels = bottom_region.shape[0] * bottom_region.shape[1]
            text_ratio = white_pixels / total_pixels
            text_detected = text_ratio > 0.05
            
            saved_frames.append({
                'index': i+1,
                'time': time,
                'filename': frame_filename,
                'path': frame_path,
                'brightness': brightness,
                'contrast': contrast,
                'text_detected': text_detected,
                'text_ratio': text_ratio,
                'rgb': (red_channel, green_channel, blue_channel)
            })
            
            print(f"  Frame {i+1:2d} ({time:6.2f}s):")
            print(f"    📁 Salvo: {frame_filename}")
            print(f"    🎨 Brilho: {brightness:6.1f}, Contraste: {contrast:6.1f}")
            print(f"    🎨 RGB: ({red_channel:5.1f},{green_channel:5.1f},{blue_channel:5.1f})")
            print(f"    📝 Texto: {'✅ Sim' if text_detected else '❌ Não'} ({text_ratio*100:.1f}%)")
            print()
        
        return saved_frames
        
    except Exception as e:
        print(f"❌ Erro ao extrair frames: {e}")
        return None

def create_frame_comparison(frames_data, output_dir="frames_analysis"):
    """Cria uma comparação visual dos frames"""
    if not frames_data:
        return
    
    print(f"📊 CRIANDO COMPARAÇÃO VISUAL DOS FRAMES")
    print("=" * 80)
    
    # Criar figura com subplots
    num_frames = len(frames_data)
    cols = 3
    rows = (num_frames + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
    fig.suptitle('Análise Visual dos Frames do Vídeo', fontsize=16)
    
    for i, frame_data in enumerate(frames_data):
        row = i // cols
        col = i % cols
        
        if rows == 1:
            ax = axes[col] if cols > 1 else axes
        else:
            ax = axes[row, col] if cols > 1 else axes[row]
        
        # Carregar e mostrar frame
        img = Image.open(frame_data['path'])
        ax.imshow(img)
        ax.set_title(f"Frame {frame_data['index']} ({frame_data['time']:.1f}s)\n"
                    f"Texto: {'Sim' if frame_data['text_detected'] else 'Não'}")
        ax.axis('off')
    
    # Ocultar subplots vazios
    for i in range(num_frames, rows * cols):
        row = i // cols
        col = i % cols
        if rows == 1:
            ax = axes[col] if cols > 1 else axes
        else:
            ax = axes[row, col] if cols > 1 else axes[row]
        ax.axis('off')
    
    # Salvar comparação
    comparison_path = os.path.join(output_dir, "frames_comparison.png")
    plt.tight_layout()
    plt.savefig(comparison_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Comparação salva: {comparison_path}")

def analyze_text_distribution(frames_data):
    """Analisa a distribuição de texto nos frames"""
    if not frames_data:
        return
    
    print(f"📝 ANÁLISE DE DISTRIBUIÇÃO DE TEXTO")
    print("=" * 80)
    
    frames_with_text = [f for f in frames_data if f['text_detected']]
    frames_without_text = [f for f in frames_data if not f['text_detected']]
    
    print(f"📊 ESTATÍSTICAS:")
    print(f"  📝 Frames com texto: {len(frames_with_text)}/{len(frames_data)} ({len(frames_with_text)/len(frames_data)*100:.1f}%)")
    print(f"  📝 Frames sem texto: {len(frames_without_text)}/{len(frames_data)} ({len(frames_without_text)/len(frames_data)*100:.1f}%)")
    
    if frames_with_text:
        avg_text_ratio = np.mean([f['text_ratio'] for f in frames_with_text])
        print(f"  📊 Proporção média de texto: {avg_text_ratio*100:.1f}%")
    
    # Análise temporal
    text_times = [f['time'] for f in frames_with_text]
    no_text_times = [f['time'] for f in frames_without_text]
    
    if text_times:
        print(f"  ⏱️ Tempos com texto: {', '.join([f'{t:.1f}s' for t in text_times])}")
    
    if no_text_times:
        print(f"  ⏱️ Tempos sem texto: {', '.join([f'{t:.1f}s' for t in no_text_times])}")

def main():
    """Função principal"""
    video_path = "referencialegendas.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Arquivo não encontrado: {video_path}")
        return
    
    print("🎬 VISUALIZAÇÃO COMPLETA DE FRAMES DO VÍDEO")
    print("=" * 80)
    print(f"📁 Arquivo: {video_path}")
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    # Extrair frames
    frames_data = extract_and_save_frames(video_path, num_frames=12)
    
    if frames_data:
        # Criar comparação visual
        create_frame_comparison(frames_data)
        
        # Análise de distribuição
        analyze_text_distribution(frames_data)
        
        print(f"\n✅ FRAMES SALVOS EM: frames_analysis/")
        print(f"📁 Abra a pasta para visualizar os frames individuais")
        print(f"📊 Comparação visual: frames_analysis/frames_comparison.png")
    
    print("\n" + "=" * 80)
    print(f"✅ VISUALIZAÇÃO CONCLUÍDA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main() 