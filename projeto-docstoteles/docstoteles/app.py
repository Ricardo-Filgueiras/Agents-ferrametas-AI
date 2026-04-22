import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Garantir que o diretório atual está no path para as importações funcionarem
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from presentation import scraping
from presentation import chat

load_dotenv()

st.set_page_config(page_title="Docstóteles", page_icon="📚", layout="wide")
st.title("📚 Docstóteles - RAG Simples")

# Sidebar para seleção
with st.sidebar:
    st.header("Coleções")
    mode = st.radio("Modo:", ["Chat", "Scraping"])
    
    st.divider()
    st.subheader("Coleções Disponíveis")
    
    collections_dir = "data/collections"
    if os.path.exists(collections_dir):
        collections = [d for d in os.listdir(collections_dir) 
                      if os.path.isdir(os.path.join(collections_dir, d))]
        
        for collection in collections:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📁 {collection}")
            with col2:
                if st.button("Usar", key=f"use_{collection}"):
                    st.session_state.collection = collection
                    st.rerun()

# Estados de sessão
if "messages" not in st.session_state:
    st.session_state.messages = []
if "collection" not in st.session_state:
    st.session_state.collection = None

# Importar páginas
if mode == "Scraping":
    scraping.show()
else:
    chat.show() 