import os
from src.graph.workflow import create_workflow
from src.database.repository import ArticleRepository
from src.schemas.state import AgentState

def run_blog_pipeline(topic: str, keywords: list):
    # 1. Configurar Estado Inicial
    initial_state: AgentState = {
        "topic": topic,
        "keywords": keywords,
        "plan": None,
        "draft": None,
        "review": None,
        "design": None,
        "validation": None,
        "revision_history": [],
        "iteration_count": 0,
        "current_step": "start",
        "logs": [],
        "is_validated": False,
        "final_score": 0.0
    }

    # 2. Criar Workflow
    app = create_workflow()

    # 3. Executar Pipeline
    print(f"--- INICIANDO PIPELINE: {topic} ---")
    final_state = app.invoke(initial_state)
    print(f"--- FIM DO FLUXO. STATUS: {final_state['current_step']} ---")
    
    # Salva no banco de dados com "Pára-quedas" (Fallback)
    repo = ArticleRepository()
    try:
        article_id = repo.save_agent_state(final_state)
        print(f"✅ Artigo persistido no banco com sucesso! ID: {article_id}")
    except Exception as e:
        print(f"❌ Falha crítica ao salvar no banco de dados: {e}")
        print("🪂 Acionando Pára-quedas: Salvando backup em arquivo local...")
        
        # Cria um backup do artigo para não perder o processamento
        with open("ARTIGO_BACKUP_EMERGENCIA.md", "w", encoding="utf-8") as f:
            f.write(f"# {final_state['topic']}\n\n")
            
            # Tenta pegar o rascunho (pode ser objeto Pydantic ou string)
            draft = final_state.get("draft", "")
            content = draft.markdown_content if hasattr(draft, "markdown_content") else str(draft)
            f.write(content)
            
        print("✅ Backup salvo com sucesso no arquivo 'ARTIGO_BACKUP_EMERGENCIA.md' na raiz do projeto!")
    
    return final_state

if __name__ == "__main__":
    # Sua instrução personalizada:
    tema = "Finanças Pessoais: Guia Definitivo para Iniciantes como organizar suas finanças de casa"
    palavras_chave = ["Finanças Pessoais", "Guia Definitivo", "Iniciantes"]
    
    run_blog_pipeline(tema, palavras_chave)
