import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente antes de importar qualquer componente do projeto
load_dotenv()

from src.graph.workflow import create_workflow
from src.database.repository import ArticleRepository
from src.schemas.state import AgentState

def run_blog_pipeline(topic: str, keywords: list, model_config: dict = None):
    # 1. Configurar Estado Inicial
    initial_state: AgentState = {
        "topic": topic,
        "keywords": keywords,
        "model_config": model_config or {
            "planner": "gemini",
            "writer": "ollama",
            "reviewer": "ollama"
        },
        "plan": None,
        "draft": None,
        "review": None,
        "design": None,
        "validation": None,
        "chat_history": [{"role": "user", "content": f"Ideia: {topic}. Keywords: {keywords}"}], # Salva contexto inicial
        "revision_history": [],
        "iteration_count": 0,
        "current_step": "start",
        "logs": [],
        "is_validated": False,
        "final_score": 0.0,
        "artifacts": {}
    }

    # 2. Criar Workflow
    app = create_workflow()

    # 3. Executar Pipeline com Streaming para o Streamlit
    print(f"--- INICIANDO PIPELINE: {topic} ---")
    
    # Usamos stream para capturar cada passo
    final_state = initial_state
    for output in app.stream(initial_state):
        # O output do stream é um dicionário {nó: estado_atualizado}
        for node_name, state_update in output.items():
            print(f"--- STEP COMPLETED: {node_name} ---")
            final_state.update(state_update)
            yield node_name, final_state

    print(f"--- FIM DO FLUXO. STATUS: {final_state['current_step']} ---")
    
    # Salva no banco de dados
    repo = ArticleRepository()
    try:
        article_id = repo.save_agent_state(final_state)
        yield "saved", (article_id, final_state)
    except Exception as e:
        print(f"❌ Falha crítica ao salvar no banco de dados: {e}")
        yield "error", str(e)

def refine_article(article_id: int, user_message: str, model_config: dict = None):
    """Retoma um artigo existente e executa apenas o nó de refinamento"""
    repo = ArticleRepository()
    article = repo.get_article_by_id(article_id)
    
    if not article or not article.last_state:
        yield "error", "Artigo não encontrado ou sem estado salvo."
        return

    # 1. Recupera o estado anterior
    state = article.last_state
    
    # 2. Atualiza o chat e o tópico (se necessário)
    if "chat_history" not in state: state["chat_history"] = []
    state["chat_history"].append({"role": "user", "content": user_message})
    
    # Atualiza config se fornecida
    if model_config:
        state["model_config"] = model_config
    
    # 3. Executar refinamento
    print(f"--- REFINANDO ARTIGO: {article.topic} ---")

    # Executa o nó de refinamento
    from src.graph.nodes import refinement_node
    new_state = refinement_node(state)

    # 4. Salva atualização
    repo.update_article_chat(article_id, new_state["chat_history"], repo._serialize_state(new_state))

    # Atualiza o conteúdo do artigo no banco
    session = repo.Session()
    art = session.query(Article).filter(Article.id == article_id).first()
    if art:
        content_md = new_state["draft"].markdown_content if hasattr(new_state["draft"], "markdown_content") else str(new_state["draft"])
        art.content_markdown = content_md
        session.commit()
    session.close()

    yield "refinement", new_state
    yield "saved", (article_id, new_state)


if __name__ == "__main__":
    # Sua instrução personalizada:
    tema = "Finanças Pessoais: Guia Definitivo para Iniciantes como organizar suas finanças de casa"
    palavras_chave = ["Finanças Pessoais", "Guia Definitivo", "Iniciantes"]
    
    run_blog_pipeline(tema, palavras_chave)
