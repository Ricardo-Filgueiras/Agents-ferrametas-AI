# 🤖 Agents & AI Tools Stack

Bem-vindo ao repositório central da minha stack de **Inteligência Artificial e Agentes Autônomos**. Este ecossistema reúne diversos projetos focados em processamento local, automação inteligente e interfaces modernas para interação com LLMs.

O objetivo deste repositório é servir como base sólida para o desenvolvimento de ferramentas que priorizam a privacidade, a eficiência e a modularidade.

---

## 🚀 Ecossistema de Projetos

Abaixo estão os principais módulos e ferramentas que compõem esta stack:

### 📽️ [Projeto Grava](projeto-grava/)
Uma solução de "MeetGPT" 100% local. Captura áudio/vídeo de reuniões, realiza transcrição offline via `faster-whisper` e gera atas inteligentes usando **Ollama** e **LangChain**.

### 🏗️ [Projeto Graph](projeto-graph/)
Infraestrutura profissional para agentes de IA baseada em **LangGraph**. Focado em arquitetura modular, escalabilidade e persistência de estado de longa duração com SQLite.

### 📚 [Projeto Docstóteles](projeto-docstoteles/)
Transforma qualquer documentação web em um assistente de IA. Utiliza **Fire Crawl** para scraping inteligente e um pipeline de **RAG** (Retrieval-Augmented Generation) para respostas precisas e atualizadas.

### 🐙 [Projeto Octo](projeto-octo/)
Laboratório de experimentos práticos com LLMs locais. Demonstra integrações de LangChain com Ollama, uso de embeddings, chains e automação de desenvolvimento assistida por IA.

### 🛰️ [Projeto Tenmode](projeto-tenmode/)
Agente Pessoal ("Tentáculo Mode") com interface via **Telegram**. Opera 100% localmente, possui motor ReAct para uso de ferramentas e sistema de *Hot-Reload* para carregamento dinâmico de habilidades (*Skills*).

---

## 🛠️ Outros Projetos em Desenvolvimento
Os seguintes projetos fazem parte da stack e estão em fases iniciais de desenvolvimento ou servem como módulos de suporte:

*   **projeto-agents**: (Em breve)
*   **projeto-agno**: (Em breve)
*   **projeto-cubo**: (Em breve)
*   **projeto-langchain**: (Em breve)
*   **projeto-nova**: (Em breve)

---

## ⚙️ Stack Tecnológica Base

*   **Orquestração:** LangChain, LangGraph.
*   **LLMs Locais:** Ollama (Llama 3.2, Phi 3, etc.).
*   **Interface:** Streamlit, Telegram API, CLI (Rich).
*   **Banco de Dados:** SQLite (com persistência de estado).
*   **Processamento de Mídia:** PyAV, Faster-Whisper.
*   **Gerenciamento de Pacotes:** [UV](https://github.com/astral-sh/uv).

---

## 📝 Licença
Este repositório está sob a licença MIT. Sinta-se à vontade para explorar e adaptar os agentes para suas necessidades.
