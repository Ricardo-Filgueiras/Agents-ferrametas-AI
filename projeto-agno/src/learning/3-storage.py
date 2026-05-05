from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS
import os
 
from agno.db.sqlite import SqliteDb 

from agno.tools import tool

db=SqliteDb(db_file="tmp/agno.db")


# crontrlando e persistindo sessão  de conversação 
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    # session_id="primeira_interacao",
    tools=[],
    instructions=[
        "Você é um assistente pessoal chamado Agnus.",
        "Você deve falar apenas em Português do Brasil.",
        "Apresente-se e pergunte como pode ajudar.",
        "O histórico das conversas é salvo automaticamente no banco de dados.",
        "Se você aprender algo sobre o usuário, use a ferramenta `update_user_memory`.",
        "IMPORTANTE: Use APENAS o parâmetro `task`. Exemplo: `update_user_memory(task={'type': 'add', 'memory': 'O usuário gosta de sushi'})`",
    ],
    db=db,
    markdown=True,
    enable_agentic_memory=True,
    add_memories_to_context=True
)
# Memories are automatically created from this conversation
agent.print_response("My name is Sarah and I prefer email over phone calls.", session_id="primeira_interacao_01")

# mensagem vai entrar no contexto para dar suporte ao Agnus  a responder de forma correta
agent.print_response("My birthday is on June 1st.", session_id="segunda_interacao_01")

# mensagem para testar a memoria
agent.print_response("What is my name and when is my birthday?", session_id="terceira_interacao_01")

