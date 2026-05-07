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
     "Analise a transcrição abaixo e produza o resumo no formato exato:\n\n"
     "Resumo reunião:\n"
     "- [texto corrido com os principais assuntos, máx. 450 caracteres]\n\n"
     "Acordos da Reunião:\n"
     "- [acordo 1]\n"
     "- [acordo 2]\n"
     "- Se não houver acordos explícitos, escreva: '- Nenhum acordo registrado.'\n\n"
     "Transcrição:\n####\n{transcricao}\n####\n\n"
     "IMPORTANTE: Responda EXCLUSIVAMENTE em português brasileiro."
     ),
])

# ── v1 — Resumo de chunk (map phase de map-reduce) ─────────────────────
CHUNK_SUMMARY_PROMPT_V1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um assistente especialista em análise de reuniões corporativas. "
        "Seja direto e objetivo. Responda sempre em português."
    ),
    ("human",
     "Extraia os pontos principais e decisões deste trecho de transcrição.\n"
     "Seja conciso — máximo 150 palavras.\n"
     "Liste como bullet points.\n\n"
     "Trecho:\n####\n{chunk}\n####\n\n"
     "IMPORTANTE: Responda EXCLUSIVAMENTE em português brasileiro."
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
