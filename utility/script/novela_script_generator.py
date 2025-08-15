import os
from openai import OpenAI
import json
import re
from typing import Dict, List, Optional
from utility.script.novela_scraper import NovelaScraper

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

def extract_novela_info(topic: str) -> Dict[str, str]:
    """
    Extrai informações da novela do tópico fornecido
    """
    topic_lower = topic.lower()
    
    # Mapeamento de novelas conhecidas
    novelas_map = {
        "dona de mim": "Dona de Mim",
        "fuzuê": "Fuzuê", 
        "vai na fé": "Vai na Fé",
        "terra e paixão": "Terra e Paixão",
        "amor perfeito": "Amor Perfeito",
        "mar do sertão": "Mar do Sertão"
    }
    
    # Detectar novela
    novela_name = "novela"
    for key, value in novelas_map.items():
        if key in topic_lower:
            novela_name = value
            break
    
    # Detectar tipo de conteúdo
    content_type = "resumo_semanal"
    if "capítulo" in topic_lower or "episódio" in topic_lower:
        content_type = "resumo_capitulo"
    elif "personagem" in topic_lower:
        content_type = "analise_personagem"
    elif "previsão" in topic_lower or "próximo" in topic_lower:
        content_type = "previsoes"
    elif "curiosidade" in topic_lower:
        content_type = "curiosidades"
    elif "bastidor" in topic_lower:
        content_type = "behind_scenes"
    
    return {
        "novela_name": novela_name,
        "content_type": content_type,
        "original_topic": topic
    }

def generate_novela_script(topic: str) -> str:
    """
    Gera script específico para resumos de novelas usando dados reais
    """
    if not client:
        return "Erro: Nenhuma API configurada para geração de scripts."
    
    # Extrair informações da novela
    novela_info = extract_novela_info(topic)
    
    # Buscar resumo real da novela
    scraper = NovelaScraper()
    real_resumo = scraper.get_novela_resumo(novela_info['novela_name'])
    
    # Usar resumo real se disponível
    resumo_content = ""
    if real_resumo:
        resumo_content = real_resumo['content']
        print(f"✅ Resumo real encontrado: {len(resumo_content)} caracteres")
    else:
        print("⚠️ Resumo real não encontrado, usando dados genéricos")
    
    prompt = f"""
    Você é um especialista em novelas brasileiras e criador de conteúdo para redes sociais. 
    Crie um roteiro envolvente para um vídeo de resumo de novela de 60-90 segundos (200-300 palavras).

    NOVELA: {novela_info['novela_name']}
    TIPO DE CONTEÚDO: {novela_info['content_type']}
    TÓPICO ORIGINAL: {novela_info['original_topic']}
    
    RESUMO REAL DA NOVELA:
    {resumo_content[:1000] if resumo_content else "Resumo não disponível"}

    🎬 ESTRUTURA PARA RESUMOS DE NOVELAS:

    ✅ ABERTURA (5-10 segundos):
    - Saudação envolvente: "Fala galera!", "Oi pessoal!", "E aí, novela lovers!"
    - Anúncio da novela: "Resumo da semana de {novela_info['novela_name']}"
    - Hook dramático: "Você não vai acreditar no que aconteceu!", "A semana foi de arrepiar!"

    ✅ DESENVOLVIMENTO (45-75 segundos):
    - Resumo dos principais acontecimentos da semana
    - Destaque dos personagens principais e suas ações
    - Conflitos e reviravoltas mais marcantes
    - Cenas mais emocionantes ou surpreendentes
    - Relacionamentos e dramas amorosos

    ✅ FECHAMENTO (10-15 segundos):
    - Teaser para próxima semana: "Na próxima semana promete muito mais drama!"
    - Convite para comentários: "Deixe seu comentário, qual foi sua cena favorita?"
    - Call to action: "Não perca o próximo capítulo!", "Compartilha com quem ama novela!"

    🎙️ TOM DE VOZ:
    - Envolvente e dramático
    - Linguagem jovem e acessível
    - Emoção e suspense
    - Comentários pessoais e opinativos

    📝 EXEMPLOS DE ESTRUTURA:

    Para resumo semanal:
    "Fala galera! Resumo da semana de {novela_info['novela_name']} e vocês não vão acreditar no que rolou! 
    [Desenvolvimento com principais acontecimentos, personagens e conflitos]
    Na próxima semana promete muito mais drama! Deixe seu comentário, qual foi sua cena favorita?"

    Para análise de personagem:
    "Oi pessoal! Hoje vamos falar sobre [personagem] de {novela_info['novela_name']}! 
    [Desenvolvimento com análise do personagem, suas ações e motivações]
    O que vocês acham desse personagem? Deixe seu comentário!"

    REGRAS IMPORTANTES:
    1. SEMPRE use PORTUGUÊS BRASILEIRO
    2. Mantenha o conteúdo entre 200-300 palavras (60-90 segundos)
    3. Use linguagem jovem e envolvente
    4. Inclua elementos dramáticos e suspense
    5. Evite spoilers excessivos
    6. Termine sempre com uma chamada à ação
    7. Use expressões típicas de redes sociais

    Forneça estritamente o roteiro em formato JSON como abaixo, e apenas forneça um objeto JSON analisável com a chave 'script'.

    # Saída
    {{"script": "Aqui está o roteiro completo seguindo a estrutura para resumos de novelas..."}}
    """

    try:
        if model == "llama3-70b-8192":
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1000
            )
            script_text = response.choices[0].message.content
        else:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1000
            )
            script_text = response.choices[0].message.content
        
        # Extrair JSON da resposta
        try:
            # Tentar encontrar JSON na resposta
            json_match = re.search(r'\{.*\}', script_text, re.DOTALL)
            if json_match:
                script_json = json.loads(json_match.group())
                return script_json.get('script', script_text)
            else:
                return script_text
        except json.JSONDecodeError:
            return script_text
            
    except Exception as e:
        print(f"Erro ao gerar script: {e}")
        return f"Erro na geração do script: {e}"

def generate_novela_script_with_template(topic: str, template_config: Dict) -> Dict:
    """
    Gera script de novela usando configurações de template
    """
    script = generate_novela_script(topic)
    
    return {
        "script": script,
        "template": template_config,
        "novela_info": extract_novela_info(topic)
    }

# Função para testar o gerador
def test_novela_script():
    """
    Função para testar o gerador de scripts de novela
    """
    test_topics = [
        "Resumo da semana de Dona de Mim",
        "Análise do personagem principal de Fuzuê", 
        "Previsões para próximos capítulos de Vai na Fé",
        "Curiosidades sobre Terra e Paixão"
    ]
    
    print("🎬 Testando Gerador de Scripts de Novela")
    print("=" * 50)
    
    for topic in test_topics:
        print(f"\n📺 Tópico: {topic}")
        print("-" * 30)
        script = generate_novela_script(topic)
        print(f"Script gerado: {script[:200]}...")
        print()

if __name__ == "__main__":
    test_novela_script() 