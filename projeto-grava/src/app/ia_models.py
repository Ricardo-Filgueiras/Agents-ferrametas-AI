"""
ia_models — camada de IA (transcrição + resumo).

Refatorado para usar:
  - LLMFactory: sem clientes globais, com cache por (provider, model)
  - ChatPromptTemplate tipado (llm/prompts.py)
  - MeetingCallbackHandler: latência e tokens logados automaticamente
"""
import streamlit as st
from faster_whisper import WhisperModel

from utils import le_arquivo, salva_arquivo
from llm.factory import LLMFactory
from llm.prompts import SUMMARY_PROMPT_V1
from llm.callbacks import MeetingCallbackHandler


# ── Transcrição (Faster-Whisper local) ──────────────────────────────────────

@st.cache_resource
def carregar_whisper(tamanho_modelo: str = 'base') -> WhisperModel:
    """Carrega o modelo Whisper uma vez e reutiliza via cache do Streamlit."""
    return WhisperModel(tamanho_modelo, device="cpu", compute_type="int8")


def transcreve_audio(caminho_audio) -> str:
    """Transcreve um arquivo de áudio usando Faster-Whisper (local, CPU)."""
    tamanho_modelo = st.session_state.get('modelo_whisper', 'base')
    whisper = carregar_whisper(tamanho_modelo)
    segments, _ = whisper.transcribe(str(caminho_audio), beam_size=5, language='pt')
    return " ".join(s.text for s in segments)


# ── Resumo (LLM via LCEL) ────────────────────────────────────────────────────

def gerar_resumo(pasta_reuniao) -> None:
    """
    Gera resumo da reunião via LLM e salva em resumo.txt.

    Usa LCEL: SUMMARY_PROMPT_V1 | LLM — compatível com streaming futuro.
    Provider e modelo lidos do session_state do Streamlit.
    """
    transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
    if not transcricao:
        st.error('Não há transcrição para gerar resumo.')
        return

    provedor_ui = st.session_state.get('provedor', 'Ollama (Local)')
    modelo_ollama = st.session_state.get('modelo_ollama', 'llama3.2:3b')
    model = modelo_ollama if provedor_ui == 'Ollama (Local)' else 'gpt-4o-mini'

    try:
        llm = LLMFactory.create(provider=provedor_ui, model=model)
        chain = SUMMARY_PROMPT_V1 | llm

        resposta = chain.invoke(
            {"transcricao": transcricao},
            config={"callbacks": [MeetingCallbackHandler()]},
        )

        resumo = resposta.content
        resumo += f'\n\n---\n*Resumo gerado pelo modelo: {model} ({provedor_ui})*'
        salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)

    except Exception as e:
        st.error(f'Erro ao gerar resumo: {e}')
