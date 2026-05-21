# 📖 Documentação - Agents Ferramentas AI

A documentação está organizada de forma clara e progressiva para facilitar o onboarding de novos desenvolvedores.

---

## 🎯 Comece Aqui

### ✨ Primeira Vez no Projeto?

**Tempo estimado: 2-3 horas**

1. **[ONBOARDING.md](./ONBOARDING.md)** - Guia de Inicialização (30 min)
   - Instalação e configuração do ambiente
   - Estrutura de projeto explicada
   - Primeiras tarefas simples

2. **[PIPELINE_OCR.md](./PIPELINE_OCR.md)** - Entenda o Fluxo (1 hora)
   - Como funciona o processamento de documentos
   - Arquitetura dos componentes
   - Exemplos práticos de código

3. **[CONTRIBUINDO.md](./CONTRIBUINDO.md)** - Padrões do Projeto (1 hora)
   - Como escrever código
   - Fluxo de contribuição
   - Boas práticas

4. **Explore o código** (30 min)
   - Leia comentários nos arquivos principais
   - Execute um teste simples
   - Faça uma pequena mudança

---

## 📚 Documentação Completa

| Documento | Propósito | Público |
|-----------|-----------|---------|
| **[INDEX.md](./INDEX.md)** | Índice e navegação | Todos |
| **[ONBOARDING.md](./ONBOARDING.md)** | Setup e primeiros passos | Novos devs |
| **[PIPELINE_OCR.md](./PIPELINE_OCR.md)** | Arquitetura OCR detalhada | Devs back-end |
| **[CONTRIBUINDO.md](./CONTRIBUINDO.md)** | Padrões de código e workflow | Todos os contributors |
| **[arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md)** | Design profundo do projeto | Arquitetos/Seniors |
| **[CHEAT_SHEET.md](./CHEAT_SHEET.md)** | Comandos rápidos | Todos |

---

## 🗂️ Navegação Rápida

Procurando por algo específico?

### 🚀 Setup & Ambiente
- [Setup inicial do projeto](./ONBOARDING.md#-setup-do-ambiente)
- [Variáveis de ambiente](./ONBOARDING.md#configurar-variáveis-de-ambiente)
- [Erros comuns e soluções](./ONBOARDING.md#-troubleshooting)

### 🤖 Processamento de Documentos (OCR)
- [Fluxo visual do pipeline](./PIPELINE_OCR.md#-visão-geral-do-pipeline)
- [Componentes e arquitetura](./PIPELINE_OCR.md#-arquitetura-de-componentes)
- [Como o OCR funciona](./PIPELINE_OCR.md#novaagentservice)
- [Suporte para novos formatos](./PIPELINE_OCR.md#5-extractors-para-diferentes-formatos)

### 👨‍💻 Desenvolvimento
- [Fluxo Git (branch, commit, PR)](./CONTRIBUINDO.md#-fluxo-de-trabalho)
- [Padrões Python/Django](./CONTRIBUINDO.md#-padrões-de-código)
- [Segurança e multi-tenancy](./CONTRIBUINDO.md#-segurança)
- [Como escrever testes](./CONTRIBUINDO.md#-testes)

### 🔐 Segurança
- [Multi-tenancy explicado](./ONBOARDING.md#multi-tenancy-isolamento-de-dados)
- [Exemplo de código seguro](./CONTRIBUINDO.md#django-views)
- [Checklist de segurança](./CONTRIBUINDO.md#checklist-de-segurança)

### 💾 Banco de Dados
- [Modelo de dados visual](./arquitetura_e_integracao_ia.md#-modelagem-de-dados--relacionamentos)
- [Como adicionar novo campo](./CONTRIBUINDO.md#adicionar-campo-ao-modelo)
- [Migrações do BD](./CONTRIBUINDO.md#-migrações-de-banco-de-dados)

---

## 📋 Tarefas Comuns

### Preciso fazer meu primeiro commit
1. Leia [Fluxo de Trabalho](./CONTRIBUINDO.md#1-criar-uma-branch)
2. Use [Conventional Commits](./CONTRIBUINDO.md#4-commit-com-mensagens-claras)
3. Revise [Checklist de Qualidade](./CONTRIBUINDO.md#-checklist-antes-de-fazer-push)

### Preciso entender o OCR
1. Veja [Visão Geral do Pipeline](./PIPELINE_OCR.md#-visão-geral-do-pipeline)
2. Explore [Arquitetura de Componentes](./PIPELINE_OCR.md#-arquitetura-de-componentes)
3. Revise [Exemplos de Código](./PIPELINE_OCR.md#4-novaagentservice)

### Preciso adicionar uma nova feature
1. [Crie uma branch](./CONTRIBUINDO.md#1-criar-uma-branch)
2. Siga [Padrões de Código](./CONTRIBUINDO.md#-padrões-de-código)
3. Escreva [Testes](./CONTRIBUINDO.md#-testes)
4. Faça [Pull Request](./CONTRIBUINDO.md#5-push-e-pull-request)

### Estou vendo um erro/bug
1. Consulte [Troubleshooting](./ONBOARDING.md#-troubleshooting)
2. Procure em [Tratamento de Erros do Pipeline](./PIPELINE_OCR.md#-tratamento-de-erros)
3. Abra issue no GitHub com detalhes

---

## 🎓 Por Função

### Backend Developer
**Leitura essencial (ordem):**
1. [ONBOARDING.md](./ONBOARDING.md) - Setup
2. [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Arquitetura OCR
3. [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Padrões Python
4. [arquitetura_e_integracao_ia.md](./arquitetura_e_integracao_ia.md) - Modelagem BD

**Referência rápida:** [CHEAT_SHEET.md](./CHEAT_SHEET.md)

### Frontend Developer
**Leitura essencial (ordem):**
1. [ONBOARDING.md](./ONBOARDING.md) - Setup
2. [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Fluxo de Dados
3. [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Segurança

### DevOps / Infra
**Leitura essencial (ordem):**
1. [ONBOARDING.md](./ONBOARDING.md) - Dependências
2. [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Componentes externos

### QA / Tester
**Leitura essencial (ordem):**
1. [PIPELINE_OCR.md](./PIPELINE_OCR.md) - Fluxo visual
2. [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Seção Testes

---

## ⚡ Tl;dr (Resumo Muito Curto)

```bash
# Setup
git clone <REPO>
cd projeto-django
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py runserver

# Código
python manage.py test          # Rodar testes
git checkout -b feature/nome   # Criar branch
git commit -m "feat: descrição" # Commit
git push origin feature/nome    # Push
# Abrir PR no GitHub
```

→ Detalhes em [CHEAT_SHEET.md](./CHEAT_SHEET.md)

---

## 🔍 Índice Completo

Para um mapa interativo e detalhado de toda documentação:

👉 **[INDEX.md](./INDEX.md)** - Navegação por tópico, profissão, e FAQ

---

## 📊 Documentação por Tema

### Arquitetura & Design
- [Decisão Streamlit vs Django](./arquitetura_e_integracao_ia.md#-streamlit-vs-django-decisão-arquitetural)
- [Modelagem de dados](./arquitetura_e_integracao_ia.md#-modelagem-de-dados--relacionamentos)
- [Fluxo do pipeline](./PIPELINE_OCR.md#-visão-geral-do-pipeline)

### Setup & Configuração
- [Instalação passo a passo](./ONBOARDING.md#-setup-do-ambiente)
- [Variáveis .env](./ONBOARDING.md#configurar-variáveis-de-ambiente)
- [Troubleshooting](./ONBOARDING.md#-troubleshooting)

### Processamento de Dados
- [Pipeline OCR completo](./PIPELINE_OCR.md)
- [Suporte de formatos](./PIPELINE_OCR.md#5-extractors-para-diferentes-formatos)
- [Integração Docling/Ollama](./PIPELINE_OCR.md#-fluxo-de-dados-detalhado)

### Código & Qualidade
- [Padrões PEP8](./CONTRIBUINDO.md#python---pep-8)
- [Testes unitários](./CONTRIBUINDO.md#-testes)
- [Segurança](./CONTRIBUINDO.md#-segurança)

### Processo de Contribuição
- [Workflow Git](./CONTRIBUINDO.md#-fluxo-de-trabalho)
- [Pull Requests](./CONTRIBUINDO.md#5-push-e-pull-request)
- [Conventional Commits](./CONTRIBUINDO.md#4-commit-com-mensagens-claras)

---

## ❓ Pergunta Frequente?

**"Por onde eu começo?"**
→ Leia [ONBOARDING.md](./ONBOARDING.md) em 30 minutos

**"Como funciona o OCR?"**
→ Veja [PIPELINE_OCR.md](./PIPELINE_OCR.md)

**"Qual é o padrão de código?"**
→ Consulte [CONTRIBUINDO.md](./CONTRIBUINDO.md#-padrões-de-código)

**"Como faço um Pull Request?"**
→ Siga [Fluxo de Trabalho](./CONTRIBUINDO.md#-fluxo-de-trabalho)

**"Comandos rápidos?"**
→ [CHEAT_SHEET.md](./CHEAT_SHEET.md)

Mais perguntas? Veja [INDEX.md - FAQ](./INDEX.md#-faq-rápida)

---

## 📞 Suporte

Encontrou problema ou tem dúvida?

1. ✅ Procure na documentação (use Ctrl+F)
2. 💬 Pergunte no Slack/Discord do time
3. 🐛 Abra issue no GitHub
4. 📧 Email para o mantainer

---

## 🎉 Pronto para Começar?

Escolha seu caminho:

- 🆕 **Novo no projeto?** → [ONBOARDING.md](./ONBOARDING.md)
- 🤖 **Quer entender OCR?** → [PIPELINE_OCR.md](./PIPELINE_OCR.md)
- 👨‍💻 **Pronto para codificar?** → [CONTRIBUINDO.md](./CONTRIBUINDO.md)
- 📚 **Quer explorar tudo?** → [INDEX.md](./INDEX.md)
- ⚡ **Só precisa de comandos?** → [CHEAT_SHEET.md](./CHEAT_SHEET.md)

---

## 📈 Evolução da Documentação

Esta documentação é **viva** e evolui com o projeto:

- ✅ Versão 1.0 - Documentação Completa (Mai/2026)
  - ONBOARDING.md
  - PIPELINE_OCR.md
  - CONTRIBUINDO.md
  - INDEX.md
  - CHEAT_SHEET.md

**Contribua com melhorias!**

---

**Bem-vindo ao Agents Ferramentas AI! 🚀**

*Última atualização: Maio 2026*
*Mantido por: Time de Desenvolvimento*
