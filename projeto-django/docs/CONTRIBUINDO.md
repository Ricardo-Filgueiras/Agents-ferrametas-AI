# 🤝 Guia de Contribuição

Obrigado por querer contribuir para o **Agents Ferramentas AI**! Este documento descreve como trabalhar de forma eficiente, mantendo qualidade e consistência do código.

---

## 📋 Antes de Começar

1. Leia [ONBOARDING.md](./ONBOARDING.md) para configurar o ambiente
2. Revise [PIPELINE_OCR.md](./PIPELINE_OCR.md) para entender o fluxo principal
3. Leia [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) para arquitetura geral

---

## 🎯 Fluxo de Trabalho

### 1. Criar uma Branch

```bash
git checkout main
git pull origin main
git checkout -b feature/sua-feature
# ou
git checkout -b bugfix/seu-bugfix
```

**Convenção de nomes:**
- `feature/nome-descritivo` - Nova funcionalidade
- `bugfix/nome-descritivo` - Correção de bug
- `docs/nome-descritivo` - Documentação
- `refactor/nome-descritivo` - Refatoração de código

### 2. Fazer Alterações

Veja as seções específicas abaixo por tipo de mudança.

### 3. Testar

```bash
# Testes unitários
python manage.py test

# Testes específicos
python manage.py test app.nova.tests
python manage.py test app.user.tests

# Teste de coverage
coverage run --source='.' manage.py test
coverage report
```

### 4. Commit com Mensagens Claras

```bash
git add .
git commit -m "feat: adiciona validação de arquivo PDF

- Implementa verificação de PDF corrompido
- Adiciona logging detalhado
- Trata erro com mensagem amigável ao usuário
"
```

**Convenção (Conventional Commits):**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `refactor:` - Refatoração sem mudança de comportamento
- `test:` - Adição/alteração de testes
- `chore:` - Mudanças em dependências, configs, etc

### 5. Push e Pull Request

```bash
git push origin feature/sua-feature
```

Crie um PR no GitHub com:
- **Título claro:** "Adiciona validação de PDFs corrompidos"
- **Descrição:** Por que? O que muda? Como testar?
- **Checklist:**
  - [ ] Testes adicionados/atualizados
  - [ ] Documentação atualizada
  - [ ] Sem quebra de mudanças (breaking changes)
  - [ ] Código segue padrões do projeto

---

## 📝 Padrões de Código

### Python - PEP 8

```python
# ✅ BOM
def extract_pdf(file_path: str) -> str:
    """
    Extrai texto de um arquivo PDF.
    
    Args:
        file_path: Caminho do arquivo PDF
    
    Returns:
        Texto extraído em Markdown
    
    Raises:
        FileNotFoundError: Se arquivo não existe
        ValueError: Se PDF é inválido
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    # Implementação...
    return markdown_text

# ❌ RUIM
def extract_pdf(f):
    # Extrai texto
    return x
```

### Django Models

```python
# ✅ BOM
class Documentos_clientes(models.Model):
    """Modelo para documentos carregados pelos clientes."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único do documento"
    )
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        help_text="Cliente proprietário do documento"
    )
    arquivo = models.FileField(
        upload_to='documentos/%Y/%m/%d',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])],
        help_text="Arquivo original enviado"
    )
    
    class Meta:
        verbose_name = "Documento de Cliente"
        verbose_name_plural = "Documentos de Clientes"
        ordering = ['-data_cadastro']
        indexes = [
            models.Index(fields=['cliente', 'data_cadastro']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.cliente.nome})"

# ❌ RUIM
class Documentos_clientes(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    file = FileField()
    # Sem documentação, sem Meta
```

### Django Views

```python
# ✅ BOM - Com segurança multi-tenant
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def documento_detail(request, cliente_pk, pk):
    """
    Exibe detalhes de um documento específico.
    Segurança: Valida que o documento pertence ao usuário logado.
    """
    # Filtra por usuário para evitar vazamento de dados
    cliente = get_object_or_404(
        Clientes,
        pk=cliente_pk,
        user=request.user
    )
    documento = get_object_or_404(
        Documentos_clientes,
        pk=pk,
        cliente=cliente
    )
    
    return render(request, 'documento_detail.html', {'documento': documento})

# ❌ RUIM - Sem verificação de propriedade
def documento_detail(request, pk):
    documento = Documentos_clientes.objects.get(pk=pk)
    return render(request, 'documento_detail.html', {'documento': documento})
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# ✅ BOM
logger.info(f"[Módulo] Iniciando processamento do documento {documento_id}")
logger.warning(f"[Módulo] Docling indisponível, usando fallback")
logger.error(f"[Módulo] Erro crítico: {e}", exc_info=True)

# ❌ RUIM
print("Processando...")
print("Erro!")  # Não inclui stack trace
logger.info("doc")  # Sem contexto
```

---

## 🔐 Segurança

### Checklist de Segurança

- [ ] Validação de entrada em todas as views
- [ ] Filtros por `request.user` em queries
- [ ] Sem informações sensíveis em logs/erros
- [ ] Proteção CSRF em formulários
- [ ] Permissões verificadas no backend (não apenas frontend)
- [ ] Senhas hashadas (Django faz automaticamente)
- [ ] Sem SQL injection (usar ORM Django)

### Exemplo: Validação Segura

```python
# ✅ SEGURO
@login_required
def create_documento(request, cliente_pk):
    cliente = get_object_or_404(Clientes, pk=cliente_pk, user=request.user)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            # Valida extensão
            arquivo = form.cleaned_data['arquivo']
            if not arquivo.name.endswith(('.pdf', '.docx')):
                messages.error(request, "Formato de arquivo inválido")
                return redirect('documento_list')
            
            # Cria documento associado ao cliente do usuário
            documento = form.save(commit=False)
            documento.cliente = cliente
            documento.save()
            return redirect('documento_detail', pk=documento.pk)

# ❌ INSEGURO
def create_documento(request):
    cliente_id = request.GET.get('cliente_id')  # Sem validação!
    cliente = Clientes.objects.get(pk=cliente_id)  # Pode ser de outro usuário!
```

---

## 📦 Mudanças em Dependências

### Adicionar Dependência

1. Identifique o pacote:
```bash
pip search seu-pacote
```

2. Instale:
```bash
pip install novo-pacote
```

3. Atualize requirements.txt:
```bash
pip freeze > requirements.txt
```

4. Commit:
```bash
git add requirements.txt
git commit -m "chore: adiciona novo-pacote==1.0.0"
```

### Remover Dependência

```bash
pip uninstall pacote-antigo
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: remove pacote-antigo (deprecado)"
```

---

## 🗄️ Migrações de Banco de Dados

### Adicionar Campo

```python
# 1. Edite models.py
class Clientes(models.Model):
    novo_campo = models.CharField(max_length=100, null=True, blank=True)

# 2. Crie migração
python manage.py makemigrations

# 3. Revise a migração (muito importante!)
# Arquivo: app/user/migrations/000X_add_novo_campo.py

# 4. Aplique
python manage.py migrate

# 5. Commit
git add app/user/migrations/
git commit -m "feat: adiciona novo_campo a modelo Clientes"
```

### Remover Campo

```python
# 1. Remova de models.py
# 2. Crie migração
python manage.py makemigrations
# 3. Revise (certifique-se de que os dados não serão perdidos)
# 4. Aplique
python manage.py migrate
# 5. Commit
```

⚠️ **IMPORTANTE:** Sempre revise as migrações geradas automaticamente!

---

## 📚 Documentação

### Docstrings

```python
def process_document_file(documento):
    """
    Processa um arquivo de documento usando Docling e Ollama.
    
    Este é um resumo de uma linha, seguido de descrição mais detalhada.
    
    O fluxo é:
    1. Extrai texto do arquivo usando NovaAgentService
    2. Salva Markdown em arquivo_markdown
    3. Gera análise usando Ollama
    4. Salva análise em analise_ia
    
    Args:
        documento (Documentos_clientes): Instância do documento a processar
    
    Returns:
        bool: True se processamento bem-sucedido, False caso contrário
    
    Raises:
        FileNotFoundError: Se arquivo não existe
        ValueError: Se formato de arquivo não suportado
    
    Example:
        >>> documento = Documentos_clientes.objects.get(pk=uuid)
        >>> success = process_document_file(documento)
        >>> if success:
        ...     print(documento.analise_ia)
    """
    # Implementação...
```

### Comentários no Código

```python
# ✅ BOM - Explica o "porquê"
# Usa Docling primeiro para melhor layout, depois fallback pypdf
# porque Docling é mais preciso mas pode não estar disponível
try:
    agent = NovaAgentService()
    return agent.process_document(file_path)
except ImportError:
    return extract_with_pypdf(file_path)

# ❌ RUIM - Óbvio demais
# Tenta usar Docling
try:
    agent = NovaAgentService()
```

### Atualizar Documentação

Quando mudar funcionalidade, **atualize a documentação**:

- [ ] Docstring do método/classe
- [ ] Docstring da função
- [ ] Arquivo relevante em `docs/`
- [ ] `PIPELINE_OCR.md` (se relacionado a OCR)
- [ ] `README.md` (se é mudança importante)

---

## 🧪 Testes

### Estrutura de Testes

```python
# tests.py
from django.test import TestCase, Client
from app.user.models import Documentos_clientes, Clientes
from app.nova.services import NovaAgentService

class DocumentoModelTest(TestCase):
    """Testes para o modelo Documentos_clientes."""
    
    def setUp(self):
        """Cria fixtures para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.cliente = Clientes.objects.create(
            nome='Cliente Teste',
            email='cliente@example.com',
            cpf_cnpj='12345678901234',
            user=self.user
        )
    
    def test_documento_creation(self):
        """Testa criação de documento."""
        doc = Documentos_clientes.objects.create(
            nome='Test Doc',
            cliente=self.cliente,
            arquivo='test.pdf'
        )
        self.assertEqual(doc.nome, 'Test Doc')
        self.assertEqual(doc.cliente, self.cliente)
    
    def test_extensao_property(self):
        """Testa propriedade extensao."""
        doc = Documentos_clientes.objects.create(
            nome='Test Doc',
            cliente=self.cliente,
            arquivo='test.pdf'
        )
        self.assertEqual(doc.extensao, '.pdf')

class NovaAgentServiceTest(TestCase):
    """Testes para NovaAgentService."""
    
    def test_process_document(self):
        """Testa processamento de documento."""
        agent = NovaAgentService()
        # Usar arquivo de teste pequeno
        result = agent.process_document('tests/fixtures/sample.pdf')
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
```

### Rodar Testes

```bash
# Todos os testes
python manage.py test

# App específico
python manage.py test app.nova

# Classe específica
python manage.py test app.nova.tests.OCRPipelineTest

# Método específico
python manage.py test app.nova.tests.OCRPipelineTest.test_process_document

# Com coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

---

## ✅ Checklist Antes de Fazer Push

- [ ] Código segue PEP 8
- [ ] Docstrings adicionadas/atualizadas
- [ ] Testes escritos e passando
- [ ] Sem código comentado desnecessário
- [ ] Sem print() (use logging)
- [ ] Validação de segurança multi-tenant
- [ ] Migrações de BD revisadas e comitadas
- [ ] Documentação atualizada em `docs/`
- [ ] Mensagem de commit segue convenção
- [ ] Sem arquivos sensíveis (.env, senhas)

---

## 🚀 Processo de Review

1. **Submeter PR** com descrição clara
2. **Aguardar review** de um maintainer
3. **Responder comentários** e fazer ajustes
4. **Re-request review** após alterações
5. **Merge** quando aprovado

**Tempo de resposta esperado:** 1-3 dias úteis

---

## 🎓 Recursos de Aprendizado

### Django
- [Official Django Tutorial](https://docs.djangoproject.com/en/4.2/intro/)
- [Django for Beginners](https://djangoforbeginners.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### OCR & Document Processing
- [IBM Docling](https://github.com/IBM/docling)
- [Ollama](https://ollama.ai)
- [RAG Pattern](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)

### Python
- [Real Python](https://realpython.com/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)

---

## 💬 Precisa de Ajuda?

- 📧 Email: seu-email@example.com
- 💬 Slack: #development
- 🐛 Issues: GitHub Issues
- 📚 Docs: Começar por ONBOARDING.md

---

## 📜 Código de Conduta

Todos os contribuidores devem seguir nosso Código de Conduta:
- Seja respeitoso
- Sem discriminação
- Foque na ideia, não na pessoa
- Relate comportamento inadequado

**Violações podem resultar em ban do projeto.**

---

**Obrigado por contribuir! 🎉**
