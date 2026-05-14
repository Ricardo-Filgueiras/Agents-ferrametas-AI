# Projeto Grava — Gravador de Reuniões Local

Solução local para gravação de reuniões corporativas. Captura tela, webcam e áudio (microfone, sistema ou ambos), transcreve automaticamente com timestamps e gera uma ata com timeline indexada por segundos — tudo offline, sem nenhum dado saindo da máquina.

## Caso de uso

Sala de reunião com slides sendo apresentados e debate entre participantes. O app roda num notebook conectado ao projetor, capturando tela e microfone. Ao fim da reunião, a ata já está pronta com cada decisão indexada ao segundo exato do áudio em que foi tomada.

## Funcionalidades

- **Três modos de áudio** — microfone (WebRTC), áudio do sistema (WASAPI Loopback) ou ambos simultaneamente mesclados
- **Gravação de tela e webcam** — captura em MP4 via MSS + PyAV (H.264)
- **Importação de áudio** — transcreve arquivos M4A / MP3 / WAV existentes
- **Transcrição offline com timestamps** — Faster-Whisper (int8 CPU); cada segmento armazenado com seu segundo exato no áudio original (`[Xs-Ys] texto`)
- **Resumo indexado por tempo** — transcrição dividida em janelas de ~25s; cada janela resumida individualmente e identificada pelo intervalo de segundos (`[0s-25s]`, `[25s-48s]`…) seguida de síntese global
- **Pré-processamento de fala** — remove hesitações e repetições (`ãhn`, `hmm`, `né né né`) antes de enviar ao LLM; preserva termos corporativos em inglês (`call`, `workspace`, `feedback`, `sprint`)
- **Checkpoint de resumo** — cada janela de tempo salva assim que processada; ao refazer o resumo, apenas os trechos que falharam são reprocessados
- **Retry automático** — em caso de queda de conexão com o Ollama, a chamada é repetida uma vez antes de marcar o trecho como não processado
- **Suporte a Ollama e OpenAI** — modelos detectados automaticamente na sidebar
- **Re-transcrição** — refaz a transcrição de uma reunião já gravada com qualquer modelo Whisper
- **Privacidade total** — nenhum dado sai da máquina quando usando Ollama

## Pré-requisitos

- Python 3.12+
- [Ollama](https://ollama.com/) rodando localmente com pelo menos um modelo instalado:
  ```bash
  ollama pull llama3.2
  # ou
  ollama pull gemma3:4b
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
├── titulo.txt               # Título informado antes da gravação
├── audio.mp3                # Áudio completo da reunião
├── reuniao.mp4              # Vídeo da tela ou webcam (se ativado)
├── transcricao.txt          # Transcrição com timestamps por segmento
├── resumo.txt               # Timeline por janela de tempo + síntese global + acordos
└── chunks/                  # Criado ao gerar o resumo
    ├── 0000_0s-25s.txt      # Texto bruto do Whisper para a janela
    ├── 0000_0s-25s_clean.txt # Após remoção de artefatos de fala
    └── 0000_0s-25s_resumo.txt # Resumo da janela (checkpoint)
```

### Formato do resumo

```
[0s-25s]
- Abertura da reunião
- Discussão sobre orçamento Q2

[25s-48s]
- João ficou responsável pelo relatório até sexta

---
Resumo reunião:
- [síntese dos principais assuntos]

Acordos da Reunião:
- João entrega relatório até sexta
```

## Roadmap

Itens estudados e planejados estão em [`.agents/itens-importentes.md`](.agents/itens-importentes.md), incluindo:

- Diarização de falantes (quem disse o quê)
- Extração de itens de ação com responsável e prazo
- OCR nos frames da tela para injetar contexto dos slides na transcrição
- Timestamps clicáveis — clicar na transcrição e o vídeo pular para aquele momento
- Leitura simultânea em tempo real (modo teleprompter)
- Templates de resumo por metodologia (CRISP-DM, Scrum Sprint)
- Pausar e retomar gravação sem encerrar a sessão
- Busca semântica entre reuniões (RAG)
- Exportação de ata em PDF
- Conformidade com LGPD (registro de consentimento)
