"""
utils — helpers de I/O, configuração de caminhos e serviços externos.

Sem lógica de IA aqui. PROMPT removido — prompts agora em llm/prompts.py.
"""
import re
from pathlib import Path

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# ── Caminhos ─────────────────────────────────────────────────────────────────

PASTA_ARQUIVOS = Path(__file__).parent.parent.parent / 'data'
PASTA_ARQUIVOS.mkdir(exist_ok=True)


# ── I/O de arquivos ──────────────────────────────────────────────────────────

def salva_arquivo(caminho_arquivo, conteudo: str) -> None:
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)


def le_arquivo(caminho_arquivo) -> str:
    path = Path(caminho_arquivo)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''


# ── Pré-processamento de transcrição ─────────────────────────────────────────

# Sons de hesitação do português falado — não filtra por idioma
_HESITACOES = re.compile(r'\b([aã]+h+n?|h+m+n?)\b', re.IGNORECASE)
# Palavra repetida 3 ou mais vezes seguidas (ex: "né né né", "eu eu eu")
_REPETICOES = re.compile(r'\b(\w{2,})([ \t]+\1){2,}\b', re.IGNORECASE)


def limpar_transcricao(texto: str) -> str:
    """
    Remove artefatos de fala sem filtrar por idioma.
    Preserva palavras em inglês de uso corporativo (call, workspace, etc.).
    """
    texto = _HESITACOES.sub('', texto)
    texto = _REPETICOES.sub(r'\1', texto)
    texto = re.sub(r' {2,}', ' ', texto)
    return texto.strip()


# ── Serviços externos ────────────────────────────────────────────────────────

def listar_modelos_ollama() -> list[str]:
    """Consulta o Ollama local e retorna os modelos disponíveis."""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            return [m['name'] for m in response.json().get('models', [])]
    except Exception:
        pass
    return []


def listar_reunioes() -> dict[str, str]:
    """Retorna {folder_stem: label} das reuniões gravadas, mais recente primeiro."""
    pastas = sorted(
        [p for p in PASTA_ARQUIVOS.glob('*') if p.is_dir()],
        reverse=True,
    )
    reunioes_dict: dict[str, str] = {}
    for pasta in pastas:
        stem = pasta.stem
        try:
            ano, mes, dia, hora, minuto, seg = stem.split('_')
            label = f'{ano}/{mes}/{dia} {hora}:{minuto}:{seg}'
        except ValueError:
            label = stem
        titulo = le_arquivo(pasta / 'titulo.txt')
        if titulo:
            label += f' - {titulo}'
        reunioes_dict[stem] = label
    return reunioes_dict
