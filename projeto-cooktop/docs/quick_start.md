# 🎂 Guia de Início Rápido: Cozinha Digital (Multi-Agentes)

Este projeto implementa uma arquitetura profissional de multi-agentes usando **LangGraph**, baseada na metáfora da **"Tigela"** (Estado Central).

## 🚀 Como Começar

### 1. Pré-requisitos
*   **Python 3.10+** instalado.
*   **Ollama** instalado e rodando localmente.
*   Modelos recomendados no Ollama: `llama3.2:3b` ou `granite4.1:3b`.

### 2. Configuração do Ambiente
Abra o terminal na pasta raiz e siga os passos:

```bash
# Instalar dependências usando uv (recomendado) ou pip
uv pip install -r requirements.txt

# Configurar variáveis de ambiente
# Crie um arquivo .env na raiz (se não existir) com:
BASE_MODEL=ollama:llama3.2:3b
OLLAMA_API_URL=http://localhost:11434
```

### 3. Executando a Cozinha
Para iniciar o preparo de um bolo, execute o comando:

```bash
python src/main.py
```

---

## 🥣 A Arquitetura da "Tigela"

O sistema opera em um fluxo circular onde o **Estado** (State) evolui a cada passo:

1.  **Sous Chef (O Preparador)**: Recebe o seu pedido, busca a receita nas ferramentas e organiza os ingredientes brutos na tigela.
2.  **Confeiteiro (O Executor)**: Lê a tigela, consulta o caderno de notas e transforma os ingredientes em massa (batida e depois assada).
3.  **Inspetor (O Auditor)**: Avalia o bolo final. Se a nota for baixa (< 7), ele anota os erros no caderno e o fluxo recomeça no Sous Chef para correção.

## 🛠️ Ferramentas Disponíveis
Os agentes têm acesso a:
*   **`search_recipes`**: Busca proporções corretas.
*   **`control_oven`**: Ajusta a temperatura do forno.
*   **`check_inventory`**: Verifica disponibilidade de itens.
*   **`write_note/read_notes`**: Um caderno persistente em `data/caderno.md`.

## 📁 Estrutura de Arquivos
*   `src/agents/`: Lógica e prompts de cada agente.
*   `src/graph/`: Definição do fluxo (nós e arestas).
*   `src/schemas/`: Definição da "Tigela" (Estado).
*   `src/tools/`: Utensílios da cozinha.
*   `data/`: Registros persistentes e checkpoints.
