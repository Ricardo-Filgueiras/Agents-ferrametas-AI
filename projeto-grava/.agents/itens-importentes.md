# Itens Importantes — Estudo por Etapas

## 1. Identificação de Falantes (Diarização)
Usar `whisperx` que combina Whisper + diarização em um pipeline só.
Saída esperada:
```
[00:02:14] Speaker 1: Eu acho que deveríamos revisar o orçamento...
[00:02:31] Speaker 2: Concordo, mas o prazo é o problema...
```
- Sem pré-cadastro: falantes saem como "Speaker 1", "Speaker 2"
- Com pré-cadastro (30s de áudio por pessoa): nomes reais

---

## 2. Reuniões Longas vs. Contexto do LLM
Reunião de 2h gera transcrição enorme — modelos locais têm janela de contexto limitada.
Estratégia necessária: **chunking** — resumir por blocos e depois resumir os resumos.

---

## 3. Extração de Itens de Ação
O resumo atual extrai tópicos gerais. O que torna uma ata útil:
> *"quem vai fazer o quê e até quando"*

O prompt do LLM precisa ser instruído explicitamente para extrair isso.

---

## 4. Qualidade do Áudio — Pré-processamento
Ruído de sala, ar-condicionado, falas simultâneas degradam o Whisper.
Solução: aplicar redução de ruído (`noisereduce`) antes de transcrever.

---

## 5. Contexto dos Slides na Transcrição
A tela é gravada em vídeo, mas o LLM não vê o vídeo.
Solução: OCR nos frames da tela (`pytesseract`) para extrair o texto dos slides
e injetá-lo na transcrição no momento correto.

---

## 6. Busca Entre Reuniões (RAG)
Com dezenas de reuniões gravadas, precisar encontrar *"em qual reunião decidimos X?"*
Solução: RAG sobre as transcrições — o projeto `doctotelos` já tem essa base.

---

## 7. Consumo de Recursos / Performance
Whisper + Ollama + captura de tela simultâneos podem sobrecarregar a máquina.
Solução: rodar a transcrição de forma **assíncrona**, fora do loop de gravação.

---

## 8. Pausar e Retomar Gravação
Reuniões têm intervalos. Hoje só existe parar definitivamente.
Precisaria de um estado intermediário: pausar sem encerrar a sessão, retomar continuando no mesmo arquivo.

---

## 9. Marcadores Manuais Durante a Gravação
Poder pressionar uma tecla para marcar momentos importantes em tempo real
(ex: *"decisão tomada"*, *"ponto crítico"*), gerando âncoras com timestamp na transcrição.

---

## 10. Timestamps Clicáveis — Navegação Transcrição ↔ Vídeo
Clicar em um trecho da transcrição e o vídeo pular para aquele momento.
Útil para revisar o contexto exato de uma decisão sem assistir a reunião inteira.

---

## 11. Agenda como Contexto de Entrada
Informar os tópicos da pauta antes de iniciar a gravação.
O LLM usa a agenda para estruturar o resumo por item de pauta, não como texto corrido.

---

## 12. Múltiplos Monitores / Projetor
O app hoje captura o monitor principal. Em salas de reunião o slide pode estar
num projetor conectado como segundo monitor. Precisaria permitir selecionar qual tela capturar.

---

## 13. Exportação da Ata
Gerar um PDF ou documento formatado (título, participantes, resumo, itens de ação)
pronto para enviar por email aos participantes após a reunião.

---

## 14. Consentimento dos Participantes (LGPD)
Gravar pessoas sem registro de consentimento pode ser um problema legal no Brasil.
Solução simples: tela de confirmação antes de iniciar (*"Todos os presentes concordam com a gravação"*)
com log registrado em arquivo junto aos dados da reunião.

---

## 15. Gestão de Armazenamento
Com uso diário, os arquivos acumulam rapidamente (áudio + vídeo + transcrições).
Necessário: política de retenção, compressão automática de gravações antigas,
ou indicador de espaço em disco na interface.
