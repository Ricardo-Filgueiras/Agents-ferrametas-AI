# 🎥 Projeto Grava: MeetGPT Local

O **Projeto Grava** é uma solução de "MeetGPT" 100% local e focada em privacidade. Ele permite capturar áudio e vídeo de reuniões, transcrever o conteúdo de forma automatizada e gerar resumos inteligentes utilizando modelos de IA rodando localmente.

## ✨ Funcionalidades

- **Gravação Local:** Captura de tela e janelas diretamente para formato MP4 via `PyAV`.
- **Transcrição Offline:** Utiliza o `faster-whisper` para converter áudio em texto sem enviar dados para a nuvem.
- **Resumos com IA:** Integração com **Ollama** e **LangChain** para análise de conteúdo e geração de atas de reunião.
- **Transparência de Modelos:** Identificação automática do modelo utilizado tanto na transcrição quanto no resumo gerado.
- **Privacidade Total:** Processamento local garante que nenhuma informação sensível saia da sua máquina.

## 🛠️ Tecnologias Utilizadas

- **Interface:** [Streamlit](https://streamlit.io/)
- **Processamento de Mídia:** [PyAV (FFmpeg)](https://pyav.org/)
- **Transcrição:** [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
- **Modelos de Linguagem (LLM):** [Ollama](https://ollama.com/) & [LangChain](https://www.langchain.com/)
- **Gerenciamento de Pacotes:** [UV](https://github.com/astral-sh/uv)

## 📂 Estrutura do Projeto

```text
projeto-grava/
├── data/               # Arquivos gerados (vídeos, áudios, transcrições)
│   └── YYYY_MM_DD_HH_MM_SS/
│       ├── audio.mp3       # Áudio completo da reunião
│       ├── reuniao.mp4     # Vídeo da reunião (opcional)
│       ├── transcricao.txt # Texto transcrito com nota do modelo
│       └── resumo.txt      # Resumo inteligente com nota do modelo
├── src/
│   ├── app/            # Código fonte da aplicação principal
│   │   └── main.py     # Ponto de entrada Streamlit
│   └── aprendizado/    # Documentação, estudos e protótipos
├── main.py             # Script de entrada (wrapper)
├── pyproject.toml      # Configurações do projeto e dependências
└── requirements.txt    # Lista de dependências legada
```

## 🚀 Como Começar

### Pré-requisitos

1.  **Python 3.12+**
2.  **Ollama** instalado e rodando (para os resumos).
    *   Para baixar um modelo novo: `ollama pull llama3.2` ou `ollama pull gemma2`.

### Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/Ricardo-Filgueiras/Agents-ferrametas-AI.git
    cd Agents-ferrametas-AI/projeto-grava
    ```

2.  Instale as dependências (recomendado usar `uv`):
    ```bash
    uv sync
    ```
    *Ou via pip:*
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure o arquivo `.env` (use o `.env.example` como base).

### Execução

Para iniciar a interface do projeto:

```bash
streamlit run src/app/main.py
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
