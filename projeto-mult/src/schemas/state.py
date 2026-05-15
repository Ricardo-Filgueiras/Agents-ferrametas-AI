from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field
from datetime import datetime

# --- 1. Schemas de Observabilidade ---

class AgentExecutionLog(BaseModel):
    agent_name: str
    step: str
    execution_time: float
    token_usage: Optional[int] = 0
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool
    error_message: Optional[str] = None

# --- 2. Contratos de Saída dos Agentes (Leis do Projeto) ---

class ContentPlan(BaseModel):
    title: str
    category: Optional[str] = Field(default="Geral", description="Categoria Sugerida")
    tags: List[str] = Field(default_factory=list, description="Lista de tags")
    meta_title: Optional[str] = Field(default="", description="Título SEO (máx 70 chars)")
    meta_description: Optional[str] = Field(default="", description="Descrição SEO (máx 160 chars)")
    outline: List[str] = Field(description="Lista de H1, H2, H3")
    primary_keywords: List[str]
    lsi_keywords: List[str]
    target_audience: str
    estimated_word_count: int

class Draft(BaseModel):
    markdown_content: str
    excerpt: Optional[str] = Field(default="", description="Resumo de 2-3 frases para o card do blog.")
    technical_check: List[str] = Field(description="Lista de pontos técnicos validados no texto")
    word_count: int

class ReviewResult(BaseModel):
    is_approved: bool
    feedback: List[str] = Field(description="Notas de revisão para o escritor")
    clash_points: List[str] = Field(description="Onde o texto desvia do plano de SEO")

class DesignPrompts(BaseModel):
    image_prompts: List[str]
    style_guidelines: str

class ValidationScore(BaseModel):
    is_validated: bool
    seo_score: float = Field(ge=0, le=10, description="Nota de 0 a 10 para SEO")
    readability_score: float = Field(ge=0, le=10)
    final_remarks: str

# --- 3. Estado Global do Grafo (LangGraph State) ---

class AgentState(TypedDict):
    # Contexto Inicial
    topic: str
    keywords: List[str]
    
    # Artefatos Gerados
    plan: Optional[ContentPlan]
    draft: Optional[Draft]
    review: Optional[ReviewResult]
    design: Optional[DesignPrompts]
    validation: Optional[ValidationScore]
    
    # Controle de Fluxo
    revision_history: List[str]
    iteration_count: int
    current_step: str
    
    # Observabilidade
    logs: List[AgentExecutionLog]
