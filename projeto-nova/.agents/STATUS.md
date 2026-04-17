# ✅ 1. REQUISITOS DE SISTEMA

## 🔧 Hardware (Confirmado)
- CPU: Intel i5 9ª geração (OK)
- GPU: GTX 1660 Super (6GB VRAM) (OK - Suporte CUDA Habilitado)
- RAM: 16GB (OK)

---

## 🐳 Infraestrutura (Docker)
- [x] Dockerfile com `nvidia/cuda:11.8.0` (OK)
- [x] Docker Compose com GPU Reservations (OK)
- [x] Volume para Ollama Models (OK)
- [x] Mapeamento `/dev/snd` para áudio (OK)

---

# 🚀 STATUS DO DESENVOLVIMENTO

## ✅ Fase 1: Fundação Modular (CONCLUÍDO)
- [x] **Core:** Criação de `BaseSTT`, `BaseLLM`, `BaseTTS`.
- [x] **State:** Refatoração do `AgentState` com sistema de notificações.
- [x] **Controller:** Centralização da lógica LCEL e Memória.
- [x] **Providers:** Implementação Whisper (GPU), Ollama e Piper.
- [x] **Configuração:** Idioma pt-BR e modelos Qwen2.5/Piper-Faber definidos.

## ✅ Fase 2: Hardware e Integração (CONCLUÍDO)
- [x] **Audio:** Implementação do `AudioListener` (PyAudio + Wake Word).
- [x] **Audio:** Implementação do `AudioSpeaker` (ffplay).
- [x] **Engine:** Orquestrador Slim integrando todos os módulos.
- [x] **Observabilidade:** TUI (Rich) e Logs em arquivo (`nova.log`).

---

## 📄 COMPONENTES (Checklist Detalhado)

### **app/core/**
- [x] `base.py` (Interfaces)
- [x] `controller.py` (Cérebro LCEL + pt-BR)
- [x] `engine.py` (Orquestrador Slim v2)
- [x] `state.py` (Estado de observabilidade)

### **app/providers/**
- [x] `stt_whisper.py` (CUDA float16 enabled)
- [x] `llm_ollama.py` (LangChain Ollama Connector)
- [x] `tts_piper.py` (Geração WAV via CLI)

### **app/audio/**
- [x] `listener.py` (Wake Word "Nova")
- [x] `speaker.py` (Execução WAV via ffplay)

---

## 🚩 PRÓXIMOS PASSOS CRÍTICOS
1. **Modelos:** Baixar `pt_BR-faber-medium.onnx` e `.json` para a pasta `models/`.
2. **Build Docker:** Executar o `docker-compose up --build` para validar drivers NVIDIA e acesso ao som.
3. **VAD:** (Opcional) Refinar detecção de silêncio para comandos de duração variável.

## 🧠 Estado Final Esperado (v2)
- Sistema 100% funcional, modular e brasileiro. 🇧🇷
