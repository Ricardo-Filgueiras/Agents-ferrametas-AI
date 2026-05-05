from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS
import os
 
from agno.db.sqlite import SqliteDb 

from agno.tools import tool



# Ferramenta que auxilia o agente a ter persistência de estado na conversa 

def carrinho(session_state):
    """
    Esta ferramenta é utilizada para armazenar os itens do carrinho no banco de dadossqlite.
    ela deve conter o nome do produto , quantidade e valor do item.
    e armazenar no banco de dados sqlite.
    """
    carrinho = session_state['carrinho']
    db.save(carrinho)   
    return carrinho
    

def adicionar_carrinho(session_state,item):
    """
    Esta ferramenta é utilizada para adicionar itens ao carrinho.
    """
    session_state['carrinho'].append(item)
    return session_state['carrinho']

def remover_carrinho(session_state,item):
    """
    Esta ferramenta é utilizada para remover itens do carrinho.
    """

    for i,item in enumerate(session_state['carrinho']):
        if item == item:
            session_state['carrinho'].pop(i)  # remove o item pela posição i
            return f"Item {item} removido do carrinho"


def ver_carrinho(session_state,item):
    """
    Esta ferramenta é utilizada para ver os itens do carrinho.
    """

    return '\n'.join([ f'- {item}' for item in session_state['carrinho']])








# crontrlando e persistindo sessão  de conversação 
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    session_state={'carrinho':[] },
    db=SqliteDb(db_file="tmp/carrinho.db"),
    tools=[ adicionar_carrinho,ver_carrinho],
    instructions="""
    Você é um assistente de vendas que irá auxiliar os clientes com suas compras. 
    seu papel é oferecer produtos ao cliente e adicionar ao carrinho se ele quiser
    voce tem um estado de carrinho que deve ser atualizado a cada venda 
    voce deve responder sempre em portugues,
    Se o cliente solicitar voce deve remover o item do carrinho e subtrair o valor do total

    esses são alguns dos itens e seus valores :
    produto A - R$ 10,00
    produto B - R$ 20,00
    produto C - R$ 30,00

    """,
    markdown=True,
    add_history_to_context=True,
    num_history_messages=7

)

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()