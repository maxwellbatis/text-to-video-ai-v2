import whisper
import re
import os
from datetime import timedelta

def generate_timed_captions(audio_filename, model_size="base"):
    WHISPER_MODEL = whisper.load_model(model_size)
    
    # Forçar português e desabilitar detecção automática
    result = WHISPER_MODEL.transcribe(
        audio_filename, 
        language="pt", 
        task="transcribe",
        verbose=False,
        fp16=False,
        # Configurações adicionais para melhor reconhecimento
        condition_on_previous_text=False,
        temperature=0.0,
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6
    )
    
    return getCaptionsWithTime(result)

def generate_srt_file(captions_pairs, output_filename):
    """
    Gera arquivo SRT a partir das legendas cronometradas
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for i, ((start_time, end_time), text) in enumerate(captions_pairs, 1):
                # Converter segundos para formato SRT (HH:MM:SS,mmm)
                start_str = str(timedelta(seconds=int(start_time))) + f",{int((start_time % 1) * 1000):03d}"
                end_str = str(timedelta(seconds=int(end_time))) + f",{int((end_time % 1) * 1000):03d}"
                
                # Formatar linha SRT
                f.write(f"{i}\n")
                f.write(f"{start_str} --> {end_str}\n")
                f.write(f"{text}\n\n")
        
        print(f"✅ Arquivo SRT gerado: {output_filename}")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar SRT: {e}")
        return False

def generate_vtt_file(captions_pairs, output_filename):
    """
    Gera arquivo VTT a partir das legendas cronometradas
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Cabeçalho VTT
            f.write("WEBVTT\n\n")
            
            for i, ((start_time, end_time), text) in enumerate(captions_pairs, 1):
                # Converter segundos para formato VTT (HH:MM:SS.mmm)
                start_str = str(timedelta(seconds=int(start_time))) + f".{int((start_time % 1) * 1000):03d}"
                end_str = str(timedelta(seconds=int(end_time))) + f".{int((end_time % 1) * 1000):03d}"
                
                # Formatar linha VTT
                f.write(f"{start_str} --> {end_str}\n")
                f.write(f"{text}\n\n")
        
        print(f"✅ Arquivo VTT gerado: {output_filename}")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar VTT: {e}")
        return False

def generate_subtitle_files(audio_filename, output_dir="."):
    """
    Gera legendas cronometradas e arquivos SRT/VTT
    """
    # Gerar legendas cronometradas
    captions_pairs = generate_timed_captions(audio_filename)
    
    # Nome base do arquivo
    base_name = os.path.splitext(os.path.basename(audio_filename))[0]
    
    # Gerar arquivos SRT e VTT
    srt_filename = os.path.join(output_dir, f"{base_name}.srt")
    vtt_filename = os.path.join(output_dir, f"{base_name}.vtt")
    
    generate_srt_file(captions_pairs, srt_filename)
    generate_vtt_file(captions_pairs, vtt_filename)
    
    return {
        'captions_pairs': captions_pairs,
        'srt_file': srt_filename,
        'vtt_file': vtt_filename
    }

def splitWordsBySize(words, maxCaptionSize):
   
    halfCaptionSize = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions

def getTimestampMapping(whisper_analysis):
   
    index = 0
    locationToTimestamp = {}
    for segment in whisper_analysis['segments']:
        # Para Whisper padrão, usamos o segmento completo
        text = segment['text']
        start_time = segment['start']
        end_time = segment['end']
        
        # Dividir o texto em palavras
        words = text.split()
        word_duration = (end_time - start_time) / len(words) if words else 0
        
        for i, word in enumerate(words):
            word_start = start_time + (i * word_duration)
            word_end = start_time + ((i + 1) * word_duration)
            
            newIndex = index + len(word) + 1
            locationToTimestamp[(index, newIndex)] = word_end
            index = newIndex
    
    return locationToTimestamp

def cleanWord(word):
   
    return re.sub(r'[^\w\s\-_"\'\']', '', word)

def interpolateTimeFromDict(word_position, d):
   
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None

def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15, considerPunctuation=False):
    """
    Gera legendas cronometradas com detecção de pausas melhorada
    """
    wordLocationToTime = getTimestampMapping(whisper_analysis)
    position = 0
    start_time = 0
    CaptionsPairs = []
    text = whisper_analysis['text']
    
    if considerPunctuation:
        sentences = re.split(r'(?<=[.!?]) +', text)
        words = [word for sentence in sentences for word in splitWordsBySize(sentence.split(), maxCaptionSize)]
    else:
        words = text.split()
        words = [cleanWord(word) for word in splitWordsBySize(words, maxCaptionSize)]
    
    # Filtrar palavras vazias
    words = [word for word in words if word.strip()]
    
    for word in words:
        position += len(word) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        
        if end_time and word:
            # Verificar se há pausa muito longa (mais de 1 segundo)
            if end_time - start_time > 1.0:
                # Dividir pausas longas em segmentos menores
                pause_duration = end_time - start_time
                if pause_duration > 2.0:  # Pausas muito longas
                    print(f"⚠️ Pausa longa detectada: {pause_duration:.2f}s - pulando")
                    start_time = end_time
                    continue
                else:
                    # Pausa moderada, manter mas ajustar timing
                    adjusted_start = start_time + (pause_duration * 0.1)  # Começar 10% depois
                    CaptionsPairs.append(((adjusted_start, end_time), word))
            else:
                CaptionsPairs.append(((start_time, end_time), word))
            
            start_time = end_time

    return CaptionsPairs
