# Instalação & Setup

## Pré-requisitos

| Requisito | Versão | Nota |
|-----------|--------|------|
| **Python** | 3.12+ | Verificar com `python --version` |
| **Ollama** | Qualquer | Para IA local (alternativa: OpenAI na nuvem) |
| **FFmpeg** | Qualquer | Para muxar áudio em vídeo |
| **Git** | Qualquer | Para clonar o repositório |

### Windows: Instalação de Ollama e FFmpeg

**Ollama:**
```bash
# Baixar em https://ollama.ai/download
# Instalar e validar
ollama --version
```

**FFmpeg:**
```bash
# Via Chocolatey (recomendado)
choco install ffmpeg

# Ou via winget
winget install FFmpeg

# Validar
ffmpeg -version
```

Se FFmpeg não estiver no PATH, coloque `ffmpeg.exe` na pasta `src/app/` do projeto.

### macOS / Linux

```bash
# macOS (Homebrew)
brew install ollama ffmpeg

# Linux (apt, exemplo Ubuntu/Debian)
sudo apt-get install ollama ffmpeg
```

---

## Instalação do Projeto

### 1. Clonar repositório

```bash
git clone https://github.com/Ricardo-Filgueiras/Agents-ferrametas-AI.git
cd Agents-ferrametas-AI/projeto-grava
```

### 2. Instalar dependências (com `uv` — recomendado)

```bash
# Se não tiver uv, instalar primeiro
pip install uv

# Instalar dependências do projeto
uv sync
```

**Alternativa com `pip` (legado):**
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copiar `.env.example` para `.env`:

```bash
cp .env.example .env
```

Editar `.env` e adicionar sua chave do OpenAI (apenas se quiser usar OpenAI em vez de Ollama):

```
OPENAI_API_KEY=sua_chave_aqui
```

Se usar apenas Ollama, pode deixar em branco ou comentado.

### 4. Baixar modelos Ollama

Antes de rodar a aplicação, baixe pelo menos um modelo:

```bash
# Recomendado: llama3.2 (7B, balanceado)
ollama pull llama3.2

# Alternativa: gemma3:4b (mais rápido, menor)
ollama pull gemma3:4b

# Ou médium: mistral (7B, código-friendly)
ollama pull mistral
```

Listar modelos disponíveis:
```bash
ollama list
```

---

## Executar a aplicação

### Passo 1: Iniciar Ollama (em um terminal separado)

```bash
ollama serve
```

Deixe este terminal aberto. A API estará em `http://localhost:11434`.

### Passo 2: Rodar a aplicação

Em outro terminal, na pasta do projeto:

```bash
streamlit run src/app/main.py
```

A aplicação abrirá em `http://localhost:8501` (ou mostrará a URL no terminal).

---

## Primeiro uso

1. **Sidebar — Configurar:**
   - **Provedor AI:** Selecionar "Ollama (Local)" ou "OpenAI"
   - **Modelo Ollama:** Escolher o modelo que foi baixado (ex: `llama3.2:3b`)
   - **Modelo Whisper:** Deixar como "base" (bom balanço velocidade/qualidade)
   - **Fonte de áudio:** Selecionar "Microfone"

2. **Tab "Gravar Reunião":**
   - Digitar o título da reunião (opcional)
   - Clicar no botão **⭕ Clique para iniciar** (será vermelho/pulsante)
   - A gravação começará; você verá "REC" no topo

3. **Gravando:**
   - A transcrição aparece em tempo real
   - Pressione novamente para parar

4. **Após gravar:**
   - A aplicação redireciona automaticamente para a aba **"Histórico"**
   - Seu vídeo e transcrição estão em `data/YYYY_MM_DD_HH_MM_SS/`

---

## Solução de problemas de instalação

### ❌ `ModuleNotFoundError: No module named 'streamlit'`

Você não rodou `uv sync` ou `pip install`. Execute o comando de instalação acima.

### ❌ `FileNotFoundError: ffmpeg not found`

FFmpeg não está instalado ou não está no PATH. Opções:
1. Instalar via gerenciador (veja Pré-requisitos)
2. Baixar executável e colocar em `src/app/ffmpeg.exe` (Windows)
3. Adicionar ao PATH do sistema

### ❌ `ConnectionError: Failed to connect to http://localhost:11434`

Ollama não está rodando. Abra um terminal e execute:
```bash
ollama serve
```

### ❌ `openai.error.AuthenticationError`

Sua chave OpenAI está errada ou não está configurada. Verificar:
1. `.env` existe no diretório raiz do projeto
2. `OPENAI_API_KEY=` tem um valor válido
3. A aplicação Streamlit foi reiniciada após alterar `.env`

### ❌ Python version error

Você tem Python < 3.12. Instale Python 3.12+ ou use um gerenciador como `pyenv` ou `conda`.

---

## Próximos passos

Veja [Guia do Usuário](guia-usuario.md) para entender como usar a aplicação.
