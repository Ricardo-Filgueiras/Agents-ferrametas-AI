from langchain_core.tools import tool , BaseTool

@tool
def somar(a: float, b: float) -> float:
    """
    Soma dois números a e b (a + b).
    Útil para somar valores intermediários ou finais.
    """
    return a + b

@tool
def subtrair(a: float, b: float) -> float:
    """
    Subtrai o segundo número do primeiro (a - b).
    Útil para calcular diferenças.
    """
    return a - b

@tool
def multiplicar(a: float, b: float) -> float:
    """
    Multiplica dois números a e b (a * b).
    Útil para escalonamentos, produtos e fatorações.
    """
    return a * b

@tool
def dividir(a: float, b: float) -> float:
    """
    Divide o primeiro número pelo segundo (a / b).
    Retorna uma mensagem de erro em caso de divisão por zero.
    """
    if b == 0:
        raise ValueError("Divisão por zero não é permitida.")
    return a / b

TOOLS: list[BaseTool] = [somar, subtrair, multiplicar, dividir]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}