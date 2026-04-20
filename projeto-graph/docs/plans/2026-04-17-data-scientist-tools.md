# Data Scientist Toolset Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implementar uma suite de 3 ferramentas para análise de dados CSV via Sandbox Python, integrada ao grafo LangGraph.

**Architecture:** Abordagem atômica com isolamento de diretório e execução controlada via `exec()`.

**Tech Stack:** LangGraph, Pandas, Python Standard Library.

---

### Task 1: Preparação do Ambiente e Diretórios

**Files:**
- Create: `data/storage/`
- Modify: `pyproject.toml` (garantir pandas)

**Step 1: Criar o diretório de armazenamento seguro**
Run: `mkdir -p data/storage`

**Step 2: Verificar/Adicionar Pandas**
Run: `uv add pandas`

---

### Task 2: Implementação das Ferramentas de Dados

**Files:**
- Create: `src/nodes/data_tools.py`

**Step 1: Implementar `list_available_files`**
Criar a função decorada com `@tool` que lista arquivos `.csv` com tamanho.

**Step 2: Implementar `inspect_csv_structure`**
Criar a função que lê o cabeçalho e as primeiras 5 linhas usando `pd.read_csv(nrows=5)`.

**Step 3: Implementar `run_python_analysis` (A Sandbox)**
Criar a função que recebe código, injeta o DataFrame e executa `exec()` com ambiente restrito e limpeza de memória.

---

### Task 3: Integração no Grafo (Ciclo ReAct)

**Files:**
- Modify: `src/graphs/chat_graph.py`
- Modify: `src/nodes/llm_nodes.py`

**Step 1: Vincular ferramentas ao modelo**
No `llm_nodes.py`, usar `model.bind_tools([list_available_files, inspect_csv_structure, run_python_analysis])`.

**Step 2: Atualizar a Topologia do Grafo**
No `chat_graph.py`, adicionar um `ToolNode` e a lógica condicional `should_continue` para permitir que o agente use as ferramentas.

---

### Task 4: Atualização das Instruções (System Prompt)

**Files:**
- Modify: `.agents/system_prompt.md`

**Step 1: Ensinar o agente a usar a suite de dados**
Adicionar diretrizes sobre o fluxo: Listar -> Inspecionar -> Analisar.

---

**Verification & Testing:**
1. Colocar um arquivo `teste.csv` em `data/storage/`.
2. Rodar `uv run main.py`.
3. Pedir ao agente: "Quais arquivos você tem acesso?".
4. Pedir: "Qual a estrutura do arquivo teste.csv?".
5. Pedir: "Calcule a soma da coluna X do arquivo teste.csv".
