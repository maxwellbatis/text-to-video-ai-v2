# Text To Video AI 🔥

Generate video from text using AI

If you wish to add Text to Video into your application, here is an api to create video from text :- https://docs.vadoo.tv/docs/guide/create-an-ai-video

### Youtube Tutorial -> https://www.youtube.com/watch?v=AXo6VfRUgic

### Medium tutorial -> https://medium.com/@anilmatcha/text-to-video-ai-how-to-create-videos-for-free-a-complete-guide-a25c91de50b8

### Demo Video

https://github.com/user-attachments/assets/1e440ace-8560-4e12-850e-c532740711e7

### 🌟 Show Support

If you enjoy using Text to Video AI, we'd appreciate your support with a star ⭐ on our repository. Your encouragement is invaluable and inspires us to continually improve and expand Text to Video AI. Thank you, and happy content creation! 🎉

[![GitHub star chart](https://img.shields.io/github/stars/SamurAIGPT/Text-To-Video-AI?style=social)](https://github.com/SamurAIGPT/Text-To-Video-AI/stargazers)

## 🆕 Melhorias Implementadas

### 🎬 Vídeos Longos (1-10 Minutos) - NOVO!
- **Duração flexível**: 1 a 10 minutos com estrutura adaptativa
- **Scripts otimizados**: 150 palavras por minuto (aproximadamente)
- **Pausas estratégicas**: Baseadas na duração do conteúdo
- **Estrutura proporcional**: Abertura, desenvolvimento e fechamento adequados

### 🙏 Template Específico para Orações - NOVO!
- **Template `prayer_extended`**: Especializado em orações e conteúdo espiritual
- **Estrutura tradicional**: Adoração, confissão, gratidão, petição
- **Momentos de silêncio**: Pausas para contemplação e reflexão
- **Vozes apropriadas**: Phillip e Deep Ray para conteúdo espiritual

### 📝 Prompts Aprimorados
- **Vídeos mais longos**: 60-90 segundos (200-300 palavras)
- **Estrutura profissional**: Abertura, desenvolvimento e fechamento claros
- **Pausas estratégicas**: Para reflexão e melhor engajamento
- **Linguagem acessível**: Mas respeitosa e envolvente

### 🎬 Estrutura de Vídeo Religioso
- **Abertura (5-15s)**: Saudação calorosa + frase impactante
- **Desenvolvimento (40-70s)**: Tema principal + exemplos + reflexões
- **Fechamento (10-15s)**: Conclusão inspiradora + chamada à ação

### 🎙️ Sistema de Vozes Profissional
- **ElevenLabs**: Vozes de alta qualidade
- **Fallback automático**: Edge TTS se ElevenLabs falhar
- **Detecção inteligente**: Escolhe voz baseada no conteúdo

### Steps to run

#### 🎬 Vídeos Longos e Orações (NOVO!)
O sistema agora suporta vídeos de 1-10 minutos e orações específicas:

```bash
# Oração de 3 minutos
python app.py "Oração pela família" --prayer --duration 3

# Estudo bíblico de 5 minutos
python app.py "Estudo sobre fé" --template prayer_extended --duration 5

# Vídeo de curiosidades de 2 minutos
python app.py "História do Brasil" --voice james --duration 2

# Listar vozes disponíveis
python app.py --list-voices

# Listar templates disponíveis
python app.py --list-templates
```

#### 🎤 Vozes ElevenLabs
O sistema suporta vozes profissionais da ElevenLabs:

```bash
# Gerar vídeo com voz específica
python app.py "Fatos curiosos sobre o Brasil" --voice james

# Vídeo espiritual
python app.py "Versículos bíblicos" --voice phillip

# Vídeo reflexivo
python app.py "O significado da vida" --voice drew
```

**Vozes Disponíveis:**
- 🇬🇧 **James**: Britânico profundo (fatos curiosos)
- 🇺🇸 **Bill**: Americano clássico (documentários)
- 🎙️ **Neil**: Equilibrado (explicações)
- 🧘 **Drew**: Reflexivo (filosófico)
- ⛪ **Phillip**: Espiritual (religioso)
- 🙏 **Deep Ray**: Voz de Deus (bíblico)

**Detecção Automática**: Se não especificar voz, o sistema detecta automaticamente o tipo de conteúdo e escolhe a voz apropriada.

#### 🚀 Configuração Rápida (Recomendado)

```bash
# 1. Instalar dependências
pip install -r requirements.txt
npm install

# 2. Configurar banco de dados
python setup_env.py

# 3. Configurar credenciais
python -m database.setup_database

# 4. Gerar vídeo
python app.py "Topic name"
```

#### 🔧 Configuração Manual (Sem Banco)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
export OPENAI_KEY="api-key"
export PEXELS_KEY="pexels-key"

# 3. Gerar vídeo sem banco
python app.py "Topic name" --no-db
```

Output will be generated in rendered_video.mp4

### 🗄️ Banco de Dados

Este projeto agora inclui integração com banco de dados PostgreSQL para:

- ✅ Histórico completo de vídeos
- ✅ Armazenamento seguro de credenciais
- ✅ Rastreamento de status de processamento
- ✅ Múltiplas credenciais de API

Veja [README_DATABASE.md](README_DATABASE.md) para detalhes completos.

### Quick Start

Without going through the installation hastle here is a simple way to generate videos from text

For a simple way to run the code, checkout the [colab link](/Text_to_Video_example.ipynb)

To generate a video, just click on all the cells one by one. Setup your api keys for openai and pexels

## 💁 Contribution

As an open-source project we are extremely open to contributions. To get started raise an issue in Github or create a pull request

### Other useful Video AI Projects

[AI Influencer generator](https://github.com/SamurAIGPT/AI-Influencer-Generator)

[AI Youtube Shorts generator](https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator/)

[Faceless Video Generator](https://github.com/SamurAIGPT/Faceless-Video-Generator)

[AI B-roll generator](https://github.com/Anil-matcha/AI-B-roll)

[AI video generator](https://www.vadoo.tv/ai-video-generator)

[Text to Video AI](https://www.vadoo.tv/text-to-video-ai)

[Autoshorts AI](https://www.vadoo.tv/autoshorts-ai)

[Pixverse alternative](https://www.vadoo.tv/pixverse-ai)

[Hailuo AI alternative](https://www.vadoo.tv/hailuo-ai)

[Minimax AI alternative](https://www.vadoo.tv/minimax-ai)
