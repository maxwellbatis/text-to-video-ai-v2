#!/usr/bin/env python3
"""
Gerador de Vídeos de Resumos de Novelas
Baseado no projeto Text-To-Video-AI
"""

import os
import asyncio
import argparse
import json
from typing import Optional, List

# Importar módulos do projeto principal
from utility.script.novela_script_generator import generate_novela_script, extract_novela_info
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url, getBestVideo
from utility.video.character_image_generator import CharacterImageGenerator
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals

# Importar sistema de templates
from utility.templates.template_manager import TemplateManager
from utility.render.template_render_engine import TemplateRenderEngine

# Importar banco de dados
try:
    from database import VideoDatabase
    DB_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Banco de dados não disponível: {e}")
    DB_AVAILABLE = False

class NovelaVideoGenerator:
    def __init__(self):
        self.template_manager = TemplateManager()
        self.template_render_engine = TemplateRenderEngine()
        self.character_generator = CharacterImageGenerator()
        self.novela_template = self.template_manager.get_template("novela_resumo")
        
        if not self.novela_template:
            print("⚠️ Template de novela não encontrado. Usando configurações padrão.")
            self.novela_template = self._get_default_template()
    
    def _get_default_template(self):
        """Template padrão caso o arquivo não seja encontrado"""
        return {
            "name": "Resumo de Novela",
            "visual_settings": {
                "text_style": {
                    "font": "Impact",
                    "font_size": 85,
                    "color": "white",
                    "stroke_color": "black",
                    "stroke_width": 4
                }
            },
            "audio_settings": {
                "background_music": {
                    "volume": 0.2
                }
            }
        }
    
    async def generate_novela_video(self, topic: str, voice_name: Optional[str] = None, 
                                   use_db: bool = True, credentials_name: str = "default"):
        """
        Gera vídeo de resumo de novela completo
        """
        print(f"🎬 Iniciando geração de vídeo para: {topic}")
        
        # Extrair informações da novela
        novela_info = extract_novela_info(topic)
        print(f"📺 Novela detectada: {novela_info['novela_name']}")
        print(f"📝 Tipo de conteúdo: {novela_info['content_type']}")
        
        # Conectar ao banco de dados se disponível
        db = None
        video_id = None
        
        if use_db and DB_AVAILABLE:
            try:
                db = VideoDatabase()
                await db.connect()
                
                credentials = await db.get_credentials(credentials_name)
                if credentials:
                    if credentials.openaiKey:
                        os.environ['OPENAI_KEY'] = credentials.openaiKey
                    if credentials.groqKey:
                        os.environ['GROQ_API_KEY'] = credentials.groqKey
                    if credentials.pexelsKey:
                        os.environ['PEXELS_KEY'] = credentials.pexelsKey
                
                # Criar registro de vídeo
                video = await db.create_video(
                    title=f"Resumo de {novela_info['novela_name']} - {topic}",
                    topic=topic,
                    script="",
                    credentials_id=credentials.id if credentials else None
                )
                video_id = video.id
                print(f"📊 Vídeo registrado no banco: {video_id}")
                
                await db.update_video_status(video_id, "PROCESSING")
            except Exception as e:
                print(f"⚠️ Erro ao conectar com banco: {e}")
                use_db = False
        
        try:
            # 1. Gerar script específico para novela
            print("📝 Gerando script de novela...")
            script = generate_novela_script(topic)
            
            if script.startswith("Erro"):
                print(f"❌ Erro na geração do script: {script}")
                return None
            
            print(f"✅ Script gerado: {script[:100]}...")
            
            # Atualizar script no banco
            if use_db and video_id:
                await db.update_video_status(video_id, "SCRIPT_GENERATED")
            
            # 2. Gerar áudio
            print("🎙️ Gerando áudio...")
            audio_filename = f"audio_novela_{video_id}.wav" if video_id else "audio_novela.wav"
            
            # Usar voz específica para novelas se não especificada
            if not voice_name:
                voice_name = "francisco"  # Voz padrão para novelas
            
            await generate_audio(script, audio_filename, voice_name)
            print(f"✅ Áudio gerado: {audio_filename}")
            
            # 3. Gerar legendas temporizadas
            print("📺 Gerando legendas...")
            captions = generate_timed_captions(audio_filename)
            print(f"✅ Legendas geradas: {len(captions)} segmentos")
            
            # 4. Gerar consultas de busca para vídeos de fundo
            print("🎬 Gerando consultas de busca para vídeos...")
            search_queries = getVideoSearchQueriesTimed(script, captions)
            print(f"✅ Consultas geradas: {len(search_queries)} segmentos")
            
            # 5. Buscar imagens de personagens e criar vídeos baseados em imagens
            print("🎭 Buscando imagens de personagens para criar vídeos...")
            character_videos = []
            
            # Extrair personagens do script
            character_segments = self._extract_character_segments(script)
            print(f"🔍 Segmentos com personagens encontrados: {len(character_segments)}")
            
            for i, segment in enumerate(character_segments):
                print(f"🎭 Buscando imagem para: {segment[:50]}...")
                image_url = self.character_generator.get_character_image(segment)
                if image_url:
                    # Criar vídeo baseado na imagem do personagem
                    video_data = {
                        'time_range': search_queries[i][0] if i < len(search_queries) else (i*5, (i+1)*5),
                        'image_url': image_url,
                        'character_name': self._extract_character_name(segment),
                        'segment_text': segment
                    }
                    character_videos.append(video_data)
                    print(f"✅ Vídeo de personagem criado: {video_data['character_name']}")
                else:
                    print(f"⚠️ Imagem não encontrada para: {segment[:50]}")
            
            print(f"✅ Vídeos de personagens criados: {len(character_videos)}")
            
            # Converter para formato compatível com render_engine
            video_urls = []
            for video_data in character_videos:
                # Usar a imagem como "vídeo" (será convertida para vídeo)
                video_urls.append((video_data['time_range'], video_data['image_url']))
            
            # 6. Renderizar vídeo final
            print("🎬 Renderizando vídeo final...")
            output_filename = f"novela_resumo_{video_id}.mp4" if video_id else "novela_resumo.mp4"
            
            # Aplicar template de novela
            if self.novela_template:
                # Primeiro gerar vídeo básico
                temp_output = get_output_media(audio_filename, captions, video_urls, "temp_" + output_filename)
                # Depois aplicar template
                output_filename = self.template_render_engine.apply_template_to_video(
                    temp_output, self.novela_template, audio_filename
                )
            else:
                output_filename = get_output_media(audio_filename, captions, video_urls, output_filename)
            
            print(f"✅ Vídeo renderizado: {output_filename}")
            
            # 7. Atualizar banco de dados
            if use_db and video_id and db:
                await db.update_video_status(
                    video_id, "COMPLETED", 
                    audio_path=audio_filename,
                    video_path=output_filename
                )
                print(f"📊 Status atualizado no banco: COMPLETED")
            
            return {
                "success": True,
                "video_path": output_filename,
                "audio_path": audio_filename,
                "script": script,
                "novela_info": novela_info,
                "video_id": video_id
            }
            
        except Exception as e:
            print(f"❌ Erro durante a geração: {e}")
            
            if use_db and video_id and db:
                await db.update_video_status(video_id, "ERROR")
            
            return {
                "success": False,
                "error": str(e)
            }
        
        finally:
            if db:
                await db.disconnect()
    
    def _extract_character_segments(self, script: str) -> List[str]:
        """
        Extrai segmentos relacionados a personagens do script
        """
        segments = []
        
        # Dividir script em frases
        sentences = script.split('.')
        
        # Palavras-chave relacionadas a personagens
        character_keywords = [
            'maria', 'joão', 'luna', 'dante', 'sol', 'daniel', 'alice', 'caio',
            'lívia', 'rafael', 'carolina', 'ricardo', 'marina', 'cuba',
            'protagonista', 'vilão', 'antagonista', 'mocinha', 'mocinho',
            'personagem', 'ator', 'atriz', 'herói', 'heroína'
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in character_keywords):
                if len(sentence.strip()) > 10:  # Filtrar frases muito curtas
                    segments.append(sentence.strip())
        
        # Limitar a 5 segmentos para não sobrecarregar
        return segments[:5]
    
    def _extract_character_name(self, segment: str) -> str:
        """
        Extrai o nome do personagem de um segmento
        """
        # Nomes de personagens conhecidos
        character_names = [
            'maria', 'joão', 'luna', 'dante', 'sol', 'daniel', 'alice', 'caio',
            'lívia', 'rafael', 'carolina', 'ricardo', 'marina', 'cuba'
        ]
        
        segment_lower = segment.lower()
        for name in character_names:
            if name in segment_lower:
                return name.title()
        
        # Se não encontrar nome específico, extrair primeira palavra relevante
        words = segment.split()
        for word in words:
            if len(word) > 3 and word.lower() not in ['que', 'com', 'para', 'essa', 'essa', 'foi', 'está', 'vai']:
                return word.title()
        
        return "Personagem"

async def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Gerador de Vídeos de Resumos de Novelas")
    parser.add_argument("topic", nargs="?", help="Tópico do resumo (ex: 'Resumo da semana de Dona de Mim')")
    parser.add_argument("--voice", "-v", help="Nome da voz (francisco, maria, etc.)")
    parser.add_argument("--no-db", action="store_true", help="Não usar banco de dados")
    parser.add_argument("--credentials", "-c", default="default", help="Nome das credenciais")
    parser.add_argument("--list-novelas", action="store_true", help="Listar novelas suportadas")
    
    args = parser.parse_args()
    
    if args.list_novelas:
        print("📺 Novelas Suportadas:")
        print("- Dona de Mim")
        print("- Fuzuê")
        print("- Vai na Fé") 
        print("- Terra e Paixão")
        print("- Amor Perfeito")
        print("- Mar do Sertão")
        print("\n💡 Exemplos de uso:")
        print("py -3 novela_video_generator.py 'Resumo da semana de Dona de Mim'")
        print("py -3 novela_video_generator.py 'Análise do personagem principal de Fuzuê'")
        print("py -3 novela_video_generator.py 'Previsões para próximos capítulos de Vai na Fé'")
        return
    
    if not args.topic:
        parser.print_help()
        return
    
    # Verificar se APIs estão configuradas
    if not os.environ.get("GROQ_API_KEY") and not os.environ.get("OPENAI_KEY"):
        print("❌ Erro: Configure pelo menos uma API de IA (GROQ_API_KEY ou OPENAI_KEY)")
        print("💡 Exemplo: export GROQ_API_KEY='sua_chave_aqui'")
        return
    
    if not os.environ.get("PEXELS_KEY"):
        print("❌ Erro: Configure a API do Pexels (PEXELS_KEY)")
        print("💡 Exemplo: export PEXELS_KEY='sua_chave_aqui'")
        return
    
    # Gerar vídeo
    generator = NovelaVideoGenerator()
    result = await generator.generate_novela_video(
        topic=args.topic,
        voice_name=args.voice,
        use_db=not args.no_db,
        credentials_name=args.credentials
    )
    
    if result and result["success"]:
        print(f"\n🎉 Vídeo gerado com sucesso!")
        print(f"📁 Arquivo: {result['video_path']}")
        print(f"📺 Novela: {result['novela_info']['novela_name']}")
        print(f"📝 Tipo: {result['novela_info']['content_type']}")
        if result['video_id']:
            print(f"🆔 ID: {result['video_id']}")
    else:
        print(f"\n❌ Erro na geração do vídeo")
        if result:
            print(f"Erro: {result.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    asyncio.run(main()) 