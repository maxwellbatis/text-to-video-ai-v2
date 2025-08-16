# 🎬 Vídeos Longos e Orações - Guia Completo

## 🆕 Novas Funcionalidades Implementadas

### ✅ Suporte a Vídeos de 1-10 Minutos
- **Duração flexível**: 1 a 10 minutos
- **Estrutura adaptativa**: Abertura, desenvolvimento e fechamento proporcionais
- **Pausas estratégicas**: Baseadas na duração do conteúdo
- **Scripts otimizados**: 150 palavras por minuto (aproximadamente)

### ✅ Template Específico para Orações
- **Template `prayer_extended`**: Especializado em orações e conteúdo espiritual
- **Estrutura tradicional**: Adoração, confissão, gratidão, petição
- **Momentos de silêncio**: Pausas para contemplação e reflexão
- **Vozes apropriadas**: Phillip e Deep Ray para conteúdo espiritual

### ✅ Sistema de Vozes Aprimorado
- **Detecção automática**: Escolhe voz baseada no conteúdo
- **Configurações específicas**: Otimizadas para cada tipo de conteúdo
- **Fallback robusto**: Edge TTS quando ElevenLabs não está disponível

## 🚀 Como Usar

### Via Linha de Comando

#### 1. **Orações Específicas**
```bash
# Oração de 3 minutos
python app.py "Oração pela família" --prayer --duration 3

# Oração de 5 minutos com voz específica
python app.py "Oração pela paz mundial" --prayer --voice phillip --duration 5

# Oração de 10 minutos
python app.py "Oração de gratidão" --prayer --duration 10
```

#### 2. **Estudos Bíblicos Longos**
```bash
# Estudo de 5 minutos
python app.py "Estudo sobre fé" --template prayer_extended --duration 5

# Estudo de 10 minutos com voz profunda
python app.py "Estudo sobre Apocalipse" --template prayer_extended --voice deep_ray --duration 10
```

#### 3. **Conteúdo Geral Longo**
```bash
# Vídeo de curiosidades de 3 minutos
python app.py "História do Brasil" --voice james --duration 3

# Vídeo reflexivo de 5 minutos
python app.py "O significado da vida" --voice drew --duration 5
```

#### 4. **Comandos Úteis**
```bash
# Listar vozes disponíveis
python app.py --list-voices

# Listar templates disponíveis
python app.py --list-templates

# Ver ajuda
python app.py --help
```

### Via Interface Web

1. **Acesse** `http://localhost:5000`
2. **Digite** o tópico do vídeo
3. **Selecione** a duração (1-10 minutos)
4. **Escolha** uma voz (opcional)
5. **Selecione** template (para orações, use `prayer_extended`)
6. **Clique** em "Gerar Vídeo"

## 🎤 Vozes Recomendadas por Tipo de Conteúdo

### 🙏 **Conteúdo Espiritual / Orações**
- **Phillip**: Voz espiritual e contemplativa
- **Deep Ray**: Voz profunda (voz de Deus)

### 📚 **Estudos Bíblicos**
- **Phillip**: Para estudos profundos
- **James**: Para estudos históricos

### 🧘 **Meditações e Reflexões**
- **Drew**: Voz calma e contemplativa
- **Phillip**: Para reflexões espirituais

### 📖 **Fatos Curiosos / Documentários**
- **James**: Tom britânico profundo
- **Bill**: Voz americana clássica
- **Neil**: Equilibrado e confiável

## 📋 Templates Disponíveis

### 🆕 **prayer_extended** (NOVO!)
- **Categoria**: Religioso estendido
- **Duração**: 1-10 minutos
- **Ideal para**: Orações, estudos bíblicos, meditações
- **Características**:
  - Estrutura tradicional de oração
  - Momentos de silêncio estratégicos
  - Vozes espirituais apropriadas
  - Pausas para contemplação

### 🎬 **cinematic_religious**
- **Categoria**: Religioso cinematográfico
- **Duração**: 1-2 minutos
- **Ideal para**: Vídeos religiosos curtos
- **Características**:
  - Efeitos dramáticos
  - Pausas estratégicas
  - Estilo cinematográfico

### 📈 **vsl_magnetic**
- **Categoria**: Vendas e marketing
- **Duração**: 1-3 minutos
- **Ideal para**: Vídeos de vendas
- **Características**:
  - Estrutura persuasiva
  - Chamadas à ação
  - Tom envolvente

## 🎯 Estrutura dos Vídeos Longos

### **1 Minuto**
- **Palavras**: ~150
- **Estrutura**: Condensada
- **Pausas**: Mínimas

### **3 Minutos**
- **Palavras**: ~450
- **Estrutura**: Padrão
- **Pausas**: Moderadas

### **5 Minutos**
- **Palavras**: ~750
- **Estrutura**: Detalhada
- **Pausas**: Estendidas

### **10 Minutos**
- **Palavras**: ~1500
- **Estrutura**: Abrangente
- **Pausas**: Contemplativas

## 🙏 Estrutura Específica para Orações

### **Abertura (10-20 segundos)**
- Saudação espiritual
- Contextualização do tema
- Preparação do coração

### **Desenvolvimento (1-9 minutos)**
- Oração de adoração e gratidão
- Oração específica sobre o tema
- Momentos de silêncio e contemplação
- Versículos bíblicos relevantes
- Oração de intercessão
- Oração de petição pessoal

### **Fechamento (10-20 segundos)**
- Oração de gratidão
- Bênção final
- "Amém"
- Convite à interação

## ⚙️ Configurações de Voz para Orações

### **Phillip (Voz Principal)**
- **Stability**: 0.8 (muito estável)
- **Similarity Boost**: 0.85
- **Style**: 0.4 (expressivo)
- **Use Speaker Boost**: True

### **Deep Ray (Voz Secundária)**
- **Stability**: 0.9 (extremamente estável)
- **Similarity Boost**: 0.9
- **Style**: 0.5 (muito expressivo)
- **Use Speaker Boost**: True

## 🎵 Música de Fundo Recomendada

### **Para Orações**
- Piano suave
- Harpa espiritual
- Coral instrumental
- Violão acústico
- Música de meditação

### **Configurações**
- **Volume**: 0.3 (30%)
- **Fade In**: 2.0 segundos
- **Fade Out**: 3.0 segundos

## 📊 Exemplos Práticos

### **Exemplo 1: Oração pela Família (3 minutos)**
```bash
python app.py "Oração pela família" --prayer --duration 3 --voice phillip
```

**Resultado esperado**:
- Script de ~360 palavras
- Estrutura: Adoração → Petição → Intercessão → Gratidão
- Pausas estratégicas para contemplação
- Tom solene e reverente

### **Exemplo 2: Estudo Bíblico (5 minutos)**
```bash
python app.py "Estudo sobre o amor de Deus" --template prayer_extended --duration 5
```

**Resultado esperado**:
- Script de ~600 palavras
- Estrutura: Introdução → Versículos → Explicação → Aplicação
- Múltiplos pontos de desenvolvimento
- Conclusão inspiradora

### **Exemplo 3: Vídeo de Curiosidades (2 minutos)**
```bash
python app.py "Fatos curiosos sobre o espaço" --voice james --duration 2
```

**Resultado esperado**:
- Script de ~300 palavras
- Estrutura: Abertura → Desenvolvimento → Fechamento
- Tom britânico e envolvente
- Chamada à ação

## 🔧 Configuração do Sistema

### **Variáveis de Ambiente Necessárias**
```bash
# Para scripts (obrigatório)
export GROQ_API_KEY="sua_chave_groq"

# Para vídeos de fundo (obrigatório)
export PEXELS_KEY="sua_chave_pexels"

# Para vozes profissionais (opcional)
export ELEVENLABS_API_KEY="sua_chave_elevenlabs"
```

### **Dependências**
```bash
pip install -r requirements.txt
```

## 🎯 Dicas para Melhores Resultados

### **Para Orações**
1. **Use o template `prayer_extended`** para conteúdo espiritual
2. **Escolha vozes apropriadas**: Phillip ou Deep Ray
3. **Defina duração adequada**: 3-5 minutos para orações completas
4. **Inclua momentos de silêncio** para contemplação

### **Para Vídeos Longos**
1. **Estruture o conteúdo** com múltiplos pontos
2. **Use transições suaves** entre tópicos
3. **Inclua pausas estratégicas** para assimilação
4. **Mantenha engajamento** com perguntas e reflexões

### **Para Qualidade de Áudio**
1. **Configure ElevenLabs** para vozes profissionais
2. **Use detecção automática** de categoria
3. **Ajuste configurações** por tipo de conteúdo
4. **Teste diferentes vozes** para encontrar a ideal

## 🚨 Solução de Problemas

### **Erro: "Duração deve estar entre 1 e 10 minutos"**
- Verifique o parâmetro `--duration`
- Use valores entre 1 e 10

### **Erro: "Template não encontrado"**
- Use `python app.py --list-templates` para ver templates disponíveis
- Verifique se o template está instalado

### **Erro: "Voz não encontrada"**
- Use `python app.py --list-voices` para ver vozes disponíveis
- Deixe vazio para detecção automática

### **Vídeo muito longo/curto**
- Ajuste o parâmetro `--duration`
- O sistema calcula ~150 palavras por minuto

## 📈 Próximas Melhorias

- [ ] Suporte a vídeos de 15-30 minutos
- [ ] Templates específicos para pregações
- [ ] Sistema de música automática
- [ ] Integração com mais APIs de voz
- [ ] Editor visual de scripts
- [ ] Sistema de legendas avançado

---

**🎉 Agora você pode criar vídeos de oração e conteúdo longo de alta qualidade!**
