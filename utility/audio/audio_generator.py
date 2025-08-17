import edge_tts
import os
import requests
import json
from typing import Optional, Dict, Any

# Configuração das vozes ElevenLabs recomendadas
ELEVENLABS_VOICES = {
    # Vozes para fatos curiosos e documentários
    "james": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # James - tom britânico calmo e profundo
        "description": "Tom britânico calmo e profundo, excelente para narrativas históricas e curiosidades",
        "category": "curiosities"
    },
    "bill": {
        "voice_id": "pqHfZKP75Cgmzxl6c6pk",  # Bill - voz americana clássica
        "description": "Voz americana clássica, firme e clara — muito usada em vídeos explicativos e documentais",
        "category": "curiosities"
    },
    "neil": {
        "voice_id": "piTKgcLEGmPE4e6mEKli",  # Neil - equilibrado e confiável
        "description": "Equilibrado e confiável, ótimo para explicações e comentários informativos",
        "category": "curiosities"
    },
    "drew": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Drew - calmo e ligeiramente místico
        "description": "Voz calma e ligeiramente mística, ideal para conteúdo mais reflexivo ou filosófico",
        "category": "reflection"
    },
    # Vozes para conteúdo espiritual/bíblico
    "phillip": {
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Phillip - Spiritual Sage
        "description": "Projetada para temas espirituais e de meditação, com presença emocional e calma profunda",
        "category": "spiritual"
    },
    "deep_ray": {
        "voice_id": "pFZP5JQG7iQjIQuC4Bku",  # Deep Ray - Deep Voice of God
        "description": "Voz muito profunda e suave, perfeita para 'voz de Deus' em leituras bíblicas",
        "category": "spiritual"
    },
    "readwell": {
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Readwell - Deep and Narrative
        "description": "Voz profunda e narrativa, perfeita para leituras dramáticas e conteúdo envolvente",
        "category": "narrative"
    }
}

def detect_content_category(text: str) -> str:
    """
    Detecta a categoria do conteúdo baseado no texto
    """
    text_lower = text.lower()
    
    # Palavras-chave para conteúdo espiritual/bíblico
    spiritual_keywords = [
        'deus', 'jesus', 'bíblia', 'apocalipse', 'versículo', 'oração', 'fé',
        'espírito', 'sagrado', 'profecia', 'malaquias', 'revelação', 'salvação',
        'igreja', 'religião', 'espiritual', 'meditação', 'alma', 'céu', 'inferno'
    ]
    
    # Palavras-chave para conteúdo reflexivo/filosófico
    reflection_keywords = [
        'por que', 'significado', 'filosofia', 'existência', 'vida', 'morte',
        'pensamento', 'reflexão', 'contemplação', 'mistério', 'universo', 'consciência'
    ]
    
    # Verificar se é conteúdo espiritual
    for keyword in spiritual_keywords:
        if keyword in text_lower:
            return "spiritual"
    
    # Verificar se é conteúdo reflexivo
    for keyword in reflection_keywords:
        if keyword in text_lower:
            return "reflection"
    
    # Padrão: fatos curiosos/documentários
    return "curiosities"

def get_recommended_voice(content_category: str) -> str:
    """
    Retorna a voz recomendada baseada na categoria do conteúdo
    """
    if content_category == "spiritual":
        return "readwell"  # Readwell para conteúdo espiritual (deep and narrative)
    elif content_category == "reflection":
        return "drew"     # Drew para conteúdo reflexivo
    else:
        return "james"    # James para fatos curiosos/documentários

async def generate_audio_elevenlabs(text: str, output_filename: str, voice_name: Optional[str] = None) -> bool:
    """
    Gera áudio usando ElevenLabs
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("⚠️ ELEVENLABS_API_KEY não configurada. Usando Edge TTS...")
        return False
    
    # Detectar categoria do conteúdo se voz não especificada
    if not voice_name:
        content_category = detect_content_category(text)
        voice_name = get_recommended_voice(content_category)
        print(f"🎯 Categoria detectada: {content_category} -> Voz: {voice_name}")
    
    if voice_name not in ELEVENLABS_VOICES:
        print(f"⚠️ Voz '{voice_name}' não encontrada. Usando Edge TTS...")
        return False
    
    voice_config = ELEVENLABS_VOICES[voice_name]
    voice_id = voice_config["voice_id"]
    
    try:
        # Configuração da API ElevenLabs
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        # Configurações de voz baseadas na categoria
        voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        # Ajustes específicos por categoria
        if voice_config["category"] == "spiritual":
            voice_settings.update({
                "stability": 0.8,  # Mais estável para conteúdo solene
                "similarity_boost": 0.85,
                "style": 0.4  # Mais expressivo
            })
        elif voice_config["category"] == "narrative":
            voice_settings.update({
                "stability": 0.9,  # Muito estável para narrativas
                "similarity_boost": 0.9,
                "style": 0.5  # Muito expressivo
            })
        elif voice_config["category"] == "reflection":
            voice_settings.update({
                "stability": 0.6,
                "similarity_boost": 0.7,
                "style": 0.2  # Moderadamente expressivo
            })
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",  # Modelo multilíngue para português
            "voice_settings": voice_settings
        }
        
        print(f"🎤 Gerando áudio com ElevenLabs - Voz: {voice_name}")
        print(f"📝 Configuração: {voice_config['description']}")
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(output_filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Áudio gerado com ElevenLabs: {output_filename}")
            return True
        else:
            print(f"❌ Erro na API ElevenLabs: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao gerar áudio com ElevenLabs: {e}")
        return False

async def generate_audio(text: str, output_filename: str, voice_name: Optional[str] = None) -> None:
    """
    Gera áudio usando ElevenLabs (se disponível) ou Edge TTS como fallback
    """
    # Tentar ElevenLabs primeiro
    if await generate_audio_elevenlabs(text, output_filename, voice_name):
        return
    
    # Fallback para Edge TTS com retry automático
    print("🔄 Usando Edge TTS como fallback...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"🎤 Tentativa {attempt + 1}/{max_retries} - Gerando áudio com Edge TTS...")
            
            # Criar nova instância do Communicate para gerar novo token
            communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural", rate="-20%")
            await communicate.save(output_filename)
            
            print(f"✅ Áudio gerado com Edge TTS: {output_filename}")
            return
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Tentativa {attempt + 1} falhou: {error_msg}")
            
            if "403" in error_msg or "Invalid response status" in error_msg:
                print("🔄 Token expirado, tentando novamente...")
                # Aguardar um pouco antes da próxima tentativa
                import asyncio
                await asyncio.sleep(2)
                continue
            elif attempt == max_retries - 1:
                print(f"❌ Todas as tentativas falharam. Erro final: {e}")
                raise e
            else:
                print(f"🔄 Tentando novamente em 1 segundo...")
                import asyncio
                await asyncio.sleep(1)
    
    print(f"❌ Falha ao gerar áudio após {max_retries} tentativas")

def list_available_voices() -> Dict[str, Any]:
    """
    Lista todas as vozes disponíveis com suas descrições
    """
    return {
        "voices": ELEVENLABS_VOICES,
        "categories": {
            "curiosities": ["james", "bill", "neil"],
            "reflection": ["drew"],
            "spiritual": ["phillip", "deep_ray"]
        },
        "recommendations": {
            "Fatos curiosos / Documentários": ["james", "bill", "neil"],
            "Reflexão / Mistério / Filosófico": ["drew"],
            "Conteúdo religioso ou bíblico": ["readwell", "deep_ray"],
            "Narrativas dramáticas": ["readwell", "phillip"]
        }
    }