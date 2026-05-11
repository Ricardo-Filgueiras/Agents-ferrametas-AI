import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS
from pathlib import Path
from agno.skills import  Skills , LocalSkills 


# Configuração da página Streamlit
st.set_page_config(
    page_title="Agno Local Agent Hub",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agno Local Agent Hub")
st.markdown("### Foco em Economia: Modelos Locais via Ollama")

# Inicialização do Agente (usando Ollama para economizar tokens)
@st.cache_resource
def get_agent():
    return Agent(
        model=Ollama(id="llama3.2:3b"),
        skills=Skills(
            loaders=[LocalSkills(path=str(Path(__file__).parent.parent / "skills"))],
        ),
        instructions=[
            "Você é um assistente de IA focado em eficiência e produtividade.",
            "Responda sempre em Português do Brasil.",
            "Sempre que possível, sugira formas de automatizar tarefas para economizar tempo ou dinheiro.",
            "Como você roda localmente, lembre o usuário que o custo de tokens é zero!"
        ],
        markdown=True,
    )

agent = get_agent()

# Interface de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Usuário
if prompt := st.chat_input("Como posso te ajudar a economizar hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Usando print_response mas capturando o retorno para o Streamlit
        # Agno Agent.run() retorna um objeto que contém a resposta
        response_container = st.empty()
        full_response = ""
        
        # Simulando streaming ou apenas pegando a resposta
        # Nota: O Agno tem suporte nativo a streaming, vamos usar o run(stream=True)
        response_gen = agent.run(prompt, stream=True)
        
        for chunk in response_gen:
            if hasattr(chunk, 'content'):
                full_response += chunk.content
                response_container.markdown(full_response + "▌")
        
        response_container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
