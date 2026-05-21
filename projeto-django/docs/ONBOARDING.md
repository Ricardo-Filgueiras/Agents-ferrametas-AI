# 🚀 Guia de Onboarding - Agents Ferramentas AI

Bem-vindo ao time de desenvolvimento! Este guia irá ajudá-lo a configurar o ambiente, entender a arquitetura do projeto e começar a contribuir rapidamente.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+**
- **pip** (gerenciador de pacotes Python)
- **Git**
- **Visual Studio Code** (recomendado)
- **PostgreSQL 12+** (ou SQLite para desenvolvimento local)

---

## 🔧 Setup do Ambiente

### 1. Clone o Repositório

```bash
git clone <REPO_URL>
cd projeto-django
```

### 2. Crie um Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Ollama (local LLM)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# IBM Docling (OCR/PDF Processing)
DOCLING_API_URL=http://localhost:5000
```

### 5. Execute as Migrações do Banco de Dados

```bash
cd src
python manage.py migrate
```

### 6. Crie um Usuário Administrador

```bash
python manage.py createsuperuser
# Siga as instruções interativas
```

### 7. Inicie o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse a aplicação em: **http://localhost:8000**

---

## 📚 Estrutura do Projeto

```
projeto-django/
├── docs/                           # 📄 Documentação
│   ├── arquitetura_e_integracao_ia.md
│   ├── ONBOARDING.md              # ← Você está aqui
│   ├── PIPELINE_OCR.md
│   └── CONTRIBUINDO.md
├── src/
│   ├── manage.py                  # CLI do Django
│   ├── core/                      # ⚙️ Configurações do Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── app/                       # 📦 Aplicações Django
│       ├── chatbot/              # Chat com IA
│       ├── interface/            # Interface web
│       ├── nova/                 # 🤖 Agente Nova (OCR/Análise)
│       │   ├── services.py       # Processamento com Docling
│       │   ├── tasks.py          # Background tasks
│       │   └── views.py          # APIs/Endpoints
│       └── user/                 # 👤 Gestão de usuários e documentos
│           ├── models.py         # Clientes, Documentos_clientes
│           ├── services.py       # Extração de dados dos arquivos
│           └── views.py          # CRUD de clientes/docs
├── pyproject.toml                 # Configuração de dependências
├── main.py                        # Script principal (opcional)
└── README.md

```

---

## 🎯 Fluxo Principal de Trabalho

### 1. Entender o Modelo de Dados

A aplicação segue um modelo **multi-tenant** com isolamento de dados por usuário:

```
Usuário (Django User)
  └─ Clientes (Múltiplos clientes por usuário)
      └─ Documentos_clientes (Múltiplos documentos por cliente)
          └─ Análise da IA (Processamento OCR/Docling)
```

**Arquivo de referência:** [src/app/user/models.py](../src/app/user/models.py)

### 2. Pipeline OCR (Processo Principal)

Quando um usuário faz upload de um documento:

1. **Upload** → Arquivo salvo em `/media/documentos/`
2. **Trigger** → Background task `ocr_and_markup_file` é acionada
3. **Processamento** → IBM Docling converte o documento em Markdown
4. **Análise** → Ollama analisa o Markdown (via agente Nova)
5. **Armazenamento** → Resultados salvos no banco de dados
6. **Exibição** → Interface mostra o resultado para o usuário

**Arquivo de referência:** [docs/PIPELINE_OCR.md](./PIPELINE_OCR.md)

### 3. Estrutura de Apps Django

| App | Responsabilidade |
|-----|-----------------|
| **user** | Gestão de usuários, clientes e upload de documentos |
| **nova** | Agente de IA (OCR, análise com Ollama, integração Docling) |
| **chatbot** | Sistema de chat com RAG (recuperação de contexto) |
| **interface** | Interface web genérica |

---

## 🔑 Conceitos Importantes

### Multi-Tenancy (Isolamento de Dados)

Cada usuário só pode ver seus próprios clientes e documentos. **Nunca** confie apenas no frontend para filtro de dados!

```python
# ✅ CORRETO: Filtra por usuário no backend
documentos = Documentos_clientes.objects.filter(
    cliente__user=request.user,
    cliente_id=cliente_pk
)

# ❌ ERRADO: Confiar apenas no frontend
documentos = Documentos_clientes.objects.all()
```

### UUIDs em URLs

As URLs usam UUIDs em vez de IDs sequenciais para segurança:

```
✅ /clientes/550e8400-e29b-41d4-a716-446655440000/
❌ /clientes/1/
```

### Background Tasks

Processamento pesado (OCR, análise) é feito em background usando Django Signals:

```python
# Em models.py - Após salvar um documento
@receiver(post_save, sender=Documentos_clientes)
def trigger_ocr_task(sender, instance, created, **kwargs):
    if created:
        from app.nova.tasks import ocr_and_markup_file
        ocr_and_markup_file(instance.id)
```

---

## 🛠️ Tarefas Comuns

### Adicionar um Novo Campo ao Modelo

1. Edite `src/app/user/models.py`
2. Execute: `python manage.py makemigrations`
3. Execute: `python manage.py migrate`
4. Registre o campo no admin se necessário

### Criar um Novo Endpoint de API

1. Crie a view em `src/app/nova/views.py` (ou app apropriado)
2. Registre a rota em `src/app/nova/urls.py`
3. Inclua a URL no `src/core/urls.py`
4. Teste com curl ou Postman

### Melhorar o Pipeline OCR

1. Edite `src/app/nova/services.py` (NovaAgentService)
2. Ou edite `src/app/user/services.py` (extração de dados)
3. Teste com um documento de exemplo
4. Verifique os logs em `/tmp/` ou console

---

## 📖 Próximos Passos

1. **Leia a arquitetura completa:** [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md)
2. **Entenda o Pipeline OCR:** [PIPELINE_OCR.md](./PIPELINE_OCR.md)
3. **Conheça as padrões do projeto:** [CONTRIBUINDO.md](./CONTRIBUINDO.md)
4. **Explore o código** começando por:
   - `src/app/user/models.py` - Modelos de dados
   - `src/app/nova/services.py` - Processamento OCR
   - `src/app/nova/tasks.py` - Background tasks

---

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'docling'"

```bash
# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Connection refused" (Ollama/Docling)

Certifique-se de que os serviços estão rodando:

```bash
# Ollama
ollama serve

# Docling (em outro terminal)
python -m docling.web.api
```

### Erro de Migrações

Limpe e recrie o banco:

```bash
# ⚠️ Cuidado! Isso deleta todos os dados
rm db.sqlite3
python manage.py migrate
```

---

## 💬 Dúvidas?

- Pergunte no Slack ou Discord do time
- Consulte os arquivos de documentação em `docs/`
- Revise os comentários no código
- Abra uma issue no repositório

**Bem-vindo ao time! 🎉**
