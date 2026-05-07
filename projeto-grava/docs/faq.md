# FAQ & Troubleshooting

---

## Erros comuns

### ❌ "Ollama não detectado. Certifique-se de que ele está rodando."

**Causa:** A aplicação tentou conectar em `http://localhost:11434` e não conseguiu.

**Soluções:**
1. Verificar se Ollama está instalado: `ollama --version`
2. Iniciar Ollama em outro terminal: `ollama serve`
3. Aguardar 3-5 segundos (Ollama demora para iniciar)
4. Recarregar a página do Streamlit (F5 ou Ctrl+R)

---

### ❌ "Nenhum dispositivo WASAPI Loopback encontrado"

**Causa:** Você selecionou "Áudio do Sistema" mas o driver de áudio não suporta WASAPI Loopback (só Windows).

**Soluções:**
1. **Verificar drivers:** Painel de Controle → Som → Gravação
   - Procure por "Estéreo Mix" ou "Wave Out Mix"
   - Se não houver: atualizar drivers da placa de som
2. **Alternativa:** Usar modo "Microfone" e gravar manualmente a chamada de vídeo
3. **Último recurso:** VirtualAudio (software de terceiros) como `VB-Audio Virtual Cable`

---

### ❌ `openai.error.AuthenticationError`

**Causa:** Chave OpenAI inválida ou não configurada.

**Soluções:**
1. Verificar `.env` existe no diretório raiz do projeto
2. Verificar que `OPENAI_API_KEY=sk-...` tem um valor válido
3. Remover espaços extras: `OPENAI_API_KEY=sk-xxx` (não `OPENAI_API_KEY = sk-xxx`)
4. Reiniciar a aplicação após alterar `.env`

---

### ❌ `FileNotFoundError: ffmpeg not found`

**Causa:** FFmpeg não está instalado ou não está no PATH.

**Soluções:**
1. **Windows:**
   ```bash
   choco install ffmpeg  # Chocolatey
   # ou
   winget install FFmpeg
   ```
   Depois reiniciar o terminal.

2. **macOS:**
   ```bash
   brew install ffmpeg
   ```

3. **Linux:**
   ```bash
   sudo apt-get install ffmpeg
   ```

4. **Manual (Windows):**
   - Baixar `ffmpeg.exe` de https://ffmpeg.org/download.html
   - Colocar em `src/app/ffmpeg.exe`
   - A aplicação procura lá primeiro, depois no PATH

---

### ❌ `ModuleNotFoundError: No module named 'streamlit'`

**Causa:** Dependências não instaladas.

**Solução:**
```bash
uv sync
# ou
pip install -r requirements.txt
```

---

### ❌ Transcrição está em branco

**Causas possíveis:**
1. **Microfone não estava ativo:** Streamlit pediu permissão e você clicou "Negar"
2. **Áudio muito silencioso:** Whisper não consegue detectar fala
3. **Reunião muito curta:** < 1 segundo de áudio não gera chunks

**Soluções:**
1. Verificar volume do microfone (control panel ou sistema)
2. Recarregar página e permitir microfone
3. Tentar novamente com áudio mais claramente

---

### ❌ Vídeo foi gravado mas sem áudio

**Causa:** FFmpeg falhou ao muxar ou não estava disponível.

**Solução:**
1. Verificar que FFmpeg está no PATH: `ffmpeg -version`
2. Verificar logs do Streamlit (terminal onde rodou `streamlit run`)
3. Se FFmpeg falhar, vídeo e áudio ficam separados (você pode muxar manualmente)

---

### ❌ Resumo gerado mas está em inglês

**Causa:** Modelo Gemma 3.4B às vezes ignora instruções de idioma (bug conhecido).

**Solução:**
1. Usar outro modelo: `llama3.2:3b` ou `mistral:7b`
2. Se quiser continuar com Gemma: ele melhora após atualização do Ollama

---

## Limitações conhecidas

| Limitação | Impacto | Status |
|-----------|---------|--------|
| **Sem speaker diarization** | Não sabe quem falou | Roadmap (item 1) |
| **Transcrição de reunião longa é cortada** | Resumo LLM pode ser incomplete | Roadmap: chunking (item 2) |
| **Sem ação item extraction** | "Quem faz o quê" não é destaque | Roadmap (item 3) |
| **Sem noise reduction** | Ruído de fundo degrada Whisper | Roadmap: `noisereduce` (item 4) |
| **Sem contexto de slides** | LLM não vê o que foi apresentado | Roadmap: OCR (item 5) |
| **Sem RAG cross-meeting** | Não dá pra buscar "em que reunião falamos de X?" | Roadmap (item 6) |
| **Transcrição é async com CPU** | Pode sobrecarregar máquina | Roadmap: async worker (item 7) |
| **Sem pause/resume** | Ou grava tudo ou para | Roadmap (item 8) |
| **Sem marcadores manuais** | Não pode marcar momentos importantes | Roadmap (item 9) |
| **Sem clique em timestamp** | Não pode pular pro vídeo em um momento | Roadmap (item 10) |
| **Sem agenda como input** | Não estrutura resumo por agenda | Roadmap (item 11) |
| **Só captura monitor principal** | Em meeting rooms com projetor secundário: não grava slides | Roadmap (item 12) |
| **Sem PDF export** | Resumo é `.txt` | Roadmap (item 13) |
| **Sem consent screen (LGPD)** | Nenhuma verificação de consentimento | Roadmap (item 14) |
| **Sem cleanup automático** | Disco cheio com o tempo | Roadmap: retention policy (item 15) |

---

## Performance

### Whisper é muito lento

**Causa:** Você está usando um modelo grande (small/medium) ou sua CPU é lenta.

**Soluções:**
1. Usar modelo menor:
   - `tiny` — ~1s de processamento por 10s de áudio
   - `base` (padrão) — ~3s de processamento por 10s
   - `small` — ~10s de processamento por 10s
   - `medium` — ~30s de processamento por 10s

2. Se CPU está no máximo:
   - Fechar outros apps
   - Usar `tiny` ou `base`
   - Aguardar o processamento (é async com a gravação)

### Aplicação travou durante gravação

**Causa:** Whisper + Ollama + screen capture simultâneos podem sobrecarregar.

**Soluções:**
1. Usar modelo menor (`tiny` ou `base`)
2. Desabilitar "Gravar Tela" ou "Gravar Webcam"
3. Usar modo simples de áudio ("Microfone" apenas)
4. Fechar apps pesados (Chrome, VS Code com grandes projetos)

---

## Dúvidas gerais

### P: Onde os arquivos são salvos?

**R:** Em `data/YYYY_MM_DD_HH_MM_SS/`, relativo ao diretório onde você rodou `streamlit run`.

Exemplo: Se você está em `C:\Users\You\projeto-grava\`, os dados ficam em `C:\Users\You\projeto-grava\data\`.

### P: Posso deletar `audio_part_*.mp3` após a gravação?

**R:** Sim. Após gravação terminar, `audio_part_0001.mp3`, `audio_part_0002.mp3`, etc. são redundantes (já foram mergeados em `audio.mp3`).

### P: Posso mover/backup das reuniões?

**R:** Sim. A pasta `data/YYYY_MM_DD_HH_MM_SS/` é auto-contida. Pode copiar/mover inteira.

### P: OpenAI ou Ollama — qual escolher?

| Aspecto | Ollama | OpenAI |
|--------|--------|--------|
| **Custo** | Grátis (CPU/GPU local) | $$ (pay-per-token) |
| **Privacidade** | 100% local | Dados vão para nuvem |
| **Qualidade** | Bom (llama3.2, mistral) | Excelente (GPT-4) |
| **Latência** | 10-30s por reunião | 5-10s (depende internet) |
| **Requisito** | Ollama rodando | Chave + internet |

**Recomendação:** Ollama para 90% dos casos (privacidade, custo). OpenAI se precisar de máxima qualidade.

### P: Posso usar Google Gemini?

**R:** `langchain-google-genai` já está instalado como dependência. Ainda não foi exposto na UI. Planejado para futuro.

### P: Quantas reuniões posso gravar?

**R:** Depende do disco. Cada reunião: ~5-10MB áudio (Whisper) + 20-100MB vídeo (se ativado).

Exemplo: 1TB comporta ~10,000 reuniões (só áudio).

### P: Como limpar dados antigos?

**R:** Manualmente deletar pasta de reunião em `data/`. Planejado: retention policy automática (roadmap item 15).

---

## Roadmap (15 itens)

O que está planejado:

1. ✅ **Speaker diarization** — "João falou isto", "Maria respondeu isto"
2. ✅ **Long-meeting support** — Chunking de transcrição longa para resumo
3. ✅ **Action item extraction** — Destacar "Quem faz o quê até quando"
4. ✅ **Noise reduction** — `noisereduce` library
5. ✅ **Slide context (OCR)** — Ler texto de slides e injetar na transcrição
6. ✅ **RAG cross-meeting search** — "Em que reunião decidimos X?" via FAISS
7. ✅ **Async transcription** — Não bloquear gravação
8. ✅ **Pause & resume** — Pausar sem finalizar sessão
9. ✅ **Manual markers** — Apertar tecla para marcar momento importante
10. ✅ **Clickable timestamps** — Clicar transcrição → pula vídeo
11. ✅ **Meeting agenda input** — Estruturar resumo por agenda
12. ✅ **Multiple monitors** — Capturar monitor secundário (projetor)
13. ✅ **PDF export** — Gerar documento pronto para email
14. ✅ **LGPD consent** — Tela de consentimento antes de gravar
15. ✅ **Storage management** — Auto-cleanup, compressão, quotas

---

## Feedback & Contribuições

Se encontrou bug ou tem sugestão:

- **Abrir issue:** https://github.com/Ricardo-Filgueiras/Agents-ferrametas-AI/issues
- **Pull requests:** Bem-vindos!
- **Email:** contact via GitHub

---

## Recursos adicionais

- [Instalação](instalacao.md)
- [Guia do Usuário](guia-usuario.md)
- [Arquitetura](arquitetura.md)
- [API & Módulos](api-modulos.md)
- [Ollama Documentation](https://ollama.ai/docs)
- [Whisper Documentation](https://github.com/openai/whisper)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Streamlit Documentation](https://docs.streamlit.io)
