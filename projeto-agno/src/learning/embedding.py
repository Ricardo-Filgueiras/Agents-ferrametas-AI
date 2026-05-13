import os
import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge 
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

from fastapi import FastAPI
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

# Esse funcção recebe e guarda os arquivos recebidos em formato original (PDF,TXT,JPG,PNG,MD,etc)
def add_files(path: str, arquivo: str) -> str:
    if not os.path.exists(arquivo):
        return "Arquivo não encontrado"
    knowledge.insert(path=f"{path}/{arquivo}", upsert=True)
    return "Arquivo adicionado com sucesso" 

# Essa função faz o embedding dos arquivos e salva no banco
def embedding():
    knowledge.embed()
    
