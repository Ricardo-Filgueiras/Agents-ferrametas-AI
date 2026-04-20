# Especificação Técnica: Suite de Análise de Dados (Data Scientist Toolset)

## 📋 Resumo do Projeto
Criação de um conjunto de ferramentas atômicas para o agente LangGraph, permitindo a exploração e análise de arquivos CSV em um ambiente Python controlado (Sandbox).

## 🏗️ Arquitetura das Ferramentas (Abordagem B)

### 1. `list_available_files()`
- **Objetivo**: Listar arquivos para análise.
- **Escopo**: Apenas arquivos `.csv` dentro de `data/storage/`.
- **Metadados**: Retorna nome e tamanho (em KB/MB).

### 2. `inspect_csv_structure(filename)`
- **Objetivo**: Dar visibilidade dos dados ao agente antes da codificação.
- **Saída**: 
  - Nomes das colunas.
  - Tipos de dados (Pandas dtypes).
  - Amostra das primeiras 5 linhas.

### 3. `run_python_analysis(code, filename)`
- **Objetivo**: Executar lógica complexa de agregação e insights.
- **Sandbox**:
  - Utiliza `exec()` com dicionário de globais restrito.
  - `__builtins__` desativados (bloqueia `import`, `open`, etc).
  - Injeção automática de `import pandas as pd`.
  - Injeção automática do arquivo em um DataFrame `df`.
- **Ciclo de Vida**: O DataFrame `df` é removido da memória (`del df`) imediatamente após a captura dos resultados para otimização de recursos.

## 🔒 Segurança e Restrições
- **Pasta Fixa**: O agente não tem permissão para ler caminhos fora de `data/storage/`.
- **Transparência de Erro**: Erros de execução Python são retornados integralmente ao usuário para supervisão.
- **Sem Persistência de Variáveis**: Cada chamada de ferramenta é independente (Stateless).

## ✅ Critérios de Sucesso
- O agente consegue identificar um arquivo, entender quais colunas ele tem e calcular métricas (como médias ou somas) sem alucinar nomes de campos.

---
## 📝 Decision Log
- **2026-04-17**: Escolha da Abordagem B (Atômica) para reduzir erros lógicos.
- **2026-04-17**: Implementação de Sandbox via `exec()` com limpeza de memória pós-execução.
