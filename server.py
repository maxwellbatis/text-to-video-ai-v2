#!/usr/bin/env python3
"""
Servidor Web para Text-to-Video AI
Gerencia criação, status e visualização de vídeos
"""

import os
import asyncio
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
import threading
import time

# Importar módulos do projeto
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals

# Importar sistema de templates
from utility.script.template_script_generator import TemplateScriptGenerator
from utility.render.template_render_engine import TemplateRenderEngine

# Importar banco de dados (opcional)
try:
    from database import VideoDatabase
    DB_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Banco de dados não disponível: {e}")
    DB_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'textoemvideos_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Inicializar sistema de templates
template_script_generator = TemplateScriptGenerator()
template_render_engine = TemplateRenderEngine()

# Armazenamento temporário de jobs (se não houver banco)
jobs = {}
completed_videos = {}

class VideoJob:
    def __init__(self, topic, user_id=None):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.user_id = user_id
        self.status = "PENDING"
        self.progress = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.video_path = None
        self.audio_path = None
        self.srt_file = None
        self.vtt_file = None
        self.duration = None
        self.error = None

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'video_path': self.video_path,
            'audio_path': self.audio_path,
            'srt_file': self.srt_file,
            'vtt_file': self.vtt_file,
            'duration': self.duration,
            'error': self.error
        }

def update_job_progress(job_id, progress, status=None):
    """Atualiza progresso do job e notifica via WebSocket"""
    if job_id in jobs:
        jobs[job_id].progress = progress
        if status:
            jobs[job_id].status = status
        jobs[job_id].updated_at = datetime.now()
        
        # Emitir atualização via WebSocket
        socketio.emit('job_update', {
            'job_id': job_id,
            'progress': progress,
            'status': jobs[job_id].status
        })

async def generate_video_async(job_id, topic, template_id=None, voice_id=None, use_db=False, duration_minutes=1, background_music=None):
    """Gera vídeo de forma assíncrona com suporte a templates e duração personalizada"""
    try:
        job = jobs[job_id]
        update_job_progress(job_id, 10, "PROCESSING")
        
        # Verificar se as variáveis de ambiente estão configuradas
        if not os.environ.get("GROQ_API_KEY"):
            raise Exception("GROQ_API_KEY não configurada. Configure a variável de ambiente.")
        if not os.environ.get("PEXELS_KEY"):
            raise Exception("PEXELS_KEY não configurada. Configure a variável de ambiente.")
        
        # 1. Gerar script (com template se especificado)
        update_job_progress(job_id, 20)
        if template_id:
            script_data = template_script_generator.generate_script_for_template(topic, template_id, duration_minutes)
            response = script_data['script']
            template_config = script_data['template']
            print(f"Script gerado com template '{template_id}' ({duration_minutes} min): {response[:100]}...")
        else:
            response = generate_script(topic, duration_minutes)
            template_config = None
            print(f"Script gerado ({duration_minutes} min): {response[:100]}...")
        
        # 2. Gerar áudio
        update_job_progress(job_id, 40)
        audio_file = f"audio_tts_{job_id}.wav"
        await generate_audio(response, audio_file, voice_id)  # Usar voz selecionada ou detectar automaticamente
        job.audio_path = audio_file
        print(f"Áudio gerado: {audio_file}")
        
        # 3. Gerar legendas e arquivos SRT/VTT
        update_job_progress(job_id, 60)
        from utility.captions.timed_captions_generator import generate_subtitle_files
        
        subtitle_data = generate_subtitle_files(audio_file)
        timed_captions = subtitle_data['captions_pairs']
        job.srt_file = subtitle_data['srt_file']
        job.vtt_file = subtitle_data['vtt_file']
        print(f"Legendas geradas: {len(timed_captions)} segmentos")
        print(f"Arquivos SRT/VTT: {job.srt_file}, {job.vtt_file}")
        
        # 4. Gerar termos de busca
        update_job_progress(job_id, 70)
        search_terms = getVideoSearchQueriesTimed(response, timed_captions)
        print(f"Termos de busca gerados: {len(search_terms) if search_terms else 0}")
        
        # 5. Gerar vídeos de fundo
        update_job_progress(job_id, 80)
        background_video_urls = None
        if search_terms:
            background_video_urls = generate_video_url(search_terms, "pexel")
            background_video_urls = merge_empty_intervals(background_video_urls)
        print(f"Vídeos de fundo: {len(background_video_urls) if background_video_urls else 0}")
        
        # 6. Renderizar vídeo final
        update_job_progress(job_id, 90)
        if background_video_urls:
            # Usar renderização normal com legendas
            output_video = get_output_media(audio_file, timed_captions, background_video_urls, "pexel", template_id)
            
            # 6.5. Aplicar template se especificado
            if template_id and template_config:
                update_job_progress(job_id, 95)
                # Adicionar música de fundo ao template config se especificada
                if background_music:
                    template_config['background_music'] = background_music
                    print(f"🎵 Música de fundo adicionada ao template: {background_music}")
                
                output_video = template_render_engine.apply_template_to_video(output_video, template_config, audio_file)
                print(f"Template '{template_id}' aplicado ao vídeo")
            
            job.video_path = output_video
            job.status = "COMPLETED"
            job.duration = 47.0  # Aproximado
            print(f"Vídeo renderizado: {output_video}")
            
            # Mover para completed_videos
            completed_videos[job_id] = job.to_dict()
            
            update_job_progress(job_id, 100, "COMPLETED")
            socketio.emit('job_completed', {'job_id': job_id, 'video_path': output_video})
        else:
            raise Exception("Não foi possível gerar vídeos de fundo")
            
    except Exception as e:
        print(f"❌ Erro na geração do vídeo: {e}")
        job.status = "FAILED"
        job.error = str(e)
        update_job_progress(job_id, 0, "FAILED")
        socketio.emit('job_failed', {'job_id': job_id, 'error': str(e)})

def run_async_generation(job_id, topic, template_id=None, voice_id=None, use_db=False, duration_minutes=1, background_music=None):
    """Executa geração de vídeo em thread separada"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(generate_video_async(job_id, topic, template_id, voice_id, use_db, duration_minutes, background_music))
    finally:
        loop.close()

# Rotas da aplicação

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """Lista todos os jobs"""
    all_jobs = {**jobs, **completed_videos}
    
    # Se o banco de dados estiver disponível, carregar vídeos do banco
    if DB_AVAILABLE:
        try:
            async def load_db_videos():
                db = VideoDatabase()
                await db.connect()
                db_videos = await db.list_videos()
                await db.disconnect()
                return db_videos
            
            # Executar em thread separada para não bloquear
            def run_async_load():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    db_videos = loop.run_until_complete(load_db_videos())
                    for video in db_videos:
                        # Converter vídeo do banco para formato compatível
                        video_dict = {
                            'id': str(video['id']),
                            'topic': video['topic'],
                            'status': video['status'],
                            'progress': 100 if video['status'] == 'COMPLETED' else 0,
                            'created_at': video['created_at'].isoformat() if video['created_at'] else datetime.now().isoformat(),
                            'updated_at': video['updated_at'].isoformat() if video['updated_at'] else datetime.now().isoformat(),
                            'video_path': video['video_path'],
                            'audio_path': video['audio_path'],
                            'duration': video['duration'],
                            'error': None
                        }
                        all_jobs[str(video['id'])] = video_dict
                except Exception as e:
                    print(f"Erro ao carregar vídeos do banco: {e}")
                finally:
                    loop.close()
            
            # Executar em thread separada
            import threading
            thread = threading.Thread(target=run_async_load)
            thread.daemon = True
            thread.start()
            thread.join(timeout=5)  # Aguardar máximo 5 segundos
            
        except Exception as e:
            print(f"Erro ao carregar banco de dados: {e}")
    
    return jsonify({
        'jobs': [job.to_dict() if hasattr(job, 'to_dict') else job for job in all_jobs.values()]
    })

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Cria um novo job de geração de vídeo"""
    data = request.get_json()
    topic = data.get('topic', '').strip()
    template_id = data.get('template_id', '').strip() or None
    voice_id = data.get('voice_id', '').strip() or None
    background_music = data.get('background_music', '').strip() or None
    
    if not topic:
        return jsonify({'error': 'Tópico é obrigatório'}), 400
    
    # Criar novo job
    job = VideoJob(topic)
    jobs[job.id] = job
    
    # Obter duração (padrão: 1 minuto)
    duration_minutes = int(data.get('duration_minutes', 1))
    if duration_minutes < 1 or duration_minutes > 10:
        duration_minutes = 1
    
    # Iniciar geração em thread separada
    thread = threading.Thread(
        target=run_async_generation,
        args=(job.id, topic, template_id, voice_id, DB_AVAILABLE, duration_minutes, background_music)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job.id,
        'message': 'Job criado com sucesso',
        'status': job.status,
        'template_id': template_id,
        'background_music': background_music
    }), 201

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """Obtém status de um job específico"""
    all_jobs = {**jobs, **completed_videos}
    
    if job_id not in all_jobs:
        return jsonify({'error': 'Job não encontrado'}), 404
    
    job = all_jobs[job_id]
    return jsonify(job.to_dict() if hasattr(job, 'to_dict') else job)

@app.route('/api/videos/<job_id>', methods=['GET'])
def download_video(job_id):
    """Download do vídeo gerado"""
    if job_id not in completed_videos:
        return jsonify({'error': 'Vídeo não encontrado'}), 404
    
    video_data = completed_videos[job_id]
    video_path = video_data.get('video_path')
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Arquivo de vídeo não encontrado'}), 404
    
    return send_file(video_path, as_attachment=True)

@app.route('/api/videos/<job_id>/srt', methods=['GET'])
def download_srt(job_id):
    """Download do arquivo SRT"""
    if job_id not in completed_videos:
        return jsonify({'error': 'Vídeo não encontrado'}), 404
    
    video_data = completed_videos[job_id]
    srt_path = video_data.get('srt_file')
    
    if not srt_path or not os.path.exists(srt_path):
        return jsonify({'error': 'Arquivo SRT não encontrado'}), 404
    
    return send_file(srt_path, as_attachment=True, download_name=f"legendas_{job_id}.srt")

@app.route('/api/videos/<job_id>/vtt', methods=['GET'])
def download_vtt(job_id):
    """Download do arquivo VTT"""
    if job_id not in completed_videos:
        return jsonify({'error': 'Vídeo não encontrado'}), 404
    
    video_data = completed_videos[job_id]
    vtt_path = video_data.get('vtt_file')
    
    if not vtt_path or not os.path.exists(vtt_path):
        return jsonify({'error': 'Arquivo VTT não encontrado'}), 404
    
    return send_file(vtt_path, as_attachment=True, download_name=f"legendas_{job_id}.vtt")

@app.route('/gallery')
def gallery():
    """Página da galeria de vídeos"""
    return render_template('gallery.html', videos=completed_videos)

@app.route('/status/<job_id>')
def status_page(job_id):
    """Página de status de um job específico"""
    return render_template('status.html', job_id=job_id)

@app.route('/api/templates/suggest', methods=['POST'])
def suggest_templates():
    """Sugere templates apropriados para um tópico"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'error': 'Tópico é obrigatório'}), 400
        
        suggestions = template_script_generator.get_template_suggestions(topic)
        return jsonify(suggestions)
        
    except Exception as e:
        print(f"Erro ao sugerir templates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voices', methods=['GET'])
def list_voices():
    """Lista todas as vozes disponíveis"""
    try:
        from utility.audio.audio_generator import list_available_voices
        voices_info = list_available_voices()
        return jsonify(voices_info)
    except Exception as e:
        print(f"Erro ao listar vozes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Chat com IA para sugestões de tópicos"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Mensagem é obrigatória'}), 400
        
        # Verificar se GROQ_API_KEY está configurada
        if not os.environ.get("GROQ_API_KEY"):
            return jsonify({'error': 'GROQ_API_KEY não configurada'}), 500
        
        # Gerar resposta usando Groq
        import groq
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Prompt para sugestões de tópicos
        prompt = f"""
        Você é um assistente especializado em criar conteúdo para vídeos curtos (Shorts/Reels).
        
        O usuário disse: "{message}"
        
        Forneça sugestões criativas e interessantes de tópicos para vídeos. 
        Foque em:
        - Fatos curiosos e interessantes
        - História e cultura
        - Ciência e tecnologia
        - Lugares e viagens
        - Pessoas famosas e suas histórias
        - Descobertas e invenções
        
        Responda de forma amigável e entusiasmada, sugerindo 3-5 tópicos específicos.
        Use emojis para tornar a resposta mais atrativa.
        """
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Você é um assistente criativo especializado em sugestões de conteúdo para vídeos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Erro no chat: {e}")
        return jsonify({
            'error': 'Erro ao processar mensagem',
            'details': str(e)
        }), 500

# WebSocket events

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

@socketio.on('subscribe_job')
def handle_subscribe_job(data):
    """Inscreve cliente para atualizações de um job"""
    job_id = data.get('job_id')
    if job_id in jobs:
        emit('job_update', jobs[job_id].to_dict())

if __name__ == '__main__':
    print("🚀 Iniciando servidor Text-to-Video AI...")
    print("📱 Interface web disponível em: http://localhost:5000")
    print("🎬 API disponível em: http://localhost:5000/api")
    
    # Configuração para produção - desabilitar debug e usar configurações mais seguras
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True) 