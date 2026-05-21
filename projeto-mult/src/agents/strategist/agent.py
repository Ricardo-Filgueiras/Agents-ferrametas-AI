"""
🎯 STRATEGIST AGENT - ReAct Pattern
===================================
Agente de estratégia de conteúdo com Reasoning + Acting.
Usa modelos locais com fallback automático.

Padrão ReAct:
Thought → Action → Observation → Thought → ... → Final Answer
"""

import time
from typing import Optional
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from src.schemas.state import ContentPlan
from src.llm.config import (
    OPENAI_API_KEY,
    GOOGLE_API_KEY,
    DEFAULT_OLLAMA_MODEL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_GEMINI_MODEL,
)


# ============================================================================
# OBTER LLM COM FALLBACK (Centralizado em src/llm/config.py)
# ============================================================================

def get_llm_strategist(model_name: Optional[str] = None):
    """
    Obtém LLM para Strategist com fallback automático.
    Configuração centralizada em src/llm/config.py
    
    Prioridade:
    1. Modelo passado como argumento
    2. DEFAULT_OLLAMA_MODEL (de config.py)
    3. Gemini (se API key disponível)
    4. OpenAI (se API key disponível)
    
    Exemplo:
    >>> llm = get_llm_strategist()  # Usa DEFAULT_OLLAMA_MODEL
    >>> llm = get_llm_strategist("mistral:latest")  # Modelo específico
    """
    
    # Passo 1: Usar modelo explícito se passado
    if model_name:
        try:
            model = Ollama(id=model_name)
            print(f"✅ STRATEGIST: Modelo Ollama '{model_name}'")
            return model
        except Exception as e:
            print(f"⚠️  Erro ao carregar {model_name}: {e}")
    
    # Passo 2: Usar DEFAULT_OLLAMA_MODEL (de config.py)
    try:
        model = Ollama(id=DEFAULT_OLLAMA_MODEL)
        print(f"✅ STRATEGIST: Modelo Ollama '{DEFAULT_OLLAMA_MODEL}' (config.py)")
        return model
    except Exception as e:
        print(f"⚠️  Ollama não disponível: {e}")
    
    # Passo 3: Fallback Gemini
    if GOOGLE_API_KEY:
        try:
            model = Gemini(id=DEFAULT_GEMINI_MODEL)
            print("✅ STRATEGIST: Modelo Gemini (fallback)")
            return model
        except Exception as e:
            print(f"⚠️  Erro ao conectar Gemini: {e}")
    
    # Passo 4: Fallback OpenAI
    if OPENAI_API_KEY:
        try:
            model = OpenAIChat(id=DEFAULT_OPENAI_MODEL)
            print("✅ STRATEGIST: Modelo OpenAI (fallback final)")
            return model
        except Exception as e:
            print(f"⚠️  Erro ao conectar OpenAI: {e}")
    
    raise Exception(
        "❌ NENHUM MODELO DISPONÍVEL!\n"
        "Configure: DEFAULT_OLLAMA_MODEL em src/llm/config.py ou .env"
    )


# ============================================================================
# DEFINIÇÃO DO AGENTE STRATEGIST COM ReAct
# ============================================================================

def create_strategist_agent(model=None, debug: bool = True) -> Agent:
    """
    Cria um agente Strategist com pattern ReAct.
    
    Args:
        model: Instância LLM customizada (padrão: usa configuração automática)
        debug: Ativa modo debug (verbose logging)
        
    Returns:
        Agent: Agente pronto para análise estratégica
    """
    
    if model is None:
        model = get_llm_strategist()
    
    strategist = Agent(
        name="Strategic Planner",
        model=model,
        role="Estrategista de Conteúdo e Especialista em SEO",
        instructions=[
            """
            === INSTRUÇÕES DO AGENTE STRATEGIST ===
            
            OBJETIVO:
            Você é um estrategista de conteúdo elite. Seu trabalho é transformar 
            ideias brutas em planos de conteúdo de alto impacto que geram tráfego 
            orgânico, leads qualificados e autoridade de marca.
            
            PADRÃO DE RACIOCÍNIO (ReAct):
            1. THOUGHT (Pensamento): Analise o problema, organize informações
            2. ACTION (Ação): Execute pesquisa, planejamento, estruturação
            3. OBSERVATION (Observação): Avalie resultados e ajuste
            4. Repita até chegar na resposta final
            
            ETAPAS DE ANÁLISE:
            
            ▶ ETAPA 1: ENTENDER O CONTEXTO
               - Qual é o tema proposto?
               - Qual é a intenção por trás (problema do usuário)?
               - Qual é o objetivo (tráfego, leads, autoridade)?
            
            ▶ ETAPA 2: ANÁLISE SWOT DO TEMA
               Strengths (Forças):
                 • Demanda real de mercado?
                 • Diferencial competitivo possível?
                 • Potencial de rankear no Google?
               
               Weaknesses (Fraquezas):
                 • Alta concorrência?
                 • Difícil abordar?
               
               Opportunities (Oportunidades):
                 • Ângulo único possível?
                 • Keywords complementares?
               
               Threats (Ameaças):
                 • Quem já domina este tema?
                 • Como superar?
            
            ▶ ETAPA 3: REFINAMENTO DO TEMA
               TRANSFORME:
               ❌ "Dicas de produtividade"
               ✅ "Por que técnicas de produtividade famosas falharam (e o que realmente funciona)"
               
               REGRAS:
               • Seja específico: não use "Guia Definitivo"
               • Seja valioso: prometa transformação real
               • Seja pesquisável: baseado em keywords reais
            
            ▶ ETAPA 4: PESQUISA DE KEYWORDS
               - Primárias: alto volume + baixa concorrência + alto CPC
               - LSI (semânticas): para contextualizar e cobrir variações
               - Relacionadas: para expandir cobertura
               
               Ferramentas mentais:
               • Imagine como o usuário busca
               • Pense em diferentes estágios (awareness, consideration, decision)
            
            ▶ ETAPA 5: ESTRUTURAÇÃO DO OUTLINE
               Hierarquia:
               H1 - Título Principal (1 único)
                 ├─ H2 - Seção 1 (2-5 seções)
                 │   ├─ H3 - Subseção 1.1 (1-3 subsseções)
                 │   └─ H3 - Subseção 1.2
                 └─ H2 - Seção 2
               
               Critério de qualidade:
               ✅ Cada H2 responde UMA pergunta clara
               ✅ Fluxo lógico: começa fácil, termina complexo
               ✅ Inclui: Intro (hook), Desenvolvimento, Conclusão (CTA)
            
            ▶ ETAPA 6: OTIMIZAÇÃO SEO
               Meta Title (máx 60 chars):
               • Inclua keyword primária no início
               • Seja atrativo
               • Exemplo: "Python Performance: 5 Técnicas Que Aumentam Velocidade em 10x"
               
               Meta Description (máx 160 chars):
               • Inclua keyword + proposta de valor
               • Inclua CTA implícito
               • Exemplo: "Aprenda 5 técnicas comprovadas para otimizar performance em Python..."
               
               Tags: 5-8 tags contextualizadas
            
            ▶ ETAPA 7: DEFINIÇÃO DE AUDIÊNCIA
               - Persona: quem é? Nível técnico?
               - Problema: qual dor específica tem?
               - Busca: como procura informações?
               - Valor: o que o faria compartilhar?
            
            FORMATO DA RESPOSTA:
            
            Estruture a resposta em JSON com:
            {
              "title": "Título otimizado e atrativo",
              "category": "Categoria sugerida",
              "tags": ["tag1", "tag2", ...],
              "meta_title": "Meta title otimizada (máx 60 chars)",
              "meta_description": "Meta description otimizada (máx 160 chars)",
              "outline": ["H1: Título", "H2: Seção 1", "H3: Subsseção", ...],
              "primary_keywords": ["keyword1", "keyword2", ...],
              "lsi_keywords": ["lsi1", "lsi2", ...],
              "target_audience": "Descrição clara da audiência",
              "estimated_word_count": 2500
            }
            
            QUALIDADE ESPERADA:
            ✅ Resposta estratégica e fundamentada
            ✅ Diferencial competitivo claro
            ✅ SEO-friendly e pronto para implementar
            ✅ Audiência bem definida
            ✅ Prioridades claras
            """,
        ],
        markdown=True,
        debug_mode=debug,
    )
    
    return strategist


# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

# Cria instância padrão (usa .env)
strategist_agent = create_strategist_agent()


# ============================================================================
# API PÚBLICA
# ============================================================================

def get_strategist(model=None) -> Agent:
    """
    Retorna uma instância do Strategist.
    
    Args:
        model: Modelo customizado (padrão: None, usa .env)
        
    Returns:
        Agent: Agente Strategist
        
    Exemplo:
        >>> strategist = get_strategist()
        >>> result = strategist.run("Meu tema aqui")
    """
    return create_strategist_agent(model=model)


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🎯 DEMONSTRAÇÃO DO AGENTE STRATEGIST")
    print("=" * 70)
    
    # Cria agente
    strategist = get_strategist()
    
    # Exemplo de uso
    tema = "Otimização de Performance em Python"
    keywords_iniciais = ["python performance", "otimização", "benchmarking"]
    
    prompt = f"""
    ANÁLISE DE ESTRATÉGIA DE CONTEÚDO
    
    Tema: {tema}
    Keywords Iniciais: {', '.join(keywords_iniciais)}
    
    Por favor, realize uma análise estratégica completa e crie um plano de conteúdo robusto.
    """
    
    print(f"\n📊 Tema: {tema}")
    print(f"🔑 Keywords: {keywords_iniciais}")
    print("\n⏳ Analisando... (isso pode levar alguns segundos)\n")
    
    start = time.time()
    try:
        result = strategist.run(prompt, response_model=ContentPlan)
        elapsed = time.time() - start
        
        print(f"✅ Análise concluída em {elapsed:.2f}s\n")
        print("📋 PLANO ESTRATÉGICO:")
        print("-" * 70)
        
        # result.content tem o ContentPlan
        plan = result.content
        if hasattr(plan, 'title'):
            print(f"Título: {plan.title}")
            print(f"Categoria: {plan.category}")
            print(f"Meta Title: {plan.meta_title}")
            print(f"Meta Description: {plan.meta_description}")
            print(f"Audiência-Alvo: {plan.target_audience}")
            print(f"Palavras-chave Primárias: {', '.join(plan.primary_keywords)}")
            print(f"Outline ({len(plan.outline)} seções):")
            for i, item in enumerate(plan.outline[:5], 1):
                print(f"  {i}. {item}")
            if len(plan.outline) > 5:
                print(f"  ... e mais {len(plan.outline) - 5} seções")
        else:
            print(result)
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
