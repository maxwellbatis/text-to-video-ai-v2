import time
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests

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
        text_clip = (TextClip(txt=text,
                              fontsize=120,  # Aumentado de 90 para 120
                              font="Arial-Bold",
                              color="white",
                              stroke_color="black",
                              stroke_width=6,  # Aumentado de 4 para 6
                              method="label",
                              bg_color="rgba(0,0,0,0.7)",  # Fundo semi-transparente
                              size=(1920, None))  # Largura fixa para melhor legibilidade
                  .set_start(t1)
                  .set_end(t2)
                  .set_position(("center", "bottom"))
                  .margin(bottom=150)  # Aumentado de 100 para 150
                  .crossfadein(0.3)
                  .crossfadeout(0.3))
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

def get_output_media_vsl(audio_file_path, script, background_video_data, video_server, template_config=None):
    """Renderiza vídeo VSL sem legendas tradicionais, usando overlays de texto"""
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

    # Gerar overlays de texto VSL em vez de legendas
    if template_config:
        from utility.render.template_render_engine import TemplateRenderEngine
        template_engine = TemplateRenderEngine()
        text_overlays = template_engine.generate_vsl_text_overlays(script, template_config)
        
        for overlay in text_overlays:
            # Criar TextClip com estilo VSL otimizado para vertical
            style = overlay['style']
            font_size = int(style['size'].split('-')[0]) if '-' in style['size'] else int(style['size'])
            
            # Ajustar tamanho para vídeo vertical
            if font_size > 100:
                font_size = 80  # Limitar tamanho para vertical
            
            text_clip = (TextClip(txt=overlay['text'],
                                  fontsize=font_size,
                                  font=style['font'],
                                  color=style['color'],
                                  stroke_color=style['stroke'],
                                  stroke_width=style['stroke_width'],
                                  method="label",
                                  bg_color=style['bg_color'],
                                  size=(1080, None))  # Largura para vertical
                      .set_start(overlay['start_time'])
                      .set_end(overlay['end_time'])
                      .set_position(("center", overlay['position']))
                      .margin(bottom=100 if overlay['position'] == 'bottom' else 50)
                      .crossfadein(0.3)
                      .crossfadeout(0.3))
            visual_clips.append(text_clip)
    else:
        # Fallback para texto simples se não houver template
        text_clip = (TextClip(txt="VSL - Video Sales Letter",
                              fontsize=80,  # Menor para vertical
                              font="Arial-Bold",
                              color="white",
                              stroke_color="black",
                              stroke_width=4,
                              method="label",
                              bg_color="rgba(0,0,0,0.9)",
                              size=(1080, None))  # Largura para vertical
                  .set_start(0)
                  .set_end(5)
                  .set_position(("center", "center"))
                  .crossfadein(0.5)
                  .crossfadeout(0.5))
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
