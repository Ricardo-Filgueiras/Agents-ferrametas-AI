# ✅ Checklist de Setup - Seleção de Modelos Ollama

## 📋 Pré-Requisitos

- [ ] Python 3.13+
- [ ] Dependências instaladas (`pip install -r requirements.txt` ou `pip install langchain-ollama`)
- [ ] `.env` configurado ou variáveis de ambiente

---

## 🚀 Instalação e Setup

### Fase 1: Instalar Ollama

- [ ] Baixar Ollama em https://ollama.ai
- [ ] Executar instalador
- [ ] Verificar instalação: `ollama --version`

### Fase 2: Iniciar Ollama

- [ ] Abrir terminal/prompt
- [ ] Executar: `ollama serve`
- [ ] Verificar mensagem: "Listening on 127.0.0.1:11434"
- [ ] ⚠️ DEIXAR ESTE TERMINAL ABERTO

### Fase 3: Baixar Modelo

- [ ] Abrir novo terminal
- [ ] Executar: `ollama pull llama3.2:3b`
- [ ] Aguardar download (pode levar 5-10 minutos)
- [ ] Verificar: `ollama list` (deve mostrar o modelo)

### Fase 4: Configurar Projeto

- [ ] Criar/editar `.env` na raiz do projeto
- [ ] Adicionar:
  ```
  OLLAMA_BASE_URL=http://localhost:11434
  DEFAULT_OLLAMA_MODEL=llama3.2:3b
  DEFAULT_TEMPERATURE=0.7
  ```
- [ ] Salvar `.env`

---

## 🧪 Testes

### Teste 1: Verificar Instalação

```bash
python test_model_selection.py
```

- [ ] Teste 1 (Conexão) passou? ✅
- [ ] Teste 2 (Listar modelos) passou? ✅
- [ ] Todos os testes passaram? ✅

### Teste 2: Teste Rápido Python

```python
python
>>> from src.services.model_manager import OllamaModelManager
>>> OllamaModelManager.is_ollama_available()
# Deve retornar: True
>>> OllamaModelManager.get_model_names()
# Deve retornar: ['llama3.2:3b'] ou similar
```

- [ ] Conexão com Ollama OK? ✅
- [ ] Modelo listado? ✅

### Teste 3: Teste de Invocação

```python
python
>>> from src.services.llm_factory import LLMFactory
>>> llm = LLMFactory.get_model("ollama", "llama3.2:3b")
>>> response = llm.invoke("Olá! Diga oi em português.")
>>> print(response.content)
# Deve retornar resposta do modelo
```

- [ ] Modelo respondeu? ✅

---

## 🎯 Integração no Seu Projeto

### Passo 1: Escolha a Forma de Uso

- [ ] **Opção A:** Usar `setup_sidebar_model_config()` (Recomendado)
  - Adicione ao seu app.py conforme EXEMPLO_INTEGRACAO_APP.py
  
- [ ] **Opção B:** Usar `model_selector()` simples
  - Ver exemplos_model_selection.py
  
- [ ] **Opção C:** Uso programático direto
  - Ver examples_model_selection.py

### Passo 2: Implementar

- [ ] Copie os imports necessários
- [ ] Adapte ao seu código
- [ ] Execute testes

### Passo 3: Verificar

- [ ] Interface Streamlit mostra seletor? ✅
- [ ] Modelo pode ser selecionado? ✅
- [ ] Modelo pode ser invocado? ✅

---

## 📁 Estrutura de Arquivos

- [ ] ✅ `src/core/config.py` - Existe e tem conteúdo
- [ ] ✅ `src/services/model_manager.py` - Existe e tem conteúdo
- [ ] ✅ `src/services/llm_factory.py` - Atualizado
- [ ] ✅ `src/interface/model_selector.py` - Existe e tem conteúdo
- [ ] ✅ `test_model_selection.py` - Pronto para testar
- [ ] ✅ `examples_model_selection.py` - Exemplos de código
- [ ] ✅ `EXEMPLO_INTEGRACAO_APP.py` - Guia de integração

---

## 🐛 Troubleshooting

### ❌ "Ollama não está disponível"

- [ ] Ollama está rodando? (`ollama serve` no terminal)
- [ ] Endereço correto no `.env`? (`OLLAMA_BASE_URL=http://localhost:11434`)
- [ ] Firewall bloqueando porta 11434?

**Solução:** Execute `ollama serve` e tente novamente

### ❌ "Nenhum modelo encontrado"

- [ ] Modelo foi baixado? (`ollama list`)
- [ ] Nenhum modelo aparece na lista?

**Solução:** Execute `ollama pull llama3.2:3b`

### ❌ "ImportError: cannot import name..."

- [ ] Caminho do import está correto?
- [ ] Você está no diretório certo?

**Solução:** Use `from src.services.model_manager import OllamaModelManager`

### ❌ Modelo muito lento

- [ ] Você está usando o modelo correto?
- [ ] Seu computador tem recursos suficientes?

**Solução:** Use `llama3.2:3b` (pequeno e rápido)

### ❌ Erro "Connection refused"

- [ ] Ollama está rodando?
- [ ] Porta correta?

**Solução:**
```bash
# Terminal 1
ollama serve

# Terminal 2 (teste)
python test_model_selection.py
```

---

## ✨ Otimizações (Opcional)

### Cache em Session State (Streamlit)

```python
if "llm_instance" not in st.session_state:
    st.session_state.llm_instance = LLMFactory.get_model(...)

llm = st.session_state.llm_instance
```

- [ ] Implementado? ⚪ (opcional)

### Fallback Automático

```python
if LLMFactory.is_ollama_available():
    llm = LLMFactory.get_model("ollama", model)
else:
    llm = LLMFactory.get_model("openai", "gpt-4o-mini")
```

- [ ] Implementado? ⚪ (opcional)

---

## 📚 Recursos

- [ ] Consultei `GUIA_RAPIDO.md`?
- [ ] Consultei `GUIA_SELECAO_MODELOS.md`?
- [ ] Consultei `SUMARIO_IMPLEMENTACAO.md`?
- [ ] Consultei `EXEMPLO_INTEGRACAO_APP.py`?

---

## 🎉 Status Final

### Setup Completo?

- [ ] Ollama instalado e rodando
- [ ] Modelo baixado (`ollama list` mostra modelos)
- [ ] `.env` configurado
- [ ] Arquivos criados
- [ ] Testes passando
- [ ] Integração implementada
- [ ] Interface funcionando

**VOCÊ ESTÁ PRONTO! 🚀**

---

## 📞 Próximos Passos

1. **Adicione** `setup_sidebar_model_config()` ao seu app.py
2. **Teste** a interface com `streamlit run src/interface/app.py`
3. **Selecione** um modelo na sidebar
4. **Use** o modelo em sua aplicação

---

## 🔍 Comandos Rápidos

```bash
# Iniciar Ollama
ollama serve

# Listar modelos instalados
ollama list

# Baixar modelo
ollama pull llama3.2:3b
ollama pull mistral

# Remover modelo
ollama rm llama3.2:3b

# Testar setup
python test_model_selection.py

# Testar individual
python -c "from src.services.model_manager import OllamaModelManager; print(OllamaModelManager.is_ollama_available())"
```

---

**Status de Conclusão:** Marque cada item conforme completa! ✅

*Última atualização: Maio 2026*
