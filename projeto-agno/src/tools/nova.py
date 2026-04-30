from pydantic import BaseModel , Field
from typing import List, Optional

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




@Tool()
async def vendas(vendas : List[VendasOutput]) -> str:
    """
    Esta ferramenta é utilizada para realizar vendas de produtos.
    """
    return "Vendas realizadas com sucesso"
