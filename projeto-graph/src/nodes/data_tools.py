import os
import pandas as pd
import io
import sys
from contextlib import redirect_stdout
from langchain_core.tools import tool

STORAGE_PATH = "data/storage"

@tool
def list_available_files() -> str:
    """
    Lista todos os arquivos CSV disponíveis no diretório de armazenamento seguro.
    Retorna o nome do arquivo e o tamanho em KB.
    """
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)
    
    files = [f for f in os.listdir(STORAGE_PATH) if f.endswith('.csv')]
    if not files:
        return "Nenhum arquivo CSV encontrado em data/storage/."
    
    results = []
    for f in files:
        size = os.path.getsize(os.path.join(STORAGE_PATH, f)) / 1024
        results.append(f"- {f} ({size:.2f} KB)")
    
    return "Arquivos disponíveis:\n" + "\n".join(results)

@tool
def inspect_csv_structure(filename: str) -> str:
    """
    Lê os metadados de um arquivo CSV específico.
    Retorna os nomes das colunas, tipos de dados e as primeiras 5 linhas.
    """
    safe_name = os.path.basename(filename)
    path = os.path.join(STORAGE_PATH, safe_name)
    
    if not os.path.exists(path):
        return f"Erro: Arquivo '{safe_name}' não encontrado."
    
    try:
        df = pd.read_csv(path, nrows=5)
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        
        sample = df.to_markdown()
        
        return (
            f"### Estrutura de {safe_name}\n"
            f"**Resumo do Pandas:**\n```text\n{info_str}\n```\n"
            f"**Amostra de dados (Top 5):**\n\n{sample}"
        )
    except Exception as e:
        return f"Erro ao inspecionar o arquivo: {str(e)}"

@tool
def run_python_analysis(code: str, filename: str) -> str:
    """
    Executa código Python em uma Sandbox para analisar um DataFrame 'df' carregado do arquivo informado.
    Use 'print()' para exibir os resultados ou insights.
    """
    safe_name = os.path.basename(filename)
    path = os.path.join(STORAGE_PATH, safe_name)
    
    if not os.path.exists(path):
        return f"Erro: Arquivo '{safe_name}' não encontrado."
    
    try:
        # Carrega o DF
        df = pd.read_csv(path)
        
        # Prepara o ambiente da Sandbox
        # Bloqueia built-ins perigosos
        safe_builtins = __builtins__.copy()
        for dangerous in ['open', 'eval', 'exec', '__import__', 'getattr', 'setattr']:
            if dangerous in safe_builtins:
                del safe_builtins[dangerous]
        
        sandbox_locals = {
            'df': df,
            'pd': pd,
            'print': print
        }
        
        # Captura a saída do console
        f = io.StringIO()
        with redirect_stdout(f):
            # Executa o código
            exec(code, {'__builtins__': safe_builtins}, sandbox_locals)
        
        output = f.getvalue()
        
        # Limpeza de memória
        del df
        del sandbox_locals
        
        return (
            f"### Resultado da Análise em {safe_name}\n"
            f"**Código Executado:**\n```python\n{code}\n```\n"
            f"**Saída do Console:**\n```text\n{output if output else 'Nenhuma saída gerada (use print()).'}\n```"
        )
    except Exception as e:
        return f"Erro de execução na Sandbox: {str(e)}"
