# 🚀 Projeto Agno - Agents & Ferramentas AI

Este projeto é uma implementação avançada de Agentes de IA utilizando o framework **Agno** (anteriormente Phidata), focado em modularidade, ferramentas personalizadas (Tools) e execução local via **Ollama**.

## 🏗️ Arquitetura do Projeto

O projeto segue o padrão de layout `src/`, garantindo que o código seja tratável como um pacote Python profissional e facilitando a escalabilidade.

```text
projeto-agno/
├── src/
│   ├── agents/      # Definições de agentes especializados
│   ├── core/        # Lógica central e configurações
│   ├── learning/    # Scripts de aprendizado e exemplos (ex: 0-hello.py)
│   ├── molho/       # Scripts de teste e utilitários
│   ├── tools/       # Ferramentas personalizadas (Math, Vendas, etc.)
│   └── workflows/   # Fluxos de trabalho complexos
├── pyproject.toml   # Gerenciamento de dependências (UV)
└── README.md        # Documentação do projeto
```

## 🛠️ Tecnologias Utilizadas

- **[Agno](https://agno.com/)**: Framework de orquestração para agentes de IA.
- **[Ollama](https://ollama.com/)**: Execução local de LLMs.
- **[UV](https://github.com/astral-sh/uv)**: Gerenciador de pacotes Python ultra-rápido.
- **FastAPI / AgentOS**: Para servir os agentes como APIs prontas para produção.
- **Pydantic**: Validação de dados e esquemas de saída (Structured Outputs).

## 🌐 Interface e Monitoramento (Agno UI)

Este projeto está integrado ao ecossistema **AgnoOS**, permitindo uma interface de chat moderna e ferramentas de monitoramento em tempo real.

- **Agno UI**: Você pode interagir com seus agentes locais através da interface oficial em [os.agno.com](https://os.agno.com/chat?type=agent).
- **AgentOS**: Ao rodar o comando `fastapi dev`, o projeto expõe endpoints compatíveis que o AgnoOS utiliza para conectar seu agente local à interface web, permitindo depuração visual e testes rápidos.

## 🧠 Modelos de IA (LLMs)

O projeto prioriza a execução **100% local** e a soberania dos dados, utilizando o **Ollama**:

- **💰 Custo Zero**: Uso ilimitado sem preocupações com faturas ou consumo de tokens.
- **🔑 Independência de API Keys**: Não é necessário configurar chaves da OpenAI, Google ou Anthropic para o funcionamento básico.
- **🛡️ Privacidade**: Seus dados e interações permanecem processados localmente na sua infraestrutura.

**Configuração Atual:**
- **Modelo Principal**: `llama3.2:3b` rodando via Ollama.
- **Capacidades**: O modelo suporta **Tool Calling** (chamada de funções) e **Structured Outputs**, permitindo interações precisas com ferramentas de vendas e cálculos.

## 🚀 Como Começar

### 1. Pré-requisitos
Certifique-se de ter o **Ollama** instalado e o modelo baixado:
```bash
ollama run llama3.2:3b
```

### 2. Instalação
Utilizamos o `uv` para gerenciar o ambiente. Instale as dependências e o projeto em modo editável:
```powershell
uv pip install -e .
```

> [!IMPORTANT]
> Se encontrar erros relacionados ao JWT, certifique-se de usar o pacote `PyJWT` em vez de `jwt`.

### 3. Execução

Para rodar os scripts de exemplo ou o servidor de agentes:

**Rodar como módulo:**
```powershell
python -m src.learning.0-hello
```

**Rodar via FastAPI (AgentOS):**
```powershell
uv run fastapi dev src/learning/0-hello.py
```

## 🤖 Agentes e Ferramentas

### Ferramenta de Vendas (`VendasTool`)
Implementada com suporte a **Structured Outputs**, permitindo que o agente retorne dados formatados como:
- Valor total das vendas.
- Quantidade de produtos.
- Gestão de descontos e descrições.

### Ferramentas Matemáticas (`mathtools`)
Conjunto de ferramentas para operações aritméticas básicas que os agentes podem invocar para garantir precisão em cálculos complexos, evitando alucinações matemáticas.

## 🛣️ Próximos Passos (Roadmap)

- [ ] **Integração RAG (Retrieval-Augmented Generation)**: Permitir que o agente consulte documentos PDF ou bases de conhecimento locais.
- [ ] **Interface Web**: Criar um frontend moderno para interagir com os agentes em tempo real.
- [ ] **Multi-Agent Orchestration**: Implementar fluxos onde um agente delega tarefas para outro (ex: Agente de Vendas -> Agente de Logística).
- [ ] **Memória Persistente**: Armazenar o histórico de conversas em um banco de dados vetorial.

---
Desenvolvido por **Ricardo Filgueiras** - *Agents-ferrametas-AI*
