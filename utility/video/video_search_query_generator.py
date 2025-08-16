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
- Instead of "prayer", use "praying hands", "church interior", "candles"
- Instead of "family", use "family gathering", "home interior", "loving family"
- Instead of "god", use "heavenly light", "divine presence", "spiritual atmosphere"

Focus on visual elements that are commonly available in stock video libraries.

CRITICAL JSON FORMAT: Ensure your response is valid JSON. Do not include any text before or after the JSON array. The format must be exactly: [[[time1, time2], ["keyword1", "keyword2", "keyword3"]], ...]

IMPORTANT: 
- Each array must have exactly 3 keywords
- Time segments must be consecutive and cover the entire duration
- Use only English keywords
- Avoid special characters or accents
- Ensure all quotes are properly closed

Note: Your response should be the response only and no extra text or data.
  """

def fix_json(json_str):
    """Corrige JSON malformado de várias formas - VERSÃO ULTRA MELHORADA"""
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
    
    # Corrigir problemas específicos de vírgulas e colchetes
    json_str = re.sub(r',\s*]', ']', json_str)  # Remove vírgulas antes de ]
    json_str = re.sub(r',\s*}', '}', json_str)  # Remove vírgulas antes de }
    
    # Corrigir aspas duplas malformadas
    json_str = re.sub(r'([^\\])"([^"]*?)([^\\])"', r'\1"\2\3"', json_str)
    
    # Garantir que arrays estejam bem formados
    json_str = re.sub(r'\[\[\[', '[[[', json_str)
    json_str = re.sub(r'\]\]\]', ']]]', json_str)
    json_str = json_str.replace('"you"re missing"', '"you\'re missing"')
    json_str = json_str.replace('"you"re missing out"', '"you\'re missing out"')
    json_str = json_str.replace('"what you"re"', '"what you\'re"')
    
    # Corrigir aspas com apóstrofes problemáticas
    json_str = re.sub(r'"([^"]*)"([^"]*)"', r'"\1\2"', json_str)
    json_str = re.sub(r'"([^"]*)"([^"]*)"([^"]*)"', r'"\1\2\3"', json_str)
    
    # Corrigir aspas duplas múltiplas
    json_str = re.sub(r'""+', '"', json_str)
    
    # NOVA: Corrigir problemas específicos de vírgulas antes de fechamentos
    json_str = re.sub(r',\s*(\]|\})', r'\1', json_str)
    
    # NOVA: Corrigir arrays malformados com vírgulas extras
    json_str = re.sub(r'\[\[\[([^\]]+)\],\s*\[([^\]]+)\],\s*\]', r'[[[\1], [\2]]', json_str)
    
    # NOVA: Corrigir problemas de aspas não fechadas
    json_str = re.sub(r'"([^"]*?)(?=\]|,|$)', r'"\1"', json_str)
    
    # NOVA: Tentar encontrar JSON válido por partes
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
    
    # NOVA: Tentar reconstruir JSON cortado
    try:
        # Procurar por arrays individuais válidos
        individual_arrays = re.findall(r'\[\[\[[^\]]+\],\s*\[[^\]]+\]\]', json_str)
        if individual_arrays:
            # Tentar reconstruir um JSON válido
            reconstructed = "[" + ",".join(individual_arrays) + "]"
            try:
                json.loads(reconstructed)
                return reconstructed
            except:
                pass
    except Exception as e:
        print(f"⚠️ Erro ao reconstruir JSON: {e}")
        pass
    
    # NOVA: Tentar extrair apenas a parte válida do JSON
    try:
        # Procurar por padrões de array válidos
        valid_patterns = re.findall(r'\[\[\[[^\]]+\],\s*\[[^\]]+\]\]', json_str)
        if valid_patterns:
            # Pegar apenas os primeiros padrões válidos
            limited_json = "[" + ",".join(valid_patterns[:5]) + "]"
            try:
                json.loads(limited_json)
                return limited_json
            except:
                pass
    except Exception as e:
        print(f"⚠️ Erro ao extrair JSON válido: {e}")
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
        
        # NOVA: Tentar cortar o JSON em um ponto válido
        try:
            # Procurar por fechamentos de array válidos
            valid_endings = re.findall(r'\]\]', cleaned)
            if len(valid_endings) > 1:
                # Cortar no último fechamento válido
                last_valid_pos = cleaned.rfind(']]')
                if last_valid_pos > 0:
                    cleaned = cleaned[:last_valid_pos + 2]
                    # Adicionar fechamento final se necessário
                    if not cleaned.endswith(']'):
                        cleaned += ']'
            
            json.loads(cleaned)
            return cleaned
        except:
            pass
        
        # Testar se o JSON limpo é válido
        json.loads(cleaned)
        return cleaned
    except:
        pass
    
    # Se tudo falhar, retornar estrutura padrão
    print("⚠️ Não foi possível corrigir JSON, usando padrão")
    return [[[0, 10], ["storm clouds", "dark sky", "church"]]]

def generate_manual_json(script, duration):
    """Gera JSON manualmente baseado no conteúdo do script"""
    try:
        # Dividir o script em segmentos de tempo
        segment_duration = min(4, duration / 10)  # Máximo 4 segundos por segmento
        segments = []
        current_time = 0
        
        # Palavras-chave baseadas no conteúdo
        script_lower = script.lower()
        
        # Detectar tipo de conteúdo
        if any(word in script_lower for word in ['senhor', 'deus', 'jesus', 'oração', 'fé', 'espiritual']):
            keywords = [
                ["praying hands", "church interior", "spiritual atmosphere"],
                ["worship", "adoration", "divine presence"],
                ["peaceful atmosphere", "calmness", "serenity"],
                ["heavenly light", "divine guidance", "spiritual wisdom"],
                ["bible reading", "scripture study", "religious text"],
                ["family prayer", "group worship", "community faith"],
                ["gratitude", "thankfulness", "blessed moment"],
                ["inner peace", "spiritual reflection", "meditation"],
                ["god's love", "divine mercy", "heavenly grace"],
                ["faith journey", "spiritual growth", "religious devotion"]
            ]
        elif any(word in script_lower for word in ['família', 'pais', 'filhos', 'amor', 'casa']):
            keywords = [
                ["family gathering", "loving family", "home interior"],
                ["parents and children", "family love", "togetherness"],
                ["happy family", "family unity", "domestic life"],
                ["family meal", "family time", "family bonding"],
                ["family celebration", "family joy", "family happiness"],
                ["family support", "family care", "family protection"],
                ["family values", "family tradition", "family heritage"],
                ["family home", "family comfort", "family warmth"],
                ["family connection", "family relationship", "family bond"],
                ["family future", "family hope", "family dreams"]
            ]
        else:
            keywords = [
                ["nature landscape", "beautiful scenery", "peaceful environment"],
                ["sunrise", "morning light", "new day"],
                ["mountain view", "forest path", "natural beauty"],
                ["ocean waves", "beach sunset", "coastal beauty"],
                ["city life", "urban landscape", "modern living"],
                ["technology", "innovation", "future world"],
                ["education", "learning", "knowledge"],
                ["success", "achievement", "goal reaching"],
                ["friendship", "community", "social connection"],
                ["inspiration", "motivation", "positive energy"]
            ]
        
        # Gerar segmentos
        keyword_index = 0
        while current_time < duration:
            next_time = min(current_time + segment_duration, duration)
            
            # Usar keywords em ciclo
            current_keywords = keywords[keyword_index % len(keywords)]
            
            segments.append(f'[[{current_time:.1f}, {next_time:.1f}], {json.dumps(current_keywords)}]')
            
            current_time = next_time
            keyword_index += 1
        
        # Montar estrutura Python (não JSON string)
        manual_structure = []
        for segment in segments:
            # Converter string JSON para estrutura Python
            segment_data = json.loads(segment)
            manual_structure.append(segment_data)
        
        print(f"📝 JSON manual gerado: {len(manual_structure)} segmentos")
        return manual_structure
        
    except Exception as e:
        print(f"❌ Erro ao gerar JSON manual: {e}")
        # Fallback simples - retornar estrutura Python
        return [[[0, 10], ["storm clouds", "dark sky", "church"]]]

def getVideoSearchQueriesTimed(script,captions_timed):
    """Gera termos de busca para vídeos de fundo com fallback robusto"""
    try:
        end = captions_timed[-1][0][1]
        print(f"🎯 Duração total do vídeo: {end:.2f} segundos")
        
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
        
        # Terceira tentativa: Gerar JSON manualmente baseado no script
        try:
            print("🔄 Gerando JSON manualmente...")
            print(f"📝 Script detectado: {script[:100]}...")
            manual_structure = generate_manual_json(script, end)
            print(f"📋 Estrutura manual criada: {len(manual_structure)} segmentos")
            if manual_structure and len(manual_structure) > 0:
                print("✅ JSON manual gerado com sucesso")
                return manual_structure
        except Exception as e3:
            print(f"❌ Erro ao gerar JSON manual: {e3}")
            print(f"🔍 Detalhes do erro: {str(e3)}")
        
        # Quarta tentativa: Gerar estrutura básica baseada no script
        try:
            # Extrair palavras-chave do script
            words = script.lower().split()
            keywords = []
            
            # Palavras-chave religiosas
            religious_keywords = ['deus', 'jesus', 'bíblia', 'igreja', 'fé', 'espiritual', 'sagrado', 'oração', 'pai', 'senhor']
            for word in words:
                if any(keyword in word for keyword in religious_keywords):
                    keywords.extend(['church', 'spiritual', 'religious', 'prayer'])
                    break
            
            # Palavras-chave de família
            family_keywords = ['família', 'pais', 'filhos', 'irmãos', 'amor', 'casa']
            for word in words:
                if any(keyword in word for keyword in family_keywords):
                    keywords.extend(['family', 'home', 'love', 'togetherness'])
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
            
            # Criar estrutura básica com múltiplos segmentos
            segment_duration = min(10, end / 3)  # Dividir em 3 segmentos ou 10s cada
            basic_structure = []
            current_time = 0
            
            while current_time < end:
                next_time = min(current_time + segment_duration, end)
                basic_structure.append([[current_time, next_time], keywords])
                current_time = next_time
            
            print(f"✅ Usando estrutura básica: {basic_structure}")
            return basic_structure
            
        except Exception as e3:
            print(f"❌ Erro ao gerar estrutura básica: {e3}")
        
        # Fallback final - Gerar múltiplos segmentos
        print("⚠️ Usando fallback padrão com múltiplos segmentos")
        fallback_segments = []
        segment_duration = min(5, end / 10)  # 5 segundos ou dividir em 10 segmentos
        current_time = 0
        
        while current_time < end:
            next_time = min(current_time + segment_duration, end)
            fallback_segments.append([[current_time, next_time], ["storm clouds", "dark sky", "church"]])
            current_time = next_time
        
        print(f"✅ Fallback gerado: {len(fallback_segments)} segmentos")
        return fallback_segments
        
    except Exception as e:
        print(f"❌ Erro geral em getVideoSearchQueriesTimed: {e}")
        # Retornar estrutura padrão com múltiplos segmentos em caso de falha
        end = captions_timed[-1][0][1] if captions_timed else 10
        fallback_segments = []
        segment_duration = min(5, end / 10)  # 5 segundos ou dividir em 10 segmentos
        current_time = 0
        
        while current_time < end:
            next_time = min(current_time + segment_duration, end)
            fallback_segments.append([[current_time, next_time], ["storm clouds", "dark sky", "church"]])
            current_time = next_time
        
        print(f"✅ Fallback final gerado: {len(fallback_segments)} segmentos")
        return fallback_segments

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
