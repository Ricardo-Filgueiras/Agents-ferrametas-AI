import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Agno Chat PDF", page_icon="📄", layout="centered")
agent_id = "agent_os_fast"
# URL da sua API (Removida a barra no final)
API_URL = f"http://127.0.0.1:8000/agents/{agent_id}/runs"

def stream_response(user_query):
    """Gera a resposta do agente palavra por palavra vinda da API"""
    try:
        # Faz a requisição POST para a API com streaming habilitado usando Form Data
        with requests.post(
            API_URL,
            data={"message": user_query, "stream": "true"}, # O AgentOS exige Form Data e não JSON
            stream=True
        ) as response:
            response.raise_for_status()
            
            # O AgentOS retorna eventos SSE (Server-Sent Events), geralmente no formato "data: ..."
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    # Tenta limpar o prefixo "data: " se existir, ou apenas retorna a linha
                    if decoded_line.startswith("data: "):
                        yield decoded_line.replace("data: ", "")
                    elif not decoded_line.startswith("event: "): # Ignora as linhas de controle
                        yield decoded_line
    except Exception as e:
        yield f"❌ Erro ao conectar com a API: {str(e)}"

# Interface Streamlit
st.title("📄 Consulta de Pedidos (Agno)")
st.info("Digite sua pergunta sobre os pedidos contidos no PDF.")

# Histórico de chat simples (opcional, para visualização)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input do usuário
if user_input := st.chat_input("Ex: Qual o valor total do pedido 2644114?"):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Exibe a pergunta do usuário
    with st.chat_message("user"):
        st.markdown(user_input)

    # Exibe a resposta do assistente em streaming
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = st.write_stream(stream_response(user_input))
        
    # Adiciona a resposta final ao histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
