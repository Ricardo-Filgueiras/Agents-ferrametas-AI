# 🚀 Agents Ferramentas AI (Hub Django Multi-Tenant)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Package Manager](https://img.shields.io/badge/Gerenciador-UV-cyan.svg)](https://github.com/astral-sh/uv)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)

Este projeto é um **Hub de IA Multi-Tenant** desenvolvido em Django para servir de portal de gerenciamento de clientes e processamento de documentos PDF. Ele substitui a arquitetura rígida do Streamlit por uma plataforma web de alta performance, segura e responsiva. 

O objetivo principal é carregar documentos PDF de clientes e, em seguida, utilizar **Agentes de IA autônomos** integrados com **IBM Docling** e **RAG (Retrieval-Augmented Generation)** para analisar os arquivos e salvar relatórios ricos em Markdown diretamente no banco de dados.

---

## 🛠️ O Que Já Construímos (Status Atual)

Toda a base estrutural e de interface web do projeto já está **100% implementada, migrada e em pleno funcionamento**:

1. **🔒 Portal de Autenticação Completo**:
   * Cadastro de usuários, login e logout seguros.
   * Restrição e segurança integradas a todas as páginas (`@login_required`).

2. **👥 Perfis de Clientes Multi-Tenant**:
   * Gerenciamento de clientes (Criar, Visualizar, Editar, Deletar).
   * **Isolamento Absoluto**: Cada usuário logado gerencia apenas seus próprios clientes (`user=request.user`), com segurança total baseada em chaves primárias do tipo **UUIDv4** para evitar invasões e enumeração de URLs.

3. **📂 Upload e Gestão Dual-File de PDFs**:
   * Formulário de upload robusto aceitando estritamente arquivos `.pdf` binários via `enctype="multipart/form-data"`.
   * **Organização no Disco**: Armazenamento automático e organizado por data em `media/documentos/%Y/%m/%d/`.
   * **Slot de Markdown (`arquivo_markdown`)**: Campo no banco de dados pronto para armazenar o arquivo `.md` estruturado que será gerado pelo parser **IBM Docling**.

4. **✨ Editor Visual IA (MartorField)**:
   * Campo `analise_ia` integrado com o editor **Martor**, permitindo que as análises feitas pelos agentes de IA futuros sejam visualizadas com títulos, listas, tabelas e trechos de código em Markdown de forma espetacular.

5. **🎨 Interface Premium Dark Mode**:
   * UI customizada em Vanilla CSS inspirada em designs modernos (*glassmorphism*, luzes cianas e índigas, cards responsivos e animações de hover).

---

## 🔮 O Que Vamos Fazer a Seguir (Fase de Inteligência Artificial)

Embora a interface e o banco de dados estejam completamente prontos, **ainda não implementamos os Agentes de IA e o RAG**, o que será feito na próxima fase do projeto:

1. **💾 Integração com IBM Docling**:
   * Instalação e chamada do Docling no Django para pegar o PDF do cliente e convertê-lo em um Markdown `.md` altamente estruturado (preservando tabelas e layouts).

2. **🤖 Orquestração de Agentes de IA (Agno / LangChain)**:
   * Criação de agentes inteligentes autônomos para ler o conteúdo Markdown gerado pelo Docling.
   * Execução do agente para fazer resumos automáticos, auditar contratos ou extrair dados cruciais do cliente.

3. **🔍 Motor RAG (Retrieval-Augmented Generation)**:
   * Fragmentação do texto em pedaços (*chunks*), vetorização e indexação de dados em banco vetorial (ChromaDB ou pgvector) para permitir "conversar" com os documentos do cliente.
   * Filtro de metadados rígido por `cliente_id` (UUID), garantindo isolamento total de dados na busca vetorial.

---

## 📁 Estrutura de Pastas do Projeto

```text
projeto-django/
├── docs/                             # Documentação técnica de arquitetura e RAG
│   └── arquitetura_e_integracao_ia.md
├── media/                            # Arquivos binários salvos (PDFs e Markdowns)
│   └── documentos/
│       ├── 2026/05/18/contrato.pdf   # PDFs originais dos clientes
│       └── md/2026/05/18/contrato.md # Arquivo processado pelo Docling
├── src/
│   ├── app/
│   │   ├── interface/                # App de Landing Page e Portal Principal
│   │   └── user/                     # App principal de CRUD de Clientes, PDFs e IA
│   │       ├── models.py             # Modelos de Clientes e Documentos (com UUID)
│   │       ├── views.py              # CRUD seguro e processamento de arquivos
│   │       ├── forms.py              # Formulários web customizados
│   │       └── urls.py               # Roteamento seguro com UUIDs
│   ├── core/                         # Configurações centrais do Django (settings)
│   └── templates/                    # Telas HTML customizadas (Dark Mode Premium)
├── pyproject.toml                    # Configurações do projeto e dependências UV
└── README.md                         # Este documento de visão geral
```

---

## 🚀 Como Executar o Projeto Localmente

Certifique-se de que o **UV** (gerenciador de pacotes rápido) está instalado em sua máquina.

### 1. Clonar e Acessar o Diretório
```powershell
cd c:\Github\Agents-ferrametas-AI\projeto-django
```

### 2. Criar as Migrações de Banco de Dados (SQLite)
Registre as tabelas e colunas adicionadas no banco:
```powershell
uv run .\src\manage.py makemigrations
```

### 3. Aplicar as Migrações
Sincronize a base de dados:
```powershell
uv run .\src\manage.py migrate
```

### 4. Criar um Usuário Administrador
Gere uma conta para acessar o painel Django Admin:
```powershell
uv run .\src\manage.py createsuperuser
```

### 5. Iniciar o Servidor
```powershell
uv run .\src\manage.py runserver
```

Agora abra `http://127.0.0.1:8000/` no seu navegador!

---

## 🧪 Prontos Para Iniciar a Fase IA?
O ecossistema Django está com a base sólida e robusta. Diga-me quando estiver pronto para iniciarmos a programação do Agente de IA com o **Docling**! 🚀🔥
