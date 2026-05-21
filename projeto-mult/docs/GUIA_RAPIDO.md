# 🚀 Guia Rápido: Seleção de Modelos Ollama

## ⚡ TL;DR (Resumo Executivo)

### 1. Instale e Inicie o Ollama

```bash
# Baixe em https://ollama.ai

# Inicie o servidor
ollama serve

# Em outro terminal, baixe um modelo
ollama pull llama3.2:3b
```

### 2. Três Formas de Usar

#### 🎨 Na Interface Streamlit (Recomendado)

```python
from src.interface.model_selector import setup_sidebar_model_config
from src.services.llm_factory import LLMFactory

# Na sua função main():
selected_model = setup_sidebar_model_config()

if selected_model:
    llm = LLMFactory.get_model("ollama", selected_model)
    response = llm.invoke("Sua pergunta aqui")
```

#### 📊 Listar Modelos

```python
from src.services.model_manager import OllamaModelManager

models = OllamaModelManager.get_model_names()
print(models)  # ['llama3.2:3b', 'mistral', ...]
```

#### 🔧 Programaticamente

```python
from src.services.llm_factory import LLMFactory

llm = LLMFactory.get_model("ollama", "llama3.2:3b")
response = llm.invoke("Teste")
print(response.content)
```

---

## 📁 O Que Foi Criado

| Arquivo | Descrição |
|---------|-----------|
| `src/core/config.py` | ✨ Configurações centralizadas |
| `src/services/model_manager.py` | ✨ Gerenciador de modelos Ollama |
| `src/services/llm_factory.py` | 🔄 Atualizado - integrado com model_manager |
| `src/interface/model_selector.py` | ✨ Componentes Streamlit para UI |
| `GUIA_SELECAO_MODELOS.md` | 📖 Documentação completa |
| `test_model_selection.py` | 🧪 Script de testes |
| `examples_model_selection.py` | 💡 Exemplos de uso |
| `EXEMPLO_INTEGRACAO_APP.py` | 📝 Exemplo de integração |

---

## 🎯 Funções Principais

### OllamaModelManager (src/services/model_manager.py)

```python
OllamaModelManager.is_ollama_available()      # Verifica se está rodando
OllamaModelManager.get_model_names()          # Lista de nomes
OllamaModelManager.list_models()              # Com detalhes (tamanho, data)
OllamaModelManager.pull_model("llama3.2")     # Baixa um modelo
```

### LLMFactory (src/services/llm_factory.py)

```python
LLMFactory.get_model(provider, model_name)              # Cria instância
LLMFactory.get_available_ollama_models()                # Lista de modelos
LLMFactory.is_ollama_available()                        # Verifica disponibilidade
```

### Componentes Streamlit (src/interface/model_selector.py)

```python
model_selector()                              # Seletor simples
display_ollama_status()                       # Status visual
model_info_display()                          # Tabela de modelos
provider_and_model_selector()                 # Seletor com provider
setup_sidebar_model_config()                  # Setup completo
```

---

## 🧪 Testar

```bash
# Teste rápido
python test_model_selection.py

# Teste com Python
python
>>> from src.services.model_manager import OllamaModelManager
>>> OllamaModelManager.is_ollama_available()
True
>>> OllamaModelManager.get_model_names()
['llama3.2:3b', 'mistral']
```

---

## ⚙️ Configuração (.env)

```bash
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_OLLAMA_MODEL=llama3.2:3b
DEFAULT_TEMPERATURE=0.7
```

---

## 🎨 Exemplos Simples

### Ex. 1: Listar Modelos

```python
from src.services.model_manager import OllamaModelManager

for model in OllamaModelManager.list_models():
    print(f"{model['name']} - {model['size']}")
```

### Ex. 2: Usar Modelo

```python
from src.services.llm_factory import LLMFactory

llm = LLMFactory.get_model("ollama", "llama3.2:3b")
print(llm.invoke("Olá!"))
```

### Ex. 3: Fallback Automático

```python
if LLMFactory.is_ollama_available():
    llm = LLMFactory.get_model("ollama", "llama3.2:3b")
else:
    llm = LLMFactory.get_model("openai", "gpt-4o-mini")
```

### Ex. 4: Na Sidebar (Streamlit)

```python
import streamlit as st
from src.interface.model_selector import setup_sidebar_model_config

st.set_page_config(layout="wide")
model = setup_sidebar_model_config()
st.write(f"Modelo: {model}")
```

---

## 🔍 Troubleshooting

| Problema | Solução |
|----------|---------|
| ❌ "Ollama não disponível" | Execute `ollama serve` |
| ❌ "Nenhum modelo" | Execute `ollama pull llama3.2:3b` |
| ❌ Conexão recusada | Verifique `.env` OLLAMA_BASE_URL |
| ❌ ImportError | Use `from src.services...` (caminho correto) |
| 🐢 Modelo lento | Use `llama3.2:3b` (pequeno/rápido) |

---

## 📚 Arquivos de Referência

| Arquivo | Conteúdo |
|---------|----------|
| `GUIA_SELECAO_MODELOS.md` | Documentação detalhada |
| `EXEMPLO_INTEGRACAO_APP.py` | Como integrar ao app.py |
| `examples_model_selection.py` | Exemplos de código |
| `test_model_selection.py` | Testes automáticos |

---

## 🚀 Próximos Passos

1. ✅ Instale Ollama
2. ✅ Baixe um modelo: `ollama pull llama3.2:3b`
3. ✅ Inicie: `ollama serve`
4. ✅ Teste: `python test_model_selection.py`
5. ✅ Use na sua app

---

**Dúvidas?** Consulte `GUIA_SELECAO_MODELOS.md` para documentação completa.
