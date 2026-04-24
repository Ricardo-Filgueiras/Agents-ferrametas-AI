# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (preferred)
uv sync

# Run the application
streamlit run src/app/main.py

# Install via pip (legacy)
pip install -r requirements.txt
```

There is no test suite. Validation is done by running the app and recording a test meeting.

## Architecture

**Projeto-Grava** is a local-first meeting recorder: it captures audio/video, transcribes speech with Whisper (offline), and generates summaries via Ollama or OpenAI. All processing is local by default — no data leaves the machine.

### Module Overview (`src/app/`)

| Module | Role |
|--------|------|
| `main.py` | Streamlit entry point; two-tab UI (Record / History); orchestrates capture loop |
| `audio.py` | Converts WebRTC audio frames → pydub segments; muxes into PyAV container (AAC) |
| `video.py` | Converts BGR/RGB frames → YUV420p; H.264 encoding (ultrafast, zerolatency); handles PTS sync |
| `printela.py` | Thread-safe MSS screen capture; bounded frame queue at 15 FPS; drops oldest frame when full |
| `ia_models.py` | Whisper transcription (int8 CPU); OpenAI/Ollama chat; summary prompt template |
| `utils.py` | UTF-8 file I/O; Ollama model polling (`localhost:11434`); meeting folder enumeration |

### Data Pipeline

1. **Capture:** WebRTC audio frames → 5-second MP3 chunks (`audio_part_*.mp3`) + optional screen frames queued to PyAV container
2. **Transcribe:** Each chunk transcribed immediately → appended to `transcricao.txt` (live in UI)
3. **Finalize:** All parts merged into `audio.mp3`; video container closed; FFmpeg remuxes to `reuniao.mp4` with moov atom at start (faststart)
4. **Summarize:** User-triggered; full transcript → LLM → `resumo.txt` with model attribution

### Output Structure

Each recording is saved to a timestamped folder:
```
data/YYYY_MM_DD_HH_MM_SS/
├── titulo.txt        # User-provided meeting title
├── audio.mp3         # Merged audio
├── transcricao.txt   # Full transcript (Whisper model noted at end)
├── resumo.txt        # AI summary + agreements (LLM model noted at end)
└── reuniao.mp4       # Muxed video (if screen capture was active)
```

## Runtime Configuration

Configured in the Streamlit sidebar at runtime:
- **AI Provider:** Ollama (Local) or OpenAI
- **Ollama Model:** Auto-detected from `http://localhost:11434/api/tags`
- **Whisper Model:** tiny / base / small / medium (default: base)

## Environment

Copy `.env.example` to `.env` and set `OPENAI_API_KEY` only if using OpenAI as the summary provider. Ollama requires the `ollama` service running locally (`ollama pull llama3.2` or `gemma3:4b`).

**Python version:** 3.12 (see `.python-version`)
