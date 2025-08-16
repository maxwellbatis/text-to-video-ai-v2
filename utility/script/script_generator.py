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

def generate_script(topic, duration_minutes=1):
    """
    Gera script para vídeos de 1-10 minutos
    duration_minutes: duração desejada em minutos (1-10)
    """
    
    # Calcular palavras baseado na duração (aproximadamente 150 palavras por minuto)
    target_words = int(duration_minutes * 150)
    
    # Determinar estrutura baseada na duração
    if duration_minutes <= 2:
        structure_type = "short"
        opening_duration = "10-20 segundos"
        development_duration = f"{int((duration_minutes * 60) - 30)} segundos"
        closing_duration = "10-15 segundos"
    elif duration_minutes <= 5:
        structure_type = "medium"
        opening_duration = "15-30 segundos"
        development_duration = f"{int((duration_minutes * 60) - 45)} segundos"
        closing_duration = "15-20 segundos"
    else:
        structure_type = "long"
        opening_duration = "20-40 segundos"
        development_duration = f"{int((duration_minutes * 60) - 60)} segundos"
        closing_duration = "20-30 segundos"

    prompt = (
        f"""Você é um escritor experiente especializado em criar roteiros para vídeos de {duration_minutes} minuto(s) (aproximadamente {target_words} palavras) com estrutura profissional e narrativa envolvente.

        IMPORTANTE: Sempre responda em PORTUGUÊS BRASILEIRO.

        🎬 ESTRUTURA PROFISSIONAL PARA VÍDEOS DE {duration_minutes} MINUTO(S):

        ✅ ABERTURA ({opening_duration}):
        - Saudação calorosa e acolhedora
        - Frase impactante, pergunta intrigante ou citação relevante
        - Contextualização do tema principal
        - Exemplo: "A paz do Senhor! Hoje vamos refletir sobre {topic}. Você já se perguntou..."

        ✅ DESENVOLVIMENTO ({development_duration}):
        - Apresentação do tema principal com clareza
        - Múltiplos pontos de desenvolvimento (3-7 pontos principais)
        - Exemplos práticos da vida cotidiana
        - Reflexões profundas ou insights valiosos
        - Pausas estratégicas para reflexão
        - Transições suaves entre os tópicos
        - Para orações: momentos de silêncio e contemplação

        ✅ FECHAMENTO ({closing_duration}):
        - Resumo dos pontos principais
        - Conclusão com ensinamento ou chamada à ação
        - Convite à interação: "Deixe seu comentário, compartilhe com alguém que precisa ouvir isso"
        - Mensagem inspiradora ou motivacional
        - Para orações: momento final de gratidão e bênção

        🎙️ TOM DE VOZ E ESTILO:
        - Para conteúdo espiritual: Solene, pausado, com reverência e empatia
        - Para orações: Calmo, contemplativo, com momentos de silêncio
        - Para curiosidades: Acolhedor, leve, conversacional e envolvente
        - Para reflexões: Calmo, filosófico, contemplativo
        - Para chamadas à ação: Inspirador, encorajador, com emoção

        📝 EXEMPLOS DE ESTRUTURA:

        Para oração de {duration_minutes} minuto(s):
        "A paz do Senhor! Vamos juntos neste momento de oração e reflexão sobre {topic}.
        [Desenvolvimento com múltiplos pontos, momentos de silêncio, versículos bíblicos]
        Senhor, agradecemos por este momento. Que Sua paz esteja conosco. Amém.
        Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"

        Para estudo bíblico de {duration_minutes} minuto(s):
        "A paz do Senhor! Hoje vamos estudar juntos sobre {topic}.
        [Desenvolvimento com versículos, explicações, aplicações práticas]
        Que este estudo abençoe sua vida e fortaleça sua fé.
        Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"

        Para curiosidades de {duration_minutes} minuto(s):
        "Você sabia que [curiosidade impactante]? 
        [Desenvolvimento com múltiplos fatos, explicações detalhadas, exemplos]
        O mundo está cheio de surpresas incríveis! 
        Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"

        REGRAS IMPORTANTES:
        1. SEMPRE use PORTUGUÊS BRASILEIRO
        2. Mantenha o conteúdo em aproximadamente {target_words} palavras ({duration_minutes} minuto(s))
        3. Inclua pausas estratégicas para reflexão (marcadas com [...])
        4. Use linguagem acessível mas respeitosa
        5. Crie conexão emocional com o espectador
        6. Termine sempre com uma chamada à ação positiva
        7. Para orações: inclua momentos de silêncio e contemplação
        8. Para estudos longos: divida em seções claras com transições

        Forneça estritamente o roteiro em formato JSON como abaixo, e apenas forneça um objeto JSON analisável com a chave 'script'.

        # Saída
        {{"script": "Aqui está o roteiro completo seguindo a estrutura profissional..."}}
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

def generate_prayer_script(topic, duration_minutes=3):
    """
    Gera script específico para orações
    """
    target_words = int(duration_minutes * 120)  # Menos palavras para orações (mais pausas)
    
    prompt = (
        f"""Você é um escritor especializado em criar roteiros para orações de {duration_minutes} minuto(s) (aproximadamente {target_words} palavras).

        IMPORTANTE: Sempre responda em PORTUGUÊS BRASILEIRO.

        🙏 ESTRUTURA PARA ORAÇÃO DE {duration_minutes} MINUTO(S):

        ✅ ABERTURA (10-20 segundos):
        - Saudação espiritual: "A paz do Senhor! Vamos juntos neste momento de oração"
        - Contextualização do tema da oração
        - Preparação do coração para o momento espiritual

        ✅ DESENVOLVIMENTO ({int((duration_minutes * 60) - 40)} segundos):
        - Oração de adoração e gratidão
        - Oração específica sobre o tema
        - Momentos de silêncio e contemplação (marcados com [...])
        - Versículos bíblicos relevantes
        - Oração de intercessão
        - Oração de petição pessoal

        ✅ FECHAMENTO (10-20 segundos):
        - Oração de gratidão
        - Bênção final
        - "Amém"
        - Convite à interação

        🎙️ CARACTERÍSTICAS ESPECÍFICAS PARA ORAÇÕES:
        - Tom solene e reverente
        - Pausas frequentes para contemplação
        - Linguagem espiritual e bíblica
        - Momentos de silêncio marcados com [...]
        - Estrutura de oração tradicional (adoração, confissão, gratidão, petição)

        📝 EXEMPLO DE ESTRUTURA:

        "A paz do Senhor! Vamos juntos neste momento de oração sobre {topic}.
        
        Senhor, nós Te adoramos e Te louvamos por quem Tu és. [...]
        
        Pai, hoje queremos orar especificamente sobre {topic}. [...]
        
        [Versículo bíblico relevante]
        
        Senhor, Te pedimos que [petição específica]. [...]
        
        Agradecemos por este momento, Senhor. Que Sua paz esteja conosco. Amém.
        
        Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!"

        REGRAS IMPORTANTES:
        1. SEMPRE use PORTUGUÊS BRASILEIRO
        2. Mantenha o conteúdo em aproximadamente {target_words} palavras
        3. Inclua momentos de silêncio marcados com [...]
        4. Use linguagem espiritual e reverente
        5. Estrutura tradicional de oração
        6. Termine com "Amém" e chamada à ação

        Forneça estritamente o roteiro em formato JSON como abaixo, e apenas forneça um objeto JSON analisável com a chave 'script'.

        # Saída
        {{"script": "Aqui está o roteiro de oração completo..."}}
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
        content = content.replace('\n', ' ').replace('\r', ' ')
        content = content.replace('""', '"')
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        if json_start_index != -1 and json_end_index != -1:
            content = content[json_start_index:json_end_index+1]
            content = content.replace('\n', ' ').replace('\r', ' ')
            content = content.replace('""', '"')
            try:
                script = json.loads(content)["script"]
            except:
                script = content.replace('{"script": "', '').replace('"}', '')
        else:
            script = content
    return script
