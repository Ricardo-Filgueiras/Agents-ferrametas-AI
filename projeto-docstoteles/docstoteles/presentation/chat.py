import os
import streamlit as st
from service.rag import RAGService

def show():
    st.header("💬 Chat com Documentação")
    
    if "collection" not in st.session_state or not st.session_state.collection:
        st.warning("Selecione uma coleção na barra lateral para começar.")
        return
    
    rag = RAGService()
    loaded = rag.load_collection(st.session_state.collection)
    if not loaded:
        st.error("Não foi possível carregar a coleção selecionada.")
        return
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    question = st.text_input("Pergunte algo sobre a documentação:")
    if st.button("Enviar") and question:
        with st.spinner("Consultando IA..."):
            answer = rag.ask_question(question)
            st.session_state.messages.append((question, answer))
    
    st.divider()
    st.subheader("Histórico")
    for q, a in st.session_state.messages[::-1]:
        st.markdown(f"**Você:** {q}")
        st.markdown(f"**Docstóteles:** {a}") 