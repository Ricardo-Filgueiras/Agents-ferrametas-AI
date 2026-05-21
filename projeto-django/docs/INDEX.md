# 📚 Índice de Documentação

Bem-vindo à documentação do **Agents Ferramentas AI**! Use este índice para encontrar rapidamente o que você precisa.

---

## 🎯 Para Novos Desenvolvedores

Comece por aqui se está entrando no time:

1. **[ONBOARDING.md](./ONBOARDING.md)** ⭐ **COMECE AQUI**
   - Setup do ambiente (Python, venv, dependências)
   - Estrutura do projeto
   - Conceitos principais
   - Tarefas comuns
   - Troubleshooting básico

2. **[PIPELINE_OCR.md](./PIPELINE_OCR.md)** - Arquitetura OCR
   - Fluxo completo de processamento
   - Componentes e responsabilidades
   - Integração Docling + Ollama
   - Tratamento de erros
   - Exemplos de código

3. **[CONTRIBUINDO.md](./CONTRIBUINDO.md)** - Como Contribuir
   - Fluxo de trabalho Git
   - Padrões de código (PEP 8, Django)
   - Segurança e multi-tenancy
   - Testes e documentação
   - Checklist de qualidade

---

## 🏗️ Arquitetura e Design

- **[arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md)**
  - Decisão Streamlit vs Django
  - Modelagem de dados (ER diagram)
  - Segurança e isolamento
  - Pipeline de processamento
  - Detalhes técnicos profundos

---

## 📑 Rápido Índice por Tópico

### 🚀 Começar Rápido

| O que fazer | Arquivo | Seção |
|-----------|---------|-------|
| Configurar ambiente pela primeira vez | [ONBOARDING.md](./ONBOARDING.md) | Setup do Ambiente |
| Entender a estrutura do projeto | [ONBOARDING.md](./ONBOARDING.md) | Estrutura do Projeto |
| Rodar o servidor de desenvolvimento | [ONBOARDING.md](./ONBOARDING.md) | Execute as Migrações |
| Conhecer o fluxo OCR | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Visão Geral do Pipeline |

### 🤖 OCR e Processamento

| O que fazer | Arquivo | Seção |
|-----------|---------|-------|
| Entender como funciona o OCR | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Visão Geral do Pipeline |
| Explorar NovaAgentService | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | NovaAgentService |
| Melhorar extração de PDFs | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Extrator de PDFs |
| Processar Excel/CSV | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Extrair Diferentes Formatos |
| Adicionar novo tipo de arquivo | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Tratamento de Erros |
| Ver fluxo de dados completo | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Fluxo de Dados Detalhado |

### 💾 Banco de Dados e Modelos

| O que fazer | Arquivo | Seção |
|-----------|---------|-------|
| Entender modelo de dados | [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) | Modelagem de Dados |
| Visualizar ER Diagram | [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) | ER Diagram |
| Multi-tenancy e segurança | [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) | Segurança e Multi-tenancy |
| Adicionar novo campo | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Migrações de BD |
| Escrever testes de modelo | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Testes |

### 🔐 Segurança

| O que fazer | Arquivo | Seção |
|-----------|---------|-------|
| Entender multi-tenancy | [ONBOARDING.md](./ONBOARDING.md) | Multi-Tenancy |
| Implementar isolamento de dados | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Segurança |
| Exemplos de código seguro | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Django Views (exemplo seguro) |
| Checklist de segurança | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Checklist de Segurança |

### 👨‍💻 Desenvolvimento

| O que fazer | Arquivo | Seção |
|-----------|---------|-------|
| Iniciar nova feature | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Fluxo de Trabalho |
| Padrões de código Python | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Python - PEP 8 |
| Padrões Django | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Django Models/Views |
| Logging correto | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Logging |
| Escrever testes | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Testes |
| Commit com boas mensagens | [CONTRIBUINDO.md](./CONTRIBUINDO.md) | Fazer Alterações |

### 🚨 Troubleshooting

| Problema | Arquivo | Seção |
|----------|---------|-------|
| Erro de importação (módulos) | [ONBOARDING.md](./ONBOARDING.md) | Troubleshooting |
| OCR lento ou não funciona | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Tratamento de Erros |
| Erro de migrações BD | [ONBOARDING.md](./ONBOARDING.md) | Troubleshooting |
| Ollama/Docling offline | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Tratamento de Erros |
| Arquivo muito grande | [PIPELINE_OCR.md](./PIPELINE_OCR.md) | Nível 1: Extração |

---

## 📖 Ordem Recomendada de Leitura

### Para Novo Dev (Primeiro Dia)
1. [ONBOARDING.md](./ONBOARDING.md) - 30 min
2. [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Visão Geral - 20 min
3. Explorar código em `src/app/user/models.py` e `src/app/nova/tasks.py` - 30 min

### Para Novo Dev (Primeira Semana)
1. Tudo acima
2. [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) - 1h
3. [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Seção de Padrões - 30 min
4. Explorar projeto completo

### Para Contribuidores Regulares
- Revisar [CONTRIBUINDO.md](./CONTRIBUINDO.md) regularmente
- Referência rápida de padrões antes de cada PR
- [PIPELINE_OCR.md](./PIPELINE_OCR.md) para mudanças em OCR

---

## 🔗 Navegação Rápida

### Arquivos de Código

```
src/
├── app/
│   ├── user/
│   │   ├── models.py          → Modelos (User, Cliente, Documento)
│   │   ├── services.py        → Extractors (PDF, Excel, CSV, Word)
│   │   ├── views.py           → CRUD de clientes e documentos
│   │   └── migrations/        → Histórico de BD
│   └── nova/
│       ├── services.py        → NovaAgentService (Docling)
│       ├── tasks.py           → Background tasks OCR
│       └── views.py           → APIs de análise
└── core/
    ├── settings.py            → Configurações Django
    ├── urls.py                → Rotas principais
    └── asgi.py/wsgi.py        → Servidores
```

### Documentação

```
docs/
├── ONBOARDING.md              ← Setup e primeiros passos
├── PIPELINE_OCR.md            ← Fluxo técnico de OCR
├── CONTRIBUINDO.md            ← Padrões e processo
├── arquitetura_e_integracao_ia.md  ← Design profundo
└── INDEX.md                   ← Você está aqui
```

---

## 🎯 Links por Profissão

### Backend Developer

**Essencial:**
- [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Inteiro
- [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Padrões Python/Django
- [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) - Modelagem

**Secundário:**
- [ONBOARDING.md](./ONBOARDING.md) - Seção Setup

### Frontend Developer

**Essencial:**
- [ONBOARDING.md](./ONBOARDING.md) - Estrutura do Projeto
- [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Fluxo de Dados Detalhado

**Secundário:**
- [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Segurança

### DevOps / Infra

**Essencial:**
- [ONBOARDING.md](./ONBOARDING.md) - Setup
- [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Dependências (Docling, Ollama)

**Secundário:**
- [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md)

### QA / Tester

**Essencial:**
- [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Visão Geral
- [ONBOARDING.md](./ONBOARDING.md) - Setup

**Secundário:**
- [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Testes

### Product Manager / Stakeholder

**Essencial:**
- [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md)
- [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Visão Geral

---

## ❓ FAQ Rápida

### "Por onde eu começo?"
→ [ONBOARDING.md](./ONBOARDING.md), seção "Setup do Ambiente"

### "Como funciona o OCR?"
→ [PIPELINE_OCR.md](./PIPELINE_OCR.md), seção "Visão Geral do Pipeline"

### "Como faço um Pull Request?"
→ [CONTRIBUINDO.md](./CONTRIBUINDO.md), seção "Fluxo de Trabalho"

### "Qual é a estrutura de dados?"
→ [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md), seção "Modelagem de Dados"

### "Como adiciono um novo formato de arquivo?"
→ [PIPELINE_OCR.md](./PIPELINE_OCR.md), seção "Extractors para Diferentes Formatos"

### "Preciso entender multi-tenancy"
→ [ONBOARDING.md](./ONBOARDING.md), seção "Multi-Tenancy"

### "Quais são os padrões de código?"
→ [CONTRIBUINDO.md](./CONTRIBUINDO.md), seção "Padrões de Código"

### "Como reporto um bug?"
→ [CONTRIBUINDO.md](./CONTRIBUINDO.md), seção "Processo de Review"

---

## 📊 Mapa Conceitual

```
┌─────────────────────────────────────┐
│   NOVO DESENVOLVEDOR ONBOARDING     │
│                                     │
│  1. ONBOARDING.md (Setup)          │
│  ↓                                  │
│  2. PIPELINE_OCR.md (Visão Geral)  │
│  ↓                                  │
│  3. Explorar código-fonte          │
│  ↓                                  │
│  4. ARQUITETURA.md (Detalhes)      │
│  ↓                                  │
│  5. CONTRIBUINDO.md (Padrões)      │
│                                     │
└─────────────────────────────────────┘

┌──────────────────────────────────────┐
│   CONTRIBUINDO PRIMEIRA FEATURE      │
│                                      │
│  1. CONTRIBUINDO.md (Workflow)      │
│  2. PADRÕES (PEP8, Django)          │
│  3. Escrever testes                 │
│  4. Fazer commit + Push             │
│  5. Pull Request                    │
│                                      │
└──────────────────────────────────────┘
```

---

## 🔄 Como Atualizar Esta Documentação

Se você:
- Adiciona nova feature → Atualize o arquivo relevante
- Muda padrões de código → Atualize `CONTRIBUINDO.md`
- Muda arquitetura → Atualize `arquitetura_e_integracao_ia.md`
- Muda pipeline OCR → Atualize `PIPELINE_OCR.md`

**Sempre mantenha a documentação sincronizada com o código!**

---

## 📞 Suporte

- 📧 Email do projeto
- 💬 Slack/Discord
- 🐛 GitHub Issues
- 📚 Revise documentação primeiro

---

## ✅ Checklist Documentação Completa

- [x] ONBOARDING.md - Setup e conceitos básicos
- [x] PIPELINE_OCR.md - Arquitetura técnica de OCR
- [x] CONTRIBUINDO.md - Padrões e processo de desenvolvimento
- [x] INDEX.md - Este arquivo (navegação)
- [x] arquitetura_e_integracao_ia.md - Design profundo (existente)

**Documentação: 100% completa** ✅

---

**Última atualização:** Maio 2026
**Próxima revisão:** Quando adicionar nova funcionalidade major

---

*Explore, aprenda, contribua! 🚀*
