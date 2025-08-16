# 🎬 Gerador de Vídeos de Resumos de Novelas

Crie vídeos envolventes de resumos de novelas brasileiras automaticamente! Baseado no projeto Text-To-Video-AI.

## 🚀 Uso Rápido

```bash
# 1. Instalar dependências
py -3 -m pip install -r requirements.txt

# 2. Configurar APIs
$env:GROQ_API_KEY="sua_chave_groq"
$env:PEXELS_KEY="sua_chave_pexels"

# 3. Gerar vídeo
py -3 novela_video_generator.py "Resumo da semana de Dona de Mim"
```

## 📺 Novelas Suportadas

- **Dona de Mim** (Globo)
- **Fuzuê** (Globo) 
- **Vai na Fé** (Globo)
- **Terra e Paixão** (Globo)
- **Amor Perfeito** (Globo)
- **Mar do Sertão** (Globo)

## 🎯 Tipos de Conteúdo

- **Resumo Semanal**: Principais acontecimentos
- **Análise de Personagem**: Foco em personagem específico
- **Previsões**: Expectativas para próximos capítulos
- **Curiosidades**: Fatos interessantes
- **Behind Scenes**: Detalhes de bastidores

## 💡 Exemplos de Uso

```bash
# Resumo semanal
py -3 novela_video_generator.py "Resumo da semana de Dona de Mim"

# Análise de personagem
py -3 novela_video_generator.py "Análise do personagem principal de Fuzuê"

# Previsões
py -3 novela_video_generator.py "Previsões para próximos capítulos de Vai na Fé"

# Com voz específica
py -3 novela_video_generator.py "Curiosidades sobre Terra e Paixão" --voice francisco

# Listar novelas
py -3 novela_video_generator.py --list-novelas
```

## 🔧 Configuração

### APIs Necessárias

| API | Propósito | Obrigatório | Custo |
|-----|-----------|-------------|-------|
| **Groq** | Scripts | ✅ | Baixo |
| **Pexels** | Vídeos de fundo + Imagens de personagens | ✅ | Gratuito |
| **Unsplash** | Imagens de personagens (fallback) | ❌ | Gratuito |
| **ElevenLabs** | Vozes profissionais | ❌ | Médio |

### Configuração Windows
```powershell
$env:GROQ_API_KEY="sua_chave_groq"
$env:PEXELS_KEY="sua_chave_pexels"
$env:UNSPLASH_KEY="sua_chave_unsplash"
$env:ELEVENLABS_API_KEY="sua_chave_elevenlabs"
```

## 🎬 Estrutura do Vídeo

### Abertura (5-10s)
- Saudação envolvente
- Anúncio da novela
- Hook dramático

### Desenvolvimento (45-75s)
- Principais acontecimentos
- Personagens e conflitos
- Cenas marcantes

### Fechamento (10-15s)
- Teaser próxima semana
- Call to action

## 🎨 Características

- ✅ **Scripts Especializados**: Otimizados para novelas
- ✅ **Detecção Automática**: Identifica novela e tipo
- ✅ **Template Dramático**: Visual envolvente
- ✅ **Imagens de Personagens**: Busca automática de fotos
- ✅ **Vozes Apropriadas**: Para entretenimento
- ✅ **Banco de Dados**: Histórico completo
- ✅ **Redes Sociais**: Formato 9:16 otimizado

## 📊 Casos de Uso

### Criador de Conteúdo
- Resumos semanais para Instagram/TikTok
- Análises de personagens
- Engajamento de audiência

### Canal de Novelas
- Conteúdo regular e consistente
- Análises aprofundadas
- Curiosidades e bastidores

## 🎙️ Vozes Disponíveis

### Padrão (Edge TTS)
- **Francisco**: Masculina, ideal para novelas
- **Maria**: Feminina, envolvente

### Profissionais (ElevenLabs)
- **James**: Britânico profundo
- **Bill**: Americano clássico
- **Neil**: Equilibrado
- **Drew**: Reflexivo

## 📁 Arquivos Principais

```
novela_video_generator.py                    # Script principal
utility/script/novela_script_generator.py    # Gerador de scripts
utility/video/character_image_generator.py   # Busca de imagens de personagens
utility/templates/novela_resumo.json         # Template de novela
test_character_images.py                     # Teste de imagens de personagens
```

## 🔍 Troubleshooting

### Erro: "Nenhuma API configurada"
```bash
export GROQ_API_KEY="sua_chave"
```

### Erro: "PEXELS_KEY não configurada"
```bash
export PEXELS_KEY="sua_chave_pexels"
```

### Vídeo sem áudio
- Sistema tem fallback para Edge TTS
- Verifique configuração de APIs de voz

## 📈 Próximas Melhorias

- [ ] Integração com APIs de notícias
- [ ] Detecção automática de spoilers
- [ ] Templates para diferentes redes
- [ ] Sistema de agendamento
- [ ] Análise de tendências

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

**🎬 Crie vídeos incríveis de resumos de novelas e engaje sua audiência!**

Para mais detalhes, veja [NOVELA_VIDEO_GENERATOR.md](NOVELA_VIDEO_GENERATOR.md) 