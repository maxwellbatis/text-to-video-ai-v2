import os
from openai import OpenAI
import json

# Carregar variáveis de ambiente do arquivo .env
def load_env():
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env()

client = None
model = None

# Verificar se GROQ_API_KEY está disponível e tem tamanho adequado
groq_key = os.environ.get("GROQ_API_KEY")
if groq_key and len(groq_key) > 30:
    try:
        from groq import Groq
        model = "llama3-70b-8192"
        client = Groq(api_key=groq_key)
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Groq: {e}")
        client = None
elif os.environ.get("OPENAI_KEY"):
    try:
        model = "gpt-4o"
        client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))
    except Exception as e:
        print(f"⚠️ Erro ao inicializar OpenAI: {e}")
        client = None
else:
    print("⚠️ Nenhuma API key configurada")
    client = None

def generate_script(topic):
    prompt = (
        """Você é um escritor experiente especializado em criar roteiros para vídeos de 60-90 segundos (aproximadamente 200-300 palavras) com estrutura profissional e narrativa envolvente.

        IMPORTANTE: Sempre responda em PORTUGUÊS BRASILEIRO.

        🎬 ESTRUTURA PROFISSIONAL PARA VÍDEOS:

        ✅ ABERTURA (5-15 segundos):
        - Saudação calorosa e acolhedora
        - Frase impactante, pergunta intrigante ou citação relevante
        - Exemplo: "A paz do Senhor! Você já se perguntou por que Deus permite o sofrimento?"

        ✅ DESENVOLVIMENTO (40-70 segundos):
        - Apresentação do tema principal com clareza
        - Fatos interessantes, curiosidades ou explicações
        - Exemplos práticos da vida cotidiana
        - Reflexões profundas ou insights valiosos
        - Pausas estratégicas para reflexão

        ✅ FECHAMENTO (10-15 segundos):
        - Conclusão com ensinamento ou chamada à ação
        - Convite à interação: "Deixe seu comentário, compartilhe com alguém que precisa ouvir isso"
        - Mensagem inspiradora ou motivacional

        🎙️ TOM DE VOZ E ESTILO:
        - Para conteúdo espiritual: Solene, pausado, com reverência e empatia
        - Para curiosidades: Acolhedor, leve, conversacional e envolvente
        - Para reflexões: Calmo, filosófico, contemplativo
        - Para chamadas à ação: Inspirador, encorajador, com emoção

        📝 EXEMPLOS DE ESTRUTURA:

        Para conteúdo espiritual:
        "A paz do Senhor! Você já se perguntou por que Deus permite o sofrimento? 
        [Desenvolvimento com 3-4 pontos principais, exemplos práticos, reflexões]
        Lembre-se: Deus não prometeu uma vida sem problemas, mas prometeu estar conosco em todos os momentos. 
        Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"

        Para curiosidades:
        "Você sabia que [curiosidade impactante]? 
        [Desenvolvimento com 4-5 fatos interessantes, explicações, exemplos]
        O mundo está cheio de surpresas incríveis! 
        Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"

        REGRAS IMPORTANTES:
        1. SEMPRE use PORTUGUÊS BRASILEIRO
        2. Mantenha o conteúdo entre 200-300 palavras (60-90 segundos)
        3. Inclua pausas estratégicas para reflexão
        4. Use linguagem acessível mas respeitosa
        5. Crie conexão emocional com o espectador
        6. Termine sempre com uma chamada à ação positiva

        Forneça estritamente o roteiro em formato JSON como abaixo, e apenas forneça um objeto JSON analisável com a chave 'script'.

        # Saída
        {"script": "Aqui está o roteiro completo seguindo a estrutura profissional..."}
        """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        # Limpar caracteres de controle e quebras de linha
        content = content.replace('\n', ' ').replace('\r', ' ')
        # Remover aspas duplas extras que podem causar problemas
        content = content.replace('""', '"')
        script = json.loads(content)["script"]
    except Exception as e:
        # Tentar extrair JSON da resposta
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        if json_start_index != -1 and json_end_index != -1:
            content = content[json_start_index:json_end_index+1]
            content = content.replace('\n', ' ').replace('\r', ' ')
            content = content.replace('""', '"')
            try:
                script = json.loads(content)["script"]
            except:
                # Se ainda falhar, retornar o conteúdo limpo
                script = content.replace('{"script": "', '').replace('"}', '')
        else:
            # Se não encontrar JSON, retornar o conteúdo como está
            script = content
    return script
