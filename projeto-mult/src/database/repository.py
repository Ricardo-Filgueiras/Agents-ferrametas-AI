import json
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Article
from src.schemas.state import AgentState

class ArticleRepository:
    def __init__(self, db_url="sqlite:///data/blog_engine.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def _extract_json_from_text(self, text: str) -> dict:
        """
        Tenta extrair um objeto JSON de dentro de uma string de texto.
        Prioriza blocos marcados com ```json.
        """
        if not isinstance(text, str):
            return None
        
        try:
            # 1. Tenta encontrar blocos de código JSON ```json { ... } ```
            json_block = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_block:
                return json.loads(json_block.group(1))
            
            # 2. Tenta encontrar qualquer coisa entre chaves { ... }
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
        except:
            pass
        return None

    def save_agent_state(self, state: AgentState):
        session = self.Session()
        try:
            # Helper para extrair dados de objetos (Resiliência contra métodos nativos de strings)
            def safe_get(obj, attr, default=""):
                if obj is None: return default
                
                # Se for string, tenta extrair JSON dela primeiro
                if isinstance(obj, str):
                    extracted = self._extract_json_from_text(obj)
                    if extracted and attr in extracted:
                        return extracted[attr]
                    return default # Se não achou o atributo no JSON extraído, mantém default
                
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
            plan_obj = state.get("plan")
            title = safe_get(plan_obj, "title", state["topic"])
            category = safe_get(plan_obj, "category", "Geral")
            meta_title = safe_get(plan_obj, "meta_title", title)
            meta_description = safe_get(plan_obj, "meta_description", "")
            
            # Limpeza de conteúdo Markdown (Remover JSON sobrando se o modelo repetiu)
            content_md = safe_get(state["draft"], "markdown_content", str(state["draft"]))
            content_md = re.sub(r'```json.*?```', '', content_md, flags=re.DOTALL).strip()

            excerpt = safe_get(state["draft"], "excerpt", "")
            
            outline = []
            tags = []
            if plan_obj:
                if hasattr(plan_obj, "outline"):
                    outline = plan_obj.outline
                elif isinstance(plan_obj, str):
                    extracted = self._extract_json_from_text(plan_obj)
                    if extracted and "outline" in extracted:
                        outline = extracted["outline"]
                    else:
                        # Se não é JSON, mas é texto, tentamos pegar linhas que pareçam tópicos
                        lines = [line.strip() for line in plan_obj.split('\n') if line.strip()]
                        outline = lines[:10] # Pega as 10 primeiras linhas como fallback
                    
                if hasattr(plan_obj, "tags"):
                    tags = plan_obj.tags
                elif isinstance(plan_obj, str):
                    extracted = self._extract_json_from_text(plan_obj)
                    if extracted and "tags" in extracted:
                        tags = extracted["tags"]

            image_prompts = []
            if state["design"]:
                if hasattr(state["design"], "image_prompts"):
                    image_prompts = state["design"].image_prompts
                elif isinstance(state["design"], str):
                    extracted = self._extract_json_from_text(state["design"])
                    if extracted and "image_prompts" in extracted:
                        image_prompts = extracted["image_prompts"]
                    else:
                        # Fallback: Se o modelo mandou texto puro com prompts, tenta separar por "Prompt"
                        parts = re.split(r'Prompt \d+:', state["design"])
                        image_prompts = [p.strip() for p in parts if len(p.strip()) > 10]

            seo_score = 0.0
            if state["validation"]:
                if hasattr(state["validation"], "seo_score"):
                    seo_score = state["validation"].seo_score
                else:
                    extracted = self._extract_json_from_text(str(state["validation"]))
                    if extracted and "seo_score" in extracted:
                        seo_score = extracted["seo_score"]
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
                execution_logs=logs_dict,
                chat_history=state.get("chat_history", []),
                last_state=self._serialize_state(state)
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

    def _serialize_state(self, state: AgentState) -> dict:
        """Helper para serializar o estado completo lidando com objetos Pydantic"""
        serialized = {}
        for k, v in state.items():
            if hasattr(v, "model_dump"):
                serialized[k] = v.model_dump(mode="json")
            elif isinstance(v, list):
                serialized[k] = [item.model_dump(mode="json") if hasattr(item, "model_dump") else item for item in v]
            else:
                serialized[k] = v
        return serialized

    def get_article_by_id(self, article_id: int) -> Article:
        session = self.Session()
        try:
            return session.query(Article).filter(Article.id == article_id).first()
        finally:
            session.close()

    def update_article_chat(self, article_id: int, chat_history: list, last_state: dict):
        session = self.Session()
        try:
            article = session.query(Article).filter(Article.id == article_id).first()
            if article:
                article.chat_history = chat_history
                article.last_state = last_state
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error updating article chat: {e}")
            return False
        finally:
            session.close()
