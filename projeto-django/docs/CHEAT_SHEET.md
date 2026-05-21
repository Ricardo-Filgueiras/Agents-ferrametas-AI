# ⚡ CHEAT SHEET - Comandos Rápidos

Referência rápida de comandos, padrões e tarefas comuns.

---

## 🚀 Startup Rápido

```bash
# Ativar venv
.\.venv\Scripts\Activate.ps1                    # Windows
source .venv/bin/activate                       # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Migrações
cd src
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver

# Acessar
# http://localhost:8000
# Admin: http://localhost:8000/admin
```

---

## 🧪 Testes

```bash
cd src

# Todos os testes
python manage.py test

# App específico
python manage.py test app.nova
python manage.py test app.user

# Classe específica
python manage.py test app.nova.tests.OCRPipelineTest

# Método específico
python manage.py test app.nova.tests.OCRPipelineTest.test_process_document

# Com coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Abre em htmlcov/index.html
```

---

## 🔧 Banco de Dados

```bash
cd src

# Ver status de migrações
python manage.py showmigrations

# Fazer nova migração
python manage.py makemigrations app.user

# Revisar mudanças (antes de aplicar!)
cat app/user/migrations/000X_auto_*.py

# Aplicar migrações
python manage.py migrate

# Reverter última migração
python manage.py migrate app.user 0002

# Limpar tudo (⚠️ PERDA DE DADOS!)
rm db.sqlite3
python manage.py migrate
```

---

## 👀 Debug

```bash
cd src

# Shell interativo Django
python manage.py shell

# Dentro do shell:
from app.user.models import Documentos_clientes
docs = Documentos_clientes.objects.all()
print(docs.query)  # Ver SQL gerado

# Ver logs
tail -f /tmp/django.log

# Listar arquivos carregados
ls -la media/documentos/
```

---

## 📝 Git Workflow

```bash
# Setup inicial
git clone <REPO>
cd projeto-django

# Criar branch
git checkout -b feature/nome-descritivo

# Ver status
git status

# Adicionar mudanças
git add .
git add arquivo.py

# Commit
git commit -m "feat: descrição da mudança"

# Ver commits
git log --oneline -10

# Desfazer commit (não enviado)
git reset --soft HEAD~1

# Push
git push origin feature/nome-descritivo

# Pull Request
# Abrir no GitHub
```

---

## 🔍 Buscar & Encontrar

```bash
# Procurar por texto em código
grep -r "NovaAgentService" src/

# Procurar em arquivos Python
grep -r "def " src/app/nova/

# Procurar e contar
grep -r "ocr_and_markup_file" src/ | wc -l

# Procurar com regex
grep -r "class.*Service" src/app/

# VS Code: Ctrl+Shift+F (buscar em projeto)
# VS Code: Ctrl+P (procurar arquivo)
# VS Code: Ctrl+G (ir para linha)
```

---

## 📦 Dependências

```bash
# Instalar nova dependência
pip install novo-pacote
pip freeze > requirements.txt

# Desinstalar
pip uninstall pacote-antigo

# Listar instaladas
pip list

# Atualizar tudo (cuidado!)
pip install -r requirements.txt --upgrade

# Ver arquivo requirements
cat requirements.txt
```

---

## 🏗️ Estrutura de Código

```python
# Imports (ordem padrão)
from django.db import models
from django.contrib.auth.models import User
from app.user.models import Documentos_clientes

import logging
import os

logger = logging.getLogger(__name__)

# Models
class MyModel(models.Model):
    field = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Meu Modelo"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

# Services
class MyService:
    def process(self, data):
        logger.info(f"Processando: {data}")
        try:
            # Implementação
            result = self._helper(data)
            return result
        except Exception as e:
            logger.error(f"Erro: {e}", exc_info=True)
            raise

# Views
@login_required
def my_view(request, pk):
    obj = get_object_or_404(MyModel, pk=pk, user=request.user)
    return render(request, 'template.html', {'obj': obj})
```

---

## 🔐 Multi-Tenancy (Segurança)

```python
# ✅ CORRETO - Filtrar por usuário
docs = Documentos_clientes.objects.filter(
    cliente__user=request.user,
    cliente_id=cliente_pk
)

# ❌ ERRADO - Sem filtrar
docs = Documentos_clientes.objects.all()

# ✅ CORRETO - Em views
@login_required
def documento_detail(request, pk):
    doc = get_object_or_404(
        Documentos_clientes,
        pk=pk,
        cliente__user=request.user
    )
    return render(request, 'detail.html', {'doc': doc})
```

---

## 📋 Logging

```python
import logging

logger = logging.getLogger(__name__)

# Info (informação geral)
logger.info(f"[Módulo] Processando documento {id}")

# Warning (cuidado, mas continua)
logger.warning(f"[Módulo] Recurso indisponível, usando fallback")

# Error (erro grave)
logger.error(f"[Módulo] Erro ao processar: {e}", exc_info=True)

# Debug (informação detalhada - desenvolvimento)
logger.debug(f"Variável debug: {debug_var}")

# Ver logs
tail -f /tmp/django.log
```

---

## 🧵 Background Tasks

```python
# Em models.py - Trigger automático
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Documentos_clientes)
def trigger_ocr(sender, instance, created, **kwargs):
    if created:
        from app.nova.tasks import ocr_and_markup_file
        ocr_and_markup_file(instance.id)

# Em tasks.py - Implementação
def ocr_and_markup_file(documento_id):
    logger.info(f"Iniciando OCR para {documento_id}")
    try:
        instance = Documentos_clientes.objects.get(pk=documento_id)
        # Processar
    except Exception as e:
        logger.error(f"Erro: {e}", exc_info=True)
```

---

## 🧪 Testes - Template

```python
from django.test import TestCase
from app.user.models import Documentos_clientes, Clientes

class DocumentoTest(TestCase):
    def setUp(self):
        """Cria dados de teste"""
        self.cliente = Clientes.objects.create(
            nome='Cliente Teste',
            email='teste@example.com'
        )
    
    def test_creation(self):
        """Testa criação"""
        doc = Documentos_clientes.objects.create(
            nome='Doc',
            cliente=self.cliente
        )
        self.assertEqual(doc.nome, 'Doc')
    
    def test_str(self):
        """Testa __str__"""
        doc = Documentos_clientes.objects.create(
            nome='Doc',
            cliente=self.cliente
        )
        self.assertEqual(str(doc), 'Doc')
```

---

## 📝 Mensagens de Commit (Conventional Commits)

```bash
# Formato
git commit -m "tipo: descrição breve

Descrição mais longa explicando o porquê da mudança.

Fixa #123"

# Tipos
feat:       # Nova funcionalidade
fix:        # Correção de bug
docs:       # Documentação
refactor:   # Refatoração (sem mudança de comportamento)
test:       # Testes
chore:      # Build, dependências, etc
style:      # Formatação, semicolons, etc

# Exemplos
git commit -m "feat: adiciona validação de PDF"
git commit -m "fix: corrige erro na extração de tabelas"
git commit -m "docs: atualiza PIPELINE_OCR.md"
git commit -m "refactor: simplifica função extract_pdf"
git commit -m "test: adiciona testes para OCR"
git commit -m "chore: atualiza requirements.txt"
```

---

## 🚨 Troubleshooting Rápido

```bash
# Erro: ModuleNotFoundError
pip install -r requirements.txt

# Erro: Database locked
rm db.sqlite3
python manage.py migrate

# Erro: Port 8000 already in use
python manage.py runserver 8001

# Erro: ImportError em views
# Verifique: urls.py está correto?
# Verifique: app em INSTALLED_APPS?

# Erro: Template not found
# Verifique: TEMPLATES['DIRS'] em settings.py
# Verifique: caminho relativo correto

# Erro: Static files 404
python manage.py collectstatic

# Erro: Migrações pendentes
python manage.py migrate
```

---

## 📚 Arquivos Importantes

```
projeto-django/
├── src/
│   ├── manage.py                ← CLI Django
│   ├── core/settings.py         ← Configurações
│   ├── app/
│   │   ├── nova/
│   │   │   ├── services.py     ← Docling OCR
│   │   │   ├── tasks.py        ← Background tasks
│   │   │   └── views.py        ← Endpoints
│   │   └── user/
│   │       ├── models.py       ← Dados
│   │       ├── services.py     ← Extração
│   │       └── views.py        ← CRUD
│   └── templates/              ← HTML
├── docs/
│   ├── ONBOARDING.md           ← Comece aqui!
│   ├── PIPELINE_OCR.md         ← OCR explicado
│   ├── CONTRIBUINDO.md         ← Padrões
│   └── INDEX.md                ← Mapa
└── requirements.txt            ← Dependências
```

---

## 🔄 Fluxo Rápido de Feature

```bash
# 1. Criar branch
git checkout -b feature/nova-feature

# 2. Fazer mudanças
# ... editar arquivos ...

# 3. Testes
python manage.py test

# 4. Commit
git commit -m "feat: descrição da feature"

# 5. Push
git push origin feature/nova-feature

# 6. Pull Request (GitHub)
# Abrir PR, aguardar review, fazer merge
```

---

## 🎯 Performance

```python
# Otimizar queries - Use select_related()
docs = Documentos_clientes.objects.select_related('cliente').all()

# Otimizar queries - Use prefetch_related()
clientes = Clientes.objects.prefetch_related('documentos_clientes_set').all()

# Evitar N+1 queries
for cliente in clientes:
    print(cliente.documentos_clientes_set.count())  # ❌ N queries
    # Use prefetch_related acima

# Cache simples
from django.views.decorators.cache import cache_page

@cache_page(60)  # 60 segundos
def expensive_view(request):
    pass
```

---

## 🔗 Links Rápidos

- 📖 [Documentação Completa](./README.md)
- 🎯 [Índice Detalhado](./INDEX.md)
- 🚀 [Onboarding](./ONBOARDING.md)
- 🤖 [Pipeline OCR](./PIPELINE_OCR.md)
- 👨‍💻 [Padrões de Código](./CONTRIBUINDO.md)

---

**Última atualização:** Maio 2026
**Mais detalhes:** Veja documentação completa em `docs/`
