import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge 
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb

from fastapi import FastAPI
import uvicorn

vectordb = ChromaDb(collection_name="fast_knowledge", persist_directory="tmp/chroma")   
knowledge_base = Knowledge(vector_db=vectordb)

knowledge_base.add_content()

db=SqliteDb(db_file="tmp/fast.db")

agent = Agent(
    name="FastAgent",
    model=Ollama(id="llama3.2:3b"),
    db=db,
    knowledge=knowledge_base,
    instructions=[ "Voce é um assistente de IA para um banco simples. Responda perguntas sobre os clientes e suas transações. Use a base de conhecimento para obter informações adicionais sobre os clientes, se necessário."],

)

