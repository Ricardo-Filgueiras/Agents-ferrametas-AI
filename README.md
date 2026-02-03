# Ferrametas-de-IA 🤖

**Até onde é possível usar IA no nosso dia a dia?**

Este repositório contém projetos experimentais para explorar a integração de Inteligência Artificial (IA) em aplicações práticas, utilizando frameworks modernos como **LangChain** e **Agno**.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação do UV](#instalação-do-uv)
- [Configuração do Projeto](#configuração-do-projeto)
- [Como Usar](#como-usar)
- [Dependências](#dependências)
- [Contribuindo](#contribuindo)

---

## 🎯 Visão Geral

Este projeto explora diferentes abordagens para integrar IA em aplicações:

- **Projeto Agno**: Utiliza o framework Agno para criação de agentes inteligentes
- **Projeto LangChain**: Implementa soluções RAG (Retrieval Augmented Generation) combinando LangChain com OpenAI e Google Gemini

Ambos os projetos utilizam **UV** para gerenciamento de dependências e ambientes virtuais, oferecendo uma experiência rápida e eficiente.

---

## 🏗️ Estrutura do Projeto

```
Agents-ferrametas-AI/
├── README.md                          # Este arquivo
├── LICENSE                            # Licença do projeto
│
├── projeto-agno/                      # Projeto com framework Agno
│   ├── pyproject.toml                # Configuração do projeto (UV)
│   ├── requirements.txt               # Dependências alternativas (pip)
│   ├── README.md                      # Documentação específica
│   ├── main.py                        # Ponto de entrada principal
│   └── hello.py                       # Script de teste
│
└── projeto-langchain/                 # Projeto com LangChain e RAG
    ├── requirements.txt               # Dependências do projeto
    ├── app.py                         # Aplicação principal RAG
    ├── gem.py                         # Implementação com Google Gemini
    ├── gem2.py                        # Variação com Gemini
    ├── openai.py                      # Integração com OpenAI
    └── data/
        └── dadosbasev1.csv           # Base de dados para RAG
```

### Detalhamento dos Componentes

#### **projeto-agno/**
- **Framework**: Agno (agentes inteligentes)
- **Python**: >= 3.12
- **Propósito**: Experimentar com agentes de IA utilizando o framework Agno
- **Arquivos principais**:
  - `main.py`: Lógica principal da aplicação
  - `hello.py`: Script de demonstração

#### **projeto-langchain/**
- **Framework**: LangChain + OpenAI/Google Gemini
- **Padrão**: RAG (Retrieval Augmented Generation)
- **Propósito**: Criar assistentes inteligentes baseados em documentos
- **Arquivos principais**:
  - `app.py`: Implementação principal com OpenAI
  - `gem.py` e `gem2.py`: Alternativas com Google Gemini
  - `openai.py`: Configurações específicas OpenAI
  - `data/dadosbasev1.csv`: Base de conhecimento para o RAG

---

## 📦 Pré-requisitos

Antes de começar, você precisa ter:

- **Python** 3.12 ou superior
- **Git** (para clonar o repositório)
- **Conexão com Internet** (para baixar dependências)

### Verificar versão do Python

```bash
python --version
```

Se a versão for menor que 3.12, atualize o Python.

---

## 🚀 Instalação do UV

### O que é UV?

**UV** é um gerenciador de pacotes Python super rápido escrito em Rust. Ele substitui `pip`, `venv` e `virtualenv` com uma solução unificada, mais rápida e confiável.

**Vantagens do UV:**
- ⚡ Até 10x mais rápido que pip
- 🔒 Melhor resolução de dependências
- 📦 Gerencia ambientes virtuais automaticamente
- 🎯 Configuração centralizada via `pyproject.toml`

### Passo 1: Instalar o UV

#### **Windows (PowerShell)**

```powershell
# Opção 1: Usando Invoke-WebRequest
powershell -ExecutionPolicy BypassUser -c "irm https://astral.sh/uv/install.ps1 | iex"

# Opção 2: Usando winget (se disponível)
winget install astral-sh.uv
```

#### **macOS / Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Após a instalação, adicione UV ao PATH ou reinicie seu terminal.

### Passo 2: Verificar a Instalação

```bash
uv --version
```

Você deverá ver a versão instalada, por exemplo: `uv 0.1.0`

### Passo 3: Criar um Alias (Opcional, recomendado)

Se em Windows você preferir usar `uv` em vez de `uvx`:

```powershell
# Verificar se uv está no PATH
where.exe uv
```

---

## ⚙️ Configuração do Projeto

### Clone o Repositório

```bash
git clone https://github.com/seu-usuario/Agents-ferrametas-AI.git
cd Agents-ferrametas-AI
```

### Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz de cada projeto com suas chaves de API:

#### **projeto-agno/.env**

```env
# Adicione suas chaves de API necessárias
# AGNO_API_KEY=sua_chave_aqui
```

#### **projeto-langchain/.env**

```env
# Chave OpenAI (obrigatória para app.py)
OPENAI_API_KEY=sk-seu-token-aqui

# Chave Google Gemini (para gem.py e gem2.py)
GOOGLE_API_KEY=sua-chave-google-aqui
```

**⚠️ Segurança**: Nunca commite o arquivo `.env` ao repositório. Ele deve estar no `.gitignore`.

### Instalar Dependências com UV

#### **Para projeto-agno:**

```bash
cd projeto-agno

# Instalar dependências
uv sync

# Ativar o ambiente virtual (se necessário)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

#### **Para projeto-langchain:**

```bash
cd projeto-langchain

# Instalar dependências com pip (compatível com uv também)
uv pip install -r requirements.txt

# Ou criar ambiente virtual primeiro
uv venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt
```

---

## 🎮 Como Usar

### Executar projeto-agno

```bash
cd projeto-agno

# Executar o programa principal
python main.py

# Ou executar o script de teste
python hello.py
```

**Saída esperada:**
```
Hello from projeto-agno!
```

### Executar projeto-langchain

```bash
cd projeto-langchain

# Executar aplicação RAG
python app.py
```

Este comando:
1. Carrega os dados de `dadosbasev1.csv`
2. Cria embeddings usando OpenAI
3. Constrói um índice FAISS para busca vetorial
4. Inicializa um modelo de linguagem (GPT-4o-mini por padrão)
5. Ativa o sistema RAG para responder perguntas baseado nos documentos

---

## 📚 Dependências

### projeto-agno

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| agno | >=2.4.8 | Framework para criar agentes inteligentes |
| python-dotenv | >=1.2.1 | Carrega variáveis de ambiente do `.env` |

### projeto-langchain

| Pacote | Descrição |
|--------|-----------|
| langchain-core | Core do LangChain |
| langchain-openai | Integração com OpenAI |
| langchain-community | Ferramentas comunitárias do LangChain |
| python-dotenv | Gerenciador de variáveis de ambiente |
| langchain-google-genai | Integração com Google Generative AI |

---

## 🔧 Troubleshooting

### Erro: "uv command not found"

**Solução Windows:**
```powershell
# Adicionar ao PATH manualmente
$env:Path += ";C:\Users\SeuUsuário\.cargo\bin"
```

**Solução macOS/Linux:**
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Erro: "ModuleNotFoundError: No module named 'dotenv'"

```bash
# Reinstalar dependências
cd seu-projeto
uv sync --force
```

### Erro de conexão com API (OpenAI/Google)

- Verifique se o arquivo `.env` existe na pasta correta
- Confirme que as chaves de API estão corretas e ativas
- Verifique sua conexão com a Internet

---

## 💡 Próximos Passos

1. **Customizar prompts**: Edite os templates de prompts em `app.py`
2. **Adicionar novos dados**: Coloque mais arquivos CSV em `data/`
3. **Integrar com interfaces**: Crie um frontend com Streamlit ou FastAPI
4. **Expandir modelos**: Teste outros modelos de linguagem

---

## 📝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📧 Contato

Para dúvidas ou sugestões, entre em contato ou abra uma issue no repositório.

---

**Última atualização**: Fevereiro de 2026
