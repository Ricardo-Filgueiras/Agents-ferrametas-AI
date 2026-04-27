# 🌌 Nova Agent

**Nova Agent** é um assistente de inteligência artificial modular projetado para interação por voz e texto em tempo real. O sistema integra tecnologias avançadas de **Speech-to-Text (STT)**, **Text-to-Speech (TTS)** e processamento de linguagem natural (LLM) para criar uma experiência de agente autônomo e responsivo.

## 🚀 Funcionalidades Principais

-   **🎙️ Speech-to-Text (STT):** Transcrição de áudio em tempo real utilizando `Faster-Whisper` com suporte a quantização `int8` para alta performance em CPU.
-   **🗣️ Text-to-Speech (TTS):** Geração de voz natural com `Kokoro TTS` e suporte a motores legados como `pyttsx3`.
-   **🧠 Inteligência Artificial:** Integração via LangChain com modelos locais (**Ollama**) e na nuvem (**Google Gemini**).
-   **🖥️ Dashboard TUI:** Interface de terminal rica e responsiva desenvolvida com a biblioteca `Rich`.
-   **🛠️ Arquitetura Orientada a Estado:** Gerenciamento centralizado do estado do agente para coordenação entre áudio, lógica e interface.

## 📂 Estrutura do Projeto

```text
projeto-nova/
├── app/                # Core da aplicação
│   ├── core/           # Engine principal e gerenciamento de estado
│   ├── ui/             # Interface de usuário (Dashboard TUI)
│   ├── stt/            # Implementação de Speech-to-Text (Whisper)
│   ├── audio/          # Manipulação e gravação de áudio
│   └── providers/      # Integrações com LLMs (Ollama, Gemini)
├── tts/                # Scripts e utilitários de Text-to-Speech
│   ├── audio-to-texto.py # Script de transcrição independente
│   └── kokoro_basic.py   # Exemplo de uso do Kokoro TTS
├── models/             # Diretório para armazenamento de modelos locais
├── scripts/            # Scripts de manutenção e configuração
├── main.py             # Ponto de entrada principal do sistema
├── .env.example        # Modelo de variáveis de ambiente
└── pyproject.toml      # Configuração de dependências (UV)
```

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python 3.10+
-   **Gerenciador de Pacotes:** [uv](https://github.com/astral-sh/uv)
-   **STT:** Faster-Whisper
-   **TTS:** Kokoro TTS, pyttsx3
-   **LLM Framework:** LangChain (Ollama, Google GenAI)
-   **UI:** Rich (Terminal UI)

## 🔧 Configuração e Instalação

### Pré-requisitos
-   Python instalado (recomendado 3.10 ou superior).
-   `ffmpeg` instalado no sistema (necessário para processamento de áudio).
-   [uv](https://github.com/astral-sh/uv) instalado para gerenciamento rápido de pacotes.

### Passo a Passo

1.  **Clonar o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/projeto-nova.git
    cd projeto-nova
    ```

2.  **Configurar variáveis de ambiente:**
    Copie o arquivo `.env.example` para `.env` e preencha suas chaves de API e configurações:
    ```bash
    cp .env.example .env
    ```

3.  **Instalar dependências:**
    ```bash
    uv sync
    ```

4.  **Executar o Agente:**
    ```bash
    python main.py
    ```

## 📝 Scripts Utilitários

Na pasta `tts/`, você encontrará ferramentas independentes:
-   **Audio para Texto:** `python tts/audio-to-texto.py <arquivo_de_audio>` - Transcreve um áudio específico e gera um arquivo `.md`.

---
*Desenvolvido por Agents-ferrametas-AI*
