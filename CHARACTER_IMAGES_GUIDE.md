# 🎭 Sistema de Imagens de Personagens para Novelas

## 📺 Visão Geral

O sistema de imagens de personagens busca automaticamente fotos apropriadas dos personagens das novelas, tornando os vídeos mais envolventes e profissionais.

## 🎯 Funcionalidades

### ✅ **Recursos Principais**
- **Detecção Automática**: Identifica personagens no script
- **Busca Inteligente**: Usa múltiplas APIs (Pexels, Unsplash)
- **Banco de Dados**: Personagens mapeados por novela
- **Fallback Robusto**: Múltiplas estratégias de busca
- **Download Automático**: Salva imagens localmente

### 🎭 **Personagens Suportados**

#### **Dona de Mim**
- **Maria**: Protagonista feminina
- **João**: Protagonista masculino
- **Vilão**: Antagonista
- **Mocinha**: Jovem feminina
- **Mocinho**: Jovem masculino

#### **Fuzuê**
- **Luna**: Protagonista feminina
- **Dante**: Protagonista masculino
- **Vilão**: Antagonista
- **Mocinha**: Jovem feminina
- **Mocinho**: Jovem masculino

#### **Vai na Fé**
- **Sol**: Protagonista feminina
- **Daniel**: Protagonista masculino
- **Vilão**: Antagonista
- **Mocinha**: Jovem feminina
- **Mocinho**: Jovem masculino

#### **Terra e Paixão**
- **Alice**: Protagonista feminina
- **Caio**: Protagonista masculino
- **Vilão**: Antagonista
- **Mocinha**: Jovem feminina
- **Mocinho**: Jovem masculino

## 🚀 Como Usar

### **Configuração**

```bash
# APIs necessárias
$env:PEXELS_KEY="sua_chave_pexels"
$env:UNSPLASH_KEY="sua_chave_unsplash"  # Opcional
```

### **Uso Básico**

```python
from utility.video.character_image_generator import CharacterImageGenerator

# Inicializar
generator = CharacterImageGenerator()

# Buscar imagem de personagem
text = "Maria é a protagonista de Dona de Mim"
image_url = generator.get_character_image(text)

# Baixar imagem
if image_url:
    filepath = generator.download_character_image(image_url, "maria_protagonista")
```

### **Uso Avançado**

```python
# Extrair informações do personagem
character_info = generator.extract_character_info(text)
print(f"Personagem: {character_info['personagem']}")
print(f"Novela: {character_info['novela']}")
print(f"Tipo: {character_info['tipo']}")

# Gerar múltiplas imagens
images = generator.get_multiple_character_images(text, count=3)

# Gerar consultas de busca
queries = generator.generate_character_search_queries(character_info)
```

## 🔍 Estratégias de Busca

### **1. Busca Específica**
- Nome do personagem + novela
- Nome do personagem + "personagem"
- Nome do personagem + "ator atriz"

### **2. Busca por Tipo**
- **Protagonista**: "protagonista novela", "personagem principal"
- **Antagonista**: "vilão novela", "antagonista"
- **Mocinha/Mocinho**: "mocinha novela", "jovem mulher/homem"

### **3. Busca Genérica**
- "ator atriz novela"
- "personagem televisão"
- "rosto expressivo"

## 🎨 Configurações Visuais

### **Template de Novela**
```json
{
  "character_images": {
    "enabled": true,
    "position": "top_right",
    "size": "medium",
    "border_radius": 10,
    "border_color": "white",
    "border_width": 3,
    "shadow": true,
    "fade_in": 0.5,
    "fade_out": 0.5,
    "max_images_per_scene": 2
  }
}
```

### **Posições Disponíveis**
- `top_right`: Canto superior direito
- `top_left`: Canto superior esquerdo
- `bottom_right`: Canto inferior direito
- `bottom_left`: Canto inferior esquerdo
- `center`: Centro da tela

### **Tamanhos**
- `small`: 100x100px
- `medium`: 200x200px
- `large`: 300x300px
- `custom`: Tamanho personalizado

## 📊 Integração com Vídeos

### **No Gerador de Vídeos**

```python
# O sistema automaticamente:
# 1. Extrai personagens do script
# 2. Busca imagens apropriadas
# 3. Integra no vídeo final

character_segments = self._extract_character_segments(script)
for segment in character_segments:
    image_url = self.character_generator.get_character_image(segment)
    if image_url:
        character_images.append((segment, image_url))
```

### **Extração de Personagens**

O sistema detecta automaticamente:
- Nomes específicos (Maria, João, Luna, etc.)
- Tipos de personagem (protagonista, vilão, etc.)
- Contexto da novela

## 🔧 APIs Suportadas

### **Pexels (Principal)**
- **URL**: https://api.pexels.com/
- **Propósito**: Imagens de alta qualidade
- **Configuração**: `PEXELS_KEY`
- **Custo**: Gratuito (com limites)

### **Unsplash (Fallback)**
- **URL**: https://api.unsplash.com/
- **Propósito**: Imagens alternativas
- **Configuração**: `UNSPLASH_KEY`
- **Custo**: Gratuito (com limites)

## 📁 Estrutura de Arquivos

```
utility/video/character_image_generator.py  # Gerador principal
test_character_images.py                    # Script de teste
character_images/                           # Imagens baixadas
├── maria_protagonista.jpg
├── vilao_fuzue.jpg
└── mocinha_vaina_fe.jpg
```

## 🎯 Casos de Uso

### **1. Vídeos de Resumos**
- Mostrar personagens mencionados
- Destacar protagonistas
- Ilustrar conflitos

### **2. Análises de Personagens**
- Foco em personagem específico
- Múltiplas imagens
- Evolução do personagem

### **3. Previsões**
- Personagens em situações futuras
- Relacionamentos
- Conflitos

## 💡 Dicas de Uso

### **Para Melhor Qualidade**
1. **Use Nomes Específicos**: "Maria" em vez de "protagonista"
2. **Inclua Contexto**: "Maria de Dona de Mim"
3. **Especifique Tipo**: "vilão", "mocinha", "mocinho"

### **Para Otimização**
1. **Limite Imagens**: Máximo 2 por cena
2. **Cache Local**: Reutilize imagens baixadas
3. **Fallback**: Configure múltiplas APIs

## 🔍 Troubleshooting

### **Erro: "Nenhuma imagem encontrada"**
- Verifique se a API está configurada
- Tente consultas mais genéricas
- Configure API alternativa

### **Erro: "PEXELS_KEY não configurada"**
```bash
$env:PEXELS_KEY="sua_chave_pexels"
```

### **Imagens de Baixa Qualidade**
- Use consultas mais específicas
- Configure API do Unsplash
- Ajuste parâmetros de busca

## 📈 Próximas Melhorias

### **Planejadas**
- [ ] Cache inteligente de imagens
- [ ] Detecção de emoções
- [ ] Integração com APIs de atores
- [ ] Sistema de tags automáticas

### **Sugeridas**
- [ ] IA para seleção de imagens
- [ ] Banco de imagens local
- [ ] Edição automática de imagens
- [ ] Integração com redes sociais

## 🧪 Testes

### **Executar Testes**
```bash
py -3 test_character_images.py
```

### **Testes Incluídos**
- Detecção de personagens
- Geração de consultas
- Busca de imagens
- Download de arquivos

## 📄 Exemplo Completo

```python
#!/usr/bin/env python3
"""
Exemplo completo de uso do sistema de imagens de personagens
"""

import os
from utility.video.character_image_generator import CharacterImageGenerator

# Configurar APIs
os.environ['PEXELS_KEY'] = 'sua_chave_pexels'

# Inicializar
generator = CharacterImageGenerator()

# Texto do script
script = """
Maria é a protagonista de Dona de Mim e está enfrentando muitos desafios.
O vilão da novela está causando problemas para ela e João.
A mocinha Luna de Fuzuê também está passando por dificuldades.
"""

# Extrair e buscar imagens
character_segments = script.split('.')
for segment in character_segments:
    if segment.strip():
        image_url = generator.get_character_image(segment)
        if image_url:
            filename = f"personagem_{len(character_segments)}"
            generator.download_character_image(image_url, filename)
```

---

**🎭 Torne seus vídeos de novelas mais envolventes com imagens de personagens!** 