import streamlit as st
import pandas as pd
import sys
import os
import time
import requests
import re
import markdown
from dotenv import load_dotenv
from streamlit_ace import st_ace

load_dotenv()

# Garante que o Python encontre a pasta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.database.repository import ArticleRepository
from src.database.models import Article
from src.main import run_blog_pipeline, refine_article

def extract_markdown(text: str) -> str:
    """Extrai apenas o conteúdo markdown, removendo conversas ou blocos de código redundantes."""
    if not text: return ""
    
    # 1. Se o texto contém um bloco de código markdown ```markdown ... ```, pega apenas o conteúdo
    match = re.search(r'```markdown\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # 2. Se contém blocos genéricos ``` ... ```
    match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # 3. Se não tem blocos, mas tem ruído inicial (ex: "Ok, aqui está..."), tenta limpar
    # Se houver um cabeçalho Markdown (# ou ##), remove tudo antes dele
    header_match = re.search(r'(^|\n)(#+ .*)', text)
    if header_match:
        return text[header_match.start():].strip()
        
    return text.strip()

# --- HELPER DE ACESSO AO ESTADO ---
def get_state_content(obj, attr_name, default=""):
    """Extrai conteúdo de um objeto Pydantic ou de um dicionário de forma segura."""
    if obj is None: return default
    if isinstance(obj, dict):
        return obj.get(attr_name, default)
    return getattr(obj, attr_name, default)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Elite Blog Copilot", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO CUSTOMIZADA ---
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .article-preview {
        background-color: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 80vh;
        color: #333;
        line-height: 1.6;
    }
    .article-preview pre {
        background-color: #1e1e1e;
        color: #dcdcdc;
        padding: 20px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 20px 0;
        font-family: 'Consolas', 'Monaco', monospace;
    }
    .article-preview code {
        font-family: 'Consolas', 'Monaco', monospace;
        background-color: #f0f0f0;
        padding: 2px 4px;
        border-radius: 4px;
        color: #d63384;
    }
    .article-preview pre code {
        background-color: transparent;
        padding: 0;
        color: inherit;
    }
    .article-preview table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    .article-preview th, .article-preview td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    .article-preview th {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_article_id" not in st.session_state:
    st.session_state.current_article_id = None
if "draft_content" not in st.session_state:
    st.session_state.draft_content = ""
if "image_prompts" not in st.session_state:
    st.session_state.image_prompts = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

repo = ArticleRepository()

# --- SIDEBAR: HISTÓRICO E CONFIG ---
with st.sidebar:
    st.title("📚 Meus Artigos")
    
    with st.expander("⚙️ Configurações de IA", expanded=False):
        st.subheader("Modelos por Agente")
        ollama_models = ["ollama:llama3.2:3b", "ollama:gemma3:4b", "ollama:granite4.1:3b"]
        cloud_models = ["gemini", "openai:gpt-4o-mini"]
        planner_model = st.selectbox("Estrategista (Cloud)", cloud_models + ollama_models, index=0)
        writer_model = st.selectbox("Redator (Local/Escrita)", ollama_models + cloud_models, index=0)
        reviewer_model = st.selectbox("Revisor/Editor", ollama_models + cloud_models, index=0)
        model_config = {"planner": planner_model, "writer": writer_model, "reviewer": reviewer_model}

    try:
        session = repo.Session()
        articles = session.query(Article).order_by(Article.created_at.desc()).all()
        for art in articles:
            if st.button(f"📄 {art.title or art.topic[:30]}...", key=f"art_{art.id}", use_container_width=True):
                st.session_state.current_article_id = art.id
                st.session_state.draft_content = art.content_markdown
                st.session_state.image_prompts = art.image_prompts or []
                st.session_state.messages = art.chat_history or []
                st.rerun()
        session.close()
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
    
    st.divider()
    if st.button("➕ Novo Artigo", use_container_width=True):
        st.session_state.current_article_id = None
        st.session_state.draft_content = ""
        st.session_state.image_prompts = []
        st.session_state.messages = []
        st.rerun()

# --- LAYOUT PRINCIPAL ---
col_chat, col_display = st.columns([0.4, 0.6], gap="large")

with col_chat:
    st.subheader("💬 Copilot Interface")
    chat_container = st.container(height=500)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    if prompt := st.chat_input("Diga o tema do artigo...", disabled=st.session_state.is_processing):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                st.session_state.is_processing = True
                with st.status("🚀 Iniciando motor de elite...", expanded=True) as status:
                    if not st.session_state.current_article_id:
                        kws = [k.strip() for k in prompt.split()[:3]]
                        pipeline = run_blog_pipeline(prompt, kws, model_config=model_config)
                    else:
                        pipeline = refine_article(st.session_state.current_article_id, prompt, model_config=model_config)
                    
                    for step_name, state in pipeline:
                        if step_name == "planning":
                            st.write("✅ SEO Planning concluído.")
                            status.update(label="✍️ Redigindo conteúdo técnico...", state="running")
                        elif step_name == "writing":
                            st.write("✅ Rascunho inicial gerado.")
                            status.update(label="🧐 Revisando qualidade editorial...", state="running")
                        elif step_name == "editing":
                            st.write("✅ Revisão concluída.")
                            status.update(label="🎨 Criando prompts de design...", state="running")
                        elif step_name == "refinement":
                            st.write("✅ Texto refinado com sucesso.")
                        elif step_name == "design":
                            st.write("✅ Prompts visuais prontos.")
                        elif step_name == "validation":
                            st.write("✅ Validação SEO finalizada.")
                        elif step_name == "saved":
                            art_id, final_state = state
                            st.session_state.current_article_id = art_id
                            st.session_state.draft_content = get_state_content(final_state.get("draft"), "markdown_content", "")
                            st.session_state.image_prompts = get_state_content(final_state.get("design"), "image_prompts", [])
                            status.update(label="✅ Artigo pronto e salvo!", state="complete", expanded=False)
                
                response_text = "Seu artigo está pronto! Veja ao lado. Posso ajustar algo?"
                if st.session_state.current_article_id:
                     repo.update_article_chat(st.session_state.current_article_id, st.session_state.messages, {})
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.session_state.is_processing = False
                st.rerun()

with col_display:
    st.subheader("📄 Workspace")
    if not st.session_state.draft_content:
        st.info("Aguardando comando...")
    else:
        tab_preview, tab_editor, tab_prompts, tab_publish = st.tabs(["📖 Preview", "📝 Editor", "🎨 Prompts", "🌐 Publicar"])
        with tab_preview:
            clean_md = extract_markdown(st.session_state.draft_content)
            html_content = markdown.markdown(clean_md, extensions=['tables', 'fenced_code'])
            st.markdown(f'<div class="article-preview">{html_content}</div>', unsafe_allow_html=True)
        with tab_editor:
            edited_content = st_ace(value=st.session_state.draft_content, language="markdown", theme="github", key="editor", min_lines=30, auto_update=True)
            if edited_content != st.session_state.draft_content:
                st.session_state.draft_content = edited_content
            
            selection = st.session_state.get("editor-selection", None)
            if selection and selection.strip():
                st.info(f"Trecho: {selection[:50]}...")
                with st.popover("🎨 Refinar Seleção"):
                    instruction = st.text_input("Como melhorar?")
                    if st.button("Executar"):
                        st.session_state.edit_request = {"target_section": selection, "instruction": instruction}
                        st.rerun()
        with tab_prompts:
            if not st.session_state.image_prompts:
                st.warning("Nenhum prompt disponível.")
            else:
                for i, p in enumerate(st.session_state.image_prompts):
                    st.code(p, language="text")
        with tab_publish:
            webhook_url = st.text_input("n8n Webhook", value=os.getenv("WEBHOOK_N8N_POST_ART", ""))
            if st.button("🚀 Publicar"):
                session = repo.Session()
                art = session.query(Article).filter(Article.id == st.session_state.current_article_id).first()
                if art:
                    try:
                        requests.post(webhook_url, json={"content": st.session_state.draft_content, "title": art.title})
                        st.success("Publicado!")
                    except Exception as e: st.error(f"Erro: {e}")
                session.close()
st.caption("Lean Blog Engine v2.0")
