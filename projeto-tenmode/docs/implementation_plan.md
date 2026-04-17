# ten Agent - Implementation Plan

## Goal Description
Construir o agente de IA local "ten" com base nas especificações arquiteturais (PRD, skill-user, agent-loop, architecture). O sistema será um bot de Telegram 100% local, focado primariamente em gerenciar prompts/skills locais via hot-reload, manter histórico assíncrono em SQLite, suportar provedores LLMs múltiplos, e rodar um loop de raciocínio autônomo (ReAct).

## User Review Required
> [!IMPORTANT]
> - O `aiogram` gerencia o polling de atualizações.
> - `uv` vai ser usado para gerenciar dependências e a rodar via `uv run main.py`.
> - O banco de dados SQLite será criado em `c:\Github\tentaculo-mode\data\db.sqlite`.
> - As skills precisarão de uma pasta inicial obrigatória: `c:\Github\tentaculo-mode\.agents\skills\`.

## Proposed Changes

### 1 Setup e Infraestrutura
Criar o esqueleto do projeto com `uv`, organizar as pastas e preparar dependências.
#### [NEW] `pyproject.toml`
#### [NEW] `c:\Github\tentaculo-mode\data\.keep`
#### [NEW] `c:\Github\tentaculo-mode\tmp\.keep`
#### [NEW] `c:\Github\tentaculo-mode\.agents\skills\.keep`
#### [NEW] `src\core\config.py`

### 2. Camada de Interfaces e Modelos
Base para o sistema, tipagem estática simples.
#### [NEW] `src\core\models.py`
Modelos de dados (Mensagens, Conversation, ToolCall).
#### [NEW] `src\core\interfaces.py`
Contratos para `ILlmProvider` e `BaseTool`.

### 3. Camada de Persistência
Abstração do DB local `aiosqlite`.
#### [NEW] `src\database\db.py`
Conexão SQLite e setup inicial das tabelas `conversations` e `messages`.
#### [NEW] `src\database\repositories.py`
Classes repositório para persistência.
#### [NEW] `src\memory\manager.py`
Facade para buscar histórico recente e truncar limite de contexto do LLM.

### 4. Camada de Skills (Hot-reload local)
Gerenciamento de plugins de forma dinâmica sem reiniciar.
#### [NEW] `src\skills\loader.py`
Lê com `pyyaml` o frontmatter e body markdown das subpastas em `.agents/skills`.
#### [NEW] `src\skills\router.py`
Zero-shot router prompt par escolher qual skill focar, baseado em schema JSON.
#### [NEW] `src\skills\executor.py`
Injeta no System Prompt o conteúdo exato na execução.

### 5. Camada de Ferramentas (Tools)
Actions dinâmicas chamadas pela engine ReAct.
#### [NEW] `src\tools\base.py`
#### [NEW] `src\tools\registry.py`

### 6. Raciocínio (Agent Loop / ReAct)
Engine que implementa de fato o raciocínio.
#### [NEW] `src\agent\loop.py`
Executa o while-loop de iterar até limite (MAX_ITERATIONS). Chama factory de provedores e ferramentas.
#### [NEW] `src\agent\controller.py`
Orquestrador central "Facade" que liga o bot do Telegram ao processamento de Agent.

### 7. Camada Multi-LLM
Abstrações para conectar aos provedores via factory.
#### [NEW] `src\providers\base.py`
#### [NEW] `src\providers\gemini.py`
#### [NEW] `src\providers\openai_compatible.py`
#### [NEW] `src\providers\factory.py`

### 8. Handling de Mídia (Voz e PDF)
Integrações com whisper, py-pdf e edge-tts.
#### [NEW] `src\media\audio.py`
#### [NEW] `src\media\documents.py`

### 9. Interface do Telegram
Entrada/Saída para o usuário.
#### [NEW] `src\telegram\bot.py`
Instancia as rotas e injeta as middlewares.
#### [NEW] `src\telegram\middlewares.py`
Garante `TELEGRAM_ALLOWED_USER_IDS`.
#### [MODIFY] `src\telegram\handlers.py`
Repassa texto/voz pro `AgentController`, envia typing action, devolve mensagens segmentadas/arquivos de áudio ao usuário alvo. Deve cobrir `message:text`, `message:document` (.pdf/.md) e `message:voice`/`message:audio`, realizando download temporário e chamando classes em `src/media/` para stt/extract antes de acionar a controller. O documento especifica que "requires_audio_reply" deve ser repassado ao controller, por enquanto passaremos isso como sufixo oculto na mensagem enviada à memória.

### 10. Entrypoint Principal
#### [NEW] `main.py`
Carrega vars de ambiente, inicializa banco de dados, dá boot na instância aiogram de Dispatcher e entra no polling event loop (run_polling).

---

## Verification Plan
1. **Verificação Automatizada**: 
   - Teste unitário modular garantindo a leitura da skill YAML `pytest src/skills/loader.py`.
   - Comando teste: `uv run pytest` focado no loop (mock de provedor) para evitar API billing local.
2. **Verificação Manual**:
   - Rodar a aplicação via `uv run main.py`.
   - Adicionar o ID de usuário de Telegram no `.env`.
   - Enviar uma mensagem para o bot pelo app do celular/desktop para verificar o whitelist.
   - Solicitar à IA "Resuma o propósito da skill X", testando o roteador de Skills e Memory Fetch.
   - Enviar áudio ou fazer upload do PDF e verificar o fallback pra rotinas de documento e áudio.
