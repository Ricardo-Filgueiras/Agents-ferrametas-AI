# 🏗️ Arquitetura Ideal — Projeto-Gravando
### Perspectiva de Desenvolvedor Sênior de AI Agents (LangChain + LCEL)

---

## 🔍 Diagnóstico: O que está bom e o que precisa evoluir

### ✅ Pontos fortes atuais
| Aspecto | Status |
|---|---|
| Separação em módulos (`audio`, `video`, `utils`) | ✅ Boa base |
| Uso de `faster-whisper` local | ✅ Correto |
| Suporte a Ollama + OpenAI | ✅ Correto |
| Captura de tela + WebRTC | ✅ Funcional |

### ❌ Problemas Críticos (visão sênior)

| Problema | Impacto | Local no código |
|---|---|---|
| **Lógica de IA misturada com UI** | Impossível testar/reutilizar | `main.py` linhas 346-356 |
| **`systemprompt.md` com sintaxe errada** | O prompt está envolvido por `'''` Python dentro do `.md` — isso é lido como string literal, não como prompt | `systemprompt.md` |
| **Sem tratamento de falhas no pipeline de IA** | Uma exceção derruba toda a gravação | `main.py` linhas 355-356 |
| **Sem memória de contexto entre reuniões** | O LLM não "conhece" reuniões anteriores | `ia_models.py` |
| **Prompt hardcoded como string simples** | Sem versionamento, sem variáveis tipadas | `utils.py` L22 |
| **Sem observabilidade** | Nenhum log de tokens, latência ou erros de LLM | todo o projeto |
| **`client` global no módulo** | Estado compartilhado — falha em concorrência | `ia_models.py` L14 |
| **Sem streaming de resumo** | O usuário espera sem feedback | `ia_models.py` L42 |
| **Pipeline monolítico** | Impossível trocar Whisper por outro STT | acoplamento total |

---

## 🎯 Arquitetura Ideal Proposta

A evolução natural é transformar o projeto num **sistema de AI Agents com LangChain**, onde cada responsabilidade vira um componente bem definido e intercambiável.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CAMADA UI (Streamlit)                     │
│              main.py — apenas orquestração de UI                │
└────────────────────────┬────────────────────────────────────────┘
                         │ invoca
┌────────────────────────▼────────────────────────────────────────┐
│                   CAMADA DE SERVIÇOS (services/)                 │
│                                                                  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │ TranscriptionSvc│  │  SummaryAgent    │  │  MeetingRAG   │  │
│  │ (STT Pipeline)  │  │  (ReAct Agent)   │  │  (Retriever)  │  │
│  └────────┬────────┘  └────────┬─────────┘  └──────┬────────┘  │
└───────────┼────────────────────┼───────────────────┼───────────┘
            │                    │                    │
┌───────────▼────────────────────▼───────────────────▼───────────┐
│                    CAMADA DE LLM (llm/)                          │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │              LLMFactory (Provider Pattern)                │  │
│   │  Ollama ←→ OpenAI ←→ Qualquer futuro provider            │  │
│   └──────────────────────────────────────────────────────────┘  │
│   ┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│   │PromptRegistry│  │ CallbackManager │  │   LLM Cache      │  │
│   │ (versionado) │  │  (observab.)    │  │  (InMemory/Redis)│  │
│   └──────────────┘  └─────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
            │                    │                    │
┌───────────▼────────────────────▼───────────────────▼───────────┐
│                  CAMADA DE CAPTURA (capture/)                    │
│   audio.py │ video.py │ printela.py │ system_audio.py           │
│                    (sem alteração estrutural)                     │
└─────────────────────────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────────────┐
│                CAMADA DE DADOS (storage/)                        │
│   MeetingRepository │ VectorStore (FAISS) │ FileStorage          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Pastas Proposta

```
src/
└── app/
    ├── main.py                  # UI apenas — sem lógica de IA
    │
    ├── capture/                 # Mantém como está (bom)
    │   ├── audio.py
    │   ├── video.py
    │   ├── printela.py
    │   └── system_audio.py
    │
    ├── services/                # ← NOVO: Orquestração de AI
    │   ├── transcription_service.py   # Pipeline STT com LCEL
    │   ├── summary_agent.py           # ReAct Agent para resumos
    │   └── meeting_rag.py             # RAG sobre reuniões passadas
    │
    ├── llm/                     # ← NOVO: Camada de LLM isolada
    │   ├── factory.py                 # LLMFactory (Provider Pattern)
    │   ├── prompts.py                 # PromptRegistry versionado
    │   └── callbacks.py              # Observabilidade centralizada
    │
    ├── storage/                 # ← NOVO: Repositório de dados
    │   ├── meeting_repository.py      # CRUD de reuniões
    │   └── vector_store.py            # FAISS para RAG
    │
    └── utils.py                 # Helpers puros (sem IA)
```

---

## 💡 Implementações Concretas

### 1. `llm/factory.py` — LLMFactory (Provider Pattern)

```python
# llm/factory.py
from functools import lru_cache
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

class LLMFactory:
    """Centraliza a criação de LLMs — troca de provider sem tocar em código de negócio."""

    @staticmethod
    @lru_cache(maxsize=8)  # Evita recriar o mesmo modelo repetidamente
    def create(provider: str, model: str, streaming: bool = False) -> BaseChatModel:
        if provider == "ollama":
            return ChatOllama(
                model=model,
                temperature=0,
                streaming=streaming,
            )
        elif provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=0,
                streaming=streaming,
            )
        raise ValueError(f"Provider desconhecido: {provider}")
```

---

### 2. `llm/prompts.py` — PromptRegistry Versionado

```python
# llm/prompts.py
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

# ✅ Prompts tipados, com variáveis explícitas e versionados
SUMMARY_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente especialista em análise de reuniões corporativas. "
        "Seja objetivo e estruturado."
    ),
    ("human",
     "Analise a transcrição abaixo e produza:\n"
     "1. Resumo executivo (máx. 300 caracteres)\n"
     "2. Decisões tomadas (bullet points)\n"
     "3. Próximos passos (bullet points com responsáveis se mencionados)\n\n"
     "Transcrição:\n####\n{transcricao}\n####"
    ),
])

MEETING_QA_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente com acesso ao histórico completo de reuniões da empresa. "
        "Use apenas as reuniões fornecidas como contexto."
    ),
    ("human", "Contexto de reuniões:\n{context}\n\nPergunta: {question}"),
])
```

---

### 3. `llm/callbacks.py` — Observabilidade Centralizada

```python
# llm/callbacks.py
import logging
import time
from langchain_core.callbacks import BaseCallbackHandler

logger = logging.getLogger("projeto_grava.llm")

class MeetingCallbackHandler(BaseCallbackHandler):
    """Loga métricas de cada chamada ao LLM — sem poluir o código de negócio."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        self._start_time = time.time()
        logger.info(f"[LLM] Iniciando chamada | modelo={serialized.get('name')}")

    def on_llm_end(self, response, **kwargs):
        elapsed = time.time() - self._start_time
        usage = response.llm_output.get("token_usage", {}) if response.llm_output else {}
        logger.info(
            f"[LLM] Concluído | latência={elapsed:.2f}s "
            f"| tokens_entrada={usage.get('prompt_tokens', '?')} "
            f"| tokens_saida={usage.get('completion_tokens', '?')}"
        )

    def on_llm_error(self, error, **kwargs):
        logger.error(f"[LLM] ERRO: {error}", exc_info=True)
```

---

### 4. `services/transcription_service.py` — Pipeline STT com LCEL

```python
# services/transcription_service.py
from pathlib import Path
from faster_whisper import WhisperModel
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import streamlit as st

@st.cache_resource
def _load_whisper(model_size: str) -> WhisperModel:
    return WhisperModel(model_size, device="cpu", compute_type="int8")


def _transcribe(inputs: dict) -> dict:
    """Step puro — recebe dict, retorna dict. Testável isoladamente."""
    model = _load_whisper(inputs["model_size"])
    segments, _ = model.transcribe(
        str(inputs["audio_path"]),
        beam_size=5,
        language="pt",
    )
    return {**inputs, "transcricao": " ".join(s.text for s in segments)}


def _salvar(inputs: dict) -> dict:
    """Step de persistência separado da transcrição."""
    pasta = inputs["pasta_reuniao"]
    (pasta / "transcricao.txt").write_text(inputs["transcricao"], encoding="utf-8")
    return inputs


# ✅ Pipeline LCEL: cada step é testável, substituível, observável
transcription_pipeline = (
    RunnablePassthrough()
    | RunnableLambda(_transcribe)
    | RunnableLambda(_salvar)
)

# Uso:
# transcription_pipeline.invoke({
#     "audio_path": Path("..."),
#     "pasta_reuniao": Path("..."),
#     "model_size": "base",
# })
```

---

### 5. `services/summary_agent.py` — ReAct Agent com Tools

```python
# services/summary_agent.py
from pathlib import Path
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from llm.factory import LLMFactory
from llm.prompts import SUMMARY_PROMPT_V1
from llm.callbacks import MeetingCallbackHandler
from storage.meeting_repository import MeetingRepository

repo = MeetingRepository()

@tool
def buscar_reunioes_anteriores(tema: str) -> str:
    """Busca reuniões passadas sobre um tema específico para contextualizar o resumo."""
    return repo.search_by_topic(tema)

@tool
def salvar_resumo(pasta_reuniao: str, resumo: str) -> str:
    """Salva o resumo gerado na pasta da reunião."""
    path = Path(pasta_reuniao) / "resumo.txt"
    path.write_text(resumo, encoding="utf-8")
    return f"Resumo salvo em {path}"


def criar_summary_agent(provider: str, model: str) -> AgentExecutor:
    """Factory do agente — recria com provider/model correto sem estado global."""
    llm = LLMFactory.create(provider=provider, model=model)
    tools = [buscar_reunioes_anteriores, salvar_resumo]

    agent = create_react_agent(llm=llm, tools=tools, prompt=SUMMARY_PROMPT_V1)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=5,           # ✅ Evita loops infinitos
        handle_parsing_errors=True, # ✅ Não derruba a aplicação
        callbacks=[MeetingCallbackHandler()],
        verbose=True,
    )
```

---

### 6. `services/meeting_rag.py` — RAG sobre Reuniões Passadas

```python
# services/meeting_rag.py
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from llm.factory import LLMFactory
from llm.prompts import MEETING_QA_PROMPT_V1

class MeetingRAG:
    """
    Permite perguntar sobre o histórico de reuniões.
    Ex: "O que foi decidido sobre o projeto X nos últimos 30 dias?"
    """

    def __init__(self, provider: str, model: str):
        self._embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self._llm = LLMFactory.create(provider=provider, model=model)
        self._vectorstore = None

    def indexar_reunioes(self, reunioes: list[dict]) -> None:
        """Indexa transcrições no FAISS — chamado após cada gravação."""
        docs = [
            Document(
                page_content=r["transcricao"],
                metadata={"titulo": r["titulo"], "data": r["data"]},
            )
            for r in reunioes if r.get("transcricao")
        ]
        self._vectorstore = FAISS.from_documents(docs, self._embeddings)

    def perguntar(self, pergunta: str) -> str:
        if not self._vectorstore:
            return "Nenhuma reunião indexada ainda."

        chain = RetrievalQA.from_chain_type(
            llm=self._llm,
            chain_type="stuff",
            retriever=self._vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": MEETING_QA_PROMPT_V1},
        )
        return chain.invoke({"query": pergunta})["result"]
```

---

### 7. `main.py` refatorado — UI apenas

```python
# main.py — APENAS orquestração de UI. Zero lógica de IA aqui.
import streamlit as st
from services.transcription_service import transcription_pipeline
from services.summary_agent import criar_summary_agent
from services.meeting_rag import MeetingRAG
from storage.meeting_repository import MeetingRepository

def tab_grava_reuniao():
    # ... setup de UI ...
    # A chamada de IA é um simples invoke:
    result = transcription_pipeline.invoke({
        "audio_path": audio_temp,
        "pasta_reuniao": pasta_reuniao,
        "model_size": st.session_state["modelo_whisper"],
    })
    st.markdown(result["transcricao"])


def tab_historico():
    repo = MeetingRepository()
    provider = st.session_state.get("provedor", "ollama")
    model = st.session_state.get("modelo_ollama", "llama3.2:3b")

    if st.button("✨ Gerar Resumo Inteligente"):
        agent = criar_summary_agent(provider=provider, model=model)
        # Streaming direto no Streamlit:
        with st.chat_message("assistant"):
            for chunk in agent.stream({"transcricao": transcricao}):
                st.write(chunk)

    # RAG sobre reuniões
    rag = MeetingRAG(provider=provider, model=model)
    pergunta = st.text_input("🔍 Pergunte sobre reuniões anteriores")
    if pergunta:
        with st.spinner("Buscando no histórico..."):
            resposta = rag.perguntar(pergunta)
            st.info(resposta)
```

---

## 🗺️ Mapa de Migração (Faseado)

```
FASE 1 — Correções críticas (sem mudança estrutural)
  ├── Corrigir systemprompt.md (remover ''' Python)
  ├── Mover client LLM para função, não global
  ├── Adicionar try/except no pipeline de transcrição
  └── Tipar o PROMPT com ChatPromptTemplate

FASE 2 — Introduzir LangChain (sem quebrar nada)
  ├── Criar llm/factory.py
  ├── Criar llm/prompts.py
  ├── Criar llm/callbacks.py
  └── Refatorar ia_models.py para usar factory + prompts

FASE 3 — Services com LCEL
  ├── Criar services/transcription_service.py (pipeline LCEL)
  ├── Criar services/summary_agent.py (ReAct Agent)
  └── Slim down main.py para UI-only

FASE 4 — RAG e Memória (novo valor)
  ├── Criar storage/meeting_repository.py
  ├── Criar storage/vector_store.py (FAISS)
  └── Criar services/meeting_rag.py
```

---

## ✅ Production Checklist (LangChain)

- [ ] `LLMFactory` com `lru_cache` — sem recriar clientes desnecessariamente
- [ ] `ChatPromptTemplate` tipado — sem f-strings soltas como prompts
- [ ] `AgentExecutor` com `max_iterations` e `handle_parsing_errors=True`
- [ ] `MeetingCallbackHandler` logando latência e tokens em cada call
- [ ] `FAISS` indexando transcrições para habilitar RAG
- [ ] Streaming de resumo via `agent.stream()` no Streamlit
- [ ] Testes unitários mockando o LLM (sem custo de API)
- [ ] `.env` com `LANGCHAIN_TRACING_V2=true` para LangSmith (observabilidade)
- [ ] `systemprompt.md` limpo — sem sintaxe Python misturada

---

> **Resumo executivo:** O projeto tem uma base de captura sólida.
> A evolução é desacoplar a IA da UI usando **LCEL** como espinha dorsal,
> **LLMFactory** para portabilidade de providers, **ReAct Agent** para
> raciocínio multi-step nos resumos, e **RAG sobre transcrições** para
> transformar reuniões gravadas em memória organizacional pesquisável.
