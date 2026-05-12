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

---

## 16. Leitura Simultânea (Modo Teleprompter)
Exibir a transcrição em tempo real em formato visual ampliado — texto grande, negrito,
com timestamp de cada frase — semelhante a um teleprompter ou legenda ao vivo.
Útil para acompanhamento durante a reunião sem precisar ler texto pequeno.

Comportamento esperado:
```
┌─────────────────────────────────┐
│  Leitura Simultânea (BETA)      │
│                                 │
│  3:12                           │
│  bandeiras de cartão,     │
│  inclusive, deve tentar         │
│                                 │
│  3:14                           │
│  blindar qualquer possibilidade │
│  de um novo tarifácio.          │
└─────────────────────────────────┘
```

- Texto atual (último chunk Whisper) exibido em destaque no centro da tela
- Timestamp relativo à gravação (ex: `3:12`) acima de cada bloco de frase
- Texto em fonte grande e legível (estilo subtítulo de filme)
- Modo ativável via checkbox na sidebar ou botão dedicado durante a gravação
- Útil para speakers acompanharem o que foi dito em tempo real sem sair da reunião
- Aplicável em: apresentações, transmissões ao vivo, webinars, podcasts

---

## 17. Metodologia CRISP-DM como Padrão de Projeto para Resumos
Usar as fases do CRISP-DM (Cross Industry Standard Process for Data Mining) como estrutura
de referência para o LLM organizar o resumo de reuniões técnicas/analíticas.

Mapeamento das fases para a ata de reunião:
```
1. Entendimento do Negócio  → Objetivo da reunião, problema a resolver
2. Entendimento dos Dados   → Fontes, bases, KPIs discutidos
3. Preparação dos Dados     → ETL, transformações, pipelines mencionados
4. Modelagem                → Algoritmos, abordagens, hipóteses levantadas
5. Avaliação                → Métricas, critérios de sucesso, validações
6. Implantação              → Próximos passos, responsáveis, prazos
```

Benefícios:
- Resumo estruturado em vez de texto corrido — fácil de auditar
- O LLM só preenche as seções relevantes à reunião (omite fases não mencionadas)
- Padrão reconhecível pela equipe de dados sem curva de aprendizado
- Complementa o item 3 (Extração de Itens de Ação) com contexto de projeto

Implementação: adicionar uma opção de **"Template de Resumo"** no sidebar —
`Livre | CRISP-DM | Scrum Sprint | Genérico` — que troca o `ChatPromptTemplate`
conforme o padrão selecionado, sem alterar o pipeline de transcrição.
