import openai
import streamlit as st
from faster_whisper import WhisperModel
from utils import le_arquivo, salva_arquivo, PROMPT


# CONFIGURAÇÃO DOS CLIENTES =====================
def get_openai_client():
    try:
        return openai.OpenAI()
    except Exception:
        return openai.OpenAI(api_key='sk-no-key-provided')

client = get_openai_client()
client_local = openai.OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')


# CONFIGURAÇÃO DOS MODELOS LOCAIS =====================
@st.cache_resource
def carregar_whisper(tamanho_modelo: str = 'base') -> WhisperModel:
    return WhisperModel(tamanho_modelo, device="cpu", compute_type="int8")


def transcreve_audio(caminho_audio) -> str:
    tamanho_modelo = st.session_state.get('modelo_whisper', 'base')
    whisper = carregar_whisper(tamanho_modelo)
    segments, _ = whisper.transcribe(str(caminho_audio), beam_size=5, language='pt')
    return " ".join([segment.text for segment in segments])


def chat_openai(mensagem, modelo_default='llama3.2:3b'):
    provedor = st.session_state.get('provedor', 'OpenAI')

    if provedor == 'Ollama (Local)':
        cliente_atual = client_local
        modelo_atual = st.session_state.get('modelo_ollama', 'llama3.2:3b')
    else:
        cliente_atual = client
        modelo_atual = modelo_default

    mensagens = [{'role': 'user', 'content': mensagem}]
    resposta = cliente_atual.chat.completions.create(
        model=modelo_atual,
        messages=mensagens,
    )
    return resposta.choices[0].message.content, modelo_atual


def gerar_resumo(pasta_reuniao):
    transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
    if transcricao == '':
        st.error('Não há transcrição para gerar resumo.')
        return
    provedor = st.session_state.get('provedor', 'OpenAI')
    resumo, modelo_utilizado = chat_openai(mensagem=PROMPT.format(transcricao))
    resumo += f'\n\n---\n*Resumo gerado pelo modelo: {modelo_utilizado} ({provedor})*'
    salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)
