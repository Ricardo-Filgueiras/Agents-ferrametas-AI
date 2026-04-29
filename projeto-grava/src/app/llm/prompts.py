"""
Prompts versionados usando ChatPromptTemplate.

Vantagens sobre f-strings soltas:
  - Variáveis tipadas e explícitas (KeyError se faltar)
  - Compatíveis com LCEL pipe operator (prompt | llm)
  - Versionamento explícito (_V1, _V2...)
"""
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

# ── v1 — Resumo de reunião ────────────────────────────────────────────────
SUMMARY_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente especialista em análise de reuniões corporativas. "
        "Seja direto, objetivo e estruturado. Responda sempre em português."
    ),
    ("human",
     "Analise a transcrição abaixo e produza:\n\n"
     "**Resumo da Reunião:**\n"
     "- Um parágrafo resumindo os principais assuntos (máx. 300 caracteres).\n\n"
     "**Acordos da Reunião:**\n"
     "- Liste cada decisão ou combinado como bullet point.\n"
     "- Se não houver acordos explícitos, escreva: '- Nenhum acordo registrado.'\n\n"
     "Transcrição:\n####\n{transcricao}\n####"
     ),
])

# ── v1 — Q&A sobre histórico de reuniões (RAG) ───────────────────────────
MEETING_QA_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente com acesso ao histórico de reuniões da empresa. "
        "Responda APENAS com base nas reuniões fornecidas como contexto. "
        "Se a informação não estiver no contexto, diga: 'Não encontrei essa informação nas reuniões registradas.'"
    ),
    ("human",
     "Reuniões disponíveis como contexto:\n{context}\n\n"
     "Pergunta: {question}"
     ),
])
