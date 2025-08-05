from openai import OpenAI
import os
import json
import re
from datetime import datetime
from utility.utils import log_response,LOG_TYPE_GPT

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

log_directory = ".logs/gpt_logs"

prompt = """# Instructions

Given the following video script and timed captions, extract three visually concrete and specific keywords for each time segment that can be used to search for background videos. The keywords should be short and capture the main essence of the sentence. They can be synonyms or related terms. If a caption is vague or general, consider the next timed caption for more context. If a keyword is a single word, try to return a two-word keyword that is visually concrete. If a time frame contains two or more important pieces of information, divide it into shorter time frames with one keyword each. Ensure that the time periods are strictly consecutive and cover the entire length of the video. Each keyword should cover between 2-4 seconds. The output should be in JSON format, like this: [[[t1, t2], ["keyword1", "keyword2", "keyword3"]], [[t2, t3], ["keyword4", "keyword5", "keyword6"]], ...]. Please handle all edge cases, such as overlapping time segments, vague or general captions, and single-word keywords.

For example, if the caption is 'The cheetah is the fastest land animal, capable of running at speeds up to 75 mph', the keywords should include 'cheetah running', 'fastest animal', and '75 mph'. Similarly, for 'The Great Wall of China is one of the most iconic landmarks in the world', the keywords should be 'Great Wall of China', 'iconic landmark', and 'China landmark'.

Important Guidelines:

Use only English in your text queries.
Each search string must depict something visual.
The depictions have to be extremely visually concrete, like rainy street, or cat sleeping.
'emotional moment' <= BAD, because it doesn't depict something visually.
'crying child' <= GOOD, because it depicts something visual.
The list must always contain the most relevant and appropriate query searches.
['Car', 'Car driving', 'Car racing', 'Car parked'] <= BAD, because it's 4 strings.
['Fast car'] <= GOOD, because it's 1 string.
['Un chien', 'une voiture rapide', 'une maison rouge'] <= BAD, because the text query is NOT in English.

CRITICAL: For religious/biblical content, use more general, visually appealing terms that are likely to be found on stock video sites:
- Instead of "apocalypse", use "storm clouds", "dark sky", "lightning", "fire", "smoke"
- Instead of "bible", use "old book", "ancient text", "manuscript", "parchment"
- Instead of "religious", use "church", "cathedral", "stained glass", "candles", "prayer"
- Instead of "virgin mary", use "statue", "sculpture", "religious art", "portrait"
- Instead of "fatima", use "portugal landscape", "church building", "pilgrimage"
- Instead of "666", use "numbers", "symbols", "mysterious", "dark"
- Instead of "antichrist", use "dark figure", "shadow", "mysterious person"

Focus on visual elements that are commonly available in stock video libraries.

Note: Your response should be the response only and no extra text or data.
  """

def fix_json(json_str):
    """Corrige JSON malformado de várias formas - VERSÃO MELHORADA"""
    if not json_str or not isinstance(json_str, str):
        return "[[[0, 10], [\"storm clouds\", \"dark sky\", \"church\"]]]"
    
    # Limpeza inicial
    json_str = json_str.strip()
    
    # Remover marcadores de código se existirem
    json_str = json_str.replace("```json", "").replace("```", "")
    
    # Replace typographical apostrophes with straight quotes
    json_str = json_str.replace("'", "'")
    json_str = json_str.replace(""", "\"").replace(""", "\"")
    json_str = json_str.replace("'", "\"").replace("'", "\"")
    
    # Remover caracteres problemáticos
    json_str = json_str.replace('\n', ' ').replace('\r', ' ')
    json_str = re.sub(r'\s+', ' ', json_str)
    
    # Corrigir aspas problemáticas específicas
    json_str = json_str.replace('"you"re"', '"you\'re"')
    json_str = json_str.replace('"you"re missing"', '"you\'re missing"')
    json_str = json_str.replace('"you"re missing out"', '"you\'re missing out"')
    json_str = json_str.replace('"what you"re"', '"what you\'re"')
    
    # Corrigir aspas com apóstrofes problemáticas
    json_str = re.sub(r'"([^"]*)"([^"]*)"', r'"\1\2"', json_str)
    json_str = re.sub(r'"([^"]*)"([^"]*)"([^"]*)"', r'"\1\2\3"', json_str)
    
    # Corrigir aspas duplas múltiplas
    json_str = re.sub(r'""+', '"', json_str)
    
    # Tentar encontrar JSON válido
    try:
        # Procurar por padrão JSON mais específico
        json_pattern = r'\[\[\[.*?\]\]\]'
        matches = re.findall(json_pattern, json_str, re.DOTALL)
        if matches:
            for match in matches:
                try:
                    json.loads(match)
                    return match
                except:
                    continue
        
        # Se não encontrar, tentar extrair apenas arrays válidos
        array_pattern = r'\[\[\[.*?\]\]'
        matches = re.findall(array_pattern, json_str, re.DOTALL)
        if matches:
            # Tentar completar o JSON
            for match in matches:
                try:
                    # Adicionar fechamento se necessário
                    if not match.endswith(']]'):
                        match += ']]'
                    # Testar se é JSON válido
                    json.loads(match)
                    return match
                except:
                    continue
    except Exception as e:
        print(f"⚠️ Erro ao processar JSON: {e}")
        pass
    
    # Limpeza mais agressiva
    try:
        # Remover caracteres não-ASCII
        cleaned = re.sub(r'[^\x00-\x7F]+', '', json_str)
        
        # Manter apenas caracteres seguros para JSON
        cleaned = re.sub(r'[^\w\s\[\],".:-]', '', cleaned)
        
        # Corrigir aspas problemáticas
        cleaned = re.sub(r'([^\\])"([^"]*)"([^"]*)"', r'\1"\2\3"', cleaned)
        cleaned = re.sub(r'"([^"]*)"([^"]*)"', r'"\1\2"', cleaned)
        
        # Testar se o JSON limpo é válido
        json.loads(cleaned)
        return cleaned
    except:
        pass
    
    # Se tudo falhar, retornar JSON padrão
    print("⚠️ Não foi possível corrigir JSON, usando padrão")
    return "[[[0, 10], [\"storm clouds\", \"dark sky\", \"church\"]]]"

def getVideoSearchQueriesTimed(script,captions_timed):
    """Gera termos de busca para vídeos de fundo com fallback robusto"""
    try:
        end = captions_timed[-1][0][1]
        
        # Tentar gerar termos de busca
        content = call_OpenAI(script,captions_timed).replace("'",'"')
        
        # Primeira tentativa: JSON direto
        try:
            out = json.loads(content)
            if out and len(out) > 0:
                return out
        except Exception as e:
            print(f"⚠️ Erro no JSON direto: {e}")
        
        # Segunda tentativa: Limpar e tentar novamente
        try:
            cleaned_content = fix_json(content.replace("```json", "").replace("```", ""))
            out = json.loads(cleaned_content)
            if out and len(out) > 0:
                return out
        except Exception as e2:
            print(f"❌ Erro crítico ao processar JSON: {e2}")
            print(f"Content original: {content[:200]}...")
            print(f"Content limpo: {cleaned_content[:200]}...")
        
        # Terceira tentativa: Gerar estrutura básica baseada no script
        try:
            # Extrair palavras-chave do script
            words = script.lower().split()
            keywords = []
            
            # Palavras-chave religiosas
            religious_keywords = ['deus', 'jesus', 'bíblia', 'igreja', 'fé', 'espiritual', 'sagrado']
            for word in words:
                if any(keyword in word for keyword in religious_keywords):
                    keywords.extend(['church', 'spiritual', 'religious'])
                    break
            
            # Palavras-chave de natureza
            nature_keywords = ['céu', 'terra', 'sol', 'lua', 'estrelas', 'montanha', 'mar']
            for word in words:
                if any(keyword in word for keyword in nature_keywords):
                    keywords.extend(['nature', 'landscape', 'sky'])
                    break
            
            # Se não encontrou palavras específicas, usar padrão
            if not keywords:
                keywords = ['storm clouds', 'dark sky', 'church']
            
            # Criar estrutura básica
            basic_structure = [[[0, end], keywords]]
            print(f"✅ Usando estrutura básica: {basic_structure}")
            return basic_structure
            
        except Exception as e3:
            print(f"❌ Erro ao gerar estrutura básica: {e3}")
        
        # Fallback final
        print("⚠️ Usando fallback padrão")
        return [[[0, end], ["storm clouds", "dark sky", "church"]]]
        
    except Exception as e:
        print(f"❌ Erro geral em getVideoSearchQueriesTimed: {e}")
        # Retornar estrutura padrão em caso de falha
        return [[[0, captions_timed[-1][0][1] if captions_timed else 10], ["storm clouds", "dark sky", "church"]]]

def call_OpenAI(script,captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("Content", user_content)
    
    response = client.chat.completions.create(
        model= model,
        temperature=1,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ]
    )
    
    text = response.choices[0].message.content.strip()
    text = re.sub('\s+', ' ', text)
    print("Text", text)
    log_response(LOG_TYPE_GPT,script,text)
    return text

def merge_empty_intervals(segments):
    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            # Find consecutive None intervals
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            
            # Merge consecutive None intervals with the previous valid URL
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j-1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            
            i = j
        else:
            merged.append([interval, url])
            i += 1
    
    return merged
