import os
import streamlit as st
from service.ragv2 import RAGServiceV2

@st.cache_resource
def get_rag_service(collection_name):
    """Cria e carrega a instância do RAGV2 com cache do Streamlit"""
    rag = RAGServiceV2()
    if rag.load_collection(collection_name):
        return rag
    return None

def show():
    st.header("💬 Chat com Documentação")
    
    if "collection" not in st.session_state or not st.session_state.collection:
        st.warning("Selecione uma coleção na barra lateral para começar.")
        return
    
    # Usar cache para não reprocessar a coleção em cada interação
    rag = get_rag_service(st.session_state.collection)
    
    if not rag:
        st.error("Não foi possível carregar a coleção selecionada. Verifique se há arquivos .md na pasta.")
        return
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibir histórico de mensagens usando o novo componente chat_message
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)
            
    # Input de chat moderno
    if prompt := st.chat_input("Pergunte algo sobre a documentação:"):
        # Adicionar mensagem do usuário
        st.session_state.messages.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Gerar resposta
        with st.chat_message("assistant"):
            with st.spinner("Docstóteles pensando..."):
                answer = rag.ask_question(prompt)
                st.markdown(answer)
                st.session_state.messages.append(("assistant", answer)) 