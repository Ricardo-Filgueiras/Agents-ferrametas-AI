# Guia do Usuário

## Visão geral

Projeto-Grava tem **duas abas principais**:

1. **🔴 Gravar Reunião** — Captura áudio, vídeo e tela
2. **📂 Histórico** — Acessa gravações anteriores, reproduz e gera atas

Antes de gravar, configure a aplicação via **Sidebar** na esquerda.

---

## Sidebar — Configuração

A sidebar (esquerda) tem todos os controles de configuração:

### Provedor de IA

**Opções:**
- **Ollama (Local)** — LLM executa na sua máquina (privado, precisa Ollama rodando)
- **OpenAI** — Usa API da OpenAI (requer chave no `.env`)

### Modelo Ollama

Aparece apenas se "Ollama (Local)" for selecionado.

**Modelos recomendados:**
- `llama3.2:3b` — Rápido, boa qualidade (padrão)
- `gemma3:4b` — Muito rápido, menor
- `mistral:7b` — Mais inteligente, mais lento
- `neural-chat:7b` — Especializado em conversação

Se nenhum modelo aparecer: **Ollama não está rodando.** Abra um terminal e execute:
```bash
ollama serve
```

### Modelo Whisper

Para transcrição automática (conversão fala → texto).

**Opções (maior = mais preciso, mais lento):**
- `tiny` — Muito rápido, menos preciso (~1s por 10s de áudio)
- `base` — Padrão, bom balanço (default)
- `small` — Mais preciso, 2-3x mais lento
- `medium` — Muito preciso, 4x mais lento

**Dica:** Use `base` para a maioria. Use `tiny` se a CPU for lenta.

### Fonte de Áudio

| Opção | O que grava | Uso |
|-------|-----------|-----|
| **🎤 Microfone** | Seu microfone | Reuniões presenciais |
| **🔊 Áudio do Sistema** | Som que sai no alto-falante | Chamadas, webinar |
| **🎙️+🔊 Microfone + Sistema** | Ambos simultaneamente | Chamadas onde ambas as pessoas são capturadas |

**⚠️ Windows:** Modo sistema requer WASAPI Loopback. Se não encontrar, atualize seus drivers de áudio.

---

## Tab: Gravar Reunião

### Preparação

1. **Título (opcional):**
   - Campo de texto: Digite o título da reunião
   - Exemplo: "Planning Q2 2026"
   - Pode deixar em branco; será preenchido com timestamp

2. **Opções de vídeo (checkboxes):**
   - ☑️ **Gravar Tela** — Captura a tela principal (slides, documentos)
   - ☑️ **Gravar Webcam** — Captura câmera
   
   Se **apenas webcam** for marcado: será pedida a resolução (720p ou 1080p)

### Gravando

1. **Clique no botão vermelho** (grande, no centro)
   - Botão muda para "⏹️ Parar gravação"
   - Indicador **🔴 REC** pisca no topo com timer (MM:SS)

2. **Durante a gravação:**
   - Transcrição aparece **em tempo real** abaixo do botão
   - Tela/webcam são capturadas em background
   - Áudio é transcodificado em chunks de 5 segundos

3. **Pausar (ainda não implementado):**
   - Por enquanto: ou grava tudo ou para (roadmap: suporte a pausa)

### Parando

1. **Clique em "⏹️ Parar gravação"**
   - Áudio é finalizado e merge dos chunks
   - Vídeo é muxado com áudio via FFmpeg
   - Você é redirecionado automaticamente à aba **"📂 Histórico"**

2. **Resultado:**
   - Pasta criada em `data/YYYY_MM_DD_HH_MM_SS/`
   - Contém: `audio.mp3`, `transcricao.txt`, `reuniao.mp4` (se tela/webcam foi gravada)

---

## Tab: Histórico

### Navegar reuniões

1. **Dropdown "Selecione uma reunião":**
   - Lista todas as reuniões gravadas (mais recentes primeiro)
   - Formato: `YYYY/MM/DD HH:MM:SS — Título`

2. **Selecionar uma reunião:**
   - Mostra o título (editável se deixado em branco na gravação)
   - Exibe player de vídeo (se `.mp4` existe) ou de áudio (se só `.mp3`)

### Reproduzir

- **Vídeo:** Clique em ▶️ para reproduzir tela/webcam
- **Áudio:** Ou ouça separadamente via player de áudio

### Transcrição

**Seção expandível: "Ver transcrição completa"**
- Mostra todo o texto transcrito
- Cada linha é o resultado do Whisper para um chunk de áudio
- Rodapé mostra qual modelo Whisper foi usado: `*Transcrição gerada pelo modelo: base*`

### Resumo inteligente

**Botão: "Gerar Resumo Inteligente"** (ou "Refazer Resumo")
- Clique para enviar a transcrição ao LLM
- O LLM gera:
  - **Resumo da Reunião:** Um parágrafo (~300 caracteres)
  - **Acordos da Reunião:** Lista de decisões e ações
- Salvo em `resumo.txt` com atribuição do modelo: `*Resumo gerado pelo modelo: gpt-4o-mini (OpenAI)*`

**Nota:** Resumo é **user-triggered**, não automático. Gera novamente se clicar novamente.

### Editar título

Se a reunião não teve título:
1. Clique no campo de texto do título (acima do player)
2. Edite e pressione Enter
3. Será salvo em `titulo.txt`

---

## Estrutura de arquivos (data/)

Cada reunião é armazenada assim:

```
data/
└── YYYY_MM_DD_HH_MM_SS/          # Timestamp da criação
    ├── titulo.txt                  # Título da reunião
    ├── audio.mp3                   # Áudio final (todos os modos)
    ├── transcricao.txt             # Transcrição completa
    ├── resumo.txt                  # Ata gerada (se 'Gerar Resumo' foi clicado)
    ├── reuniao.mp4                 # Vídeo muxado (só se tela/webcam foi gravada)
    └── audio_part_0001.mp3         # [Intermediário] chunks não são deletados
        audio_part_0002.mp3
        ...
```

---

## Modos de áudio (detalhado)

### 1️⃣ Microfone

Captura seu microfone via **WebRTC** (acesso via browser).

```
Mic → PyAV container (AAC) → pydub chunks → Whisper → transcricao.txt
```

**Uso:** Reuniões presenciais onde você fala e grava a tela.

### 2️⃣ Áudio do Sistema

Captura o som que sai do alto-falante (ex: áudio de chamada, webinar) via **WASAPI Loopback** (Windows).

```
Speaker → WASAPI Loopback → MP3 chunks → Whisper → transcricao.txt
```

**Uso:** Gravação de chamadas onde você é participante silencioso, webinars, tutoriais em vídeo.

**⚠️ Windows-only:** Requer drivers WASAPI. Se não detectar, o driver de áudio pode não suportar.

### 3️⃣ Microfone + Sistema (Misto)

Captura ambos simultaneamente e **mescla**.

```
Mic ──┐
      ├─→ pydub.overlay() → Whisper → transcricao.txt
System┘
```

Cada 5 segundos, os dois streams são sobrepostos e normalizados para 16 kHz mono (ótimo para Whisper).

**Uso:** Chamadas de vídeo onde você quer capturar ambas as partes (sua voz + voz da outra pessoa).

---

## Dicas de uso

| Situação | Recomendação |
|----------|-------------|
| Gravando uma apresentação (slides) | Ativar "Gravar Tela" + Microfone |
| Chamada de vídeo com 1 pessoa | Microfone + Sistema (misto) |
| Webinar que você assiste | Apenas Áudio do Sistema |
| Reunião em sala, sem slides | Apenas Microfone |
| Ruído de fundo (A/C, ventilador) | Não há filtro built-in; roadmap: `noisereduce` |
| Reunião muito longa (2h+) | Transcrição funciona, mas resumo LLM pode ser cortado; roadmap: chunking |

---

## Próximos passos

- Veja [Arquitetura](arquitetura.md) para entender como tudo funciona internamente
- Veja [FAQ](faq.md) se tiver problemas
