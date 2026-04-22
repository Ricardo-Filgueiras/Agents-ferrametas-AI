from pathlib import Path
from datetime import datetime
import time
import queue
import requests

from streamlit_webrtc import WebRtcMode, webrtc_streamer
import streamlit as st

import pydub
import openai
import av
from faster_whisper import WhisperModel
from dotenv import load_dotenv, find_dotenv

# Configuração de Caminhos
PASTA_ARQUIVOS = Path(__file__).parent.parent.parent / 'data'
PASTA_ARQUIVOS.mkdir(exist_ok=True)

PROMPT = '''
Faça o resumo do texto delimitado por #### 
O texto é a transcrição de uma reunião.
O resumo deve contar com os principais assuntos abordados.
O resumo deve ter no máximo 300 caracteres.
O resumo deve estar em texto corrido.
No final, devem ser apresentados todos acordos e combinados 
feitos na reunião no formato de bullet points.

O formato final que eu desejo é:

Resumo reunião:
- escrever aqui o resumo.

Acordos da Reunião:
- acordo 1
- acordo 2
- acordo 3
- acordo n

texto: ####{}####
'''

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

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

# CONFIGURAÇÃO DOS CLIENTES =====================
client = openai.OpenAI()
client_local = openai.OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

# CONFIGURAÇÃO DOS MODELOS LOCAIS =====================
# Inicializamos o Whisper local (modelo 'base' é um bom equilíbrio entre velocidade e precisão)
@st.cache_resource
def carregar_whisper():
    return WhisperModel("base", device="cpu", compute_type="int8")

whisper_local = carregar_whisper()

def transcreve_audio(caminho_audio):
    segments, info = whisper_local.transcribe(str(caminho_audio), beam_size=5, language='pt')
    texto = " ".join([segment.text for segment in segments])
    return texto

def chat_openai(mensagem, modelo_default='gpt-4o-mini'):
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

# TAB GRAVA REUNIÃO =====================

def adiciona_chunck_audio(frames_de_audio, audio_chunck):
    for frame in frames_de_audio:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels),
        )
        audio_chunck += sound
    return audio_chunck

def tab_grava_reuniao():
    st.info("Dica: Ao iniciar, selecione 'Janela' ou 'Tela Cheia' no navegador para capturar a tela.")
    capturar_tela = st.checkbox('Gravar Tela (Vídeo)?', value=False)
    
    webrtx_ctx = webrtc_streamer(
        key='recebe_audio',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={'video': capturar_tela, 'audio': True},
    )

    if not webrtx_ctx.state.playing:
        return

    container_video = None
    vstream = None
    astream = None
    
    pasta_reuniao = PASTA_ARQUIVOS / datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    pasta_reuniao.mkdir(parents=True, exist_ok=True)
    
    if capturar_tela:
        video_path = str(pasta_reuniao / 'reuniao.mp4')
        container_video = av.open(video_path, mode='w')
        # Streams serão configurados ao receber o primeiro frame
    
    status_container = st.empty()
    status_container.markdown('🎙️ Gravando...')
    
    transcricao_container = st.empty()

    ultima_trancricao = time.time()
    audio_completo = pydub.AudioSegment.empty()
    audio_chunck = pydub.AudioSegment.empty()
    transcricao = ''

    try:
        while webrtx_ctx.state.playing:
            # PROCESSAMENTO DE ÁUDIO
            if webrtx_ctx.audio_receiver:
                try:
                    frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)
                except queue.Empty:
                    time.sleep(0.1)
                    continue
                
                audio_completo = adiciona_chunck_audio(frames_de_audio, audio_completo)
                audio_chunck = adiciona_chunck_audio(frames_de_audio, audio_chunck)
                
                # Gravação de Áudio para o MP4 (se vídeo ativo)
                if container_video and frames_de_audio:
                    if astream is None:
                        astream = container_video.add_stream('aac')
                    for frame in frames_de_audio:
                        for packet in astream.encode(frame):
                            container_video.mux(packet)
                
                if len(audio_chunck) > 0:
                    audio_completo.export(pasta_reuniao / 'audio.mp3')
                    agora = time.time()
                    if agora - ultima_trancricao > 5:
                        ultima_trancricao = agora
                        audio_chunck.export(pasta_reuniao / 'audio_temp.mp3')
                        try:
                            transcricao_chunck = transcreve_audio(pasta_reuniao / 'audio_temp.mp3')
                            transcricao += f" {transcricao_chunck}"
                            
                            # Adiciona nota do modelo no final da transcrição
                            nota_modelo = "\n\n---\n*Transcrição realizada pelo modelo: Faster-Whisper (Base)*"
                            salva_arquivo(pasta_reuniao / 'transcricao.txt', transcricao + nota_modelo)
                            
                            transcricao_container.markdown(transcricao)
                        except Exception as e:
                            st.error(f"Erro na transcrição: {e}")
                        audio_chunck = pydub.AudioSegment.empty()
            
            # PROCESSAMENTO DE VÍDEO
            if capturar_tela and webrtx_ctx.video_receiver:
                try:
                    frames_de_video = webrtx_ctx.video_receiver.get_frames(timeout=1)
                    for frame in frames_de_video:
                        if vstream is None:
                            vstream = container_video.add_stream('libx264', rate=30)
                            vstream.width = frame.width
                            vstream.height = frame.height
                            vstream.pix_fmt = 'yuv420p'
                        
                        for packet in vstream.encode(frame):
                            container_video.mux(packet)
                except queue.Empty:
                    pass
            
            if not webrtx_ctx.state.playing:
                break
    finally:
        # Fechar o container de vídeo adequadamente
        if container_video:
            if vstream:
                for packet in vstream.encode():
                    container_video.mux(packet)
            if astream:
                for packet in astream.encode():
                    container_video.mux(packet)
            container_video.close()
            status_container.success(f"Gravação salva em: {pasta_reuniao}")


# TAB SELEÇÃO REUNIÃO =====================
def tab_selecao_reuniao():
    reunioes_dict = listar_reunioes()
    if len(reunioes_dict) > 0:
        reuniao_selecionada = st.selectbox('Selecione uma reunião',
                                        list(reunioes_dict.values()))
        st.divider()
        reuniao_data = [k for k, v in reunioes_dict.items() if v == reuniao_selecionada][0]
        pasta_reuniao = PASTA_ARQUIVOS / reuniao_data
        
        if not (pasta_reuniao / 'titulo.txt').exists():
            st.warning('Adicione um título para esta reunião')
            titulo_reuniao = st.text_input('Título da reunião')
            if st.button('Salvar Título'):
                salvar_titulo(pasta_reuniao, titulo_reuniao)
                st.rerun()
        else:
            titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
            transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
            resumo = le_arquivo(pasta_reuniao / 'resumo.txt')
            
            st.markdown(f'### {titulo}')
            
            # Exibir Vídeo se existir
            video_file = pasta_reuniao / 'reuniao.mp4'
            if video_file.exists():
                st.video(str(video_file))
            else:
                # Exibir Áudio se não houver vídeo
                audio_file = pasta_reuniao / 'audio.mp3'
                if audio_file.exists():
                    st.audio(str(audio_file))
            
            if resumo == '':
                if st.button('✨ Gerar Resumo Inteligente'):
                    with st.spinner('Analisando transcrição...'):
                        gerar_resumo(pasta_reuniao)
                        st.rerun()
            else:
                st.info(resumo)
            
            with st.expander("📝 Ver transcrição completa"):
                st.write(transcricao)
        
def salvar_titulo(pasta_reuniao, titulo):
    salva_arquivo(pasta_reuniao / 'titulo.txt', titulo)

def gerar_resumo(pasta_reuniao):
    transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
    if transcricao == '':
        st.error('Não há transcrição para gerar resumo.')
        return
    provedor = st.session_state.get('provedor', 'OpenAI')
    resumo, modelo_utilizado = chat_openai(mensagem=PROMPT.format(transcricao))
    resumo += f'\n\n---\n*Resumo gerado pelo modelo: {modelo_utilizado} ({provedor})*'
    salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)


# MAIN =====================
def main():
    st.set_page_config(page_title="Projeto-Gravando", page_icon="🎙️")
    st.header('Projeto-Gravando 🎙️', divider='rainbow')
    
    # Seleção de Provedor na Barra Lateral
    with st.sidebar:
        st.title('🤖 Configurações de IA')
        st.session_state['provedor'] = st.selectbox(
            'Provedor de Resumo',
            ['Ollama (Local)', 'OpenAI']
        )
        
        if st.session_state['provedor'] == 'Ollama (Local)':
            modelos_ollama = listar_modelos_ollama()
            if modelos_ollama:
                st.session_state['modelo_ollama'] = st.selectbox(
                    'Selecione o Modelo Local',
                    modelos_ollama,
                    index=0
                )
                st.success(f'Ollama Ativado')
            else:
                st.error('Ollama não detectado. Certifique-se de que ele está rodando.')
                st.info('Caso tenha instalado agora, reinicie o app.')
        else:
            st.warning('Usando API da OpenAI (Nuvem)')
        
        st.divider()
        st.subheader('🔍 Status do Sistema')
        
        # Status do Whisper
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write('🎙️')
        with col2:
            st.caption('Whisper: **Pronto (Local)**')
        
        # Status do Ollama
        col3, col4 = st.columns([1, 4])
        with col3:
            if st.session_state.get('provedor') == 'Ollama (Local)':
                if listar_modelos_ollama():
                    st.write('🟢')
                else:
                    st.write('🔴')
            else:
                st.write('⚪')
        with col4:
            if st.session_state.get('provedor') == 'Ollama (Local)':
                st.caption('Ollama: **Ativo**' if listar_modelos_ollama() else 'Ollama: **Desconectado**')
            else:
                st.caption('Resumo: **OpenAI (Nuvem)**')

        st.caption('Transcrição: Faster-Whisper (Local)')
        st.caption('Modelo Transcrição: Base')

    tab_gravar, tab_selecao = st.tabs(['🔴 Gravar Reunião', '📂 Histórico'])
    
    with tab_gravar:
        tab_grava_reuniao()
        
    with tab_selecao:
        tab_selecao_reuniao()

if __name__ == '__main__':
    main()
