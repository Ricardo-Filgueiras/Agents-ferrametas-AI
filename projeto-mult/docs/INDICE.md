# 📑 Índice - Sistema de Seleção de Modelos Ollama

## 🎯 Comece por aqui

Se você é novo, comece por este arquivo:
- 👉 **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - 5 minutos de leitura

---

## 📚 Documentação Completa

### Para Entender o Sistema
1. **[README_MODELOS.md](README_MODELOS.md)** - Resumo executivo
2. **[SUMARIO_IMPLEMENTACAO.md](SUMARIO_IMPLEMENTACAO.md)** - Visão técnica
3. **[GUIA_SELECAO_MODELOS.md](GUIA_SELECAO_MODELOS.md)** - Documentação detalhada

### Para Implementar
1. **[CHECKLIST_SETUP.md](CHECKLIST_SETUP.md)** - Passo a passo de setup
2. **[EXEMPLO_INTEGRACAO_APP.py](EXEMPLO_INTEGRACAO_APP.py)** - Como integrar no seu app.py
3. **[examples_model_selection.py](examples_model_selection.py)** - Exemplos de código

### Para Testar
1. **[test_model_selection.py](test_model_selection.py)** - Script de testes

---

## 💻 Arquivos de Código Criados

### Core (Configuração)
```
src/core/config.py
```
- Configurações centralizadas
- Variáveis de ambiente
- Valores padrão

### Services (Lógica)
```
src/services/model_manager.py        ← NOVO
src/services/llm_factory.py           ← ATUALIZADO
```

**model_manager.py:**
- Lista modelos Ollama
- Verifica disponibilidade
- Gerencia downloads

**llm_factory.py:**
- Factory de modelos
- Integração com model_manager
- Suporte a múltiplos providers

### Interface (UI)
```
src/interface/model_selector.py      ← NOVO
```
- Componentes Streamlit
- Seletores visuais
- Dashboard de modelos

---

## 🔍 Mapa de Funcionalidades

### 1. Listar Modelos

```python
from src.services.model_manager import OllamaModelManager

# Apenas nomes
OllamaModelManager.get_model_names()

# Com detalhes
OllamaModelManager.list_models()
```

📍 Localização: `src/services/model_manager.py`

---

### 2. Verificar Status

```python
from src.services.model_manager import OllamaModelManager

OllamaModelManager.is_ollama_available()
```

📍 Localização: `src/services/model_manager.py`

---

### 3. Criar Modelo LLM

```python
from src.services.llm_factory import LLMFactory

llm = LLMFactory.get_model("ollama", "llama3.2:3b")
response = llm.invoke("Sua pergunta")
```

📍 Localização: `src/services/llm_factory.py`

---

### 4. Interface Streamlit

```python
from src.interface.model_selector import model_selector

# Opção A: Sidebar completa
from src.interface.model_selector import setup_sidebar_model_config
model = setup_sidebar_model_config()

# Opção B: Seletor simples
model = model_selector()
```

📍 Localização: `src/interface/model_selector.py`

---

## 🚀 Fluxo Rápido

```
1️⃣ Instalar Ollama
   → https://ollama.ai

2️⃣ Iniciar servidor
   → ollama serve

3️⃣ Baixar modelo
   → ollama pull llama3.2:3b

4️⃣ Testar setup
   → python test_model_selection.py

5️⃣ Integrar ao seu projeto
   → Ver EXEMPLO_INTEGRACAO_APP.py
```

---

## 📊 Estrutura de Arquivos

```
projeto-mult/
├── src/
│   ├── core/
│   │   └── config.py                    ✨ NOVO
│   ├── services/
│   │   ├── model_manager.py             ✨ NOVO
│   │   └── llm_factory.py               🔄 ATUALIZADO
│   └── interface/
│       └── model_selector.py            ✨ NOVO
│
├── GUIA_RAPIDO.md                       📋 (leia primeiro!)
├── README_MODELOS.md                    📋 (resumo)
├── GUIA_SELECAO_MODELOS.md              📚 (completo)
├── SUMARIO_IMPLEMENTACAO.md             📚 (técnico)
├── CHECKLIST_SETUP.md                   ✅ (passo a passo)
├── EXEMPLO_INTEGRACAO_APP.py            📝 (code ready)
├── examples_model_selection.py          💡 (exemplos)
├── test_model_selection.py              🧪 (testes)
└── INDICE.md                            📑 (este arquivo)
```

---

## 🎯 Casos de Uso

### Caso 1: Aplicação Web com Seleção Visual

```python
# Use EXEMPLO_INTEGRACAO_APP.py como template
from src.interface.model_selector import setup_sidebar_model_config

model = setup_sidebar_model_config()
# Exibe seletor na sidebar com status
```

### Caso 2: Script Batch

```python
# Use examples_model_selection.py como referência
from src.services.model_manager import OllamaModelManager

models = OllamaModelManager.get_model_names()
for model in models:
    # Processar cada modelo
    pass
```

### Caso 3: Agente com Modelo Selecionado

```python
# Use EXEMPLO_INTEGRACAO_APP.py
llm = LLMFactory.get_model("ollama", selected_model)
agent = WriterAgent(model=llm)
```

---

## ❓ Perguntas Comuns

### P: Por onde começo?
**R:** Leia `GUIA_RAPIDO.md` (5 min)

### P: Como integro no meu app.py?
**R:** Veja `EXEMPLO_INTEGRACAO_APP.py` (copy-paste ready)

### P: Como faço testes?
**R:** Execute `python test_model_selection.py`

### P: Preciso de Ollama rodando sempre?
**R:** Sim, `ollama serve` deve estar ativo

### P: Pode usar OpenAI ao invés de Ollama?
**R:** Sim, use `LLMFactory.get_model("openai", model_name)`

---

## 🔗 Dependências

Nenhuma dependência nova foi adicionada!

Usa:
- ✅ `langchain-ollama` (já no seu pyproject.toml)
- ✅ `requests` (padrão Python)
- ✅ `streamlit` (já no seu pyproject.toml)

---

## 📈 Próximos Passos

1. ✅ Leia `GUIA_RAPIDO.md`
2. ✅ Execute `python test_model_selection.py`
3. ✅ Estude `EXEMPLO_INTEGRACAO_APP.py`
4. ✅ Integre ao seu `app.py`
5. ✅ Teste com sua aplicação

---

## 🎓 Recursos Educacionais

- **[Ollama Docs](https://github.com/ollama/ollama)** - Documentação oficial
- **[LangChain Ollama](https://python.langchain.com/en/latest/modules/models/llms/integrations/ollama.html)** - Integração LangChain
- **[Agno Docs](https://docs.agno.com/)** - Framework de agentes

---

## ⚙️ Variáveis de Ambiente

```bash
# .env
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_OLLAMA_MODEL=llama3.2:3b
DEFAULT_TEMPERATURE=0.7
OPENAI_API_KEY=sk-...  (opcional)
```

---

## 🧪 Comandos Úteis

```bash
# Ollama
ollama serve                    # Iniciar servidor
ollama list                     # Ver modelos instalados
ollama pull llama3.2:3b         # Baixar modelo
ollama rm llama3.2:3b           # Remover modelo

# Projeto
python test_model_selection.py  # Testar setup
python EXEMPLO_INTEGRACAO_APP.py # Ver exemplo
```

---

## 📞 Mapa de Navegação

```
Iniciante?
  → GUIA_RAPIDO.md

Desenvolvedor?
  → EXEMPLO_INTEGRACAO_APP.py

Arquiteto?
  → SUMARIO_IMPLEMENTACAO.md

Setup?
  → CHECKLIST_SETUP.md

Exemplos?
  → examples_model_selection.py

Documentação?
  → GUIA_SELECAO_MODELOS.md

Testes?
  → test_model_selection.py
```

---

## 💾 Versão e Status

```
Versão:  1.0
Data:    Maio 2026
Status:  ✅ Pronto para Produção
Testes:  ✅ Inclusos
Docs:    ✅ Completas
Code:    ✅ Testado
```

---

## 🎯 TL;DR (Ultra Rápido)

```
1. ollama serve
2. ollama pull llama3.2:3b
3. python test_model_selection.py
4. Copie de EXEMPLO_INTEGRACAO_APP.py
5. Use em seu app!
```

---

## 📍 Localize Rápido

```
Preciso de...

✅ Função para listar modelos
   → OllamaModelManager.get_model_names()
   
✅ Função para criar LLM
   → LLMFactory.get_model()
   
✅ Componente visual Streamlit
   → model_selector()
   
✅ Setup completo Streamlit
   → setup_sidebar_model_config()
   
✅ Verificar status
   → OllamaModelManager.is_ollama_available()
```

---

**Hora de começar! Vá para [GUIA_RAPIDO.md](GUIA_RAPIDO.md)** 🚀
