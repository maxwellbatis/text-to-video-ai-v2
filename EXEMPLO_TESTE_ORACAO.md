# 🧪 Exemplo de Teste - Orações e Vídeos Longos

## 🎯 Teste Rápido das Novas Funcionalidades

### 1. **Teste de Oração Simples (1 minuto)**
```bash
python app.py "Oração pela paz" --prayer --duration 1
```

**O que esperar:**
- Script de ~120 palavras
- Estrutura: Saudação → Oração → Amém
- Voz Phillip automaticamente selecionada
- Pausas mínimas para contemplação

### 2. **Teste de Oração Completa (3 minutos)**
```bash
python app.py "Oração pela família" --prayer --duration 3 --voice phillip
```

**O que esperar:**
- Script de ~360 palavras
- Estrutura completa: Adoração → Petição → Intercessão → Gratidão
- Múltiplos momentos de silêncio [...]
- Tom solene e reverente

### 3. **Teste de Estudo Bíblico (5 minutos)**
```bash
python app.py "Estudo sobre o amor de Deus" --template prayer_extended --duration 5
```

**O que esperar:**
- Script de ~600 palavras
- Estrutura: Introdução → Versículos → Explicação → Aplicação
- Voz apropriada automaticamente selecionada
- Pausas estratégicas para assimilação

### 4. **Teste de Vídeo Longo Geral (2 minutos)**
```bash
python app.py "Fatos curiosos sobre o Brasil" --voice james --duration 2
```

**O que esperar:**
- Script de ~300 palavras
- Tom britânico envolvente
- Estrutura: Abertura → Desenvolvimento → Fechamento
- Chamada à ação no final

## 🔍 Verificando as Funcionalidades

### **Listar Vozes Disponíveis**
```bash
python app.py --list-voices
```

**Saída esperada:**
```
🎤 Vozes Disponíveis:
==================================================

📚 Fatos Curiosos / Documentários:
  • james: Tom britânico calmo e profundo, excelente para narrativas históricas e curiosidades
  • bill: Voz americana clássica, firme e clara — muito usada em vídeos explicativos e documentais
  • neil: Equilibrado e confiável, ótimo para explicações e comentários informativos

🧘 Reflexão / Mistério / Filosófico:
  • drew: Voz calma e ligeiramente mística, ideal para conteúdo mais reflexivo ou filosófico

⛪ Conteúdo religioso ou bíblico:
  • phillip: Projetada para temas espirituais e de meditação, com presença emocional e calma profunda
  • deep_ray: Voz muito profunda e suave, perfeita para 'voz de Deus' em leituras bíblicas

🔄 Fallback: Edge TTS (pt-BR-AntonioNeural)
```

### **Listar Templates Disponíveis**
```bash
python app.py --list-templates
```

**Saída esperada:**
```
🎬 Templates Disponíveis:
==================================================

📋 prayer_extended:
  Nome: Oração e Conteúdo Espiritual Estendido
  Descrição: Template para orações, estudos bíblicos e conteúdo espiritual de 1-10 minutos com estrutura aprofundada
  Categoria: religioso_estendido

📋 cinematic_religious:
  Nome: Cinematográfico Religioso
  Descrição: Template para vídeos religiosos com estilo cinematográfico, pausas estratégicas e efeitos dramáticos
  Categoria: religioso

📋 vsl_magnetic:
  Nome: VSL Magnético
  Descrição: Template para vídeos de vendas com estrutura persuasiva
  Categoria: vendas
```

## 📊 Comparação de Durações

### **1 Minuto vs 3 Minutos vs 5 Minutos**

| Aspecto | 1 Minuto | 3 Minutos | 5 Minutos |
|---------|----------|-----------|-----------|
| **Palavras** | ~120 | ~360 | ~600 |
| **Estrutura** | Condensada | Padrão | Detalhada |
| **Pausas** | Mínimas | Moderadas | Estendidas |
| **Complexidade** | Simples | Média | Alta |

### **Exemplo de Script de 1 Minuto**
```
A paz do Senhor! Vamos juntos neste momento de oração pela paz.

Senhor, nós Te adoramos e Te louvamos por quem Tu és. [...]

Pai, hoje queremos orar especificamente pela paz em nosso mundo. [...]

Senhor, Te pedimos que traga paz aos corações aflitos. [...]

Agradecemos por este momento, Senhor. Que Sua paz esteja conosco. Amém.

Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!
```

### **Exemplo de Script de 3 Minutos**
```
A paz do Senhor! Vamos juntos neste momento de oração pela família.

Senhor, nós Te adoramos e Te louvamos por quem Tu és. Tu és digno de toda honra e glória. [...]

Pai, hoje queremos orar especificamente pela família. Sabemos que a família é o alicerce da sociedade. [...]

"Honra teu pai e tua mãe, para que se prolonguem os teus dias na terra que o Senhor, teu Deus, te dá." [...]

Senhor, Te pedimos que abençoe cada família. Que os pais sejam sábios e amorosos. [...]

Que os filhos sejam respeitosos e obedientes. Que o amor reine em cada lar. [...]

Agradecemos por Tua presença em nossas vidas. Que Sua paz esteja conosco. Amém.

Deixe seu comentário, compartilhe com alguém que precisa ouvir isso!
```

## 🎵 Configurações de Áudio

### **Para Orações (Phillip)**
- **Stability**: 0.8 (muito estável)
- **Similarity Boost**: 0.85
- **Style**: 0.4 (expressivo)
- **Use Speaker Boost**: True

### **Para Estudos (Deep Ray)**
- **Stability**: 0.9 (extremamente estável)
- **Similarity Boost**: 0.9
- **Style**: 0.5 (muito expressivo)
- **Use Speaker Boost**: True

## 🎬 Estrutura Visual

### **Template prayer_extended**
- **Aspect Ratio**: 9:16 (vertical)
- **Resolution**: 1080x1920
- **Font**: Impact (legendas)
- **Color**: White text with dark gold stroke
- **Background**: Spiritual contemplative

### **Pausas Estratégicas**
- **Contemplation**: 0.5-1.2 segundos
- **Natural**: 0.3 segundos
- **Scripture**: 0.5 segundos

## 🚀 Comandos de Teste Rápido

### **Teste Básico (1 minuto)**
```bash
python app.py "Teste de oração" --prayer --duration 1
```

### **Teste Médio (3 minutos)**
```bash
python app.py "Oração pela saúde" --prayer --duration 3
```

### **Teste Longo (5 minutos)**
```bash
python app.py "Estudo sobre gratidão" --template prayer_extended --duration 5
```

### **Teste com Voz Específica**
```bash
python app.py "Oração pela paz mundial" --prayer --voice deep_ray --duration 3
```

## 📈 Resultados Esperados

### **Qualidade do Script**
- ✅ Estrutura profissional
- ✅ Momentos de silêncio estratégicos
- ✅ Linguagem espiritual apropriada
- ✅ Chamadas à ação

### **Qualidade do Áudio**
- ✅ Voz natural e expressiva
- ✅ Pausas bem posicionadas
- ✅ Tom apropriado para o conteúdo
- ✅ Duração correta

### **Qualidade do Vídeo**
- ✅ Legendas legíveis
- ✅ Transições suaves
- ✅ Música de fundo apropriada
- ✅ Efeitos visuais adequados

## 🔧 Troubleshooting

### **Se o vídeo ficar muito longo:**
- Reduza a duração com `--duration`
- Use template mais simples

### **Se o áudio não ficar bom:**
- Configure ElevenLabs API key
- Teste diferentes vozes
- Verifique as configurações de voz

### **Se o script não ficar adequado:**
- Use `--prayer` para orações
- Use `--template prayer_extended` para estudos
- Ajuste a duração conforme necessário

---

**🎯 Execute estes testes para verificar se tudo está funcionando corretamente!**
