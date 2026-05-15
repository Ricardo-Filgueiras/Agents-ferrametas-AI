import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Article
from src.schemas.state import AgentState

class ArticleRepository:
    def __init__(self, db_url="sqlite:///data/blog_engine.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_agent_state(self, state: AgentState):
        session = self.Session()
        try:
            # Helper para extrair dados de objetos (Resiliência contra métodos nativos de strings)
            def safe_get(obj, attr, default=""):
                if obj is None: return default
                if isinstance(obj, str): return default # Ignora strings puras na busca por atributos
                if hasattr(obj, attr):
                    val = getattr(obj, attr)
                    if not callable(val): # Previne pegar métodos como .title() das strings
                        return val
                return default

            # Converte logs Pydantic para dicionários seguros para JSON (lidando com datetime)
            logs_dict = []
            for log in state["logs"]:
                if hasattr(log, "model_dump"):
                    logs_dict.append(log.model_dump(mode="json")) # Pydantic v2
                else:
                    log_data = log.dict() if hasattr(log, "dict") else dict(log)
                    logs_dict.append(json.loads(json.dumps(log_data, default=str)))

            
            # Extração flexível de dados
            title = safe_get(state["plan"], "title", state["topic"])
            category = safe_get(state["plan"], "category", "Geral")
            meta_title = safe_get(state["plan"], "meta_title", title)
            meta_description = safe_get(state["plan"], "meta_description", "")
            excerpt = safe_get(state["draft"], "excerpt", "")
            
            outline = []
            tags = []
            if state["plan"]:
                if hasattr(state["plan"], "outline"):
                    outline = state["plan"].outline
                elif isinstance(state["plan"], str):
                    outline = [state["plan"]]
                    
                if hasattr(state["plan"], "tags"):
                    tags = state["plan"].tags

            content_md = safe_get(state["draft"], "markdown_content", str(state["draft"]))
            
            image_prompts = []
            if state["design"]:
                if hasattr(state["design"], "image_prompts"):
                    image_prompts = state["design"].image_prompts
                elif isinstance(state["design"], str):
                    image_prompts = [state["design"]]

            seo_score = 0.0
            if state["validation"]:
                if hasattr(state["validation"], "seo_score"):
                    seo_score = state["validation"].seo_score
                else:
                    try: seo_score = float(str(state["validation"]))
                    except: seo_score = 0.0

            new_article = Article(
                topic=state["topic"],
                keywords=state["keywords"],
                title=title,
                category=category,
                tags=tags,
                meta_title=meta_title,
                meta_description=meta_description,
                excerpt=excerpt,
                outline=outline,
                content_markdown=content_md,
                image_prompts=image_prompts,
                seo_score=seo_score,
                is_validated=1 if state.get("is_validated", False) else 0,
                iteration_count=state.get("iteration_count", 1),
                execution_logs=logs_dict
            )
            session.add(new_article)
            session.commit()
            print(f"--- ARTICLE SAVED TO DB: ID {new_article.id} ---")
            return new_article.id
        except Exception as e:
            session.rollback()
            print(f"Error saving article: {e}")
            raise e
        finally:
            session.close()
