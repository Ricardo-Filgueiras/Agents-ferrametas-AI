import streamlit as st
import pandas as pd
import sys
import os
from dotenv import load_dotenv

load_dotenv()

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

# Abas principais
tab_ler, tab_criar = st.tabs(["📖 Ler Artigos", "✨ Criar Novo Artigo"])

with tab_criar:
    st.header("Gerar Novo Artigo")
    st.markdown("Preencha os dados abaixo para iniciar a geração do artigo com os agentes.")
    tema_input = st.text_input("Tema", placeholder="Ex: Finanças Pessoais: Guia Definitivo...")
    keywords_input = st.text_input("Palavras-chave (separadas por vírgula)", placeholder="Finanças, Iniciantes, Dicas")
    
    if st.button("🚀 Iniciar Geração em Background", type="primary"):
        if not tema_input or not keywords_input:
            st.warning("Por favor, preencha o tema e as palavras-chave.")
        else:
            kws = [k.strip() for k in keywords_input.split(",") if k.strip()]
            from src.main import run_blog_pipeline
            import threading
            # Inicia o pipeline em uma thread separada para não bloquear a interface
            t = threading.Thread(target=run_blog_pipeline, args=(tema_input, kws))
            t.start()
            st.success("✅ O processo foi iniciado em background! Você pode ler outros artigos enquanto a equipe trabalha. Os logs de execução aparecerão no terminal em que o Streamlit está rodando.")

with tab_ler:
    # Sidebar para seleção de artigos
    articles = load_articles()
    if not articles:
        st.warning("Nenhum artigo encontrado no banco de dados. Crie um novo artigo na aba 'Criar Novo Artigo'!")
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
            default_webhook = os.getenv("WEBHOOK_N8N_POST_ART", "")
            webhook_url = st.text_input("Webhook URL (n8n)", value=default_webhook, placeholder="https://seu-n8n.com/webhook/...")
            is_public = st.checkbox("Tornar artigo público? (is_public)", value=False)
            
            if st.button("🚀 Enviar para n8n", use_container_width=True):
                if not webhook_url:
                    st.error("Por favor, insira a URL do Webhook.")
                else:
                    # Monta o pacote estruturado para o n8n (Blindagem contra campos vazios)
                    payload = {
                        "id": article.id,
                        "topic": article.topic,
                        "keywords": article.keywords if isinstance(article.keywords, list) else [],
                        "title": article.title or article.topic,
                        "category": article.category or "Geral",
                        "tags": article.tags if isinstance(article.tags, list) else [],
                        "meta_title": article.meta_title or "",
                        "meta_description": article.meta_description or "",
                        "excerpt": article.excerpt or "",
                        "outline": article.outline if isinstance(article.outline, list) else [],
                        "content_markdown": article.content_markdown or "",
                        "is_public": is_public,
                        "seo_score": article.seo_score or 0,
                        "image_prompts": article.image_prompts if isinstance(article.image_prompts, list) else [],
                        "created_at": article.created_at.isoformat() if article.created_at else None
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
            st.metric("SEO Score", f"{getattr(article, 'seo_score', 0)}/10")
            st.metric("Revisões", getattr(article, 'iteration_count', 0))
            
            status = "✅ Validado" if getattr(article, 'is_validated', False) else "⚠️ Pendente"
            st.info(f"Status: {status}")

            st.subheader("🎨 Image Prompts")
            for i, prompt in enumerate(getattr(article, 'image_prompts', []) or []):
                st.code(prompt, language="markdown")

            st.subheader("🕒 Logs de Execução")
            if getattr(article, 'execution_logs', None):
                df_logs = pd.DataFrame(article.execution_logs)
                st.dataframe(df_logs)

session.close()
