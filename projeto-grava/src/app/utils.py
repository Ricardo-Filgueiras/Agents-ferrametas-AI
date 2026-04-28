from pathlib import Path
import requests
from dotenv import load_dotenv, find_dotenv
import os 

PROMPT_PATH = Path(r"src\app\systemprompt.md")

def carrega_prompt(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Prompt não encontrado."
        
# Carrega variáveis de ambiente
load_dotenv(find_dotenv())

# Configuração de Caminhos
PASTA_ARQUIVOS = Path(__file__).parent.parent.parent / 'data'
PASTA_ARQUIVOS.mkdir(exist_ok=True)

PROMPT = carrega_prompt(PROMPT_PATH)

def salva_arquivo(caminho_arquivo, conteudo):
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def le_arquivo(caminho_arquivo):
    if caminho_arquivo.exists():
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return ''

def listar_modelos_ollama():
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            return [m['name'] for m in response.json().get('models', [])]
    except Exception:
        return []
    return []

def listar_reunioes():
    lista_reunioes = PASTA_ARQUIVOS.glob('*')
    lista_reunioes = [p for p in lista_reunioes if p.is_dir()]
    lista_reunioes.sort(reverse=True)
    reunioes_dict = {}
    for pasta_reuniao in lista_reunioes:
        data_reuniao = pasta_reuniao.stem
        try:
            ano, mes, dia, hora, min, seg = data_reuniao.split('_')
            label = f'{ano}/{mes}/{dia} {hora}:{min}:{seg}'
        except ValueError:
            label = data_reuniao
        
        titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
        if titulo != '':
            label += f' - {titulo}'
        reunioes_dict[data_reuniao] = label
    return reunioes_dict
