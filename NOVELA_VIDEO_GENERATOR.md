# 🎬 Gerador de Vídeos de Resumos de Novelas

## 📺 Visão Geral

Este é um gerador especializado para criar vídeos de resumos de novelas brasileiras, baseado no projeto Text-To-Video-AI. O sistema foi otimizado para criar conteúdo envolvente e dramático sobre novelas, com foco em redes sociais.

## 🎯 Funcionalidades

### ✅ **Recursos Principais**
- **Scripts Especializados**: Geração de roteiros específicos para novelas
- **Detecção Automática**: Identifica a novela e tipo de conteúdo
- **Template Dramático**: Visual e áudio otimizados para entretenimento
- **Vozes Apropriadas**: Vozes que combinam com o conteúdo dramático
- **Banco de Dados**: Histórico completo de vídeos gerados

### 📺 **Novelas Suportadas**
- **Dona de Mim** (Globo)
- **Fuzuê** (Globo)
- **Vai na Fé** (Globo)
- **Terra e Paixão** (Globo)
- **Amor Perfeito** (Globo)
- **Mar do Sertão** (Globo)

### 📝 **Tipos de Conteúdo**
- **Resumo Semanal**: Principais acontecimentos da semana
- **Resumo de Capítulo**: Análise de episódio específico
- **Análise de Personagem**: Foco em personagem específico
- **Previsões**: Expectativas para próximos capítulos
- **Curiosidades**: Fatos interessantes sobre a novela
- **Behind Scenes**: Detalhes de bastidores

## 🚀 Como Usar

### **Configuração Rápida**

```bash
# 1. Instalar dependências
py -3 -m pip install -r requirements.txt

# 2. Configurar APIs
$env:GROQ_API_KEY="sua_chave_groq"
$env:PEXELS_KEY="sua_chave_pexels"

# 3. Gerar vídeo de novela
py -3 novela_video_generator.py "Resumo da semana de Dona de Mim"
```

### **Exemplos de Uso**

```bash
# Resumo semanal
py -3 novela_video_generator.py "Resumo da semana de Dona de Mim"

# Análise de personagem
py -3 novela_video_generator.py "Análise do personagem principal de Fuzuê"

# Previsões
py -3 novela_video_generator.py "Previsões para próximos capítulos de Vai na Fé"

# Com voz específica
py -3 novela_video_generator.py "Curiosidades sobre Terra e Paixão" --voice francisco

# Sem banco de dados
py -3 novela_video_generator.py "Resumo da semana de Dona de Mim" --no-db

# Listar novelas suportadas
py -3 novela_video_generator.py --list-novelas
```

## 🎬 Estrutura do Vídeo

### **Abertura (5-10 segundos)**
- Saudação envolvente: "Fala galera!", "Oi pessoal!"
- Anúncio da novela: "Resumo da semana de [Nome da Novela]"
- Hook dramático: "Você não vai acreditar no que aconteceu!"

### **Desenvolvimento (45-75 segundos)**
- Resumo dos principais acontecimentos
- Destaque dos personagens principais
- Conflitos e reviravoltas marcantes
- Cenas mais emocionantes
- Relacionamentos e dramas amorosos

### **Fechamento (10-15 segundos)**
- Teaser para próxima semana
- Convite para comentários
- Call to action: "Não perca o próximo capítulo!"

## 🎙️ Vozes Disponíveis

### **Vozes Padrão (Edge TTS)**
- **Francisco**: Voz masculina, ideal para novelas
- **Maria**: Voz feminina, envolvente
- **Detecção Automática**: Escolhe a melhor voz

### **Vozes Profissionais (ElevenLabs)**
- **James**: Britânico profundo
- **Bill**: Americano clássico
- **Neil**: Equilibrado e confiável
- **Drew**: Reflexivo e calmo

## 🎨 Template Visual

### **Configurações de Texto**
- **Fonte**: Impact (grossa e legível)
- **Tamanho**: 85px
- **Cor**: Branco com contorno preto
- **Posição**: Inferior da tela

### **Efeitos Visuais**
- **Estilo**: Dramático e envolvente
- **Transições**: Suaves e cinematográficas
- **Paleta**: Vibrante e emocional
- **Aspecto**: 9:16 (vertical para redes sociais)

### **Áudio**
- **Música**: Dramática e envolvente
- **Efeitos**: Suspense e impacto
- **Volume**: Otimizado para redes sociais

## 📊 Banco de Dados

### **Funcionalidades**
- Histórico completo de vídeos
- Rastreamento de status
- Armazenamento de scripts
- Múltiplas credenciais

### **Status de Processamento**
- `PENDING`: Aguardando processamento
- `PROCESSING`: Em andamento
- `SCRIPT_GENERATED`: Script criado
- `COMPLETED`: Vídeo finalizado
- `ERROR`: Erro no processamento

## 🔧 Configuração

### **APIs Necessárias**

#### **1. Groq (Recomendado)**
```bash
export GROQ_API_KEY="sua_chave_groq"
```
- **Propósito**: Geração de scripts
- **Custo**: Baixo
- **Qualidade**: Excelente

#### **2. OpenAI (Alternativa)**
```bash
export OPENAI_KEY="sua_chave_openai"
```
- **Propósito**: Geração de scripts
- **Custo**: Médio
- **Qualidade**: Excelente

#### **3. Pexels (Obrigatório)**
```bash
export PEXELS_KEY="sua_chave_pexels"
```
- **Propósito**: Vídeos de fundo
- **Custo**: Gratuito
- **Qualidade**: Boa

#### **4. ElevenLabs (Opcional)**
```bash
export ELEVENLABS_API_KEY="sua_chave_elevenlabs"
```
- **Propósito**: Vozes profissionais
- **Custo**: Médio
- **Qualidade**: Excelente

### **Configuração no Windows**
```powershell
# PowerShell
$env:GROQ_API_KEY="sua_chave_groq"
$env:PEXELS_KEY="sua_chave_pexels"
$env:ELEVENLABS_API_KEY="sua_chave_elevenlabs"
```

### **Configuração no Linux/Mac**
```bash
# Bash
export GROQ_API_KEY="sua_chave_groq"
export PEXELS_KEY="sua_chave_pexels"
export ELEVENLABS_API_KEY="sua_chave_elevenlabs"
```

## 📁 Estrutura de Arquivos

```
Text-To-Video-AI/
├── novela_video_generator.py          # Script principal
├── utility/
│   ├── script/
│   │   └── novela_script_generator.py # Gerador de scripts
│   └── templates/
│       └── novela_resumo.json         # Template de novela
├── assets/
│   ├── TRILHA SONORA/
│   │   └── CINEMATIC/                 # Músicas dramáticas
│   └── EFEITOS SONOROS/
│       ├── CINEMATIC/                 # Efeitos dramáticos
│       └── IMPACTOS/                  # Efeitos de impacto
└── database/                          # Sistema de banco de dados
```

## 🎯 Casos de Uso

### **1. Criador de Conteúdo**
- Resumos semanais para Instagram/TikTok
- Análises de personagens
- Previsões para engajamento

### **2. Canal de Novelas**
- Conteúdo regular e consistente
- Análises aprofundadas
- Curiosidades e bastidores

### **3. Marketing**
- Promoção de novelas
- Engajamento de audiência
- Conteúdo viral

## 💡 Dicas de Uso

### **Para Melhor Engajamento**
1. **Use Hooks Dramáticos**: "Você não vai acreditar..."
2. **Inclua Emoção**: Foque nos conflitos e relacionamentos
3. **Crie Expectativa**: Teasers para próximos capítulos
4. **Interaja**: Peça comentários e opiniões

### **Para Otimização**
1. **Teste Diferentes Vozes**: Encontre a que mais combina
2. **Ajuste o Tom**: Mais dramático ou mais leve
3. **Monitore Performance**: Use o banco de dados
4. **Experimente Horários**: Melhores horários de postagem

## 🔍 Troubleshooting

### **Erro: "Nenhuma API configurada"**
```bash
# Configure pelo menos uma API de IA
export GROQ_API_KEY="sua_chave"
```

### **Erro: "PEXELS_KEY não configurada"**
```bash
# Configure a API do Pexels
export PEXELS_KEY="sua_chave_pexels"
```

### **Erro: "Template não encontrado"**
- Verifique se o arquivo `novela_resumo.json` existe
- O sistema usará configurações padrão

### **Vídeo sem áudio**
- Verifique se as APIs de voz estão configuradas
- O sistema tem fallback para Edge TTS

## 📈 Próximas Melhorias

### **Planejadas**
- [ ] Integração com APIs de notícias de novelas
- [ ] Detecção automática de spoilers
- [ ] Templates para diferentes redes sociais
- [ ] Sistema de agendamento de posts
- [ ] Análise de tendências de novelas

### **Sugeridas**
- [ ] Integração com YouTube/TikTok APIs
- [ ] Sistema de hashtags automáticas
- [ ] Análise de sentimento dos comentários
- [ ] Geração de thumbnails personalizados

## 🤝 Contribuição

Para contribuir com o projeto:

1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra** um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**🎬 Crie vídeos incríveis de resumos de novelas e engaje sua audiência!** 