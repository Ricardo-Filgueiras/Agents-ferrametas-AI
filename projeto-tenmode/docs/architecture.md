# Arquitetura do Projeto: ten

**Versão:** 1.0  
**Status:** Definição Central de Arquitetura  
**Autor:** Antigravity (IA)  
**Data:** 2026-03-10  

---

## 2.1 Visão Geral

O **ten** é um agente pessoal de Inteligência Artificial projetado para operar localmente no desktop do usuário. Sua interface primária de controle é o Telegram, permitindo uma interação fluida via texto, documentos e voz. O sistema é construído para ser modular, extensível através de "skills" (habilidades) e totalmente focado na privacidade, mantendo a persistência de dados localmente.

A arquitetura segue um fluxo de pipeline onde as mensagens do Telegram são capturadas, processadas por um motor de raciocínio (Agent Loop) que utiliza LLMs externos (como Gemini ou DeepSeek) apenas para inferência, e responde de volta ao usuário de forma inteligente, podendo inclusive gerar arquivos ou respostas em áudio.

---

## 2.2 Requisitos Arquiteturais

| Requisito | Tipo | Prioridade | Notas |
|-----------|------|------------|-------|
| Operação Local | Não-funcional | Crítica | O "core" deve rodar no host local (Windows). |
| Interface Telegram | Funcional | Alta | Uso da biblioteca `aiogram` para polling. |
| Persistência Local | Funcional | Alta | Armazenamento de conversas em SQLite. |
| Padronização de LLMs | Não-funcional | Alta | Troca dinâmica de provedores (Gemini, DeepSeek, Groq). |
| Multimodalidade (Input) | Funcional | Média | Suporte a PDF e Voz (STT via Whisper Local). |
| Multimodalidade (Output)| Funcional | Média | Suporte a Arquivos (.md) e Voz (TTS). |
| Segurança de Acesso | Funcional | Crítica | Whitelist estrita baseada em ID de usuário do Telegram. |

---

## 2.3 Estilo Arquitetural

O sistema adota um estilo **Monolito Modular com Sistema de Plugins**.  
- **Monolito Modular:** Facilita o desenvolvimento e deploy local sem a complexidade de microsserviços.
- **Plugin-based (Skills):** Permite que novas funcionalidades sejam adicionadas ou atualizadas via "Hot-Reload" apenas manipulando diretórios na pasta `.agents/skills`, sem reiniciar o processo principal.

**Trade-offs:**  
- **Vantagem:** Baixa latência interna, facilidade de manutenção para um único desenvolvedor, alta coesão.
- **Desvantagem:** Escalabilidade vertical limitada ao hardware do host local (não é um problema para o caso de uso de agente pessoal).

---

## 2.4 Diagrama de Contexto

```mermaid
graph TB
    User([👤 Usuário Sandeco])
    Telegram[📱 Telegram Client]
    System[🏗️ ten Engine]
    LLM[🧠 LLM APIs - Gemini/DeepSeek]
    Whisper[🎙️ Whisper Local - STT]
    EdgeTTS[🔊 Edge-TTS - TTS]

    User <-->|Envia Msg/Voz/Doc| Telegram
    Telegram <-->|Polling/Reply| System
    System <-->|Prompt/Response| LLM
    System -->|Processa Áudio| Whisper
    System -->|Gera Áudio| EdgeTTS
```

---

## 2.5 Diagrama de Componentes e Camadas

O projeto segue estritamente a **Programação Orientada a Objetos (POO)** com separação clara de responsabilidades em arquivos e módulos distintos.

```mermaid
graph TB
    subgraph "Camada de Interface (Input/Output)"
        InputH[TelegramInputHandler]
        OutputH[TelegramOutputHandler]
    end

    subgraph "Camada de Controle e Core"
        Controller[AgentController - Facade]
        Loop[AgentLoop - ReAct Engine]
        Registry[Tool/Skill Registry]
    end

    subgraph "Camada de Habilidades (Plugins)"
        SkillL[SkillLoader]
        SkillR[SkillRouter]
        SkillE[SkillExecutor]
    end

    subgraph "Camada de Persistência (Memory)"
        MemM[MemoryManager - Facade]
        ConvR[ConversationRepository]
        MsgR[MessageRepository]
        DB[(SQLite - db.sqlite)]
    end

    InputH --> Controller
    Controller --> SkillL
    SkillL --> SkillR
    SkillR --> SkillE
    SkillE --> Loop
    Loop --> MemM
    Loop <--> Registry
    MemM --> ConvR & MsgR
    ConvR & MsgR --> DB
    Loop --> OutputH
```

---

## 2.6 Decisões de Tecnologia (Source of Truth)

Este tópico centraliza as definições de stack. **Alterações aqui devem refletir mudanças em toda a arquitetura do sistema.**

| Componente | Tecnologia | Detalhes / Justificativa |
|------------|------------|-------------------------|
| **Linguagem** | **Python** | Ecossistema maduro para IA, manipulação de texto e familiaridade. |
| **Package Manager**| **uv** | Gerenciador de dependências e ambientes virtuais ultrarrápido em Rust, substituindo pip/venv. |
| **Paradigma** | **Orientação a Objetos** | Uso obrigatório de Classes, Interfaces e Padrões de Projeto (User Rule). |
| **Banco de Dados**| **SQLite** | Local, serverless, rápido (`aiosqlite`). |
| **Interface Bot** | **aiogram** | Framework moderno assíncrono para Telegram Bot API em Python. |
| **Raciocínio IA** | **ReAct Pattern** | Loop de "Thought -> Action -> Observation -> Answer". |
| **STT (Voz)** | **Whisper (Local)** | Transcrição privada sem custo de API. |
| **TTS (Fala)** | **Edge-TTS** | Geração de voz de alta qualidade (`pt-BR-Thalita`). |
| **Parser Documentos**| **pdf-parse** | Extração de texto de PDFs para processamento pela IA. |

---

## 2.7 Desing Patterns Utilizados

Para manter a alta coesão e baixo acoplamento, os seguintes padrões são aplicados:

1.  **Facade:** Utilizado no `AgentController` e `MemoryManager` para simplificar a interface com subsistemas complexos.
2.  **Factory:** `ProviderFactory` para instanciar diferentes provedores de LLM e `ToolFactory` para as ferramentas.
3.  **Repository:** Para abstrair o acesso ao banco de dados SQLite (`ConversationRepository`, `MessageRepository`).
4.  **Singleton:** Garantir instância única da conexão com o banco de dados.
5.  **Strategy:** No `TelegramOutputHandler` para decidir entre enviar texto puro, chunks ou arquivos.
6.  **Registry:** No sistema de Skills e Tools para registro dinâmico de capacidades.

---

## 2.8 Fluxos Críticos (Sequence Diagram)

### Fluxo de Processamento de Mensagem
```mermaid
sequenceDiagram
    participant U as Usuário (Telegram)
    participant I as TelegramInputHandler
    participant C as AgentController
    participant S as SkillSystem
    participant L as AgentLoop (ReAct)
    participant LLM as Provider (AI)
    participant M as MemoryManager

    U->>I: Envia Mensagem
    I->>I: Valida Whitelist
    I->>C: Repassa Input Processado
    C->>S: Router (Identifica Skill necessária)
    S-->>C: Retorna Prompt da Skill
    C->>L: Inicia Ciclo de Raciocínio
    loop ReAct Loop (até 5x)
        L->>LLM: Solicita Inferência
        LLM-->>L: Retorna Thought / Tool Call
        L->>L: Executa Tool (se houver)
    end
    L->>M: Persiste Resposta Final
    L->>U: Envia Resposta via OutputHandler
```

---

## 2.9 Infraestrutura e Deploy

- **Ambiente:** Execução direta no Windows via Terminal.
- **Process Management:** `uv run main.py` (garantindo contexto do ambiente virtual gerido pelo uv, com watchdog opcional para hot-reload do core).
- **Diretórios de Dados:**
    - `./data/`: Banco de dados SQLite (`.db`).
    - `./tmp/`: Arquivos temporários (PDFs/Áudios) deletados após uso.
    - `.agents/skills/`: Plugins de habilidades em Markdown.

---

## 2.10 Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Corrupção do SQLite | Alto | Uso de WAL (Write-Ahead Logging) e backups locais periódicos. |
| Falha na API de LLM | Alto | Implementação de `fallback` no `ProviderFactory`. |
| Vazamento de Memória (Python)| Médio | Gerenciamento estrito de Buffer de áudio e exclusão de arquivos TMP. |
| Estouro de Contexto IA | Médio | Truncamento nativo no `MemoryManager` via `MEMORY_WINDOW_SIZE`. |

---

## Gaps de Documentação (Observações)

Os seguintes elementos foram inferidos ou precisam de definição futura conforme o amadurecimento do código:

| Elemento | Status | Recomendação |
|----------|--------|--------------|
| Migrations de BD | Não documentado | No futuro, implementar scripts de migration para evoluir o esquema SQL sem perda de dados. |
| Rate Limiting Telegram | Inferido | Manter a lógica de `sleep` no OutputHandler caso a API retorne erro 429. |
| Versão do Python | Inferido | Recomenda-se versão 3.10+ para estabilidade das bibliotecas nativas e suporte a type hints avançados. |
