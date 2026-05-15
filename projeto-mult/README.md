# 📝 Multi-Agent Blog Engine (Lean Elite Team)

Este é um sistema multi-agente determinístico projetado para criar e revisar artigos de blog otimizados para SEO. A arquitetura foi baseada no princípio de **"Equipes Enxutas de Elite"**, com foco total em confiabilidade, controle de estado via contratos rígidos (Pydantic) e redução de custos através de modelos locais.

## 🚀 Tecnologias e Stack

- **Orquestração de Fluxo**: [LangGraph](https://python.langchain.com/v0.1/docs/langgraph/) (Garante um workflow linear e loops de revisão controlados)
- **Definição de Agentes**: [Agno](https://www.agno.com/) (Anteriormente Phidata)
- **Modelos Locais (LLM)**: [Ollama](https://ollama.com/) rodando `llama3.2:3b` para tarefas pesadas a **custo zero**.
- **Persistência de Dados**: SQLite com `SQLAlchemy` (ORM) 
- **Contratos e Validação**: Pydantic
- **Dashboard e Monitoramento**: Streamlit
- **Gerenciador de Dependências**: UV (Para instalação super rápida no ecossistema Python)

---

## 🧠 Arquitetura de Agentes

O projeto utiliza um pipeline com os seguintes especialistas:

1. **SEO Strategist**: Analisa a palavra-chave, define o público-alvo e cria a estrutura (Outline) do artigo.
2. **Technical Writer**: Recebe a estrutura e escreve o conteúdo massivo (Trabalho bruto).
3. **Content Editor**: Revisa gramática, fluidez e aderência ao SEO. (Se o texto não estiver bom, ele devolve para o Writer reescrever, com limite de *1 iteração*).
4. **Content Designer**: Cria os *prompts* visuais para futura geração de infográficos ou capas.
5. **SEO Validator**: Dá a nota final do artigo antes dele ser publicado ou salvo no banco.

---

## 🛡️ Resiliência (String-Safe Fallbacks)

Uma das maiores inovações deste repositório é a sua **blindagem contra alucinações estruturais**. 
Modelos locais e menores (como o Llama 3) muitas vezes falham em retornar respostas JSON puras que o Pydantic consiga extrair. 

Este projeto possui:
* **Workflow Resiliente**: O roteador (LangGraph) sabe lidar com strings impuras caso a revisão falhe.
* **Repositório Blindado**: O banco de dados inspeciona variáveis nativas do Python e ignora métodos como `.title()` para extrair dados sem crashar o `commit` do SQLAlchemy.
* **Pára-quedas de Arquivo (Emergency Fallback)**: Se tudo der errado no banco, o sistema faz o "dump" do artigo em um arquivo `ARTIGO_BACKUP_EMERGENCIA.md` físico. **Nenhum processamento de LLM é perdido.**

---

## ⚙️ Instalação e Configuração

### 1. Requisitos
- **Python** (Gerenciado via UV)
- **Ollama** instalado no seu computador.

### 2. Configurar o Ambiente
```bash
# Clone este repositório
git clone https://github.com/Ricardo-Filgueiras/Agents-ferrametas-AI.git
cd Agents-ferrametas-AI/projeto-mult

# Instale as dependências com UV
uv sync

# Baixe o modelo local do Llama
ollama pull llama3.2:3b
```

### 3. Variáveis de Ambiente
Crie um arquivo `.env` na raiz da pasta `projeto-mult` baseado no `.env.example`:
```env
OPENAI_API_KEY=sua_chave_aqui (Opcional, se quiser usar a Cloud no futuro)
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 🕹️ Como Usar

### 1. Gerar um novo Artigo
No arquivo `src/main.py`, você pode definir a instrução e as palavras-chave na variável `tema`.

Em seguida, execute:
```bash
$env:PYTHONPATH="." ; uv run python -m src.main
```
Acompanhe os logs no terminal mostrando a passagem de bastão de cada agente!

### 2. Visualizar os Artigos no Dashboard
Inicie a interface Streamlit para ler os artigos aprovados e auditar os logs de execução:
```bash
uv run streamlit run src/interface/app.py
```

---

## 📂 Estrutura do Projeto

```text
├── data/                    # Banco de dados SQLite salvo aqui
├── src/
│   ├── agents/              # Prompt Engineering de cada agente especialista
│   ├── database/            # Models e Repository (Blindados contra String)
│   ├── graph/               # Workflow e Nós do LangGraph
│   ├── interface/           # Dashboard Web (app.py)
│   ├── schemas/             # Contratos Pydantic (AgentState)
│   ├── services/            # Serviços utilitários (ex: LLMFactory)
│   ├── main.py              # Entrypoint do pipeline
│   └── __init__.py          # Marcador de pacote Python
├── tests/                   # Testes unitários (Edge cases de resiliência)
├── .env.example             # Template das chaves de API
└── README.md                # Esta documentação
```
