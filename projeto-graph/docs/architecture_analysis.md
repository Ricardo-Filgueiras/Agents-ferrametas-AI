# Análise de Arquitetura - Projeto Graph

Este documento fornece uma análise crítica da arquitetura do `projeto-graph`, avaliando sua estrutura, padrões de design, escalabilidade e segurança.

## 1. Visão Geral do Sistema

O projeto é uma infraestrutura de agentes inteligentes baseada em **LangGraph** e **LangChain**, projetada para processamento local (via Ollama) ou remoto (via Google Gemini). A arquitetura segue o padrão ReAct (Reasoning and Acting), permitindo que o agente utilize ferramentas para estender suas capacidades.

## 2. Componentes Principais

### 2.1. Orquestração (LangGraph)
- **Estado (`src/core/state.py`):** Utiliza um `TypedDict` com `Annotated` e o reducer `add_messages`. Esta é a prática recomendada pelo LangGraph para manter um histórico de mensagens imutável e persistente.
- **Grafo (`src/agent.py`):** Define um fluxo cíclico claro: `START -> call_llm -> router -> tools_node -> call_llm`.
- **Roteamento:** Implementado manualmente em `router_node`. Funciona bem, mas poderia ser substituído por `langgraph.prebuilt.tools_condition` para maior simplicidade.

### 2.2. Nós e Ferramentas
- **LLM Node (`src/nodes/llm_nodes.py`):** Centraliza a lógica de chamada ao modelo. O uso de `bind_tools` garante que a LLM saiba como invocar as ferramentas disponíveis.
- **Tools Node (`src/nodes/tools_node.py`):** Implementa a execução manual das ferramentas. 
    - *Crítica:* O projeto não utiliza o `ToolNode` pré-construído do LangGraph, o que resulta em código redundante para tratar chamadas paralelas e erros de validação.

### 2.3. Ferramentas (Tools)
- **Matemáticas (`src/tools/calcula_tools.py`):** Bem definidas e documentadas usando o decorator `@tool`.
- **Data Science (`src/nodes/data_tools.py`):** Implementa inspeção de CSVs e execução de código Python.
    - *Problema de Organização:* Estas ferramentas estão localizadas na pasta `nodes`, o que foge à convenção de separar a lógica das ferramentas da lógica dos nós do grafo. Além disso, elas não estão registradas no `tools_node.py` principal, tornando-as inacessíveis ao agente.

## 3. Análise Crítica

### 3.1. Pontos Positivos (Strengths)
1. **Modularidade:** A separação em `core`, `nodes`, `tools` e `graphs` facilita a manutenção.
2. **Streaming:** A CLI implementada em `main.py` utiliza corretamente o modo streaming do grafo, proporcionando uma excelente experiência de usuário (UX) ao mostrar os passos intermediários do agente.
3. **Gerenciamento de Dependências:** O uso de `uv` e `pyproject.toml` alinha o projeto com as melhores práticas modernas de Python.

### 3.2. Pontos de Melhoria (Weaknesses)
1. **Redundância e Depreciação:** Existem arquivos duplicados ou marcados como `DEPRECATED` (ex: `src/nodes/calcula_tools.py` e `src/graphs/chat_graph.py`) que poluem o repositório.
2. **Inconsistência de Diretórios:** As ferramentas de análise de dados estão em `src/nodes/`, enquanto deveriam estar em `src/tools/`.
3. **Persistência Inativa:** Embora existam dependências para SQLite e Postgres (checkpointers), o grafo compilado em `src/agent.py` não instancia nem utiliza um checkpointer, o que significa que o histórico de conversas é perdido ao reiniciar o processo (a CLI gera um `thread_id` novo, mas o grafo não tem onde salvar o estado).
4. **Acoplamento de Ferramentas:** O registro de ferramentas é feito de forma estática no `tools_node.py`. Para um sistema com muitas ferramentas, um padrão de registro (Registry) dinâmico seria mais escalável.

### 3.3. Vulnerabilidade de Segurança Crítica
A função `run_python_analysis` em `src/nodes/data_tools.py` utiliza `exec()` para rodar código Python gerado pela LLM.
- A "sandbox" implementada apenas removendo alguns built-ins (`open`, `eval`, etc.) é **insuficiente**.
- Um atacante (ou uma LLM alucinando) pode facilmente contornar essas restrições (ex: usando `getattr` em outras bibliotecas ou manipulação de bytecodes).
- **Recomendação:** Utilizar um ambiente de execução isolado (Docker, E2B, ou Pyodide) para execução de código arbitrário.

## 4. Recomendações de Evolução

1. **Refatoração de Ferramentas:** Mover todas as ferramentas para `src/tools/` e unificar o catálogo de ferramentas em um único ponto de entrada.
2. **Uso de Prebuilt Components:** Substituir o `tools_node` manual pelo `ToolNode` do LangGraph e o `router_node` por `tools_condition`.
3. **Ativação da Persistência:** Instanciar o `SqliteSaver` e passá-lo para `builder.compile(checkpointer=memory)`.
4. **Centralização de Configurações:** Mover caminhos de arquivos (como `data/storage`) para o `src/core/config.py`.
5. **Observabilidade:** Integrar o LangSmith para monitoramento das cadeias de pensamento do agente e depuração de custos/latência.

---
*Documento gerado automaticamente por Gemini CLI.*
