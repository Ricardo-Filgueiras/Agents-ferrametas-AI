"""
ia_models — camada de IA (transcrição + resumo).

Abordagem de resumo:
  - Transcrição armazena timestamps por segmento: [Xs-Ys] texto
  - gerar_resumo() agrupa segmentos em janelas de ~25s e resume cada janela (MAP)
  - Fase REDUCE sintetiza a timeline em resumo global + acordos
  - Fallback: transcrições antigas sem timestamps usam map-reduce por caracteres
"""
import re
import time
import streamlit as st
from faster_whisper import WhisperModel
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils import le_arquivo, salva_arquivo, limpar_transcricao
from llm.factory import LLMFactory
from llm.prompts import (
    SUMMARY_PROMPT_V1, CHUNK_SUMMARY_PROMPT_V1,
    TIME_CHUNK_PROMPT_V1, TIMELINE_REDUCE_PROMPT_V1,
)
from llm.callbacks import MeetingCallbackHandler

_TIMESTAMP_RE = re.compile(r'^\[(\d+)s-(\d+)s\]\s*(.*)')


# ── Transcrição (Faster-Whisper local) ──────────────────────────────────────

@st.cache_resource
def carregar_whisper(tamanho_modelo: str = 'base') -> WhisperModel:
    return WhisperModel(tamanho_modelo, device="cpu", compute_type="int8")


def transcreve_audio(
    caminho_audio,
    offset_seg: float = 0.0,
    modelo_override: str | None = None,
) -> str:
    """Transcreve áudio com Faster-Whisper. Retorna linhas '[Xs-Ys] texto'."""
    tamanho_modelo = modelo_override or st.session_state.get('modelo_whisper', 'base')
    whisper = carregar_whisper(tamanho_modelo)
    segments, _ = whisper.transcribe(str(caminho_audio), beam_size=5, language='pt')
    linhas = [
        f"[{int(s.start + offset_seg)}s-{int(s.end + offset_seg)}s] {s.text.strip()}"
        for s in segments
    ]
    return "\n".join(linhas)


def retranscrever_reuniao(pasta_reuniao, modelo_whisper: str) -> None:
    """Re-transcreve audio.mp3 com timestamps absolutos e salva transcricao.txt."""
    from pathlib import Path

    audio_path = Path(pasta_reuniao) / 'audio.mp3'
    if not audio_path.exists():
        st.error('Arquivo audio.mp3 não encontrado nesta reunião.')
        return

    texto = transcreve_audio(audio_path, modelo_override=modelo_whisper)
    texto += f'\n\n---\n*Transcrição gerada pelo modelo: {modelo_whisper}*'
    salva_arquivo(Path(pasta_reuniao) / 'transcricao.txt', texto)
    st.success(f'✅ Transcrição concluída com modelo {modelo_whisper}!')


# ── Chunking por janela de tempo ─────────────────────────────────────────────

def _agrupar_por_janela_tempo(transcricao: str, janela_seg: int = 25) -> list[dict]:
    """
    Lê linhas '[Xs-Ys] texto' e agrupa em janelas de até janela_seg segundos.
    Retorna lista de dicts {inicio, fim, texto}. Retorna [] se não há timestamps.
    """
    segmentos = []
    for linha in transcricao.splitlines():
        m = _TIMESTAMP_RE.match(linha.strip())
        if m:
            segmentos.append({
                'inicio': int(m.group(1)),
                'fim': int(m.group(2)),
                'texto': m.group(3).strip(),
            })

    if not segmentos:
        return []

    chunks: list[dict] = []
    chunk_atual = [segmentos[0]]
    inicio_chunk = segmentos[0]['inicio']
    fim_chunk = segmentos[0]['fim']

    for seg in segmentos[1:]:
        if seg['fim'] - inicio_chunk > janela_seg:
            chunks.append({
                'inicio': inicio_chunk,
                'fim': fim_chunk,
                'texto': ' '.join(c['texto'] for c in chunk_atual),
            })
            chunk_atual = [seg]
            inicio_chunk = seg['inicio']
            fim_chunk = seg['fim']
        else:
            chunk_atual.append(seg)
            fim_chunk = seg['fim']

    if chunk_atual:
        chunks.append({
            'inicio': inicio_chunk,
            'fim': fim_chunk,
            'texto': ' '.join(c['texto'] for c in chunk_atual),
        })
    return chunks


def _invocar_com_retry(chain, inputs: dict, max_tentativas: int = 2, espera_seg: float = 3.0):
    """Chama chain.invoke com retry — trata quedas de conexão do Ollama."""
    ultimo_erro = None
    for tentativa in range(max_tentativas):
        try:
            return chain.invoke(inputs, config={"callbacks": [MeetingCallbackHandler()]})
        except Exception as e:
            ultimo_erro = e
            if tentativa < max_tentativas - 1:
                time.sleep(espera_seg)
    raise ultimo_erro


def _split_em_chunks(texto: str, tamanho: int = 4000, overlap: int = 400) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=tamanho, chunk_overlap=overlap)
    return splitter.split_text(texto)


# ── Resumo (LLM via LCEL) ────────────────────────────────────────────────────

def gerar_resumo(pasta_reuniao) -> None:
    """
    Gera resumo da reunião via LLM e salva em resumo.txt.

    Para transcrições com timestamps: timeline indexada por segundos + síntese final.
    Para transcrições antigas (sem timestamps): map-reduce por caracteres (fallback).
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
        chunks_tempo = _agrupar_por_janela_tempo(transcricao)

        if chunks_tempo:
            # ── Abordagem principal: timeline indexada por segundos ─────────
            pasta_chunks = pasta_reuniao / 'chunks'
            pasta_chunks.mkdir(exist_ok=True)

            progress_bar = st.progress(0)
            status_text = st.empty()
            blocos_timeline: list[str] = []

            for i, chunk in enumerate(chunks_tempo):
                label = f'[{chunk["inicio"]}s-{chunk["fim"]}s]'
                nome_base = f'{i:04d}_{chunk["inicio"]}s-{chunk["fim"]}s'
                resumo_path = pasta_chunks / f'{nome_base}_resumo.txt'

                # Salva bruto e limpo independente de sucesso/falha do LLM
                salva_arquivo(pasta_chunks / f'{nome_base}.txt', chunk['texto'])
                texto_limpo = limpar_transcricao(chunk['texto'])
                salva_arquivo(pasta_chunks / f'{nome_base}_clean.txt', texto_limpo)

                # Checkpoint: reutiliza resumo já gerado sem chamar o LLM de novo
                if resumo_path.exists():
                    resumo_chunk = le_arquivo(resumo_path)
                    blocos_timeline.append(f'{label}\n{resumo_chunk.strip()}')
                    progress_bar.progress((i + 1) / len(chunks_tempo))
                    continue

                status_text.text(f'Resumindo {label}... ({i + 1}/{len(chunks_tempo)})')
                chain = TIME_CHUNK_PROMPT_V1 | llm
                try:
                    resposta = _invocar_com_retry(
                        chain,
                        {"inicio": chunk["inicio"], "fim": chunk["fim"], "trecho": texto_limpo},
                    )
                    resumo_chunk = resposta.content.strip()
                    salva_arquivo(resumo_path, resumo_chunk)
                except Exception as chunk_err:
                    st.warning(f'Falha no trecho {label} (2 tentativas): {chunk_err}')
                    resumo_chunk = '- Trecho não processado.'

                blocos_timeline.append(f'{label}\n{resumo_chunk}')
                progress_bar.progress((i + 1) / len(chunks_tempo))

            progress_bar.empty()
            status_text.empty()

            # ── Fase REDUCE: síntese global + acordos ──────────────────────
            st.info('Gerando síntese final...')
            timeline_texto = "\n\n".join(blocos_timeline)
            chain_reduce = TIMELINE_REDUCE_PROMPT_V1 | llm
            resposta_final = _invocar_com_retry(chain_reduce, {"timeline": timeline_texto})
            resumo = f'{timeline_texto}\n\n---\n{resposta_final.content.strip()}'

        else:
            # ── Fallback: transcrição sem timestamps (gravações antigas) ───
            usar_chunking = len(transcricao) > 10000
            if usar_chunking:
                chunks = _split_em_chunks(transcricao)
                progress_bar = st.progress(0)
                status_text = st.empty()
                resumos_parciais: list[str] = []
                for i, chunk in enumerate(chunks):
                    status_text.text(f'Processando trecho {i + 1}/{len(chunks)}...')
                    chain_chunk = CHUNK_SUMMARY_PROMPT_V1 | llm
                    resposta = _invocar_com_retry(chain_chunk, {"chunk": chunk})
                    resumos_parciais.append(resposta.content)
                    progress_bar.progress((i + 1) / len(chunks))
                progress_bar.empty()
                status_text.empty()
                st.info('Sintetizando resumo final...')
                chain_final = SUMMARY_PROMPT_V1 | llm
                resposta_final = _invocar_com_retry(
                    chain_final, {"transcricao": "\n\n".join(resumos_parciais)}
                )
                resumo = resposta_final.content
            else:
                chain = SUMMARY_PROMPT_V1 | llm
                resposta = _invocar_com_retry(chain, {"transcricao": transcricao})
                resumo = resposta.content

        resumo += f'\n\n---\n*Resumo gerado pelo modelo: {model} ({provedor_ui})*'
        salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)
        st.success('Resumo gerado com sucesso!')

    except Exception as e:
        st.error(f'Erro ao gerar resumo: {e}')
