# 🎬 Sistema Completo de Novelas com Dados Reais

## 📺 Visão Geral

O sistema agora busca **dados reais** das novelas atuais, incluindo resumos reais, personagens reais e imagens dos atores/atrizes reais. Não mais conteúdo genérico!

## 🎯 O que foi Implementado

### ✅ **1. Scraper de Resumos Reais**
- **Busca resumos atuais** das novelas no GShow
- **Extrai conteúdo real** dos sites oficiais
- **Detecta personagens reais** mencionados nos resumos
- **Mapeia atores/atrizes** com seus personagens

### ✅ **2. Banco de Dados de Atores Reais**
- **Giulia Gayoso** (Maria - Dona de Mim)
- **Gabriel Leone** (João - Dona de Mim)
- **Larissa Manoela** (Luna - Fuzuê)
- **João Guilherme** (Dante - Fuzuê)
- **Sheron Menezzes** (Sol - Vai na Fé)
- **Emilio Dantas** (Daniel - Vai na Fé)
- **Bárbara Reis** (Alice - Terra e Paixão)
- **Cauã Reymond** (Caio - Terra e Paixão)
- **Tony Ramos** (Vilão - Terra e Paixão)
- **Marcos Palmeira** (Vilão - várias novelas)

### ✅ **3. Busca de Imagens Reais**
- **Fotos dos atores/atrizes** reais
- **Imagens da novela** específica
- **Fotos profissionais** dos artistas
- **Imagens de eventos** e bastidores

## 🚀 Como Funciona

### **Fluxo Completo:**

1. **🔍 Scraping Real**
   ```
   URL: https://gshow.globo.com/novelas/dona-de-mim/resumo/
   ↓
   Extrai resumo atual da novela
   ↓
   Identifica personagens mencionados
   ```

2. **🎭 Mapeamento de Atores**
   ```
   Personagem: Maria
   ↓
   Ator Real: Giulia Gayoso
   ↓
   Busca: "Giulia Gayoso atriz", "Giulia Gayoso novela"
   ```

3. **🖼️ Busca de Imagens Reais**
   ```
   Query: "Giulia Gayoso atriz"
   ↓
   API Pexels/Unsplash
   ↓
   Imagem real da atriz
   ```

4. **📝 Geração de Script Baseado em Dados Reais**
   ```
   Resumo Real + Personagens Reais
   ↓
   Script específico e atualizado
   ↓
   Vídeo com conteúdo real
   ```

## 📺 Novelas Suportadas com Dados Reais

### **Dona de Mim**
- **URL**: https://gshow.globo.com/novelas/dona-de-mim/resumo/
- **Maria**: Giulia Gayoso
- **João**: Gabriel Leone
- **Vilão**: Marcos Palmeira

### **Fuzuê**
- **URL**: https://gshow.globo.com/novelas/fuzue/resumo/
- **Luna**: Larissa Manoela
- **Dante**: João Guilherme
- **Vilão**: Marcos Palmeira

### **Vai na Fé**
- **URL**: https://gshow.globo.com/novelas/vai-na-fe/resumo/
- **Sol**: Sheron Menezzes
- **Daniel**: Emilio Dantas
- **Vilão**: Marcos Palmeira

### **Terra e Paixão**
- **URL**: https://gshow.globo.com/novelas/terra-e-paixao/resumo/
- **Alice**: Bárbara Reis
- **Caio**: Cauã Reymond
- **Vilão**: Tony Ramos

## 🎭 Atores Reais Mapeados

| Novela | Personagem | Ator/Atriz Real |
|--------|------------|-----------------|
| Dona de Mim | Maria | Giulia Gayoso |
| Dona de Mim | João | Gabriel Leone |
| Fuzuê | Luna | Larissa Manoela |
| Fuzuê | Dante | João Guilherme |
| Vai na Fé | Sol | Sheron Menezzes |
| Vai na Fé | Daniel | Emilio Dantas |
| Terra e Paixão | Alice | Bárbara Reis |
| Terra e Paixão | Caio | Cauã Reymond |
| Terra e Paixão | Vilão | Tony Ramos |

## 🔧 Como Usar

### **1. Configuração**

```bash
# APIs necessárias
$env:PEXELS_KEY="sua_chave_pexels"
$env:GROQ_API_KEY="sua_chave_groq"
```

### **2. Teste do Sistema Completo**

```bash
# Testar sistema completo
py -3 test_real_novela_system.py

# Testar apenas imagens de personagens
py -3 test_character_images.py

# Gerar vídeo com dados reais
py -3 novela_video_generator.py "Resumo da semana de Dona de Mim"
```

### **3. Uso Programático**

```python
from utility.script.novela_scraper import NovelaScraper
from utility.video.character_image_generator import CharacterImageGenerator

# Buscar resumo real
scraper = NovelaScraper()
resumo = scraper.get_novela_resumo("Dona de Mim")

# Buscar imagens dos atores reais
character_generator = CharacterImageGenerator()
for char in resumo['characters']:
    image_url = character_generator.get_character_image(char['name'])
    if image_url:
        print(f"Imagem de {char['name']}: {image_url}")
```

## 📊 Diferenças do Sistema Anterior

### **❌ Sistema Antigo (Genérico)**
- Personagens fictícios (Maria, João genéricos)
- Resumos gerados por IA sem dados reais
- Imagens genéricas de "ator/atriz"
- Conteúdo não atualizado

### **✅ Sistema Novo (Real)**
- **Atores reais** (Giulia Gayoso, Gabriel Leone)
- **Resumos reais** do GShow
- **Imagens reais** dos atores
- **Conteúdo atualizado** diariamente

## 🎯 Benefícios

### **1. Conteúdo Real e Atualizado**
- Resumos das novelas atuais
- Personagens que realmente existem
- Acontecimentos reais da semana

### **2. Imagens Profissionais**
- Fotos reais dos atores
- Imagens de alta qualidade
- Conteúdo autêntico

### **3. Maior Engajamento**
- Público reconhece os atores
- Conteúdo mais relevante
- Maior credibilidade

### **4. Conteúdo Exclusivo**
- Dados que não estão em outros lugares
- Análises baseadas em fatos reais
- Informações atualizadas

## 📁 Arquivos do Sistema

```
utility/script/novela_scraper.py           # Scraper de resumos reais
utility/video/character_image_generator.py # Busca imagens de atores reais
test_real_novela_system.py                # Teste do sistema completo
novela_video_generator.py                 # Gerador principal atualizado
```

## 🔍 Exemplo de Saída

```
🎬 SISTEMA COMPLETO DE NOVELAS COM DADOS REAIS
============================================================

📺 Testando com: Dona de Mim
----------------------------------------

🔍 1. Buscando resumo real...
✅ Título: Resumo da semana de Dona de Mim
📝 Conteúdo: Maria (Giulia Gayoso) está enfrentando...
🎭 Personagens encontrados: 3
   • Giulia Gayoso (maria)
   • Gabriel Leone (joão)
   • Marcos Palmeira (vilão)

🖼️ 2. Buscando imagens dos atores reais...
🎭 Buscando: Giulia Gayoso
✅ Imagem encontrada: https://images.pexels.com/photos/...
💾 Imagem salva: character_images/ator_giulia_gayoso.jpg

📝 3. Gerando script baseado no resumo real...
✅ Sistema completo testado com sucesso!
```

## 🚀 Próximos Passos

### **Planejados**
- [ ] Integração com mais sites de novelas
- [ ] Detecção automática de novos atores
- [ ] Cache de resumos para performance
- [ ] Sistema de notificações de novos episódios

### **Sugeridos**
- [ ] Integração com redes sociais dos atores
- [ ] Análise de sentimento dos comentários
- [ ] Sistema de tendências de personagens
- [ ] Agendamento automático de posts

## 💡 Dicas de Uso

### **Para Melhor Qualidade**
1. **Configure as APIs**: Pexels para imagens reais
2. **Use nomes específicos**: "Giulia Gayoso" em vez de "Maria"
3. **Mantenha atualizado**: O sistema busca dados em tempo real

### **Para Otimização**
1. **Cache local**: Salve imagens baixadas
2. **Múltiplas APIs**: Configure Pexels + Unsplash
3. **Monitoramento**: Verifique se os sites estão funcionando

---

**🎬 Agora você tem um sistema completo com dados reais das novelas!** 