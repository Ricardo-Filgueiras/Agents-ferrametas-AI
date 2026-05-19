# LangGraph Agent: Infraestrutura Profissional

Este projeto demonstra a construção de agentes de IA utilizando **LangGraph**, focando em uma arquitetura modular, escalável e com persistência de estado (memória de longo prazo).

## 🏗️ Arquitetura do Projeto

O projeto foi reestruturado seguindo as melhores práticas de engenharia de software para agentes:

```text
projeto-graph/
├── data/               # Banco de dados SQLite (Checkpoints)
├── src/
│   ├── core/           # Fundações: Estado (state.py) e Configurações (config.py)
│   ├── graphs/         # Definição da topologia e lógica do grafo
│   ├── nodes/          # Lógica de execução das tarefas (nodes)
│   └── exemplo/        # Protótipos iniciais (ex003.py, ex004.py)
├── .env                # Variáveis de ambiente e chaves de API
├── main.py             # Ponto de entrada (CLI)
└── pyproject.toml      # Gerenciamento de dependências com UV
```

## 🚀 Funcionalidades Principais

- **Persistência com SQLite**: Diferente de chats básicos, este agente utiliza o `SqliteSaver`. Isso significa que ele pode manter o contexto de milhares de conversas diferentes, persistindo os dados em disco.
- **Modularidade Total**: Cada componente (LLM, Estado, Grafo) é isolado, facilitando a manutenção e a adição de novas funcionalidades como ferramentas (tools) e lógica condicional.
- **Gestão de Ambiente**: Suporte nativo a `.env` para proteção de chaves de API e configurações dinâmicas.
- **Ferramentas de Cálculo Integradas**: Implementadas em `src/nodes/calcula_tools.py` (`somar`, `subtrair`, `multiplicar`, `dividir`) para demonstrar o loop do agente ReAct.
- **Interface CLI Robusta**: Interface interativa construída com a biblioteca `Rich`, oferecendo feedback visual limpo e suporte a Markdown.

## 🛠️ Stack Tecnológica

- **LangGraph**: Orquestração de grafos de estado.
- **LangChain Core**: Abstrações de modelos e mensagens.
- **Ollama**: Execução de LLMs locais (Padrão: `llama3.2:3b`).
- **SQLite**: Persistência de estado entre sessões.
- **UV**: Gerenciador de pacotes Python de alta performance.

## 📦 Como Iniciar

1. **Instale as dependências**:
   ```bash
   uv sync
   ```

2. **Configure suas chaves**:
   Copie o arquivo de exemplo e preencha suas chaves:
   ```bash
   cp .env.example .env
   ```

3. **Execute o Agente**:
   ```bash
   uv run main.py
   ```

4. **Testar o Loop do ReAct Agent (Cálculos Múltiplos)**:
   Para visualizar o agente chamando ferramentas de cálculo em loop passo a passo (streaming de nós e mensagens):
   ```bash
   uv run test_math_agent.py
   ```

## 📝 Próximos Passos (Backlog)

- [x] **Tool Integration**: Adicionar ferramentas de pesquisa e cálculos.
- [x] **Conditional Routing**: Lógica para decidir quando usar ferramentas.
- [ ] **Async Support**: Migrar o grafo para execução assíncrona.
- [ ] **Observability**: Integrar LangSmith para monitoramento de traces.
