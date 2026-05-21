from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String, nullable=False)
    keywords = Column(JSON)
    
    # Artefatos
    title = Column(String)
    category = Column(String)
    tags = Column(JSON)
    meta_title = Column(String)
    meta_description = Column(String)
    excerpt = Column(Text)
    outline = Column(JSON)
    content_markdown = Column(Text)
    image_prompts = Column(JSON)
    
    # Métricas e Status
    seo_score = Column(Float)
    is_validated = Column(Integer, default=0) # 0 para False, 1 para True
    iteration_count = Column(Integer)
    
    # Observabilidade
    execution_logs = Column(JSON)
    chat_history = Column(JSON) # Histórico de conversas do chat
    last_state = Column(JSON)   # Snapshot do AgentState para retomar fluxos
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
