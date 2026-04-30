from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS

from pydantic import BaseModel , Field
from typing import List, Optional

from agno.tools import tool

class VendasOutput(BaseModel):
    valor : float = Field(description="Valor total das vendas")
    qtde : float = Field(description="Quantidade de produtos vendidos")
    desconto : float = Field(description="Valor total de desconto aplicado")
    descricao : str = Field(description="Descrição do produto")

def vendas_hoje():
    """
    Esta ferramenta é utilizada para obter as vendas de hoje.
    """
    vendas = [
            ["item aaa", 122.45 , 2 , 0.59 , "item aaa vendido com sucesso"],
            ["item bbb", 112.45 , 4 , 0.10 , "item bbb vendido com sucesso"],
            ["item ccc", 12.45 , 5 , 550.90 , "item ccc vendido com sucesso"    ]

    ]
    return  vendas




@tool()
async def vendas(vendas : List[VendasOutput]) -> str:
    """
    Esta ferramenta é utilizada para realizar vendas de produtos.
    """
    return "Vendas realizadas com sucesso"

agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[vendas_hoje, vendas],
    instructions="""
    Você é um assistente de vendas que irá auxiliar os clientes com suas compras. 
    Você deve utilizar as ferramentas disponíveis para obter as vendas de hoje e realizar novas vendas.
    
    """,
    output_schema=VendasOutput,
    markdown=True
)

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

# agent.print_response("Quanto é 1 + 1 * 4 - (2 + 1) qual o valor desse calculo ?", stream=True)
# agent.print_response("Quanto é 0 * 150 + 250 - 14 - 78 + 10 * 45 - ( 100 +15 ) / 5 ?", stream=True)
# agent.print_response("Qual o valor de 100 menos 50 dividindo por 10 ?", stream=True)
# agent.print_response("Quanto é 5, mais 5 elevado a 2 mais 90 dividido por 3 ?", stream=True)
# agent.print_response(
#     """ Uma ONG está organizando kits de doação para distribuir em comunidades.

#         No início do dia, já havia 5 kits prontos no estoque.

#         Durante a manhã, 5 voluntários trabalharam na montagem, e cada um conseguiu montar 5 kits, totalizando uma produção de 5² kits.

#         À tarde, a ONG recebeu uma doação de 90 itens individuais, que foram organizados em kits dividindo igualmente entre 3 equipes, resultando em novos kits prontos.

#         Ao final do dia, quantos kits a ONG tem disponíveis para distribuição?
#     """, 
#     stream=True)