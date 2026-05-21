# Pontos de Melhoria e Recomendações - Projeto Graph

Este documento detalha as oportunidades de melhoria identificadas na arquitetura atual do `projeto-graph`, bem como recomendações técnicas para elevar a qualidade, segurança e escalabilidade do sistema.

## 1. Segurança e Isolamento (Crítico)

### 1.1. Execução de Código Arbitrário
- **Ponto de Melhoria:** A ferramenta `run_python_analysis` utiliza `exec()` com uma "sandbox" baseada apenas em remoção de built-ins.
- **Risco:** Contorno fácil de restrições (RCE - Remote Code Execution), permitindo acesso ao sistema de arquivos, variáveis de ambiente e rede.
- **Recomendação:** 
    - Migrar para ambientes isolados como **Docker Containers** (usando bibliotecas como `python-on-whales`).
    - Utilizar bibliotecas de sandbox seguras como **Pyodide** (WASM) ou serviços gerenciados como **E2B**.

---

## 2. Estrutura e Organização do Código

### 2.1. Inconsistência de Diretórios
- **Ponto de Melhoria:** Ferramentas de negócio (`data_tools.py`) estão localizadas na pasta `src/nodes/`.
- **Recomendação:** Mover todas as ferramentas para `src/tools/`. A pasta `nodes` deve conter apenas a lógica de fluxo do grafo (chamadas de LLM, roteamento, lógica de controle).

### 2.2. Arquivos Depreciados e Duplicados
- **Ponto de Melhoria:** Arquivos como `src/nodes/calcula_tools.py` e `src/graphs/chat_graph.py` contêm avisos de depreciação, mas permanecem no repositório.
- **Recomendação:** Remover arquivos depreciados após garantir que todas as referências foram migradas para os novos locais (`src/tools/` e `src/agent.py`).

### 2.3. Descoberta de Ferramentas (Tool Discovery)
- **Ponto de Melhoria:** O agente não está utilizando as ferramentas de Data Science definidas em `data_tools.py` porque elas não estão importadas no `tools_node.py`.
- **Recomendação:** Implementar um padrão de registro centralizado em `src/tools/__init__.py` que exporte uma lista única de todas as ferramentas disponíveis para o agente.

---

## 3. Persistência e Memória

### 3.1. Ativação de Checkpointers
- **Ponto de Melhoria:** O sistema possui dependências para SQLite e Postgres, mas o grafo é compilado sem um checkpointer.
- **Recomendação:** 
    - Instanciar `SqliteSaver` (ou `AsyncSqliteSaver`) em `src/agent.py`.
    - Passar o checkpointer no método `.compile(checkpointer=memory)`.
    - Isso permitirá que o `thread_id` enviado pela CLI realmente recupere o histórico de sessões anteriores.

---

## 4. Uso de Padrões LangGraph

### 4.1. Componentes Pré-construídos
- **Ponto de Melhoria:** Lógica manual em `router_node` e `tools_node`.
- **Recomendação:** 
    - Substituir `router_node` pela função `tools_condition` do `langgraph.prebuilt`.
    - Substituir o nó manual de ferramentas pela classe `ToolNode` do `langgraph.prebuilt`. Isso simplifica o tratamento de erros e execuções paralelas nativamente.

---

## 5. Novos Pontos de Melhoria (Adicionais)

### 5.1. Gestão de Configurações (Centralização)
- **Ponto de Melhoria:** Variáveis como `STORAGE_PATH` e `MODEL_NAME` estão espalhadas pelos arquivos.
- **Recomendação:** Criar uma classe `Settings` em `src/core/config.py` usando `pydantic-settings`. Isso facilita a validação de variáveis de ambiente e centraliza caminhos de arquivos.

### 5.2. Observabilidade e Tracing
- **Ponto de Melhoria:** Não há visibilidade sobre as "cadeias de pensamento" do agente em ambiente de desenvolvimento fora da CLI.
- **Recomendação:** Integrar o **LangSmith**. Basta configurar as variáveis de ambiente `LANGCHAIN_TRACING_V2` e `LANGCHAIN_API_KEY` para ter um dashboard completo de execução e debug.

### 5.3. Validação de Input do Usuário
- **Ponto de Melhoria:** A CLI aceita qualquer entrada e a envia diretamente para o grafo.
- **Recomendação:** Implementar uma camada de validação ou "guardrails" (ex: **NeMo Guardrails**) para evitar que o agente processe inputs maliciosos ou fora do escopo do projeto.

### 5.4. Documentação de Ferramentas para a LLM
- **Ponto de Melhoria:** As docstrings das ferramentas em `data_tools.py` são boas, mas poderiam ser mais específicas sobre *quando* usar cada uma.
- **Recomendação:** Melhorar as docstrings com exemplos de "Few-Shot" ou descrições mais ricas sobre o formato esperado de dados, o que ajuda modelos menores (como o Llama 3.2 3B) a não cometerem erros de invocação.

---
*Documento gerado automaticamente por Gemini CLI.*
