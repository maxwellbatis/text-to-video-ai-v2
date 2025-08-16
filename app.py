from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.script.script_generator import generate_script, generate_prayer_script
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

async def generate_video_with_db(topic: str, credentials_name: str = "default", use_db: bool = True, template_id: str = None, voice_name: str = None, duration_minutes: int = 1):
    """Gera vídeo e salva no banco de dados com suporte a templates e duração personalizada"""
    
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
                    title=f"Vídeo sobre {topic} ({duration_minutes}min)",
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
            print(f"🎬 Usando template: {template_id} ({duration_minutes} minuto(s))")
            script_data = template_script_generator.generate_script_for_template(topic, template_id, duration_minutes)
            response = script_data['script']
            template_config = script_data['template']
            print(f"Script gerado com template '{template_id}': {response[:100]}...")
        else:
            response = generate_script(topic, duration_minutes)
            template_config = None
            print(f"Script gerado ({duration_minutes} minuto(s)): {response[:100]}...")
        
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
        
        # Renderizar vídeo final
        output_filename = f"output_video_{video_id}.mp4" if video_id else "output_video.mp4"
        get_output_media(SAMPLE_FILE_NAME, background_video_urls, timed_captions, output_filename)
        
        # Atualizar banco de dados
        if use_db and video_id:
            await db.update_video_status(video_id, "COMPLETED")
            await db.update_video_output_path(video_id, output_filename)
            print(f"✅ Vídeo salvo no banco: {video_id}")
        
        print(f"✅ Vídeo gerado com sucesso: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"❌ Erro ao gerar vídeo: {e}")
        if use_db and video_id:
            await db.update_video_status(video_id, "ERROR")
        raise e
    finally:
        if db:
            await db.close()

def main():
    parser = argparse.ArgumentParser(description='Gerador de Vídeos com IA - Suporte a Templates e Vozes')
    parser.add_argument('topic', nargs='?', help='Tópico do vídeo')
    parser.add_argument('--credentials', '-c', default='default', help='Nome das credenciais (padrão: default)')
    parser.add_argument('--no-db', action='store_true', help='Não usar banco de dados')
    parser.add_argument('--template', '-t', help='ID do template a usar')
    parser.add_argument('--voice', '-v', help='Nome da voz (james, bill, neil, drew, phillip, deep_ray)')
    parser.add_argument('--duration', '-d', type=int, default=1, help='Duração em minutos (1-10, padrão: 1)')
    parser.add_argument('--list-voices', action='store_true', help='Listar vozes disponíveis')
    parser.add_argument('--list-templates', action='store_true', help='Listar templates disponíveis')
    parser.add_argument('--prayer', action='store_true', help='Gerar oração específica')
    
    args = parser.parse_args()
    
    # Validar duração
    if args.duration < 1 or args.duration > 10:
        print("❌ Duração deve estar entre 1 e 10 minutos")
        return
    
    # Listar vozes disponíveis
    if args.list_voices:
        from utility.audio.audio_generator import list_available_voices
        voices_info = list_available_voices()
        print("\n🎤 Vozes Disponíveis:")
        print("=" * 50)
        
        for category, voices in voices_info['recommendations'].items():
            print(f"\n📚 {category}:")
            for voice_id in voices:
                voice_info = voices_info['voices'][voice_id]
                print(f"  • {voice_id}: {voice_info['description']}")
        
        print(f"\n🔄 Fallback: Edge TTS (pt-BR-AntonioNeural)")
        return
    
    # Listar templates disponíveis
    if args.list_templates:
        from utility.templates.template_manager import TemplateManager
        tm = TemplateManager()
        templates = tm.list_templates()
        
        print("\n🎬 Templates Disponíveis:")
        print("=" * 50)
        
        for template_id, template_info in templates.items():
            print(f"\n📋 {template_id}:")
            print(f"  Nome: {template_info['name']}")
            print(f"  Descrição: {template_info['description']}")
            print(f"  Categoria: {template_info['category']}")
        
        return
    
    # Verificar se tópico foi fornecido
    if not args.topic:
        print("❌ Tópico é obrigatório!")
        print("\n📖 Exemplos de uso:")
        print("  python app.py 'Oração pela família' --prayer --duration 3")
        print("  python app.py 'Estudo sobre fé' --template prayer_extended --duration 5")
        print("  python app.py 'Fatos curiosos' --voice james --duration 2")
        print("  python app.py --list-voices")
        print("  python app.py --list-templates")
        return
    
    # Configurar template padrão para orações
    if args.prayer and not args.template:
        args.template = "prayer_extended"
        print("🙏 Usando template de oração por padrão")
    
    # Executar geração
    try:
        asyncio.run(generate_video_with_db(
            topic=args.topic,
            credentials_name=args.credentials,
            use_db=not args.no_db,
            template_id=args.template,
            voice_name=args.voice,
            duration_minutes=args.duration
        ))
    except KeyboardInterrupt:
        print("\n⚠️ Geração interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()