# Projeto Grava — Gravador de Reuniões Local

Solução local para gravação de reuniões presenciais em salas corporativas. Captura a tela (slides apresentados), grava o áudio ambiente, transcreve automaticamente e gera uma ata com resumo e itens de ação — tudo offline, sem nenhum dado saindo da máquina.

## Caso de uso

Sala de reunião com 5 pessoas, slides sendo apresentados e debate entre os participantes. O app roda em um notebook conectado ao projetor ou TV da sala, capturando a tela e o microfone. Ao fim da reunião, a ata já está pronta.

## Funcionalidades

- **Gravação de tela** — captura o monitor principal em MP4 via MSS + PyAV (H.264)
- **Gravação de áudio** — captura o microfone via WebRTC em chunks de 5 segundos
- **Transcrição offline** — Faster-Whisper (int8 CPU), modelos tiny / base / small / medium
- **Resumo com IA local** — Ollama + LangChain, modelo detectado automaticamente
- **Suporte a OpenAI** — alternativa de nuvem configurável na sidebar
- **Histórico de reuniões** — navegação, reprodução de vídeo/áudio e geração de resumo retroativo
- **Privacidade total** — nenhum dado sai da máquina quando usando Ollama

## Pré-requisitos

- Python 3.12+
- [Ollama](https://ollama.com/) rodando localmente com pelo menos um modelo instalado:
  ```bash
  ollama pull llama3.2
  ```
- FFmpeg disponível no PATH (ou `ffmpeg.exe` na pasta `src/app/`)

## Instalação

```bash
git clone https://github.com/Ricardo-Filgueiras/Agents-ferrametas-AI.git
cd Agents-ferrametas-AI/projeto-grava
uv sync
```

Ou via pip:
```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha `OPENAI_API_KEY` apenas se for usar o provedor OpenAI.

## Execução

```bash
streamlit run src/app/main.py
```

Acesse `http://localhost:8501`. Configure o modelo Whisper e o provedor de resumo na sidebar antes de gravar.

## Saída por reunião

```
data/YYYY_MM_DD_HH_MM_SS/
├── titulo.txt        # Título informado antes da gravação
├── audio.mp3         # Áudio completo da reunião
├── reuniao.mp4       # Vídeo da tela (se captura de tela ativada)
├── transcricao.txt   # Transcrição completa com modelo utilizado
└── resumo.txt        # Resumo + acordos da reunião com modelo utilizado
```

## Roadmap

Itens estudados e planejados estão em [`.agents/itens-importentes.md`](.agents/itens-importentes.md), incluindo:

- Diarização de falantes (quem disse o quê)
- Extração de itens de ação
- Suporte a reuniões longas (chunking de transcrição)
- Marcadores manuais durante a gravação
- Exportação de ata em PDF
- Conformidade com LGPD (registro de consentimento)
- Busca entre reuniões via RAG
