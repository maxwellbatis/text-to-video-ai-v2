import time
import os
import tempfile
import zipfile
import platform
import subprocess
import re
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests

def process_text_for_captions(text):
    """
    Processa texto para legendas seguindo as especificações:
    - Máximo 42 caracteres por linha
    - Máximo 2 linhas
    - Quebra de linhas inteligente
    """
    # Limpar texto
    text = text.strip()
    
    # Se texto já é curto, retornar como está
    if len(text) <= 42:
        return text
    
    # Dividir em palavras
    words = text.split()
    
    # Se tem poucas palavras, tentar quebrar no meio
    if len(words) <= 4:
        mid = len(text) // 2
        # Procurar espaço próximo ao meio
        for i in range(mid - 10, mid + 10):
            if 0 <= i < len(text) and text[i] == ' ':
                return text[:i] + '\n' + text[i+1:]
        return text
    
    # Para textos longos, quebrar por palavras
    lines = []
    current_line = ""
    
    for word in words:
        # Se adicionar esta palavra excede 42 caracteres
        if len(current_line + " " + word) > 42:
            if current_line:
                lines.append(current_line.strip())
                current_line = word
            else:
                # Palavra muito longa, quebrar no meio
                lines.append(word[:42])
                current_line = word[42:]
        else:
            current_line += (" " + word) if current_line else word
    
    # Adicionar última linha
    if current_line:
        lines.append(current_line.strip())
    
    # Limitar a 2 linhas
    if len(lines) > 2:
        lines = lines[:2]
        # Adicionar "..." se necessário
        if len(lines[1]) > 39:
            lines[1] = lines[1][:39] + "..."
    
    return '\n'.join(lines)

def download_file(url, filename):
    with open(filename, 'wb') as f:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        f.write(response.content)

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    magick_path = get_program_path("magick")
    print(magick_path)
    if magick_path:
        os.environ['IMAGEMAGICK_BINARY'] = magick_path
    else:
        os.environ['IMAGEMAGICK_BINARY'] = '/usr/bin/convert'
    
    visual_clips = []
    for (t1, t2), video_url in background_video_data:
        # Download the video file
        video_filename = tempfile.NamedTemporaryFile(delete=False).name
        download_file(video_url, video_filename)
        
        # Create VideoFileClip from the downloaded file
        video_clip = VideoFileClip(video_filename)
        video_clip = video_clip.set_start(t1)
        video_clip = video_clip.set_end(t2)
        visual_clips.append(video_clip)
    
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)

    for (t1, t2), text in timed_captions:
        # Pular legendas muito curtas ou vazias
        if len(text.strip()) < 3:
            continue
            
        # Calcular duração do segmento
        segment_duration = t2 - t1
        
        # Ajustar timing para melhor distribuição
        if segment_duration < 1.0:  # Segmentos muito curtos
            continue
        
        # Processar texto para quebra de linhas adequada (máximo 42 caracteres por linha)
        processed_text = process_text_for_captions(text)
            
        text_clip = (TextClip(txt=processed_text,
                              fontsize=48,  # ~3.8% da altura do frame (1280px)
                              font="Arial-Bold",  # Sans-serif moderna
                              color="white",  # Branco puro #FFFFFF
                              stroke_color="black",  # Contorno preto
                              stroke_width=4,  # Contorno espesso (3-4px)
                              method="label",
                              bg_color="rgba(0,0,0,0.0)",  # Sem fundo (apenas contorno)
                              size=(720, None))  # Largura para vídeo vertical (720px)
                  .set_start(t1)
                  .set_end(t2)
                  .set_position(("center", "bottom"))  # Centralizado horizontalmente
                  .margin(bottom=60)  # 60px acima da borda inferior
                  .crossfadein(0.1)  # Cortes secos (fade mínimo)
                  .crossfadeout(0.1))
        visual_clips.append(text_clip)

    video = CompositeVideoClip(visual_clips)
    
    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video.duration = audio.duration
        video.audio = audio

    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
    
    # Clean up downloaded files
    for (t1, t2), video_url in background_video_data:
        video_filename = tempfile.NamedTemporaryFile(delete=False).name
        os.remove(video_filename)

    return OUTPUT_FILE_NAME
