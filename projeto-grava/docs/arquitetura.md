# Arquitetura

## Visão geral da camada

```
┌─────────────────────────────────────────────────────┐
│  UI Layer (Streamlit)                               │
│  src/app/main.py — interface, tabs, sidebar         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  LLM & Services Layer                               │
│  src/app/ia_models.py — transcrição + resumo       │
│  src/app/llm/ — factory, prompts, callbacks         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Storage & Data Layer                               │
│  src/app/storage/ — CRUD de reuniões               │
│  src/app/utils.py — I/O de arquivos                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Capture & Codec Layer (paralelo)                   │
│  src/app/capture/ — áudio, vídeo, tela              │
└─────────────────────────────────────────────────────┘
```

---

## Estrutura de módulos

```
src/app/
├── main.py
│   ├── tab_grava_reuniao()     — UI gravação
│   ├── tab_selecao_reuniao()   — UI histórico
│   ├── _transcrever_e_salvar() — pipeline de transcrição
│   └── _muxar_audio_no_video() — FFmpeg muxing
│
├── ia_models.py
│   ├── carregar_whisper()      — cache do Whisper
│   ├── transcreve_audio()      — chunk → transcrição
│   └── gerar_resumo()          — LCEL chain para IA
│
├── utils.py
│   ├── le_arquivo()            — lê arquivo → string
│   ├── salva_arquivo()         — escreve arquivo
│   ├── listar_modelos_ollama() — poll HTTP Ollama
│   ├── listar_reunioes()       — enumera data/
│   └── ...
│
├── llm/
│   ├── factory.py              — LLMFactory.create()
│   ├── prompts.py              — ChatPromptTemplate versionadas
│   └── callbacks.py            — MeetingCallbackHandler
│
├── capture/
│   ├── audio.py                — WebRTC mic → pydub
│   ├── video.py                — frames → H.264 MP4
│   ├── system_audio.py         — WASAPI Loopback
│   ├── mixed_audio.py          — overlay mic + system
│   ├── printela.py             — screen capture MSS
│   └── __init__.py
│
└── storage/
    └── meeting_repository.py    — CRUD de reuniões
```

---

## Pipeline de captura

### Audio

#### Modo Microfone

```
Browser (WebRTC)
    ↓
PyAV container (AAC)
    ↓
pydub AudioSegment [5s chunks]
    ↓
Arquivo: audio_part_0001.mp3, audio_part_0002.mp3, ...
    ↓
Merge via pydub concatenate()
    ↓
audio.mp3 (arquivo final)
```

#### Modo Sistema (WASAPI Loopback, Windows)

```
Speaker out (Windows)
    ↓
pyaudiowpatch (WASAPI Loopback capture)
    ↓
pydub AudioSegment [5s chunks]
    ↓
audio_part_*.mp3
    ↓
audio.mp3
```

#### Modo Misto (Microfone + Sistema)

```
Mic ────────────────────┐
                        │ pydub.overlay() (a cada 5s)
System ─────────────────┤ Normaliza → 16 kHz mono
                        ↓
                    audio_part_*.mp3
                        ↓
                    audio.mp3
```

### Vídeo

```
Tela (MSS) ou Webcam (WebRTC)
    ↓
Frames BGR/RGB [x, y, 3]
    ↓
PyAV encoding (H.264, ultrafast + zerolatency)
    ↓
*.mp4 sem áudio (vídeo mudo)
    ↓
FFmpeg mux: vídeo + audio.mp3
    ↓
reuniao.mp4 (faststart para streaming)
```

---

## Pipeline de transcrição

```
1. CAPTURA (paralelo em background)
   ├─ Audio frames → pydub chunks (5s)
   ├─ Tela/webcam frames → PyAV container
   └─ Salva arquivo: audio_part_NNNN.mp3

2. TRANSCRIÇÃO (on-the-fly)
   ├─ Lê audio_part_NNNN.mp3
   ├─ Faster-Whisper (modelo: tiny/base/small/medium)
   ├─ Retorna texto
   └─ Append a transcricao.txt

3. FINALIZAÇÃO (ao parar)
   ├─ Merge audio_part_*.mp3 → audio.mp3
   ├─ Close vídeo container
   ├─ FFmpeg mux audio + vídeo → reuniao.mp4
   └─ Salva transcricao.txt final

4. RESUMO (user-triggered)
   ├─ Lê transcricao.txt completa
   ├─ LCEL chain: SUMMARY_PROMPT_V1 | LLM
   ├─ LLM (Ollama ou OpenAI) retorna resumo
   └─ Salva resumo.txt
```

---

## Pipeline de IA (LCEL)

### Resumo de reunião

```
Input: transcricao (texto completo)

ChatPromptTemplate.from_messages([
    SystemMessage("Você é especialista em análise de reuniões..."),
    HumanMessage("Analise a transcrição:\n{transcricao}")
])
    ↓
Invoke: {"transcricao": texto_lido}
    ↓
LLM (ChatOllama ou ChatOpenAI) com callbacks
    ↓
Response: (resumo + acordos)
    ↓
Salva em resumo.txt
```

### Callbacks

Durante a invocação LCEL, `MeetingCallbackHandler` loga:
- **Latência** — tempo da chamada LLM
- **Tokens** — input + output tokens (se disponível)
- **Erros** — exceções capturadas

Logs vão para `logger("projeto_grava.llm")`.

---

## LLMFactory

```python
LLMFactory.create(
    provider="Ollama (Local)" ou "OpenAI",
    model="llama3.2:3b" ou "gpt-4o-mini",
    streaming=False
)
    ↓
Normaliza UI name → chave interna (via UI_TO_KEY)
    ↓
Dispatch a _criar_ollama() ou _criar_openai()
    ↓
Chamada cached (@lru_cache) — evita recriar clientes
    ↓
Retorna BaseChatModel (LangChain)
```

**Cache:** Até 8 combinações (provider, model, streaming).

---

## Decisões arquiteturais

| Decisão | Razão |
|---------|-------|
| **Chunks de 5s** | Whisper rápido, feedback ao vivo, recuperável se crash |
| **PyAV + H.264** | Codec universal, baixo overhead, suporta streaming |
| **LCEL (não plain prompts)** | Versionamento, tipagem, compatível com streaming futuro |
| **LLMFactory com cache** | Evita recriar conexões caras, suporta troca dinâmica provider/modelo |
| **Sem banco de dados** | Simple, local-first, sem dependências extras |
| **WASAPI (só Windows)** | Única forma de capturar system audio em Windows |
| **Ollama por padrão** | Privacidade, offline, nenhuma chave necessária |

---

## Fluxo da gravação (dia a dia)

```
1. User abre app
   → Sidebar detecta Ollama em http://localhost:11434
   → Carrega modelos disponíveis via /api/tags

2. User clica "Gravar"
   → WebRTC abre acesso ao mic
   → MSS começa capturar tela (se ativado)
   → Inicia loop de captura

3. Loop de captura (enquanto recording)
   → A cada 5s: export audio_part_NNNN.mp3
   → Whisper transcreve chunk
   → Append transcricao.txt
   → UI mostra transcrição ao vivo

4. User clica "Parar"
   → Finaliza WebRTC e captura
   → Merge audio_part_* → audio.mp3
   → Close vídeo e FFmpeg mux
   → Salva metadata (título, timestamps)
   → Auto-redirect para Histórico

5. Histórico: User clica "Gerar Resumo"
   → Lê transcricao.txt
   → Cria LCEL chain
   → Invoca LLM (Ollama ou OpenAI)
   → MeetingCallbackHandler loga latência
   → Salva resumo.txt

6. Reunião armazenada em data/YYYY_MM_DD_HH_MM_SS/
   → titulo.txt
   → audio.mp3
   → transcricao.txt
   → resumo.txt
   → reuniao.mp4 (se tela/webcam)
```

---

## Dependências principais

| Pacote | Função |
|--------|--------|
| `streamlit` | Framework UI |
| `streamlit-webrtc` | Acesso ao mic/webcam |
| `faster-whisper` | Transcrição local |
| `av` | PyAV, containers áudio/vídeo |
| `pydub` | Processamento e merge de áudio |
| `opencv-python` | Manipulação de frames |
| `mss` | Screen capture |
| `pyaudiowpatch` | WASAPI Loopback (Windows) |
| `langchain-core` | LCEL e abstrações |
| `langchain-ollama` | Ollama integration |
| `langchain-openai` | OpenAI integration |
| `ollama` | Cliente Python Ollama |
| `openai` | Cliente Python OpenAI |
| `faiss-cpu` | RAG (pronto, não usado ainda) |

---

## Roadmap arquitetural

Veja [FAQ — Roadmap](faq.md) para as 15 melhorias planejadas.

Principais categorias:
- **Processamento:** Speaker diarization, noise reduction, OCR em slides
- **Escalabilidade:** Async transcription, chunking para reuniões longas
- **UX:** Pause/resume, timestamps clicáveis, PDF export
- **Privacidade/Compliance:** Consent logging (LGPD)
- **RAG:** Cross-meeting search (FAISS já instalado)

---

## Próximos passos

- [API & Módulos](api-modulos.md) — Detalhes de cada classe/função pública
- [FAQ](faq.md) — Troubleshooting e limites conhecidos
