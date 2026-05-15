import streamlit as st
import pandas as pd
import sys
import os

import requests

# Garante que o Python encontre a pasta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Article

# Configuração da Página
st.set_page_config(page_title="Lean Blog Engine - Dashboard", layout="wide")

# Conexão com o Banco
engine = create_engine("sqlite:///data/blog_engine.db")
Session = sessionmaker(bind=engine)
session = Session()

def load_articles():
    return session.query(Article).order_by(Article.created_at.desc()).all()

st.title("🚀 Lean Blog Engine")
st.markdown("Equipe Multi-Agente de Elite para Conteúdo Orgânico")

# Sidebar para seleção de artigos
articles = load_articles()
if not articles:
    st.warning("Nenhum artigo encontrado no banco de dados. Rode o pipeline primeiro!")
else:
    article_titles = [f"{a.id} - {a.topic}" for a in articles]
    selected_option = st.sidebar.selectbox("Selecione um Artigo", article_titles)
    selected_id = int(selected_option.split(" - ")[0])
    
    # Busca o artigo selecionado
    article = session.query(Article).filter(Article.id == selected_id).first()

    # Layout Principal
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"📝 {getattr(article, 'title', article.topic)}")
        st.caption(f"Tópico: {article.topic} | Categoria: {getattr(article, 'category', 'Geral')} | Tags: {', '.join(getattr(article, 'tags', []) or [])}")
        
        st.markdown("---")
        st.markdown(article.content_markdown)

    with col2:
        st.subheader("🌐 Publicação via n8n")
        webhook_url = st.text_input("Webhook URL (n8n)", value="", placeholder="https://seu-n8n.com/webhook/...")
        is_public = st.checkbox("Tornar artigo público? (is_public)", value=False)
        
        if st.button("🚀 Enviar para n8n", use_container_width=True):
            if not webhook_url:
                st.error("Por favor, insira a URL do Webhook.")
            else:
                # Monta o pacote estruturado para o n8n
                payload = {
                    "id": article.id,
                    "title": getattr(article, "title", article.topic),
                    "category": getattr(article, "category", "Geral"),
                    "tags": getattr(article, "tags", []),
                    "meta_title": getattr(article, "meta_title", ""),
                    "meta_description": getattr(article, "meta_description", ""),
                    "excerpt": getattr(article, "excerpt", ""),
                    "content_markdown": article.content_markdown,
                    "is_public": is_public,
                    "seo_score": article.seo_score
                }
                
                try:
                    with st.spinner("Enviando para o n8n..."):
                        response = requests.post(webhook_url, json=payload)
                        response.raise_for_status()
                    st.success("✅ Publicado no n8n com sucesso!")
                except Exception as e:
                    st.error(f"❌ Erro ao enviar: {str(e)}")
                    
        st.markdown("---")
        st.subheader("📊 Metadados & SEO")
        st.metric("SEO Score", f"{article.seo_score}/10")
        st.metric("Revisões", article.iteration_count)
        
        status = "✅ Validado" if article.is_validated else "⚠️ Pendente"
        st.info(f"Status: {status}")

        st.subheader("🎨 Image Prompts")
        for i, prompt in enumerate(article.image_prompts):
            st.code(prompt, language="markdown")

        st.subheader("🕒 Logs de Execução")
        if article.execution_logs:
            df_logs = pd.DataFrame(article.execution_logs)
            st.dataframe(df_logs)

session.close()
