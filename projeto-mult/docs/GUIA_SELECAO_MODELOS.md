# 🤖 Guia de Seleção de Modelos Ollama

Este documento explica como usar o sistema de seleção de modelos Ollama do projeto.

## 📋 Sumário

1. [Instalação do Ollama](#instalação-do-ollama)
2. [Arquitetura](#arquitetura)
3. [Como Usar](#como-usar)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Instalação do Ollama

### 1. Baixar e Instalar

- **Website:** https://ollama.ai
- **Windows:** Baixe o instalador e execute
- **macOS:** `brew install ollama`
- **Linux:** `curl -fsSL https://ollama.ai/install.sh | sh`

### 2. Iniciar o Ollama

```bash
ollama serve
```

Isso inicia o servidor na porta 11434 (padrão).

### 3. Baixar um Modelo

```bash
ollama pull llama3.2:3b    # Modelo pequeno (~3 GB)
ollama pull llama3.2       # Modelo maior (~13 GB)
ollama pull mistral        # Outro exemplo
```

### 4. Listar Modelos Locais

```bash
ollama list
```

---

## 🏗️ Arquitetura

### Arquivos Criados/Modificados

```
src/
├── core/
│   └── config.py              # ⭐ Configurações centralizadas
├── services/
│   ├── llm_factory.py         # ⭐ Modificado - Factory de modelos
│   └── model_manager.py       # ⭐ Novo - Gerenciador de modelos Ollama
└── interface/
    └── model_selector.py      # ⭐ Novo - Componentes Streamlit
```

### Componentes Principais

**1. `OllamaModelManager`** (`src/services/model_manager.py`)
   - Lista modelos disponíveis
   - Verifica disponibilidade do Ollama
   - Formata tamanhos de arquivo
   - Permite download de novos modelos

**2. `LLMFactory`** (atualizado em `src/services/llm_factory.py`)
   - Cria instâncias de modelos OpenAI/Ollama
   - Integra com `OllamaModelManager`
   - Usa configurações de `config.py`

**3. Componentes Streamlit** (`src/interface/model_selector.py`)
   - `model_selector()` - Seletor interativo
   - `display_ollama_status()` - Status do Ollama
   - `model_info_display()` - Informações dos modelos
   - `setup_sidebar_model_config()` - Setup completo na sidebar

---

## 💻 Como Usar

### Opção 1: Interface Streamlit (Recomendado)

#### Simples - Apenas um seletor

```python
from src.interface.model_selector import model_selector
from src.services.llm_factory import LLMFactory

# Na sua página Streamlit
selected_model = model_selector(label="Escolha um modelo")

if selected_model:
    llm = LLMFactory.get_model("ollama", selected_model)
    # Use o LLM
```

#### Completo - Com sidebar

```python
from src.interface.model_selector import setup_sidebar_model_config

# No main() do seu app
selected_model = setup_sidebar_model_config()

if selected_model:
    st.write(f"Usando: {selected_model}")
```

#### Com Provider (Ollama + OpenAI)

```python
from src.interface.model_selector import provider_and_model_selector
from src.services.llm_factory import LLMFactory

provider, model = provider_and_model_selector()

if model:
    llm = LLMFactory.get_model(provider, model)
```

### Opção 2: Programaticamente (Sem Streamlit)

```python
from src.services.model_manager import OllamaModelManager
from src.services.llm_factory import LLMFactory

# Listar modelos
models = OllamaModelManager.get_model_names()
print(f"Modelos: {models}")

# Usar um modelo
if models:
    llm = LLMFactory.get_model("ollama", models[0])
    response = llm.invoke("Olá!")
```

---

## 📚 Exemplos Práticos

### Exemplo 1: Listar Modelos com Informações

```python
from src.services.model_manager import OllamaModelManager

models = OllamaModelManager.list_models()

for model in models:
    print(f"Modelo: {model['name']}")
    print(f"Tamanho: {model['size']}")
    print(f"Modificado: {model['modified_at']}")
    print("---")
```

**Saída:**
```
Modelo: llama3.2:3b
Tamanho: 2.0 GB
Modificado: 2024-05-20T10:30:45Z
---
Modelo: mistral:latest
Tamanho: 4.1 GB
Modificado: 2024-05-19T15:45:22Z
---
```

### Exemplo 2: Integração com Agentes

```python
from src.services.model_manager import OllamaModelManager
from src.agents.writer.agent import WriterAgent

# Selecionar modelo
models = OllamaModelManager.get_model_names()
selected = models[0] if models else "llama3.2:3b"

# Criar agente com modelo selecionado
agent = WriterAgent(model=selected)
result = agent.run("Escreva um artigo sobre IA")
```

### Exemplo 3: Fallback Automático

```python
from src.services.model_manager import OllamaModelManager
from src.services.llm_factory import LLMFactory

# Tenta usar Ollama, fallback para OpenAI
if OllamaModelManager.is_ollama_available():
    models = OllamaModelManager.get_model_names()
    llm = LLMFactory.get_model("ollama", models[0])
    provider = "Ollama"
else:
    llm = LLMFactory.get_model("openai", "gpt-4o-mini")
    provider = "OpenAI"

print(f"Usando: {provider}")
response = llm.invoke("Teste")
```

### Exemplo 4: Filtrar Modelos

```python
from src.services.model_manager import OllamaModelManager

all_models = OllamaModelManager.get_model_names()

# Apenas modelos Llama
llama_models = [m for m in all_models if "llama" in m.lower()]

# Apenas modelos pequenos (contêm :3b)
small_models = [m for m in all_models if ":3b" in m]

print(f"Modelos Llama: {llama_models}")
print(f"Modelos Pequenos: {small_models}")
```

---

## 🧪 Testar

Execute o script de teste:

```bash
python test_model_selection.py
```

Teste individual:

```python
# python
from src.services.model_manager import OllamaModelManager
print(OllamaModelManager.is_ollama_available())
print(OllamaModelManager.get_model_names())
```

---

## ⚙️ Configuração

Edite `.env` para customizar:

```bash
# Endereço do Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Modelo padrão
DEFAULT_OLLAMA_MODEL=llama3.2:3b

# Temperatura padrão
DEFAULT_TEMPERATURE=0.7
```

---

## 🐛 Troubleshooting

### "Ollama não está disponível"

**Causa:** Servidor Ollama não está rodando

**Solução:**
```bash
ollama serve
```

### "Nenhum modelo encontrado"

**Causa:** Nenhum modelo foi baixado

**Solução:**
```bash
ollama pull llama3.2:3b
ollama list  # Verificar
```

### "Erro de conexão: refused"

**Causa:** Ollama está usando porta diferente

**Solução:** Verificar `.env`:
```bash
OLLAMA_BASE_URL=http://localhost:11434  # Padrão
# ou
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

### "ImportError: cannot import name 'OllamaModelManager'"

**Causa:** Importação incorreta

**Solução:**
```python
# ❌ Errado
from model_manager import OllamaModelManager

# ✅ Correto
from src.services.model_manager import OllamaModelManager
```

### Modelo muito lento

**Solução:** Use um modelo menor
```bash
ollama pull llama3.2:3b     # Rápido (~3 GB)
ollama pull mistral:7b       # Médio (~4 GB)
ollama pull llama3.2         # Completo (~13 GB)
```

---

## 📖 API Reference

### OllamaModelManager

```python
# Listar todos os modelos com informações
OllamaModelManager.list_models() -> List[Dict[str, str]]

# Apenas nomes
OllamaModelManager.get_model_names() -> List[str]

# Verificar se disponível
OllamaModelManager.is_ollama_available() -> bool

# Baixar modelo
OllamaModelManager.pull_model(model_name: str) -> bool
```

### LLMFactory

```python
# Criar modelo
LLMFactory.get_model(provider: str, model_name: str, temperature: float = None)

# Listar modelos Ollama
LLMFactory.get_available_ollama_models() -> List[str]

# Verificar disponibilidade
LLMFactory.is_ollama_available() -> bool
```

### Componentes Streamlit

```python
# Seletor simples
model_selector(label: str, key: str, default: str) -> str

# Status do Ollama
display_ollama_status() -> bool

# Informações dos modelos
model_info_display()

# Seletor com provider
provider_and_model_selector() -> Tuple[str, str]

# Setup completo
setup_sidebar_model_config() -> str
```

---

## 🚀 Próximos Passos

1. **Integrar com a interface:** Adicione `setup_sidebar_model_config()` ao seu app.py
2. **Persistir seleção:** Use `st.session_state` para lembrar modelo selecionado
3. **Cache de modelos:** Optimize carregando modelo uma vez por sessão
4. **Monitor de performance:** Rastreie tempo de resposta por modelo

---

## 📞 Suporte

Para mais informações:
- [Ollama Documentation](https://github.com/ollama/ollama)
- [LangChain Ollama](https://python.langchain.com/en/latest/modules/models/llms/integrations/ollama.html)
- [Agno Documentation](https://docs.agno.com/)

---

**Última atualização:** Maio 2026
