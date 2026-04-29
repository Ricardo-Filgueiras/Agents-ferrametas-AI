# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

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
├── utils.py                 # File I/O, Ollama polling, meeting folder enumeration
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

The sidebar exposes three audio modes:

| Mode | Capture | Use case |
|------|---------|----------|
| **Microfone** | WebRTC mic → PyAV container (AAC) | Voice-only meetings |
| **Áudio do Sistema** | WASAPI Loopback → separate MP3 | Record what plays on speakers |
| **🎙️+🔊 Microfone + Sistema** | Both simultaneously → `MixedAudioCapture` → merged MP3 | Capture both sides of a call |

`MixedAudioCapture` buffers mic frames and system chunks independently, overlays them
with `pydub.overlay()` and normalises to 16 kHz mono (optimal for Whisper) every 5 s.

### Data Pipeline

1. **Capture:** Audio frames → 5-second chunks (`audio_part_*.mp3`) + optional screen/webcam frames
2. **Transcribe:** Each chunk transcribed immediately via Faster-Whisper → appended to `transcricao.txt`
3. **Finalize:** All parts merged into `audio.mp3`; video closed; FFmpeg muxes to `reuniao.mp4` (faststart)
4. **Summarize:** User-triggered; full transcript → LLM (LCEL chain) → `resumo.txt` with model attribution

### LLM Layer

- **`LLMFactory.create(provider, model)`** — returns `BaseChatModel`; cached per (provider, model, streaming)
- **`SUMMARY_PROMPT_V1`** — `ChatPromptTemplate` with `{transcricao}` variable
- **`MeetingCallbackHandler`** — logs latency and token usage to `projeto_grava.llm` logger

### Output Structure

```
data/YYYY_MM_DD_HH_MM_SS/
├── titulo.txt        # User-provided meeting title
├── audio.mp3         # Merged audio (all modes)
├── transcricao.txt   # Full transcript (Whisper model noted at end)
├── resumo.txt        # AI summary + agreements (LLM model noted at end)
└── reuniao.mp4       # Muxed video (if screen/webcam capture was active)
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
