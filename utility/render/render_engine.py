import time
import os
import tempfile
import zipfile
import platform
import subprocess
import re
import random
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests

# Patch para compatibilidade com Pillow 10.x (ANTIALIAS foi removido)
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
except ImportError:
    pass

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

def get_word_color(word, template_id=None):
    """
    Define a cor para cada palavra baseada em seu significado e template
    """
    word_lower = word.lower().strip()
    
    # Configurações de cores por template
    color_schemes = {
        'cinematic_religious': {
            'divine': "#FFD700",      # Dourado para palavras divinas
            'faith': "#87CEEB",       # Azul claro para fé
            'prayer': "#90EE90",      # Verde claro para oração
            'family': "#FFB6C1",      # Rosa claro para família
            'wisdom': "#DDA0DD",      # Roxo claro para sabedoria
            'strength': "#FFA500",    # Laranja para força
            'time': "#D3D3D3",        # Cinza claro para tempo
            'default': "white"        # Branco padrão
        },
        'vsl_magnetic': {
            'divine': "#FF6B6B",      # Vermelho vibrante
            'faith': "#4ECDC4",       # Turquesa
            'prayer': "#45B7D1",      # Azul
            'family': "#96CEB4",      # Verde suave
            'wisdom': "#FFEAA7",      # Amarelo
            'strength': "#DDA0DD",    # Roxo
            'time': "#F8BBD9",        # Rosa
            'default': "#FFFFFF"      # Branco
        },
        'default': {
            'divine': "#FFD700",      # Dourado
            'faith': "#87CEEB",       # Azul claro
            'prayer': "#90EE90",      # Verde claro
            'family': "#FFB6C1",      # Rosa claro
            'wisdom': "#DDA0DD",      # Roxo claro
            'strength': "#FFA500",    # Laranja
            'time': "#D3D3D3",        # Cinza claro
            'default': "white"        # Branco
        }
    }
    
    # Selecionar esquema de cores baseado no template
    scheme = color_schemes.get(template_id, color_schemes['default'])
    
    # Palavras divinas/espirituais
    divine_words = ['deus', 'senhor', 'jesus', 'cristo', 'espírito', 'santo', 'divino', 'celestial', 'sagrado']
    if word_lower in divine_words:
        return scheme['divine']
    
    # Palavras de fé/esperança
    faith_words = ['fé', 'esperança', 'amor', 'paz', 'graça', 'bênção', 'salvação', 'redenção', 'milagre']
    if word_lower in faith_words:
        return scheme['faith']
    
    # Palavras de oração/adoração
    prayer_words = ['oração', 'adoração', 'louvor', 'agradecemos', 'obrigado', 'amém', 'aleluia']
    if word_lower in prayer_words:
        return scheme['prayer']
    
    # Palavras de família/relacionamento
    family_words = ['família', 'pais', 'filhos', 'casa', 'lar', 'união', 'juntos', 'cuidado']
    if word_lower in family_words:
        return scheme['family']
    
    # Palavras de sabedoria/conhecimento
    wisdom_words = ['sabedoria', 'conhecimento', 'ensinamento', 'palavra', 'bíblia', 'versículo', 'profecia']
    if word_lower in wisdom_words:
        return scheme['wisdom']
    
    # Palavras de força/coragem
    strength_words = ['força', 'coragem', 'vitória', 'poder', 'guerra', 'luta', 'resistência']
    if word_lower in strength_words:
        return scheme['strength']
    
    # Palavras de tempo/momento
    time_words = ['hoje', 'agora', 'sempre', 'eternamente', 'momento', 'tempo', 'dia', 'noite']
    if word_lower in time_words:
        return scheme['time']
    
    # Padrão
    return scheme['default']

def generate_colored_text_clips(processed_text, start_time, end_time, template_id=None):
    """
    Gera clips de texto palavra por palavra com cores diferentes para palavras-chave
    """
    words = processed_text.split()
    clips = []
    
    if not words:
        return clips
    
    # Calcular duração por palavra com buffer de sincronização
    total_duration = end_time - start_time
    word_duration = total_duration / len(words)
    
    # Buffer de sincronização para melhor timing
    sync_buffer = 0.05  # 50ms de buffer
    
    for i, word in enumerate(words):
        # Calcular timing para esta palavra com buffer
        word_start = max(0, start_time + (i * word_duration) - sync_buffer)
        word_end = min(end_time, start_time + ((i + 1) * word_duration) + sync_buffer)
        
        # Garantir que não ultrapasse o tempo total
        if word_start >= end_time:
            break
        
        # Criar clip para cada palavra individual
        txt = word.upper()
        
        # Limpar texto mantendo pontuação importante
        txt = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', '', txt)
        txt = txt.strip()  # Remove espaços extras
        
        # Pular palavras vazias ou muito curtas
        if len(txt) < 1:
            continue
        
        # Verificar se a palavra tem duração mínima
        if word_end - word_start < 0.1:  # Mínimo 100ms por palavra
            continue
        
        # Obter cor para esta palavra baseada no template
        word_color = get_word_color(word, template_id)
        
        try:
            # Criar múltiplas camadas para texto mais grosso
            # Camada 1: Contorno preto espesso
            txt_clip_bg = (TextClip(txt=txt,
                                    fontsize=90,  # Fonte grande e impactante
                                    font="Impact",  # Fonte Impact (mais chamativa)
                                    color="black",  # Cor preta para contorno
                                    stroke_color="black",  # Contorno preto
                                    stroke_width=12,  # Contorno muito espesso
                                    method="label")
                           .set_start(word_start)
                           .set_end(word_end)
                           .fadein(0.1)  # Fade-in rápido
                           .fadeout(0.1)  # Fade-out rápido
                           .set_position(("center", "center")))  # Centralizado na tela
        
            # Camada 2: Texto colorido principal
            txt_clip_main = (TextClip(txt=txt,
                                      fontsize=90,  # Fonte grande e impactante
                                      font="Impact",  # Fonte Impact (mais chamativa)
                                      color=word_color,  # Cor baseada na palavra
                                      stroke_color="black",  # Contorno preto
                                      stroke_width=8,  # Contorno espesso
                                      method="label")
                             .set_start(word_start)
                             .set_end(word_end)
                             .fadein(0.1)  # Fade-in rápido
                             .fadeout(0.1)  # Fade-out rápido
                             .set_position(("center", "center")))  # Centralizado na tela
            
            # Adicionar ambas as camadas
            clips.append(txt_clip_bg)
            clips.append(txt_clip_main)
            
        except Exception as e:
            print(f"⚠️ Erro ao criar clip de texto para '{txt}': {e}")
            continue
    
    return clips

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

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server, template_id=None):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    magick_path = get_program_path("magick")
    print(magick_path)
    if magick_path:
        os.environ['IMAGEMAGICK_BINARY'] = magick_path
    else:
        os.environ['IMAGEMAGICK_BINARY'] = '/usr/bin/convert'
    
    visual_clips = []
    print(f"🎬 Processando {len(background_video_data)} segmentos de vídeo de fundo")
    
    for (t1, t2), video_url in background_video_data:
        print(f"📹 Segmento [{t1:.2f}s - {t2:.2f}s]: {video_url}")
        
        # Verificar se URL é válida
        if not video_url or video_url == "":
            print(f"⚠️ URL vazia para segmento [{t1:.2f}s - {t2:.2f}s], criando clip preto")
            from moviepy.video.VideoClip import ColorClip
            video_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0))
            video_clip = video_clip.set_duration(t2 - t1)
            video_clip = video_clip.set_start(t1)
            video_clip = video_clip.set_end(t2)
            visual_clips.append(video_clip)
            continue
        
        # Download the file
        video_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg').name
        try:
            download_file(video_url, video_filename)
            print(f"✅ Download concluído: {video_filename}")
        except Exception as e:
            print(f"❌ Erro no download: {e}")
            # Criar clip preto como fallback
            from moviepy.video.VideoClip import ColorClip
            video_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0))
            video_clip = video_clip.set_duration(t2 - t1)
            video_clip = video_clip.set_start(t1)
            video_clip = video_clip.set_end(t2)
            visual_clips.append(video_clip)
            continue
        
        # Check if it's an image or video
        if video_url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            # Convert image to video clip with explicit duration
            try:
                print(f"🖼️ Processando imagem: {video_filename}")
                image_clip = ImageClip(video_filename)
                duration = t2 - t1
                video_clip = image_clip.set_duration(duration)
                video_clip = video_clip.set_start(t1)
                video_clip = video_clip.set_end(t2)
                # Resize to vertical video dimensions (9:16 aspect ratio)
                video_clip = video_clip.resize(width=1080, height=1920)
                print(f"✅ Imagem convertida para vídeo: {video_filename}")
            except Exception as e:
                print(f"❌ Erro ao processar imagem {video_filename}: {e}")
                # Criar um clip de cor sólida como fallback
                from moviepy.video.VideoClip import ColorClip
                video_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0))
                video_clip = video_clip.set_duration(t2 - t1)
                video_clip = video_clip.set_start(t1)
                video_clip = video_clip.set_end(t2)
        else:
            # Create VideoFileClip from the downloaded video file
            try:
                print(f"🎬 Processando vídeo: {video_filename}")
                video_clip = VideoFileClip(video_filename)
                video_clip = video_clip.set_start(t1)
                video_clip = video_clip.set_end(t2)
                # Resize to vertical video dimensions (9:16 aspect ratio)
                video_clip = video_clip.resize(width=1080, height=1920)
                print(f"✅ Vídeo processado com sucesso: {video_filename}")
            except Exception as e:
                print(f"❌ Erro ao processar vídeo {video_filename}: {e}")
                # Criar um clip de cor sólida como fallback
                from moviepy.video.VideoClip import ColorClip
                video_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0))
                video_clip = video_clip.set_duration(t2 - t1)
                video_clip = video_clip.set_start(t1)
                video_clip = video_clip.set_end(t2)
        
        print(f"📹 Adicionando clip ao composite: duração {t2-t1:.2f}s")
        visual_clips.append(video_clip)
    
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)

    # Detectar pausas no áudio e ajustar legendas
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_duration = audio_file_clip.duration
    
    # Filtrar legendas que correspondem a pausas ou silêncio
    filtered_captions = []
    for (t1, t2), text in timed_captions:
        # Pular legendas muito curtas ou vazias
        if len(text.strip()) < 2:
            continue
            
        # Calcular duração do segmento
        segment_duration = t2 - t1
        
        # Ajustar timing para melhor distribuição - reduzir limite mínimo
        if segment_duration < 0.3:  # Reduzido de 0.5s para 0.3s
            continue
        
        # Verificar se há áudio real neste segmento (não apenas pausa)
        # Se a duração for muito longa sem palavras suficientes, pode ser pausa
        words = text.split()
        if segment_duration > 2.0 and len(words) < 3:
            print(f"⚠️ Possível pausa detectada [{t1:.2f}s - {t2:.2f}s]: '{text}' - pulando")
            continue
        
        # Processar texto para quebra de linhas adequada
        processed_text = process_text_for_captions(text)
        
        # Limpar texto mantendo pontuação importante
        processed_text = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', '', processed_text)
        processed_text = processed_text.replace('\n', ' ').strip()
        
        # Filtrar palavras muito curtas ou irrelevantes
        words = processed_text.split()
        if len(words) < 1:  # Pular se não tiver palavras
            continue
        
        # Adicionar à lista filtrada
        filtered_captions.append(((t1, t2), processed_text))
    
    print(f"📝 Legendas filtradas: {len(filtered_captions)} de {len(timed_captions)} originais")
    
    # Aplicar legendas filtradas com melhor sincronização
    for (t1, t2), processed_text in filtered_captions:
        # Gerar clips de texto palavra por palavra com sincronização melhorada
        text_clips = generate_colored_text_clips(processed_text, t1, t2, template_id)
        if text_clips:  # Só adicionar se houver clips gerados
            visual_clips.extend(text_clips)
            print(f"✅ Legendas sincronizadas para '{processed_text[:30]}...' ({len(text_clips)} palavras)")
        else:
            print(f"⚠️ Nenhuma legenda gerada para '{processed_text[:30]}...'")

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
