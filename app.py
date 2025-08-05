from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals

# Importar sistema de templates
from utility.script.template_script_generator import TemplateScriptGenerator
from utility.render.template_render_engine import TemplateRenderEngine

import argparse

# Importar banco de dados apenas quando necessário
try:
    from database import VideoDatabase
    DB_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Banco de dados não disponível: {e}")
    DB_AVAILABLE = False

# Inicializar sistema de templates
template_script_generator = TemplateScriptGenerator()
template_render_engine = TemplateRenderEngine()

async def generate_video_with_db(topic: str, credentials_name: str = "default", use_db: bool = True, template_id: str = None, voice_name: str = None):
    """Gera vídeo e salva no banco de dados com suporte a templates"""
    
    db = None
    video_id = None
    
    if use_db and DB_AVAILABLE:
        # Conectar ao banco
        db = VideoDatabase()
        await db.connect()
        
        try:
            # Buscar credenciais
            credentials = await db.get_credentials(credentials_name)
            if not credentials:
                print(f"Credenciais '{credentials_name}' não encontradas! Usando variáveis de ambiente.")
            else:
                # Configurar variáveis de ambiente
                if credentials.openaiKey:
                    os.environ['OPENAI_KEY'] = credentials.openaiKey
                if credentials.groqKey:
                    os.environ['GROQ_API_KEY'] = credentials.groqKey
                if credentials.pexelsKey:
                    os.environ['PEXELS_KEY'] = credentials.pexelsKey
                
                # Criar registro de vídeo
                video = await db.create_video(
                    title=f"Vídeo sobre {topic}",
                    topic=topic,
                    script="",  # Será atualizado depois
                    credentials_id=credentials.id
                )
                video_id = video.id
                print(f"Vídeo criado no banco: {video_id}")
                
                # Atualizar status para PROCESSING
                await db.update_video_status(video_id, "PROCESSING")
        except Exception as e:
            print(f"⚠️ Erro ao conectar com banco: {e}. Continuando sem banco...")
            use_db = False
    
    try:
        # Gerar script (com template se especificado)
        if template_id:
            print(f"🎬 Usando template: {template_id}")
            script_data = template_script_generator.generate_script_for_template(topic, template_id)
            response = script_data['script']
            template_config = script_data['template']
            print(f"Script gerado com template '{template_id}': {response[:100]}...")
        else:
            response = generate_script(topic)
            template_config = None
            print(f"Script gerado: {response[:100]}...")
        
        # Atualizar script no banco se estiver usando
        if use_db and video_id:
            await db.update_video_status(video_id, "PROCESSING")
        
        # Gerar áudio
        SAMPLE_FILE_NAME = f"audio_tts_{video_id}.wav" if video_id else "audio_tts.wav"
        await generate_audio(response, SAMPLE_FILE_NAME, voice_name)
        
        # Aplicar pausas estratégicas se template especificado
        if template_id and template_config:
            print("⏱️ Aplicando pausas estratégicas...")
            pauses_config = template_config.get('script_pattern', {}).get('pauses_strategy', {})
            if pauses_config:
                SAMPLE_FILE_NAME = template_render_engine.apply_strategic_pauses(SAMPLE_FILE_NAME, pauses_config)
                print(f"Pausas estratégicas aplicadas ao áudio")
        
        # Gerar legendas
        timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
        print(timed_captions)
        
        # Gerar termos de busca
        search_terms = getVideoSearchQueriesTimed(response, timed_captions)
        print(search_terms)
        
        # Gerar vídeos de fundo
        VIDEO_SERVER = "pexel"
        background_video_urls = None
        if search_terms is not None:
            background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
            print(background_video_urls)
        else:
            print("No background video")
        
        background_video_urls = merge_empty_intervals(background_video_urls)
        
        # Renderizar vídeo final
        if background_video_urls is not None:
            output_video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
            
            # Aplicar template se especificado
            if template_id and template_config:
                print(f"🎨 Aplicando template '{template_id}' ao vídeo...")
                output_video = template_render_engine.apply_template_to_video(output_video, template_config, SAMPLE_FILE_NAME)
                print(f"Template aplicado com sucesso!")
            
            print(f"Vídeo renderizado: {output_video}")
            
            # Atualizar banco com caminhos dos arquivos
            if use_db and video_id:
                await db.update_video_status(
                    video_id=video_id,
                    status="COMPLETED",
                    audio_path=SAMPLE_FILE_NAME,
                    video_path=output_video,
                    duration=42.5  # Você pode calcular a duração real
                )
                print(f"✅ Vídeo '{topic}' gerado com sucesso!")
                print(f"📁 Arquivo: {output_video}")
                print(f"🆔 ID no banco: {video_id}")
                if template_id:
                    print(f"🎬 Template usado: {template_id}")
            else:
                print(f"✅ Vídeo '{topic}' gerado com sucesso!")
                print(f"📁 Arquivo: {output_video}")
                if template_id:
                    print(f"🎬 Template usado: {template_id}")
            
        else:
            if use_db and video_id:
                await db.update_video_status(video_id, "FAILED")
            print("❌ Falha ao gerar vídeo")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        if use_db and video_id:
            await db.update_video_status(video_id, "FAILED")
    
    finally:
        if db:
            await db.disconnect()

def suggest_templates_for_topic(topic: str):
    """Sugere templates apropriados para um tópico"""
    try:
        suggestions = template_script_generator.get_template_suggestions(topic)
        print(f"\n🎯 Sugestões de templates para '{topic}':")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion['name']} (Score: {suggestion['score']})")
            print(f"     ID: {suggestion['template_id']}")
            print(f"     Descrição: {suggestion['description']}")
            for reason in suggestion['reasons']:
                print(f"     - {reason}")
            print()
        return suggestions
    except Exception as e:
        print(f"❌ Erro ao sugerir templates: {e}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from a topic.")
    parser.add_argument("topic", type=str, nargs='?', help="The topic for the video")
    parser.add_argument("--credentials", type=str, default="default", help="Credentials name to use")
    parser.add_argument("--no-db", action="store_true", help="Disable database integration")
    parser.add_argument("--template", type=str, help="Template ID to use for video generation")
    parser.add_argument("--voice", type=str, help="Voice to use (james, bill, neil, drew, phillip, deep_ray)")
    parser.add_argument("--suggest-templates", action="store_true", help="Suggest templates for the topic")
    parser.add_argument("--list-voices", action="store_true", help="List available voices and their descriptions")

    args = parser.parse_args()
    
    # Se solicitado, apenas listar vozes
    if args.list_voices:
        from utility.audio.audio_generator import list_available_voices
        voices_info = list_available_voices()
        print("\n🎤 VOZES DISPONÍVEIS NO ELEVENLABS:")
        print("=" * 50)
        
        for voice_name, voice_data in voices_info["voices"].items():
            print(f"\n🎵 {voice_name.upper()}")
            print(f"   📝 {voice_data['description']}")
            print(f"   🏷️  Categoria: {voice_data['category']}")
        
        print("\n📊 RECOMENDAÇÕES POR TIPO DE CONTEÚDO:")
        print("=" * 50)
        for content_type, voices in voices_info["recommendations"].items():
            print(f"\n📖 {content_type}:")
            for voice in voices:
                voice_data = voices_info["voices"][voice]
                print(f"   • {voice}: {voice_data['description']}")
        
        print("\n💡 USO:")
        print("   python app.py 'seu tópico' --voice james")
        print("   python app.py 'seu tópico' --voice phillip")
        exit(0)
    
    # Se solicitado, apenas sugerir templates
    if args.suggest_templates:
        suggest_templates_for_topic(args.topic)
        exit(0)
    
    # Verificar se tópico foi fornecido (exceto para list-voices)
    if not args.topic and not args.list_voices and not args.suggest_templates:
        print("❌ Erro: Tópico é obrigatório para gerar vídeo")
        print("💡 Use: python app.py 'seu tópico'")
        print("💡 Ou: python app.py --list-voices")
        exit(1)
    
    if args.topic:
        use_db = not args.no_db and DB_AVAILABLE
        asyncio.run(generate_video_with_db(args.topic, args.credentials, use_db, args.template, args.voice))