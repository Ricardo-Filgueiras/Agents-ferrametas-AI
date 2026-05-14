# Design: Upload de Gravação para Transcrição

## Understanding Summary

- **O que:** Seção alternativa na aba "Gravar Reunião" para importar um arquivo de áudio já gravado
- **Por que:** Cobrir situações onde o Projeto-Grava não estava acessível no momento da reunião
- **Para quem:** Usuário local, uso individual
- **Constraints:** Local-first; formatos M4A (prioritário), MP3, WAV; integração total com o Histórico
- **Non-goals:** Não suporta vídeo; não gera resumo automaticamente; não é fluxo separado

## Assumptions

1. pydub suporta M4A → MP3 nativamente via FFmpeg (já instalado no projeto)
2. Limite de upload do Streamlit (200 MB padrão) suficiente para reuniões típicas
3. Transcrição usa o modelo Whisper configurado na sidebar
4. Após transcrição, redireciona ao Histórico — mesmo comportamento do fim de gravação ao vivo

## Design

### Arquitetura

Mudança em um único arquivo: `src/app/main.py`.

```
tab_gravar
├── st.radio → ["🔴 Gravar ao vivo", "📤 Importar arquivo"]
├── "Gravar ao vivo"   → tab_grava_reuniao()   (sem mudança)
└── "Importar arquivo" → tab_importar_audio()   (nova função)
```

### Fluxo de dados

```
Upload (.m4a/.mp3/.wav) + título opcional
        │
        ▼ clique em "Transcrever"
Cria data/YYYY_MM_DD_HH_MM_SS/
Salva titulo.txt
pydub → 16kHz mono → audio.mp3
retranscrever_reuniao() → transcricao.txt
ir_para_historico = True → rerun
```

### Reutilização de código existente

| Necessidade | Origem |
|---|---|
| Criar pasta da reunião | `PASTA_ARQUIVOS` + `datetime` (já em `main.py`) |
| Salvar título | `salva_arquivo()` (`utils.py`) |
| Transcrever + salvar | `retranscrever_reuniao()` (`ia_models.py`) |
| Redirecionar ao Histórico | `ir_para_historico` session state (já em `main()`) |
| Converter M4A → MP3 | `pydub.AudioSegment` (já instalado) |

## Decision Log

| Decisão | Alternativas | Motivo |
|---|---|---|
| Mudança só em `main.py` | Novo módulo `import_audio.py` | Função pequena, não justifica novo arquivo |
| Reutilizar `retranscrever_reuniao()` | Nova função de transcrição | Já faz exatamente o necessário |
| Converter para 16kHz mono | Salvar arquivo original | Whisper performa melhor; consistente com pipeline de gravação |
| Radio horizontal no topo | Sub-tabs, expander | Mais simples; escolha explícita do modo |
