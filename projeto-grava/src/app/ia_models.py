"""
ia_models — camada de IA (transcrição + resumo).

Refatorado para usar:
  - LLMFactory: sem clientes globais, com cache por (provider, model)
  - ChatPromptTemplate tipado (llm/prompts.py)
  - MeetingCallbackHandler: latência e tokens logados automaticamente
  - Map-reduce chunking com paralelismo para transcrições longas (> 4000 chars)
"""
import streamlit as st
from faster_whisper import WhisperModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import le_arquivo, salva_arquivo
from llm.factory import LLMFactory
from llm.prompts import SUMMARY_PROMPT_V1, CHUNK_SUMMARY_PROMPT_V1
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
    return "\n".join(s.text for s in segments)


def retranscrever_reuniao(pasta_reuniao, modelo_whisper: str) -> None:
    """Re-transcreve audio.mp3 com o modelo Whisper escolhido e salva transcricao.txt."""
    from pathlib import Path

    audio_path = Path(pasta_reuniao) / 'audio.mp3'
    if not audio_path.exists():
        st.error('Arquivo audio.mp3 não encontrado nesta reunião.')
        return

    whisper = carregar_whisper(modelo_whisper)
    segments, _ = whisper.transcribe(str(audio_path), beam_size=5, language='pt')
    texto = "\n".join(s.text for s in segments)

    texto += f'\n\n---\n*Transcrição gerada pelo modelo: {modelo_whisper}*'
    salva_arquivo(Path(pasta_reuniao) / 'transcricao.txt', texto)
    st.success(f'✅ Transcrição concluída com modelo {modelo_whisper}!')


# ── Resumo (LLM via LCEL) ────────────────────────────────────────────────────

def _split_em_chunks(texto: str, tamanho: int = 2750, overlap: int = 275) -> list[str]:
    """Divide texto em chunks usando RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=tamanho,
        chunk_overlap=overlap,
    )
    return splitter.split_text(texto)


def _resumir_chunk(args: tuple) -> tuple[int, str]:
    """Resumir um chunk individual. Executado em thread paralela."""
    idx, chunk, chain = args
    resposta = chain.invoke(
        {"chunk": chunk},
        config={"callbacks": [MeetingCallbackHandler()]},
    )
    return idx, resposta.content

def gerar_resumo(pasta_reuniao) -> None:
    """
    Gera resumo da reunião via LLM e salva em resumo.txt.

    Para transcrições longas (> 4000 chars): usa map-reduce chunking.
    Chunks pequenos são resumidos independentemente (mais rápido em CPU),
    depois os resumos parciais são sintetizados num resumo final.

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

        # Decidir se usa chunking (map-reduce) ou resumo direto
        usar_chunking = len(transcricao) > 4000

        if usar_chunking:
            # MAP phase: resumir chunks em paralelo
            chunks = _split_em_chunks(transcricao)

            progress_bar = st.progress(0)
            status_text = st.empty()

            chain_chunk = CHUNK_SUMMARY_PROMPT_V1 | llm

            # Processar chunks em paralelo com ThreadPoolExecutor
            status_text.text(f'Processando {len(chunks)} trechos em paralelo...')
            args = [(i, chunk, chain_chunk) for i, chunk in enumerate(chunks)]

            resultados = {}
            concluidos = 0

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(_resumir_chunk, arg): arg[0] for arg in args}

                for future in as_completed(futures):
                    idx, conteudo = future.result()
                    resultados[idx] = conteudo
                    concluidos += 1
                    progress_bar.progress(concluidos / len(chunks))
                    status_text.text(f'Concluído {concluidos}/{len(chunks)} trechos...')

            # Reordenar resultados pela ordem original
            resumos_parciais = [resultados[i] for i in range(len(chunks))]

            progress_bar.empty()
            status_text.empty()

            # REDUCE phase: sintetizar resumos parciais
            st.info('Sintetizando resumo final...')
            resumos_juntos = "\n\n".join(resumos_parciais)

            chain_final = SUMMARY_PROMPT_V1 | llm
            resposta_final = chain_final.invoke(
                {"transcricao": resumos_juntos},
                config={"callbacks": [MeetingCallbackHandler()]},
            )
            resumo = resposta_final.content
        else:
            # Caminho direto para transcrições curtas
            chain = SUMMARY_PROMPT_V1 | llm
            resposta = chain.invoke(
                {"transcricao": transcricao},
                config={"callbacks": [MeetingCallbackHandler()]},
            )
            resumo = resposta.content

        resumo += f'\n\n---\n*Resumo gerado pelo modelo: {model} ({provedor_ui})*'
        salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)
        st.success('Resumo gerado com sucesso!')

    except Exception as e:
        st.error(f'Erro ao gerar resumo: {e}')
