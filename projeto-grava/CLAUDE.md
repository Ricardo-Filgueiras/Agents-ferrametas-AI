# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the application
streamlit run src/app/main.py

# Install via pip (legacy)
pip install -r requirements.txt
```

There is no test suite. Validation is done by running the app and recording a test meeting.

## Architecture

**Projeto-Grava** is a local-first meeting recorder: captures audio/video, transcribes speech
with Whisper (offline), and generates summaries via Ollama or OpenAI. All processing is local
by default — no data leaves the machine.

### Module Overview (`src/app/`)

```
src/app/
├── main.py                  # Streamlit entry point — UI only, no AI logic
├── ia_models.py             # Whisper transcription + LLM summary (uses llm/ layer)
├── utils.py                 # File I/O, Ollama polling, meeting folder enumeration, limpar_transcricao()
│
├── capture/                 # Audio/video capture layer
│   ├── audio.py             # WebRTC audio frames → pydub / PyAV container (AAC)
│   ├── video.py             # BGR/RGB frames → YUV420p H.264 (ultrafast, zerolatency)
│   ├── printela.py          # Thread-safe MSS screen capture at 15 FPS
│   ├── system_audio.py      # WASAPI Loopback capture (Windows) via pyaudiowpatch
│   └── mixed_audio.py       # Simultaneous mic + system audio → merged pydub chunks
│
├── llm/                     # LLM abstraction layer
│   ├── factory.py           # LLMFactory(provider, model) with lru_cache
│   ├── prompts.py           # Versioned ChatPromptTemplate definitions
│   └── callbacks.py         # MeetingCallbackHandler — latency/token logging
│
└── storage/
    └── meeting_repository.py  # CRUD over timestamped meeting folders
```

### Audio Source Modes

| Mode | Capture | Use case |
|------|---------|----------|
| **Microfone** | WebRTC mic → PyAV container (AAC) | Voice-only meetings |
| **Áudio do Sistema** | WASAPI Loopback → separate MP3 | Record what plays on speakers |
| **🎙️+🔊 Microfone + Sistema** | Both simultaneously → `MixedAudioCapture` → merged MP3 | Capture both sides of a call |

`MixedAudioCapture` buffers mic frames and system chunks independently, overlays them
with `pydub.overlay()` and normalises to 16 kHz mono (optimal for Whisper) every 5 s.

### Data Pipeline

1. **Capture:** Audio frames → 5-second chunks (`audio_part_*.mp3`) + optional screen/webcam frames
2. **Transcribe:** Each chunk transcribed via Faster-Whisper with an absolute time offset → appended to `transcricao.txt` as timestamped lines: `[Xs-Ys] texto`
3. **Finalize:** All parts merged into `audio.mp3`; video closed; FFmpeg muxes to `reuniao.mp4` (faststart)
4. **Summarize:** User-triggered — groups transcript into ~25s time windows, preprocesses each window with `limpar_transcricao()`, calls LLM per window (MAP), then a final REDUCE call produces the global summary + agreements

### Transcript Format

`transcricao.txt` stores one Whisper segment per line with absolute audio timestamps:

```
[0s-3s] Bom dia a todos.
[3s-8s] Vamos começar discutindo o call de ontem.
[8s-15s] O workspace ainda está com problema de acesso.
```

During live recording, the offset is tracked via `audio_offset_seg` in `main.py` (incremented by each chunk's pydub duration). During re-transcription (`retranscrever_reuniao`), Whisper runs over the full `audio.mp3` so timestamps are naturally absolute.

### Summarization Strategy

`gerar_resumo()` in `ia_models.py` has two paths:

**Primary — timestamped transcripts (new recordings):**
1. `_agrupar_por_janela_tempo()` parses `[Xs-Ys]` lines and groups into ≤25s windows
2. Each window is saved as a raw file and a cleaned file (via `limpar_transcricao()`)
3. LLM summarizes each window → saved immediately to `chunks/NNNN_Xs-Ys_resumo.txt`
4. A final REDUCE call synthesises all window summaries into global summary + agreements
5. Checkpoint: if `_resumo.txt` already exists for a window, it is reused — retrying a failed summary only reprocesses failed windows

**Fallback — transcripts without timestamps (old recordings):**
- ≤10 000 chars: single LLM call
- >10 000 chars: `RecursiveCharacterTextSplitter` map-reduce (sequential, Ollama-safe)

### Preprocessing (`utils.limpar_transcricao`)

Applied to each chunk before the LLM call. Targets speech artifacts only — does **not** filter by language (corporate English loanwords like `call`, `workspace`, `feedback`, `sprint` are preserved):

- `_HESITACOES`: removes standalone hesitation sounds (`ãhn`, `ahh`, `hmm`, `hmmm`, …)
- `_REPETICOES`: collapses a word repeated 3+ times in a row (`né né né` → `né`)

### LLM Layer (`llm/`)

- **`LLMFactory.create(provider, model)`** — returns `BaseChatModel`; cached per `(provider, model, streaming)` via `lru_cache`
- **`SUMMARY_PROMPT_V1`** — full-transcript summary, `{transcricao}` variable (fallback path)
- **`CHUNK_SUMMARY_PROMPT_V1`** — character-based chunk summary (fallback map phase)
- **`TIME_CHUNK_PROMPT_V1`** — summarises a single time window, vars `{inicio}`, `{fim}`, `{trecho}`
- **`TIMELINE_REDUCE_PROMPT_V1`** — consolidates a complete timeline into "Resumo reunião" + "Acordos da Reunião", var `{timeline}`
- **`MEETING_QA_PROMPT_V1`** — RAG Q&A over meeting history, vars `{context}`, `{question}`
- **`MeetingCallbackHandler`** — logs latency and token usage to `projeto_grava.llm` logger

### Output Structure

```
data/YYYY_MM_DD_HH_MM_SS/
├── titulo.txt               # User-provided meeting title
├── audio.mp3                # Merged audio (all modes)
├── transcricao.txt          # Full transcript with [Xs-Ys] timestamps per segment
├── resumo.txt               # Timeline blocks + global summary + agreements
├── reuniao.mp4              # Muxed video (if screen/webcam capture was active)
└── chunks/                  # Created on first "Gerar Resumo"
    ├── 0000_0s-25s.txt      # Raw Whisper text for the window
    ├── 0000_0s-25s_clean.txt # After limpar_transcricao()
    ├── 0000_0s-25s_resumo.txt # LLM output for the window (checkpoint)
    ├── 0001_25s-48s.txt
    └── ...
```

## Runtime Configuration

Configured in the Streamlit sidebar at runtime:
- **AI Provider:** Ollama (Local) or OpenAI
- **Ollama Model:** Auto-detected from `http://localhost:11434/api/tags`
- **Whisper Model:** tiny / base / small / medium (default: base)
- **Audio Source:** Microfone | Áudio do Sistema | Microfone + Sistema

## Environment

Copy `.env.example` to `.env` and set `OPENAI_API_KEY` only if using OpenAI as the summary
provider. Ollama requires the `ollama` service running locally (`ollama pull llama3.2` or `gemma3:4b`).

**Python version:** 3.12 (see `.python-version`)
**Package manager:** UV — always use `uv sync` to install/update dependencies.
