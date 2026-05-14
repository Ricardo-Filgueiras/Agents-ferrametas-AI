from pathlib import Path
from datetime import datetime
from io import BytesIO
import time
import queue
import subprocess
import sys
import pydub
import av
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from dotenv import load_dotenv, find_dotenv

# ── Imports da nova estrutura ─────────────────────────────────────────────────
from utils import (
    PASTA_ARQUIVOS, salva_arquivo, le_arquivo,
    listar_modelos_ollama, listar_reunioes,
)
from ia_models import transcreve_audio, gerar_resumo, retranscrever_reuniao
from capture.audio import adiciona_chunck_audio, processa_audio_container
from capture.video import processa_video_container, flush_container, bgr_para_av_frame
from capture.printela import ScreenRecorder
from capture.system_audio import listar_dispositivos_loopback, SystemAudioCapture
from capture.mixed_audio import MixedAudioCapture

_ = load_dotenv(find_dotenv())

MODELOS_WHISPER = ['tiny', 'base', 'small', 'medium']

# Fonte de áudio — constantes legíveis
FONTE_MIC = 'Microfone'
FONTE_SISTEMA = 'Áudio do Sistema'
FONTE_MISTO = '🎙️+🔊 Microfone + Sistema'

# CSS injetado no iframe do webrtc_streamer via JavaScript.
_RECORDER_BTN_JS = """
<script>
(function () {
    var START_CSS = [
        "width:88px!important",
        "height:88px!important",
        "border-radius:50%!important",
        "background:radial-gradient(circle at 36% 36%,#fc8181,#9b1c1c)!important",
        "border:4px solid rgba(255,255,255,0.18)!important",
        "color:#fff!important",
        "font-size:10px!important",
        "font-weight:800!important",
        "letter-spacing:2px!important",
        "text-transform:uppercase!important",
        "cursor:pointer!important",
        "box-shadow:0 6px 28px rgba(155,28,28,.75),inset 0 2px 0 rgba(255,255,255,.25)!important",
        "transition:transform .12s,box-shadow .12s!important",
        "outline:none!important"
    ].join(";");

    var IFRAME_BODY_CSS = [
        "margin:0!important",
        "background:transparent!important",
        "display:flex!important",
        "align-items:center!important",
        "justify-content:center!important",
        "min-height:110px!important"
    ].join(";");

    function apply() {
        var frames = document.querySelectorAll("iframe");
        frames.forEach(function (f) {
            try {
                var doc = f.contentDocument;
                if (!doc || !doc.body) return;
                var btn = doc.querySelector("button");
                if (!btn || doc.querySelector("#_rec_style")) return;
                var s = doc.createElement("style");
                s.id = "_rec_style";
                s.textContent =
                    "html,body{" + IFRAME_BODY_CSS + "}" +
                    "button{" + START_CSS + "}" +
                    "button:hover{transform:scale(1.07)!important;" +
                    "box-shadow:0 10px 40px rgba(155,28,28,.95)," +
                    "inset 0 2px 0 rgba(255,255,255,.25)!important}" +
                    "button:active{transform:scale(0.94)!important}";
                doc.head.appendChild(s);
            } catch (e) {}
        });
    }

    apply();
    [150, 400, 900, 2000, 4000].forEach(function (d) { setTimeout(apply, d); });
    var mo = new MutationObserver(apply);
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); }, 30000);
})();
</script>
"""


# ── Helpers de pós-processamento ─────────────────────────────────────────────

def _merge_audio_parts(parts: list, output_path: Path):
    combined = pydub.AudioSegment.empty()
    for part in parts:
        combined += pydub.AudioSegment.from_mp3(part)
    combined.export(output_path, format='mp3')
    for part in parts:
        part.unlink(missing_ok=True)


def _muxar_audio_no_video(video_path: Path, audio_path: Path) -> bool:
    """Combina video (sem áudio) + audio.mp3 num único MP4 com faststart."""
    ffmpeg_local = Path(__file__).parent / ('ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg')
    ffmpeg_cmd = str(ffmpeg_local) if ffmpeg_local.exists() else 'ffmpeg'
    temp_path = video_path.with_suffix('.tmp.mp4')
    try:
        video_path.rename(temp_path)
        result = subprocess.run(
            [ffmpeg_cmd, '-y',
             '-i', temp_path.as_posix(),
             '-i', audio_path.as_posix(),
             '-c:v', 'copy', '-c:a', 'aac',
             '-movflags', '+faststart',
             video_path.as_posix()],
            capture_output=True,
        )
        if result.returncode != 0:
            temp_path.rename(video_path)
            return False
        temp_path.unlink(missing_ok=True)
        return True
    except Exception:
        if temp_path.exists() and not video_path.exists():
            temp_path.rename(video_path)
        return False


def _optimize_video_for_web(video_path: Path) -> bool:
    """Remux MP4 movendo o moov atom para o início (faststart)."""
    ffmpeg_local = Path(__file__).parent / ('ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg')
    ffmpeg_cmd = str(ffmpeg_local) if ffmpeg_local.exists() else 'ffmpeg'
    temp_path = video_path.with_suffix('.tmp.mp4')
    try:
        video_path.rename(temp_path)
        result = subprocess.run(
            [ffmpeg_cmd, '-y', '-i', temp_path.as_posix(),
             '-movflags', '+faststart', '-c', 'copy', video_path.as_posix()],
            capture_output=True,
        )
        if result.returncode != 0:
            temp_path.rename(video_path)
            return False
        temp_path.unlink(missing_ok=True)
        return True
    except Exception:
        if temp_path.exists() and not video_path.exists():
            temp_path.rename(video_path)
        return False


def _indicador_gravando(container, elapsed_secs: int):
    """Renderiza o indicador visual de gravação com cronômetro."""
    mins, secs = divmod(elapsed_secs, 60)
    container.markdown(f"""
<style>
@keyframes _rec_pulse {{
  0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(229,62,62,0.5); }}
  50% {{ opacity: 0.6; box-shadow: 0 0 0 6px rgba(229,62,62,0); }}
}}
</style>
<div style="display:inline-flex;align-items:center;gap:10px;
            padding:10px 18px;background:#fff5f5;border-radius:10px;
            border:1px solid #feb2b2;margin-bottom:6px">
  <span style="width:12px;height:12px;background:#e53e3e;border-radius:50%;
               display:inline-block;
               animation:_rec_pulse 1.4s ease-in-out infinite"></span>
  <strong style="color:#c53030;letter-spacing:2px;font-size:14px">REC</strong>
  <span style="font-family:monospace;font-size:15px;color:#718096;min-width:48px">
    {mins:02d}:{secs:02d}
  </span>
</div>
""", unsafe_allow_html=True)


# ── TAB IMPORTAR ÁUDIO ───────────────────────────────────────────────────────

def tab_importar_audio():
    titulo = st.text_input(
        'Título da reunião',
        placeholder='Ex: Reunião de planejamento Q2',
        help='Defina o título antes de transcrever',
    )
    arquivo = st.file_uploader(
        'Selecione o arquivo de áudio',
        type=['m4a', 'mp3', 'wav'],
        help='Formatos suportados: M4A, MP3, WAV',
    )

    if arquivo:
        if st.button('🎙️ Transcrever', type='primary'):
            pasta_reuniao = PASTA_ARQUIVOS / datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            pasta_reuniao.mkdir(parents=True, exist_ok=True)

            if titulo.strip():
                salva_arquivo(pasta_reuniao / 'titulo.txt', titulo.strip())

            try:
                with st.spinner('Convertendo áudio...'):
                    audio = pydub.AudioSegment.from_file(BytesIO(arquivo.read()))
                    audio = audio.set_frame_rate(16000).set_channels(1)
                    audio.export(pasta_reuniao / 'audio.mp3', format='mp3')
            except Exception as e:
                st.error(f'Não foi possível ler o arquivo: {e}')
                return

            modelo = st.session_state.get('modelo_whisper', 'base')
            with st.spinner(f'Transcrevendo com modelo {modelo}...'):
                retranscrever_reuniao(pasta_reuniao, modelo)

            st.session_state['ir_para_historico'] = True
            st.rerun()


# ── TAB GRAVA REUNIÃO ─────────────────────────────────────────────────────────

def tab_grava_reuniao():
    titulo_reuniao = st.text_input(
        'Título da reunião',
        placeholder='Ex: Reunião de planejamento Q2',
        help='Defina o título antes de iniciar a gravação',
    )

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capturar_tela = st.checkbox(
            '📺 Gravar Tela', value=False,
            help='Captura uma janela ou a tela inteira do seu computador',
        )
    with col_c2:
        capturar_webcam = st.checkbox(
            '📸 Gravar Webcam', value=False,
            help='Captura a sua imagem via câmera',
        )

    res_w, res_h = 1280, 720
    if capturar_webcam and not capturar_tela:
        opcao_res = st.selectbox(
            'Resolução da Webcam',
            ['720p — recomendado (menor carga de CPU)', '1080p — alta definição'],
        )
        if '1080p' in opcao_res:
            res_w, res_h = 1920, 1080

    if capturar_tela:
        st.info('💡 A tela será capturada automaticamente ao iniciar a gravação.')

    video_constraint = (
        {'width': {'ideal': res_w, 'max': res_w},
         'height': {'ideal': res_h, 'max': res_h},
         'frameRate': {'ideal': 30, 'max': 30}}
        if capturar_webcam and not capturar_tela
        else False
    )

    # ── Botão de gravação ────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;margin:32px 0 4px">
  <span style="display:inline-block;width:48px;height:1px;
               background:linear-gradient(to right,transparent,#cbd5e0);
               vertical-align:middle;margin-right:12px"></span>
  <span style="font-size:10px;letter-spacing:4px;text-transform:uppercase;
               color:#a0aec0;vertical-align:middle">gravador</span>
  <span style="display:inline-block;width:48px;height:1px;
               background:linear-gradient(to left,transparent,#cbd5e0);
               vertical-align:middle;margin-left:12px"></span>
</div>
""", unsafe_allow_html=True)

    fonte_audio = st.session_state.get('fonte_audio', FONTE_MIC)
    webrtc_key = f'recebe_audio_{fonte_audio.replace(" ", "_").replace("+", "")}'

    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        webrtx_ctx = webrtc_streamer(
            key=webrtc_key,
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=1024,
            video_receiver_size=1024,
            media_stream_constraints={
                'video': video_constraint,
                'audio': True,
            },
        )

    st.markdown(_RECORDER_BTN_JS, unsafe_allow_html=True)

    if not webrtx_ctx.state.playing:
        return

    # ── Setup de captura ─────────────────────────────────────────────────────
    container_video = None
    vstream = None
    astream = None
    v_start_time = None
    a_start_time = None
    v_last_pts = -1
    screen_recorder = None
    capture_sistema = None
    mixer = None

    pasta_reuniao = PASTA_ARQUIVOS / datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    pasta_reuniao.mkdir(parents=True, exist_ok=True)

    if titulo_reuniao.strip():
        salva_arquivo(pasta_reuniao / 'titulo.txt', titulo_reuniao.strip())

    if capturar_tela or capturar_webcam:
        video_path = (pasta_reuniao / 'reuniao.mp4').as_posix()
        container_video = av.open(video_path, mode='w')

    if capturar_tela:
        screen_recorder = ScreenRecorder(fps=15)
        screen_recorder.start()

    device_sistema = st.session_state.get('device_sistema')

    # ── Inicializa captura de áudio conforme fonte selecionada ───────────────
    if fonte_audio in (FONTE_SISTEMA, FONTE_MISTO) and device_sistema:
        capture_sistema = SystemAudioCapture(device_sistema)
        capture_sistema.start()

    if fonte_audio == FONTE_MISTO:
        mixer = MixedAudioCapture(chunk_duration_s=5)

    indicador_container = st.empty()
    transcricao_container = st.empty()

    inicio_gravacao = time.time()
    ultimo_segundo = -1
    ultima_transcricao = time.time()
    audio_chunck = pydub.AudioSegment.empty()
    audio_parts: list[Path] = []
    transcricao = ''
    audio_offset_seg = 0.0

    def _transcrever_e_salvar(chunk: pydub.AudioSegment) -> str:
        """Exporta chunk, transcreve com offset absoluto e salva — reutilizado pelos 3 modos."""
        nonlocal transcricao, ultima_transcricao, audio_offset_seg
        chunk_duration_seg = len(chunk) / 1000.0
        part_path = pasta_reuniao / f'audio_part_{len(audio_parts):04d}.mp3'
        chunk.export(part_path, format='mp3')
        audio_parts.append(part_path)
        chunk.export(pasta_reuniao / 'audio_temp.mp3', format='mp3')
        try:
            trecho = transcreve_audio(pasta_reuniao / 'audio_temp.mp3', offset_seg=audio_offset_seg)
            transcricao = (transcricao + '\n' + trecho).strip()
            modelo_whisper = st.session_state.get('modelo_whisper', 'base')
            nota = f'\n\n---\n*Transcrição: Faster-Whisper ({modelo_whisper})*'
            salva_arquivo(pasta_reuniao / 'transcricao.txt', transcricao + nota)
            transcricao_container.markdown(transcricao)
        except Exception as e:
            st.error(f'Erro na transcrição: {e}')
        audio_offset_seg += chunk_duration_seg
        ultima_transcricao = time.time()
        return transcricao

    try:
        while webrtx_ctx.state.playing:
            elapsed = int(time.time() - inicio_gravacao)
            if elapsed != ultimo_segundo:
                ultimo_segundo = elapsed
                _indicador_gravando(indicador_container, elapsed)

            # ── MODO: Microfone (WebRTC) ──────────────────────────────────
            if fonte_audio == FONTE_MIC and webrtx_ctx.audio_receiver:
                try:
                    frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)
                except queue.Empty:
                    time.sleep(0.1)
                    continue

                audio_chunck = adiciona_chunck_audio(frames_de_audio, audio_chunck)
                astream, a_start_time = processa_audio_container(
                    container_video, frames_de_audio, astream, a_start_time,
                )

                if len(audio_chunck) > 0 and time.time() - ultima_transcricao > 5:
                    _transcrever_e_salvar(audio_chunck)
                    audio_chunck = pydub.AudioSegment.empty()

            # ── MODO: Áudio do Sistema (WASAPI) ───────────────────────────
            elif fonte_audio == FONTE_SISTEMA and capture_sistema:
                chunk = capture_sistema.get_chunk()
                if chunk:
                    _transcrever_e_salvar(chunk)
                else:
                    time.sleep(0.1)

            # ── MODO: Microfone + Sistema (MixedAudioCapture) ─────────────
            elif fonte_audio == FONTE_MISTO and mixer:
                # Alimenta o mixer com frames do microfone
                if webrtx_ctx.audio_receiver:
                    try:
                        frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)
                        mixer.add_mic_frames(frames_de_audio)
                    except queue.Empty:
                        pass

                # Alimenta o mixer com chunks do sistema
                if capture_sistema:
                    sys_chunk = capture_sistema.get_chunk()
                    if sys_chunk:
                        mixer.add_system_chunk(sys_chunk)

                # Consome chunks mesclados prontos
                mixed_chunk = mixer.get_chunk()
                if mixed_chunk:
                    _transcrever_e_salvar(mixed_chunk)
                else:
                    time.sleep(0.05)

            # ── VÍDEO: Webcam (WebRTC) ────────────────────────────────────
            if capturar_webcam and not capturar_tela and webrtx_ctx.video_receiver:
                try:
                    frames_de_video = webrtx_ctx.video_receiver.get_frames(timeout=1)
                    vstream, v_start_time, v_last_pts = processa_video_container(
                        container_video, frames_de_video, vstream, v_start_time, v_last_pts,
                    )
                except queue.Empty:
                    pass
                except Exception as e:
                    st.warning(f'Erro ao processar vídeo: {e}')

            # ── VÍDEO: Tela (MSS) ─────────────────────────────────────────
            if capturar_tela and screen_recorder:
                mss_frames = []
                while True:
                    try:
                        bgr, capture_time = screen_recorder.frame_queue.get_nowait()
                        mss_frames.append(bgr_para_av_frame(bgr, capture_time))
                    except queue.Empty:
                        break
                if mss_frames:
                    try:
                        vstream, v_start_time, v_last_pts = processa_video_container(
                            container_video, mss_frames, vstream, v_start_time, v_last_pts,
                        )
                    except Exception as e:
                        st.warning(f'Erro ao processar tela: {e}')

    finally:
        # ── Flush do microfone (modo MIC) ─────────────────────────────────
        if fonte_audio == FONTE_MIC and len(audio_chunck) > 0:
            part_path = pasta_reuniao / f'audio_part_{len(audio_parts):04d}.mp3'
            audio_chunck.export(part_path, format='mp3')
            audio_parts.append(part_path)

        # ── Flush do mixer (modo MISTO) ───────────────────────────────────
        if mixer:
            remaining = mixer.flush_remaining()
            if remaining:
                part_path = pasta_reuniao / f'audio_part_{len(audio_parts):04d}.mp3'
                remaining.export(part_path, format='mp3')
                audio_parts.append(part_path)

        # ── Para SystemAudioCapture e drena chunks restantes ──────────────
        if capture_sistema:
            capture_sistema.stop()
            while True:
                chunk = capture_sistema.get_chunk()
                if chunk is None:
                    break
                if fonte_audio == FONTE_SISTEMA:
                    part_path = pasta_reuniao / f'audio_part_{len(audio_parts):04d}.mp3'
                    chunk.export(part_path, format='mp3')
                    audio_parts.append(part_path)

        if audio_parts:
            _merge_audio_parts(audio_parts, pasta_reuniao / 'audio.mp3')

        # ── Para MSS e drena frames restantes ────────────────────────────
        if screen_recorder:
            screen_recorder.stop()
            if container_video:
                mss_frames = []
                while True:
                    try:
                        bgr, capture_time = screen_recorder.frame_queue.get_nowait()
                        mss_frames.append(bgr_para_av_frame(bgr, capture_time))
                    except queue.Empty:
                        break
                if mss_frames:
                    try:
                        vstream, v_start_time, v_last_pts = processa_video_container(
                            container_video, mss_frames, vstream, v_start_time, v_last_pts,
                        )
                    except Exception:
                        pass

        flush_container(container_video, vstream, astream)

        if container_video:
            video_path = pasta_reuniao / 'reuniao.mp4'
            audio_path = pasta_reuniao / 'audio.mp3'
            # Modos que gravam áudio separado do container: SISTEMA e MISTO
            if fonte_audio in (FONTE_SISTEMA, FONTE_MISTO) and audio_path.exists():
                ok = _muxar_audio_no_video(video_path, audio_path)
                if not ok:
                    st.warning('Não foi possível combinar vídeo e áudio.')
            else:
                ok = _optimize_video_for_web(video_path)
                if not ok:
                    st.warning('Não foi possível otimizar o vídeo para reprodução web.')

        indicador_container.empty()
        st.session_state['ir_para_historico'] = True


# ── TAB SELEÇÃO REUNIÃO ───────────────────────────────────────────────────────

def tab_selecao_reuniao():
    reunioes_dict = listar_reunioes()
    if not reunioes_dict:
        st.info('Nenhuma reunião gravada ainda.')
        return

    reuniao_data = st.selectbox(
        'Selecione uma reunião',
        options=list(reunioes_dict.keys()),
        format_func=lambda k: reunioes_dict[k],
    )
    st.divider()
    pasta_reuniao = PASTA_ARQUIVOS / reuniao_data

    titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
    transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
    resumo = le_arquivo(pasta_reuniao / 'resumo.txt')

    if titulo:
        st.markdown(f'### {titulo}')
    else:
        st.warning('Esta reunião não tem título.')
        novo_titulo = st.text_input('Adicionar título', key='titulo_historico')
        if st.button('Salvar Título') and novo_titulo.strip():
            salva_arquivo(pasta_reuniao / 'titulo.txt', novo_titulo.strip())
            st.rerun()

    video_file = pasta_reuniao / 'reuniao.mp4'
    if video_file.exists():
        st.video(str(video_file))
    else:
        audio_file = pasta_reuniao / 'audio.mp3'
        if audio_file.exists():
            st.audio(str(audio_file))

    # ── Refazer Transcrição ──────────────────────────────────────────────────
    audio_file = pasta_reuniao / 'audio.mp3'
    if audio_file.exists():
        with st.expander('🔄 Refazer Transcrição'):
            TEMPOS_ESTIMADOS = {
                'tiny':   '~10 min para 20 min de áudio (qualidade ruim)',
                'base':   '~16 min para 20 min de áudio (qualidade aceitável)',
                'small':  '~30-40 min para 20 min de áudio (boa qualidade) ⭐',
                'medium': '~80+ min para 20 min de áudio (muito boa qualidade, lento)',
            }
            modelo_escolhido = st.selectbox(
                'Modelo Whisper',
                options=['tiny', 'base', 'small', 'medium'],
                index=2,  # small como padrão
                key='modelo_whisper_retranscrever',
            )
            st.caption(f'⏱️ {TEMPOS_ESTIMADOS[modelo_escolhido]}')

            if st.button('🔄 Refazer Transcrição', type='primary'):
                with st.spinner(f'Transcrevendo com modelo {modelo_escolhido}...'):
                    retranscrever_reuniao(pasta_reuniao, modelo_escolhido)
                st.rerun()

    if not transcricao:
        st.warning('Nenhuma transcrição disponível para gerar resumo.')
    else:
        if resumo:
            st.info(resumo)
        col_gerar, col_refazer = st.columns([2, 1])
        with col_gerar if not resumo else col_refazer:
            label = '✨ Gerar Resumo Inteligente' if not resumo else '🔄 Refazer Resumo'
            if st.button(label):
                with st.spinner('Analisando transcrição...'):
                    gerar_resumo(pasta_reuniao)
                    st.rerun()

    with st.expander('📝 Ver transcrição completa'):
        st.write(transcricao)


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title='Projeto-Gravando', page_icon='🎙️')
    st.header('Projeto-Gravando 🎙️', divider='rainbow')

    if st.session_state.pop('ir_para_historico', False):
        st.markdown("""
<script>
(function () {
    var attempts = 0;
    var iv = setInterval(function () {
        var tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
        if (tabs.length >= 2) { tabs[1].click(); clearInterval(iv); }
        else if (++attempts > 20) { clearInterval(iv); }
    }, 150);
})();
</script>
""", unsafe_allow_html=True)

    # ── Sidebar de configurações ─────────────────────────────────────────────
    with st.sidebar:
        st.title('🤖 Configurações de IA')
        st.session_state['provedor'] = st.selectbox(
            'Provedor de Resumo',
            ['Ollama (Local)', 'OpenAI'],
        )

        if st.session_state['provedor'] == 'Ollama (Local)':
            modelos_ollama = listar_modelos_ollama()
            if modelos_ollama:
                st.session_state['modelo_ollama'] = st.selectbox(
                    'Selecione o Modelo Local',
                    modelos_ollama,
                    index=0,
                )
                st.success('Ollama Ativado')
            else:
                st.error('Ollama não detectado. Certifique-se de que ele está rodando.')
        else:
            st.warning('Usando API da OpenAI (Nuvem)')

        st.divider()
        st.subheader('🎙️ Transcrição')
        st.session_state['modelo_whisper'] = st.selectbox(
            'Modelo Whisper',
            MODELOS_WHISPER,
            index=MODELOS_WHISPER.index('base'),
            help='tiny < base < small < medium — modelos maiores são mais precisos mas mais lentos',
        )

        st.divider()
        st.subheader('🔊 Fonte de Áudio')
        st.session_state['fonte_audio'] = st.radio(
            'Fonte de áudio',
            [FONTE_MIC, FONTE_SISTEMA, FONTE_MISTO],
            help=(
                f'**{FONTE_MIC}**: capta sua voz via navegador.\n\n'
                f'**{FONTE_SISTEMA}**: capta tudo que sai pela caixa de som (WASAPI).\n\n'
                f'**{FONTE_MISTO}**: capta microfone E sistema simultaneamente e mescla antes de transcrever.'
            ),
        )

        if st.session_state['fonte_audio'] in (FONTE_SISTEMA, FONTE_MISTO):
            dispositivos = listar_dispositivos_loopback()
            if dispositivos:
                nomes = [d['nome'] for d in dispositivos]
                idx = st.selectbox(
                    'Dispositivo de saída (WASAPI)',
                    range(len(nomes)),
                    format_func=lambda i: nomes[i],
                )
                st.session_state['device_sistema'] = dispositivos[idx]
            else:
                st.error('Nenhum dispositivo WASAPI Loopback encontrado.')
                st.session_state['device_sistema'] = None

        st.divider()
        st.subheader('🔍 Status do Sistema')
        modelo_atual = st.session_state.get('modelo_whisper', 'base')
        st.caption(f'🎙️ Whisper: **{modelo_atual} (Local)**')

    tab_gravar, tab_selecao = st.tabs(['🔴 Gravar Reunião', '📂 Histórico'])

    with tab_gravar:
        modo = st.radio(
            'Modo',
            ['🔴 Gravar ao vivo', '📤 Importar arquivo'],
            horizontal=True,
            label_visibility='collapsed',
        )
        st.divider()
        if modo == '🔴 Gravar ao vivo':
            tab_grava_reuniao()
        else:
            tab_importar_audio()

    with tab_selecao:
        tab_selecao_reuniao()


if __name__ == '__main__':
    main()
