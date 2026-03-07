(# Projeto Octo: IA Local com LangChain e Ollama)

Este projeto demonstra como utilizar modelos de linguagem (LLMs) localmente, integrando LangChain, Ollama e exemplos práticos em Python e Jupyter Notebook. O objetivo é facilitar experimentos, prototipagem e desenvolvimento de aplicações de IA generativa, com destaque para uso local e integração com o Visual Studio Code.

## Principais Recursos

- **Execução local de LLMs**: Utilize modelos como Llama, Mistral, Phi, entre outros, rodando localmente via [Ollama](https://ollama.com/).
- **Integração com LangChain**: Fluxos de IA, chains, embeddings, retrieval e muito mais usando a biblioteca LangChain.
- **Exemplos práticos**: Notebooks em `exemplos/` mostram desde o uso básico de modelos até aplicações avançadas de IA generativa.
- **Agente no VS Code**: Aproveite o poder do agente Copilot no VS Code para acelerar o desenvolvimento, gerar código, documentar e automatizar tarefas.

## Estrutura do Projeto

- `main.py`: Script principal de exemplo.
- `requirements.txt` e `pyproject.toml`: Dependências do projeto.
- `data/`: Dados de exemplo para experimentos.
- `exemplos/`: Notebooks Jupyter com tutoriais e demonstrações.

## Instalação

1. **Clone o repositório:**
	```bash
	git clone https://github.com/seu-usuario/projeto-octo.git
	cd projeto-octo
	```
2. **Crie e ative um ambiente virtual:**
	```bash
	python -m venv .venv
	# Windows:
	.venv\Scripts\activate
	# Linux/Mac:
	source .venv/bin/activate
	```
3. **Instale as dependências:**
	```bash
	pip install -r requirements.txt
	```
4. **Instale e rode o Ollama:**
	- Baixe e instale o [Ollama](https://ollama.com/download) para seu sistema operacional.
	- Inicie o Ollama:
	  ```bash
	  ollama serve
	  ```
	- Baixe um modelo, por exemplo:
	  ```bash
	  ollama pull llama3
	  ```

## Exemplos de Uso

### 1. Rodando um modelo localmente
Veja o notebook `exemplos/02_models.ipynb` para exemplos de uso do Ollama com LangChain.

### 2. Chains, Embeddings e Retrieval
Explore os notebooks em `exemplos/` para:
- Criar chains customizadas
- Utilizar embeddings e vetorização
- Realizar buscas e RAG pipelines

### 3. Desenvolvimento com o Agente no VS Code
- Utilize o agente Copilot (GPT-4.1) diretamente no VS Code para:
  - Gerar código Python e notebooks
  - Automatizar tarefas repetitivas
  - Documentar funções e fluxos
  - Receber sugestões inteligentes durante o desenvolvimento

## Sugestão de Fluxo de Trabalho

1. Inicie o Ollama localmente.
2. Abra o projeto no VS Code.
3. Use o agente Copilot para explorar, modificar e criar notebooks ou scripts.
4. Execute e teste os exemplos em Jupyter ou diretamente no terminal.

## Requisitos

- Python >= 3.12
- Ollama instalado e rodando localmente
- VS Code (recomendado) com suporte a notebooks e agente Copilot

## Créditos

Projeto inspirado em aplicações modernas de IA generativa, combinando LangChain, Ollama e o poder do desenvolvimento assistido por IA no VS Code.
