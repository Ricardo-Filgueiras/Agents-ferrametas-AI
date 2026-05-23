import os
import time
from langchain_core.tools import tool

DATA_DIR = "data"
CADERNO_PATH = os.path.join(DATA_DIR, "caderno.md")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CADERNO_PATH):
        with open(CADERNO_PATH, "w", encoding="utf-8") as f:
            f.write("# Caderno de Notas da Cozinha\n\n")

@tool
def write_note(content: str) -> str:
    """Escreve uma nova informação no caderno (cliente, pedido, status, receita)."""
    ensure_data_dir()
    data_hora = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(CADERNO_PATH, "a", encoding="utf-8") as f:
        f.write(f"- {data_hora}: {content}\n")
    return "Informação registrada com sucesso no caderno."

@tool
def read_notes() -> str:
    """Lê todas as informações registradas no caderno até o momento."""
    ensure_data_dir()
    try:
        with open(CADERNO_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return content if content.strip() else "O caderno está vazio."
    except Exception as e:
        return f"Erro ao ler o caderno: {e}"
