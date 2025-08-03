#!/usr/bin/env python3
"""
Análise do Vídeo VSL Gerado
Analisa o vídeo VSL que foi criado pelo sistema
"""

import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper
import json
from datetime import datetime

def analyze_generated_vsl(video_path):
    """Analisa o vídeo VSL gerado pelo sistema"""
    print("🎬 ANÁLISE DO VÍDEO VSL GERADO")
    print("=" * 60)
    
    if not os.path.exists(video_path):
        print(f"❌ Arquivo não encontrado: {video_path}")
        return
    
    try:
        video = VideoFileClip(video_path)
        
        # Informações básicas
        duration = video.duration
        fps = video.fps
        size = video.size
        has_audio = video.audio is not None
        
        print(f"📊 DURAÇÃO: {duration:.2f} segundos")
        print(f"🎞️ FPS: {fps}")
        print(f"📐 RESOLUÇÃO: {size[0]}x{size[1]}")
        print(f"🔊 ÁUDIO: {'Sim' if has_audio else 'Não'}")
        
        # Analisar áudio se existir
        if has_audio:
            audio = video.audio
            print(f"🎵 DURAÇÃO DO ÁUDIO: {audio.duration:.2f} segundos")
            
            # Extrair áudio para transcrição
            temp_audio = "temp_audio.wav"
            audio.write_audiofile(temp_audio, verbose=False, logger=None)
            
            # Transcrever com Whisper
            print("📝 Transcrevendo áudio...")
            model = whisper.load_model("base")
            result = model.transcribe(temp_audio, language="pt")
            
            # Limpar arquivo temporário
            os.remove(temp_audio)
            
            text = result["text"]
            segments = result["segments"]
            
            print(f"\n📄 TRANSCRIÇÃO COMPLETA:")
            print("-" * 40)
            print(text)
            print("-" * 40)
            
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"📝 PALAVRAS: {len(text.split())}")
            print(f"📝 CARACTERES: {len(text)}")
            print(f"⏱️ SEGMENTOS: {len(segments)}")
            print(f"🎯 PALAVRAS POR MINUTO: {len(text.split()) / (duration / 60):.1f}")
            
            # Analisar estrutura VSL
            analyze_vsl_structure(text, segments, duration)
        
        # Analisar frames para elementos visuais
        analyze_visual_elements(video)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao analisar vídeo: {e}")
        return False

def analyze_vsl_structure(text, segments, duration):
    """Analisa se o vídeo segue a estrutura VSL"""
    print(f"\n🎯 ANÁLISE DA ESTRUTURA VSL")
    print("=" * 40)
    
    # Verificar elementos VSL
    vsl_elements = {
        'hook': ['você sabe', 'imagine', 'problema', 'diferença'],
        'problem': ['por que', 'problema', 'frustração', 'falha'],
        'solution': ['com', 'agora', 'solução', 'transformação'],
        'offer': ['desconto', 'oferta', 'exclusivo', 'limitado'],
        'cta': ['clique', 'agora', 'saiba mais', 'comece']
    }
    
    text_lower = text.lower()
    
    print(f"🔍 ELEMENTOS VSL DETECTADOS:")
    for element, keywords in vsl_elements.items():
        found_keywords = [kw for kw in keywords if kw in text_lower]
        if found_keywords:
            print(f"  ✅ {element.upper()}: {', '.join(found_keywords)}")
        else:
            print(f"  ❌ {element.upper()}: Não encontrado")
    
    # Análise temporal
    print(f"\n⏱️ ANÁLISE TEMPORAL:")
    print(f"  📊 Duração total: {duration:.2f}s")
    
    # Dividir em seções VSL
    sections = {
        'Hook (0-10s)': (0, 10),
        'Problema (10-20s)': (10, 20),
        'Solução (20-30s)': (20, 30),
        'Oferta (30-40s)': (30, 40),
        'CTA (40-50s)': (40, 50)
    }
    
    for section_name, (start, end) in sections.items():
        if duration >= start:
            actual_end = min(end, duration)
            print(f"  📋 {section_name}: {start}s - {actual_end}s")
    
    # Verificar se tem estrutura VSL adequada
    has_hook = any(kw in text_lower for kw in vsl_elements['hook'])
    has_problem = any(kw in text_lower for kw in vsl_elements['problem'])
    has_solution = any(kw in text_lower for kw in vsl_elements['solution'])
    has_offer = any(kw in text_lower for kw in vsl_elements['offer'])
    has_cta = any(kw in text_lower for kw in vsl_elements['cta'])
    
    vsl_score = sum([has_hook, has_problem, has_solution, has_offer, has_cta])
    
    print(f"\n📊 SCORE VSL: {vsl_score}/5")
    if vsl_score >= 4:
        print("  ✅ Estrutura VSL adequada")
    elif vsl_score >= 2:
        print("  ⚠️ Estrutura VSL parcial")
    else:
        print("  ❌ Estrutura VSL inadequada")

def analyze_visual_elements(video):
    """Analisa elementos visuais do vídeo"""
    print(f"\n🎨 ANÁLISE VISUAL")
    print("=" * 40)
    
    try:
        # Analisar alguns frames
        total_frames = int(video.duration * video.fps)
        sample_frames = 5
        frame_interval = total_frames // sample_frames
        
        print(f"🎞️ ANALISANDO {sample_frames} FRAMES:")
        
        for i in range(sample_frames):
            frame_time = (i * frame_interval) / video.fps
            frame = video.get_frame(frame_time)
            
            # Análise básica do frame
            brightness = frame.mean()
            contrast = frame.std()
            
            print(f"  Frame {i+1} ({frame_time:6.2f}s): Brilho={brightness:6.1f}, Contraste={contrast:6.1f}")
        
        # Verificar se há texto sobreposto
        print(f"\n📝 DETECÇÃO DE TEXTO:")
        # Esta é uma análise simplificada - em produção seria mais complexa
        print(f"  ℹ️ Análise de texto requer processamento avançado")
        
    except Exception as e:
        print(f"❌ Erro na análise visual: {e}")

def generate_recommendations(analysis_data):
    """Gera recomendações para melhorar o VSL"""
    print(f"\n💡 RECOMENDAÇÕES PARA MELHORAR")
    print("=" * 40)
    
    print(f"🎯 ESTRUTURA VSL:")
    print(f"  ✅ Hook impactante nos primeiros 3 segundos")
    print(f"  ✅ Problema claramente identificado")
    print(f"  ✅ Solução apresentada como transformadora")
    print(f"  ✅ Oferta específica com urgência")
    print(f"  ✅ CTA claro e direto")
    
    print(f"\n🎨 ELEMENTOS VISUAIS:")
    print(f"  ✅ Contraste dramático (claro/escuro)")
    print(f"  ✅ Transições rápidas (8-10 mudanças)")
    print(f"  ✅ Overlays cinematográficos")
    print(f"  ✅ Gradientes dinâmicos")
    
    print(f"\n🎵 RITMO DE NARRAÇÃO:")
    print(f"  ✅ Velocidade: 150-180 WPM")
    print(f"  ✅ Pausas estratégicas: 2-3s")
    print(f"  ✅ Variação de velocidade")
    print(f"  ✅ Repetição de palavras-chave")
    
    print(f"\n📝 LINGUAGEM:")
    print(f"  ✅ Direta e impactante")
    print(f"  ✅ Palavras emocionais")
    print(f"  ✅ Ofertas específicas")
    print(f"  ✅ CTAs claros")

def main():
    """Função principal"""
    video_path = "rendered_video.mp4"
    
    print(f"🎬 ANÁLISE DO VÍDEO VSL GERADO")
    print(f"📁 Arquivo: {video_path}")
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    success = analyze_generated_vsl(video_path)
    
    if success:
        generate_recommendations({})
    
    print("\n" + "=" * 60)
    print(f"✅ ANÁLISE CONCLUÍDA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main() 