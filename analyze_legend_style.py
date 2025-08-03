#!/usr/bin/env python3
"""
Análise de Estilo das Legendas
Analisa modelo das letras, quebra de linhas e fundo
"""

import os
import sys
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
import cv2
from datetime import datetime

def analyze_legend_style(video_path, num_frames=8):
    """Analisa o estilo das legendas no meio do vídeo"""
    print(f"🎬 ANÁLISE DE ESTILO DAS LEGENDAS")
    print("=" * 80)
    
    try:
        video = VideoFileClip(video_path)
        duration = video.duration
        
        print(f"📊 INFORMAÇÕES DO VÍDEO:")
        print(f"  ⏱️ Duração: {duration:.2f} segundos")
        print(f"  📐 Resolução: {video.size[0]}x{video.size[1]}")
        print()
        
        # Focar no meio do vídeo (30-70% da duração)
        start_time = duration * 0.3
        end_time = duration * 0.7
        intervals = np.linspace(start_time, end_time, num_frames)
        
        legend_analysis = []
        
        for i, time in enumerate(intervals):
            frame = video.get_frame(time)
            
            # Análise da região inferior (onde ficam as legendas)
            height, width = frame.shape[:2]
            legend_region = frame[int(height*0.6):height, :, :]  # Região das legendas
            
            # Análise de cores do fundo
            bg_colors = analyze_background_colors(legend_region)
            
            # Detectar texto e quebra de linhas
            text_info = detect_text_and_line_breaks(legend_region)
            
            # Análise de contraste e legibilidade
            contrast_analysis = analyze_contrast_and_readability(legend_region)
            
            frame_analysis = {
                'time': time,
                'frame_index': i+1,
                'background_colors': bg_colors,
                'text_info': text_info,
                'contrast_analysis': contrast_analysis,
                'legend_region': legend_region
            }
            
            legend_analysis.append(frame_analysis)
            
            print(f"  Frame {i+1:2d} ({time:6.2f}s):")
            print(f"    🎨 Fundo: {bg_colors['dominant_color']} ({bg_colors['color_percentage']:.1f}%)")
            print(f"    📝 Texto detectado: {'✅ Sim' if text_info['has_text'] else '❌ Não'}")
            print(f"    📏 Quebra de linhas: {text_info['line_count']} linhas")
            print(f"    🎨 Contraste: {contrast_analysis['contrast_level']}")
            print()
        
        return legend_analysis
        
    except Exception as e:
        print(f"❌ Erro ao analisar estilo: {e}")
        return None

def analyze_background_colors(region):
    """Analisa as cores do fundo das legendas"""
    # Converter para HSV para melhor análise de cores
    hsv = cv2.cvtColor(region, cv2.COLOR_RGB2HSV)
    
    # Analisar tons de azul
    blue_pixels = np.sum((hsv[:, :, 0] >= 100) & (hsv[:, :, 0] <= 130))
    total_pixels = region.shape[0] * region.shape[1]
    blue_percentage = blue_pixels / total_pixels * 100
    
    # Analisar tons de cinza/transparente
    gray_pixels = np.sum(region.mean(axis=2) < 100)
    gray_percentage = gray_pixels / total_pixels * 100
    
    # Determinar cor dominante
    if blue_percentage > 20:
        dominant_color = "Azul"
        color_percentage = blue_percentage
    elif gray_percentage > 30:
        dominant_color = "Cinza/Transparente"
        color_percentage = gray_percentage
    else:
        dominant_color = "Misturado"
        color_percentage = 100 - (blue_percentage + gray_percentage)
    
    return {
        'dominant_color': dominant_color,
        'color_percentage': color_percentage,
        'blue_percentage': blue_percentage,
        'gray_percentage': gray_percentage
    }

def detect_text_and_line_breaks(region):
    """Detecta texto e quebra de linhas"""
    # Converter para escala de cinza
    gray = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
    
    # Detectar bordas (para identificar texto)
    edges = cv2.Canny(gray, 50, 150)
    
    # Contar linhas horizontais (indicam quebra de linhas)
    horizontal_lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=50)
    line_count = 0 if horizontal_lines is None else len(horizontal_lines)
    
    # Detectar áreas de texto (pixels claros)
    white_pixels = np.sum(gray > 200)
    total_pixels = gray.shape[0] * gray.shape[1]
    text_ratio = white_pixels / total_pixels
    
    has_text = text_ratio > 0.05  # 5% de pixels claros
    
    return {
        'has_text': has_text,
        'text_ratio': text_ratio,
        'line_count': line_count,
        'white_pixels': white_pixels,
        'total_pixels': total_pixels
    }

def analyze_contrast_and_readability(region):
    """Analisa contraste e legibilidade"""
    gray = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
    
    # Calcular contraste
    contrast = gray.std()
    
    # Calcular brilho
    brightness = gray.mean()
    
    # Determinar nível de contraste
    if contrast > 60:
        contrast_level = "Alto"
        readability = "Excelente"
    elif contrast > 40:
        contrast_level = "Médio"
        readability = "Boa"
    else:
        contrast_level = "Baixo"
        readability = "Ruim"
    
    return {
        'contrast': contrast,
        'brightness': brightness,
        'contrast_level': contrast_level,
        'readability': readability
    }

def generate_style_recommendations(analysis_data):
    """Gera recomendações de estilo baseadas na análise"""
    if not analysis_data:
        return
    
    print(f"💡 RECOMENDAÇÕES DE ESTILO")
    print("=" * 80)
    
    # Análise de fundo
    blue_frames = sum(1 for a in analysis_data if 'Azul' in a['background_colors']['dominant_color'])
    blue_percentage = blue_frames / len(analysis_data) * 100
    
    print(f"🎨 ANÁLISE DE FUNDO:")
    print(f"  📊 Frames com fundo azul: {blue_frames}/{len(analysis_data)} ({blue_percentage:.1f}%)")
    
    if blue_percentage > 50:
        print(f"  ✅ Fundo azul consistente - muito bom!")
    else:
        print(f"  ⚠️ Fundo azul inconsistente - pode melhorar")
    
    # Análise de texto
    text_frames = sum(1 for a in analysis_data if a['text_info']['has_text'])
    text_percentage = text_frames / len(analysis_data) * 100
    
    print(f"\n📝 ANÁLISE DE TEXTO:")
    print(f"  📊 Frames com texto: {text_frames}/{len(analysis_data)} ({text_percentage:.1f}%)")
    
    # Análise de quebra de linhas
    avg_lines = np.mean([a['text_info']['line_count'] for a in analysis_data])
    print(f"  📏 Média de linhas por frame: {avg_lines:.1f}")
    
    if avg_lines > 2:
        print(f"  ✅ Boa quebra de linhas - texto bem distribuído")
    else:
        print(f"  ⚠️ Pouca quebra de linhas - texto pode estar muito compacto")
    
    # Análise de contraste
    high_contrast_frames = sum(1 for a in analysis_data if a['contrast_analysis']['contrast_level'] == "Alto")
    contrast_percentage = high_contrast_frames / len(analysis_data) * 100
    
    print(f"\n🎨 ANÁLISE DE CONTRASTE:")
    print(f"  📊 Frames com alto contraste: {high_contrast_frames}/{len(analysis_data)} ({contrast_percentage:.1f}%)")
    
    if contrast_percentage > 70:
        print(f"  ✅ Excelente contraste - legendas muito legíveis")
    else:
        print(f"  ⚠️ Contraste pode melhorar - legendas podem estar difíceis de ler")
    
    print(f"\n🎬 RECOMENDAÇÕES GERAIS:")
    print(f"   🎨 Manter fundo azul consistente")
    print(f"   📝 Usar quebra de linhas adequada (2-3 linhas)")
    print(f"   🎨 Garantir alto contraste para legibilidade")
    print(f"   📱 Otimizar para vídeo vertical")

def main():
    """Função principal"""
    video_path = "referencialegendas.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Arquivo não encontrado: {video_path}")
        return
    
    print("🎬 ANÁLISE DE ESTILO DAS LEGENDAS")
    print("=" * 80)
    print(f"📁 Arquivo: {video_path}")
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    # Análise de estilo
    analysis_data = analyze_legend_style(video_path, num_frames=8)
    
    if analysis_data:
        # Gerar recomendações
        generate_style_recommendations(analysis_data)
    
    print("\n" + "=" * 80)
    print(f"✅ ANÁLISE CONCLUÍDA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main() 