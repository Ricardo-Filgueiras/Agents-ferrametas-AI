import os
import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge 
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.os import AgentOS


agent = Agent(
    id="agent_os_fast",
    name="FastAgent",
    model=Ollama(id="llama3.2:3b"),
    description="Você é um assistente brasileiro prestativo que analisa documentos de pedidos.",
    db=SqliteDb(db_file="tmp/fast.db"),
    instructions=[
        "RESPONDA SEMPRE EM PORTUGUÊS (BRASIL).",
        "Você é um assistente de IA especializado em pedidos.",
        "Ao buscar informações, use a ferramenta 'search_knowledge_base'.",
        "ERRO CRÍTICO A EVITAR: Nunca envie um JSON ou Dicionário no campo 'query'.",
        "FORMA CORRETA: search_knowledge_base(query='texto da busca')",
        "FORMA ERRADA: search_knowledge_base(query={'type': 'string', ...})",
        "Se o dado não for encontrado, informe educadamente."
    ],
    markdown=True
)
agent_os = AgentOS(
    agents=[
        agent
    ]
)

app = agent_os.get_app()

if __name__ == "__main__":
    uvicorn.run("agent_os_api:app", host="0.0.0.0", port=8000, reload=True)