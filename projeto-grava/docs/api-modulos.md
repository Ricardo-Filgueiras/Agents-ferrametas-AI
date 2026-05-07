# API & Módulos

Referência das classes e funções públicas do projeto.

---

## `llm/factory.py`

### `LLMFactory.create()`

Cria uma instância de cliente LLM com caching automático.

```python
@classmethod
def create(
    provider: str,
    model: str,
    streaming: bool = False
) -> BaseChatModel
```

**Parâmetros:**
- `provider` (str): `"Ollama (Local)"`, `"OpenAI"`, ou chaves internas `"ollama"`, `"openai"`
- `model` (str): Nome do modelo
  - Ollama: `"llama3.2:3b"`, `"gemma3:4b"`, `"mistral:7b"`, etc.
  - OpenAI: `"gpt-4o-mini"`, `"gpt-4"`, etc.
- `streaming` (bool): Se `True`, retorna cliente com streaming habilitado

**Retorna:**
- `BaseChatModel` (LangChain) — cliente pronto para usar com LCEL

**Raises:**
- `ValueError`: Se `provider` não for reconhecido

**Cache:**
- Até 8 combinações (provider, model, streaming) são cacheadas via `@lru_cache`
- Evita recriar clientes em cada chamada

**Exemplo:**
```python
from src.app.llm.factory import LLMFactory

# Ollama local
llm = LLMFactory.create("Ollama (Local)", "llama3.2:3b")

# OpenAI
llm_openai = LLMFactory.create("OpenAI", "gpt-4o-mini", streaming=True)

# Com LCEL
from src.app.llm.prompts import SUMMARY_PROMPT_V1
chain = SUMMARY_PROMPT_V1 | llm
response = chain.invoke({"transcricao": "..."})
```

---

## `storage/meeting_repository.py`

### `MeetingRepository`

Gerencia CRUD de reuniões armazenadas em disco.

```python
class MeetingRepository:
    def __init__(self, base_path: Path = PASTA_ARQUIVOS)
```

**Construtor:**
- `base_path` (Path): Diretório raiz (padrão: `data/`)
- Cria a pasta se não existir

### Métodos públicos

#### `listar()`

Lista todas as reuniões.

```python
def listar(self) -> dict[str, str]
```

**Retorna:**
- Dict: `{folder_id: formatted_label}`
- Formatado: `"YYYY/MM/DD HH:MM:SS — Título"` (mais recentes primeiro)

**Exemplo:**
```python
repo = MeetingRepository()
reunioes = repo.listar()
# {
#   "2026_05_07_10_30_45": "2026/05/07 10:30:45 — Planning Q2",
#   "2026_05_06_14_00_00": "2026/05/06 14:00:00 — One-on-one"
# }
```

#### `pasta()`

Retorna o caminho completo de uma reunião.

```python
def pasta(self, reuniao_id: str) -> Path
```

**Parâmetros:**
- `reuniao_id` (str): ID da reunião (chave de `listar()`)

**Retorna:**
- `Path` — caminho completo para a pasta

#### `titulo()`, `transcricao()`, `resumo()`

Lê arquivos de texto da reunião.

```python
def titulo(self, reuniao_id: str) -> str
def transcricao(self, reuniao_id: str) -> str
def resumo(self, reuniao_id: str) -> str
```

**Retorna:**
- String com conteúdo do arquivo
- `""` (vazio) se arquivo não existir

**Exemplo:**
```python
repo = MeetingRepository()
texto = repo.transcricao("2026_05_07_10_30_45")
print(texto)  # "João: Olá, tudo bem? Maria: Tudo, e você?..."
```

#### `salvar_titulo()`, `salvar_transcricao()`, `salvar_resumo()`

Escreve arquivos de texto.

```python
def salvar_titulo(self, reuniao_id: str, titulo: str) -> None
def salvar_transcricao(self, reuniao_id: str, texto: str) -> None
def salvar_resumo(self, reuniao_id: str, texto: str) -> None
```

**Parâmetros:**
- `reuniao_id` (str): ID da reunião
- `texto` (str): Conteúdo a salvar

**Cria a pasta se não existir.**

**Exemplo:**
```python
repo.salvar_titulo("2026_05_07_10_30_45", "Planning Q2")
repo.salvar_transcricao("2026_05_07_10_30_45", "João: ...")
repo.salvar_resumo("2026_05_07_10_30_45", "Resumo da reunião...")
```

#### `todas_transcricoes()`

Retorna todas as reuniões com suas transcrições (para RAG/indexação).

```python
def todas_transcricoes(self) -> list[dict]
```

**Retorna:**
- Lista de dicts: `[{id, titulo, transcricao}, ...]`
- Apenas reuniões que têm `transcricao.txt`

**Exemplo:**
```python
repo = MeetingRepository()
dados = repo.todas_transcricoes()
# [
#   {
#     "id": "2026_05_07_10_30_45",
#     "titulo": "Planning Q2",
#     "transcricao": "João: Olá..."
#   },
#   ...
# ]

# Útil para FAISS indexing:
from langchain.embeddings import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="llama3.2:3b")
for item in dados:
    vector = embeddings.embed_query(item["transcricao"])
    # indexar...
```

---

## `llm/prompts.py`

Templates de prompts versionados usando `ChatPromptTemplate`.

### `SUMMARY_PROMPT_V1`

Prompts para gerar atas de reunião.

```python
SUMMARY_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente especialista em análise de reuniões corporativas. "
        "Seja direto, objetivo e estruturado. Responda sempre em português."
    ),
    ("human",
     "Analise a transcrição abaixo e produza:\n\n"
     "**Resumo da Reunião:**\n"
     "- Um parágrafo resumindo os principais assuntos (máx. 300 caracteres).\n\n"
     "**Acordos da Reunião:**\n"
     "- Liste cada decisão ou combinado como bullet point.\n"
     "- Se não houver acordos explícitos, escreva: '- Nenhum acordo registrado.'\n\n"
     "Transcrição:\n####\n{transcricao}\n####\n\n"
     "IMPORTANTE: Responda EXCLUSIVAMENTE em português brasileiro."
    ),
])
```

**Variáveis:**
- `{transcricao}` — texto completo da transcrição

**Uso:**
```python
from src.app.llm.factory import LLMFactory
from src.app.llm.prompts import SUMMARY_PROMPT_V1

llm = LLMFactory.create("Ollama (Local)", "llama3.2:3b")
chain = SUMMARY_PROMPT_V1 | llm

response = chain.invoke({"transcricao": "João: Olá..."})
print(response.content)
```

### `MEETING_QA_PROMPT_V1`

Prompts para Q&A sobre histórico de reuniões (RAG).

```python
MEETING_QA_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente com acesso ao histórico de reuniões da empresa. "
        "Responda APENAS com base nas reuniões fornecidas como contexto. "
        "Se a informação não estiver no contexto, diga: 'Não encontrei essa informação nas reuniões registradas.'"
    ),
    ("human",
     "Reuniões disponíveis como contexto:\n{context}\n\n"
     "Pergunta: {question}"
    ),
])
```

**Variáveis:**
- `{context}` — reuniões relevantes (resultado de RAG/FAISS)
- `{question}` — pergunta do usuário

**Uso:**
```python
chain = MEETING_QA_PROMPT_V1 | llm

response = chain.invoke({
    "context": "Reunião 1:\nJoão: ...\n\nReunião 2:\nMaria: ...",
    "question": "Qual foi o principal acordo?"
})
```

---

## `llm/callbacks.py`

### `MeetingCallbackHandler`

Callback para logar latência, tokens e erros durante invocações LLM.

```python
class MeetingCallbackHandler(BaseCallbackHandler)
```

**Métodos principais:**
- `on_llm_start()` — Registra início da chamada
- `on_llm_end()` — Registra fim, calcula latência e tokens
- `on_llm_error()` — Loga exceções

**Logs:**
- Logger: `"projeto_grava.llm"`
- Exemplos:
  ```
  [INFO] LLM call started (model=llama3.2:3b)
  [INFO] LLM call completed in 12.34s (input_tokens=245, output_tokens=89)
  [ERROR] LLM error: ConnectionError on model=llama3.2:3b
  ```

**Uso:**
```python
from src.app.llm.callbacks import MeetingCallbackHandler

# Na invocação LCEL
response = chain.invoke(
    {"transcricao": "..."},
    config={"callbacks": [MeetingCallbackHandler()]}
)
```

---

## `ia_models.py`

### `carregar_whisper()`

Carrega o modelo Whisper com caching do Streamlit.

```python
@st.cache_resource
def carregar_whisper(tamanho_modelo: str = 'base') -> WhisperModel
```

**Parâmetros:**
- `tamanho_modelo` (str): `'tiny'`, `'base'`, `'small'`, `'medium'`

**Retorna:**
- `WhisperModel` do faster-whisper (reutilizado via cache)

**Nota:** Usa `@st.cache_resource` para evitar recarregar a cada rerun.

### `transcreve_audio()`

Transcreve um arquivo de áudio usando Whisper.

```python
def transcreve_audio(caminho_audio) -> str
```

**Parâmetros:**
- `caminho_audio` (str/Path): Caminho para arquivo `.mp3` ou `.wav`

**Retorna:**
- String: Texto completo transcrito

**Usa:**
- `st.session_state['modelo_whisper']` — tamanho do modelo
- `carregar_whisper()` — carrega/reutiliza modelo

**Exemplo:**
```python
from src.app.ia_models import transcreve_audio

texto = transcreve_audio("data/audio_part_0001.mp3")
print(texto)  # "João: Olá, Maria. Tudo bem?"
```

### `gerar_resumo()`

Gera ata de reunião via LLM (Ollama ou OpenAI).

```python
def gerar_resumo(pasta_reuniao) -> None
```

**Parâmetros:**
- `pasta_reuniao` (Path): Caminho para pasta da reunião (ex: `data/2026_05_07_10_30_45/`)

**Comportamento:**
1. Lê `transcricao.txt` da pasta
2. Cria LCEL chain: `SUMMARY_PROMPT_V1 | LLM`
3. Invoca com callbacks
4. Salva resultado em `resumo.txt` com atribuição de modelo

**Lê do session_state:**
- `st.session_state['provedor']` — `"Ollama (Local)"` ou `"OpenAI"`
- `st.session_state['modelo_ollama']` — ex: `"llama3.2:3b"`

**Erros:**
- Mostra `st.error()` se transcrição não existir ou LLM falhar

**Exemplo (do main.py):**
```python
from src.app.ia_models import gerar_resumo

if st.button("Gerar Resumo Inteligente"):
    gerar_resumo(Path("data/2026_05_07_10_30_45"))
    # Salva resultado em resumo.txt
```

---

## `utils.py` (helpers)

### `le_arquivo()`, `salva_arquivo()`

I/O básico de arquivos.

```python
def le_arquivo(caminho: Path) -> str
def salva_arquivo(caminho: Path, conteudo: str) -> None
```

### `listar_modelos_ollama()`

Faz poll HTTP para listar modelos disponíveis em Ollama.

```python
def listar_modelos_ollama() -> list[str]
```

**Retorna:**
- Lista de nomes de modelos (ex: `["llama3.2:3b", "gemma3:4b"]`)
- Lista vazia se Ollama não está rodando

### `listar_reunioes()`

Enumera pastas em `data/`.

```python
def listar_reunioes() -> dict[str, str]
```

**Retorna:**
- Dict idêntico a `MeetingRepository.listar()`

---

## Padrões LCEL

Para entender como usar os prompts e LLMs juntos:

```python
# Pattern 1: Simples
chain = prompt | llm
response = chain.invoke({"variavel": valor})

# Pattern 2: Com callbacks
response = chain.invoke(
    {"variavel": valor},
    config={"callbacks": [MeetingCallbackHandler()]}
)

# Pattern 3: Streaming (futuro)
for chunk in chain.stream({"variavel": valor}):
    print(chunk.content, end="", flush=True)
```

---

## Próximos passos

- [Arquitetura](arquitetura.md) — Diagramas de fluxo
- [FAQ](faq.md) — Troubleshooting
