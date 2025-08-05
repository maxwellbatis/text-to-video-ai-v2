# 🎤 Exemplos de Uso das Vozes ElevenLabs

## 🚀 Como Usar

### Via Interface Web
1. Acesse `http://localhost:5000`
2. Digite seu tópico
3. Selecione uma voz (opcional - deixe vazio para detecção automática)
4. Clique em "Gerar Vídeo"

### Via Linha de Comando

```bash
# Listar todas as vozes disponíveis
python app.py --list-voices

# Gerar vídeo com voz específica
python app.py "Fatos curiosos sobre o Brasil" --voice james

# Gerar vídeo espiritual com voz apropriada
python app.py "Versículos bíblicos sobre fé" --voice phillip

# Gerar vídeo reflexivo
python app.py "O significado da vida" --voice drew
```

## 🎵 Vozes Disponíveis

### 📚 Fatos Curiosos / Documentários

#### 🇬🇧 James - Britânico Profundo
- **ID**: `james`
- **Características**: Tom britânico calmo e profundo
- **Ideal para**: Narrativas históricas, curiosidades, documentários
- **Exemplo**: "Fatos curiosos sobre a história do Brasil"

#### 🇺🇸 Bill - Americano Clássico
- **ID**: `bill`
- **Características**: Voz americana clássica, firme e clara
- **Ideal para**: Vídeos explicativos, documentais, educativos
- **Exemplo**: "Como funciona a fotossíntese"

#### 🎙️ Neil - Equilibrado
- **ID**: `neil`
- **Características**: Equilibrado e confiável
- **Ideal para**: Explicações, comentários informativos
- **Exemplo**: "Curiosidades sobre o espaço"

### 🧘 Reflexão / Filosófico

#### 🧘 Drew - Reflexivo
- **ID**: `drew`
- **Características**: Voz calma e ligeiramente mística
- **Ideal para**: Conteúdo reflexivo, filosófico, contemplativo
- **Exemplo**: "O significado da existência humana"

### ⛪ Conteúdo Religioso / Espiritual

#### ⛪ Phillip - Espiritual
- **ID**: `phillip`
- **Características**: Projetada para temas espirituais e meditação
- **Ideal para**: Conteúdo religioso, meditação, espiritual
- **Exemplo**: "Versículos bíblicos sobre esperança"

#### 🙏 Deep Ray - Voz de Deus
- **ID**: `deep_ray`
- **Características**: Voz muito profunda e suave
- **Ideal para**: Leituras bíblicas, narrações solenes
- **Exemplo**: "O livro do Apocalipse"

## 🔧 Configuração

### 1. Configurar API Key
```bash
# Adicione sua chave ElevenLabs ao ambiente
export ELEVENLABS_API_KEY="sua_chave_aqui"
```

### 2. Detecção Automática
O sistema detecta automaticamente o tipo de conteúdo e escolhe a voz apropriada:

- **Palavras-chave espirituais**: `deus`, `jesus`, `bíblia`, `apocalipse`, `oração`, `fé` → Phillip
- **Palavras-chave reflexivas**: `por que`, `significado`, `filosofia`, `existência` → Drew
- **Padrão**: Fatos curiosos/documentários → James

### 3. Fallback
Se a ElevenLabs não estiver disponível, o sistema usa Edge TTS como fallback.

## 📊 Comparativo de Qualidade

| Aspecto | ElevenLabs | Edge TTS |
|---------|------------|----------|
| **Naturalidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Expressividade** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Controle** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Custo** | 💰💰💰 | 🆓 |
| **Velocidade** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎯 Exemplos Práticos

### Vídeo de Fatos Curiosos
```bash
python app.py "Fatos surpreendentes sobre o corpo humano" --voice james
```
**Resultado**: Voz britânica profunda narrando curiosidades científicas

### Vídeo Espiritual
```bash
python app.py "O poder da oração na vida cristã" --voice phillip
```
**Resultado**: Voz espiritual e meditativa para conteúdo religioso

### Vídeo Reflexivo
```bash
python app.py "Por que existimos? Reflexões filosóficas" --voice drew
```
**Resultado**: Voz calma e contemplativa para reflexões profundas

### Vídeo Documentário
```bash
python app.py "A história da Segunda Guerra Mundial" --voice bill
```
**Resultado**: Voz americana clara e firme para documentários

## 🎨 Integração com Templates

Combine vozes com templates para resultados ainda melhores:

```bash
# Vídeo espiritual com template cinematográfico
python app.py "A história de Jesus Cristo" --voice phillip --template cinematic_religious

# VSL magnético com voz americana
python app.py "Como ganhar dinheiro online" --voice bill --template vsl_magnetic
```

## 🔍 Troubleshooting

### Erro: "ELEVENLABS_API_KEY não configurada"
**Solução**: Configure sua chave API:
```bash
export ELEVENLABS_API_KEY="sua_chave_aqui"
```

### Erro: "Voz não encontrada"
**Solução**: Use uma das vozes disponíveis:
- `james`, `bill`, `neil`, `drew`, `phillip`, `deep_ray`

### Áudio não gerado
**Solução**: O sistema automaticamente usa Edge TTS como fallback

## 📈 Dicas de Otimização

1. **Para conteúdo em português**: Use detecção automática ou vozes neutras
2. **Para conteúdo internacional**: Use vozes específicas como James ou Bill
3. **Para conteúdo espiritual**: Sempre use Phillip ou Deep Ray
4. **Para reflexões**: Drew é ideal para conteúdo filosófico

## 🎬 Resultados Esperados

- **Qualidade de áudio**: Muito superior ao TTS padrão
- **Expressividade**: Vozes com emoção e personalidade
- **Sincronização**: Perfeita com legendas e vídeo
- **Profissionalismo**: Som de documentário ou narração profissional 