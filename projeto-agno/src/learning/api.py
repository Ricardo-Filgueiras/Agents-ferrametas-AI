import os
import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge 
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

# Configurando o Embedder do Ollama
embedder = OllamaEmbedder(id="nomic-embed-text", dimensions=768, host="http://localhost:11434")


# Usamos um caminho novo para garantir 768 dimensões
knowledge = Knowledge(
    name="pedidos_pdf",
    description="informações sobre os pedidos",
    vector_db=ChromaDb(
        collection="pedidos_v7",
        path="./tmp/db_v7",
        persistent_client=True,
        embedder=embedder
    )
)

db = SqliteDb(db_file="tmp/fast.db")

agent = Agent(
    name="FastAgent",
    model=Ollama(id="llama3.2:3b"),
    description="Você é um assistente brasileiro prestativo que analisa documentos de pedidos.",
    db=db,
    knowledge=knowledge,
    search_knowledge=True,
    instructions=[
        "RESPONDA SEMPRE EM PORTUGUÊS (BRASIL).",
        "Você é um assistente de IA especializado em pedidos.",
        "Ao buscar informações, use a ferramenta 'search_knowledge_base'.",
        "ERRO CRÍTICO A EVITAR: Nunca envie um JSON ou Dicionário no campo 'query'.",
        "FORMA CORRETA: search_knowledge_base(query='texto da busca')",
        "FORMA ERRADA: search_knowledge_base(query={'type': 'string', ...})",
        "Se o dado não for encontrado, informe educadamente."
    ]
)


from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

app = FastAPI(title="Api com agno", description="Api para interagir com o agente Agno")

@app.get("/")
def read_root():
    return {"message": "Api com agno"}

@app.post("/chat")
async def consulta_pdf(request: ChatRequest):
    def stream_response():
        # agent.run com stream=True permite enviar a resposta palavra por palavra
        for response_chunk in agent.run(request.message, stream=True):
            if response_chunk.content is not None:
                yield response_chunk.content

    return StreamingResponse(stream_response(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)