# 🔧 Configuração das APIs

## 📋 APIs Necessárias

### 1. ElevenLabs (Opcional - para vozes profissionais)
- **URL**: https://elevenlabs.io/
- **Propósito**: Vozes profissionais de alta qualidade
- **Configuração**: `export ELEVENLABS_API_KEY="sua_chave_aqui"`

### 2. Groq (Recomendado)
- **URL**: https://console.groq.com/
- **Propósito**: Geração de scripts com IA
- **Configuração**: `export GROQ_API_KEY="sua_chave_aqui"`

### 3. OpenAI (Alternativa ao Groq)
- **URL**: https://platform.openai.com/
- **Propósito**: Geração de scripts com IA
- **Configuração**: `export OPENAI_KEY="sua_chave_aqui"`

### 4. Pexels (Obrigatório)
- **URL**: https://www.pexels.com/api/
- **Propósito**: Vídeos de fundo
- **Configuração**: `export PEXELS_KEY="sua_chave_aqui"`

## 🚀 Configuração Rápida

### Windows (PowerShell)
```powershell
# Configurar variáveis de ambiente
$env:GROQ_API_KEY="sua_chave_groq"
$env:PEXELS_KEY="sua_chave_pexels"
$env:ELEVENLABS_API_KEY="sua_chave_elevenlabs"

# Testar configuração
py app.py --list-voices
```

### Linux/Mac
```bash
# Configurar variáveis de ambiente
export GROQ_API_KEY="sua_chave_groq"
export PEXELS_KEY="sua_chave_pexels"
export ELEVENLABS_API_KEY="sua_chave_elevenlabs"

# Testar configuração
python app.py --list-voices
```

## 🎯 Exemplos de Uso

### Com ElevenLabs (Vozes Profissionais)
```bash
# Vídeo espiritual com voz apropriada
py app.py "Versículos bíblicos sobre fé" --voice phillip

# Vídeo de fatos curiosos
py app.py "Fatos surpreendentes sobre o corpo humano" --voice james

# Vídeo reflexivo
py app.py "O significado da existência" --voice drew
```

### Sem ElevenLabs (Edge TTS)
```bash
# O sistema automaticamente usa Edge TTS se ElevenLabs não estiver configurado
py app.py "Fatos curiosos sobre o Brasil"
```

## 🔍 Troubleshooting

### Erro: "Nenhuma API key configurada"
**Solução**: Configure pelo menos uma das APIs de IA:
```bash
export GROQ_API_KEY="sua_chave"
# ou
export OPENAI_KEY="sua_chave"
```

### Erro: "PEXELS_KEY não configurada"
**Solução**: Configure a API do Pexels:
```bash
export PEXELS_KEY="sua_chave_pexels"
```

### Erro: "ELEVENLABS_API_KEY não configurada"
**Solução**: O sistema usa Edge TTS como fallback automaticamente.

## 📊 Comparativo de APIs

| API | Propósito | Qualidade | Custo | Necessário |
|-----|-----------|-----------|-------|------------|
| **Groq** | Scripts | ⭐⭐⭐⭐⭐ | 💰💰 | ✅ |
| **OpenAI** | Scripts | ⭐⭐⭐⭐⭐ | 💰💰💰 | ✅ |
| **Pexels** | Vídeos | ⭐⭐⭐⭐ | 🆓 | ✅ |
| **ElevenLabs** | Vozes | ⭐⭐⭐⭐⭐ | 💰💰 | ❌ |

## 🎤 Vozes Disponíveis

### Com ElevenLabs
- 🇬🇧 **James**: Britânico profundo
- 🇺🇸 **Bill**: Americano clássico  
- 🎙️ **Neil**: Equilibrado
- 🧘 **Drew**: Reflexivo
- ⛪ **Phillip**: Espiritual
- 🙏 **Deep Ray**: Voz de Deus

### Sem ElevenLabs
- 🎯 **Detecção Automática**: Edge TTS em português

## 💡 Dicas

1. **Para testes**: Use apenas Groq + Pexels
2. **Para produção**: Adicione ElevenLabs para vozes profissionais
3. **Para conteúdo em português**: Edge TTS funciona bem
4. **Para conteúdo internacional**: ElevenLabs oferece mais opções 