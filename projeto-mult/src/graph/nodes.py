import time
from src.schemas.state import AgentState, AgentExecutionLog, ContentPlan, Draft, ReviewResult, DesignPrompts, ValidationScore
from src.agents.seo.agent import get_seo_planner, get_seo_validator
from src.agents.writer.agent import get_technical_writer
from src.agents.editor.agent import get_editor
from src.agents.designer.agent import get_designer
from src.services.model_resolver import resolve_model

def planning_node(state: AgentState):
    print("--- SEO PLANNING & IDEA IMPROVEMENT ---")
    
    # Resolve o modelo baseado na config ou usa default (gemini)
    model_tag = state.get("model_config", {}).get("planner", "gemini")
    model = resolve_model(model_tag)
    
    planner = get_seo_planner(model=model)
    
    start_time = time.time()
    # Prompt focado em MELHORAR a ideia inicial (cloud model)
    prompt = f"""
    ESTRATÉGIA DE CONTEÚDO:
    Ideia Bruta do Usuário: {state['topic']}
    Keywords Iniciais: {state['keywords']}
    
    Sua tarefa:
    1. Melhore o tema central para torná-lo mais atraente e tecnicamente robusto.
    2. Refine a lista de palavras-chave para o contexto atual do mercado.
    3. Crie a estrutura de tópicos (outline) perfeita para SEO.
    """
    
    response = planner.run(prompt, response_model=ContentPlan)
    execution_time = time.time() - start_time
    
    # No Agno v2.x com response_model, o conteúdo já vem como objeto se disponível
    state["plan"] = response.content
    
    # Sincroniza keywords refinadas de volta para o estado global
    if hasattr(response.content, "primary_keywords"):
        state["keywords"] = response.content.primary_keywords
        
    state["current_step"] = "planning"
    
    state["logs"].append(AgentExecutionLog(
        agent_name="SEO Strategist",
        step="Planning",
        execution_time=execution_time,
        model_used=model_tag,
        success=True
    ))
    return state

def writing_node(state: AgentState):
    print("--- TECHNICAL WRITING ---")
    
    model_tag = state.get("model_config", {}).get("writer", "ollama")
    model = resolve_model(model_tag)
    writer = get_technical_writer(model=model)
    
    prompt = f"Escreva o artigo baseado no plano: {state['plan']}"
    
    # Validação de segurança para o feedback (Lei nº 2)
    review = state["review"]
    is_approved = True 
    if review:
        if hasattr(review, "is_approved"):
            is_approved = review.is_approved
        elif isinstance(review, str):
            is_approved = "aprovado" in review.lower() or "approved" in review.lower()

    if review and not is_approved:
        feedback = review.feedback if hasattr(review, "feedback") else str(review)
        prompt += f"\n\nAjuste o texto seguindo este feedback: {feedback}"
    
    start_time = time.time()
    response = writer.run(prompt, response_model=Draft)
    execution_time = time.time() - start_time
    
    state["draft"] = response.content
    state["current_step"] = "writing"
    state["iteration_count"] += 1
    
    state["logs"].append(AgentExecutionLog(
        agent_name="Technical Writer",
        step=f"Writing (It {state['iteration_count']})",
        execution_time=execution_time,
        model_used=model_tag,
        success=True
    ))
    return state

def editing_node(state: AgentState):
    print("--- EDITORIAL REVIEW ---")
    
    model_tag = state.get("model_config", {}).get("reviewer", "ollama")
    model = resolve_model(model_tag)
    editor = get_editor() # TODO: Update editor agent to accept model if needed
    
    # Validação de segurança para evitar erro de atributo
    content_to_review = ""
    if state["draft"] and hasattr(state["draft"], "markdown_content"):
        content_to_review = state["draft"].markdown_content
    else:
        content_to_review = str(state["draft"])

    start_time = time.time()
    response = editor.run(
        f"Revise este conteúdo: {content_to_review}",
        response_model=ReviewResult
    )
    execution_time = time.time() - start_time
    
    state["review"] = response.content
    state["current_step"] = "editing"
    
    state["logs"].append(AgentExecutionLog(
        agent_name="Editor",
        step="Review",
        execution_time=execution_time,
        model_used=model_tag,
        success=True
    ))
    return state

def design_node(state: AgentState):
    print("--- CONTENT DESIGN ---")
    designer = get_designer()
    
    content_to_analyze = ""
    if state["draft"] and hasattr(state["draft"], "markdown_content"):
        content_to_analyze = state["draft"].markdown_content
    else:
        content_to_analyze = str(state["draft"])

    start_time = time.time()
    response = designer.run(
        f"Gere prompts de imagem para este artigo: {content_to_analyze}",
        response_model=DesignPrompts
    )
    execution_time = time.time() - start_time
    
    state["design"] = response.content
    state["current_step"] = "design"
    
    state["logs"].append(AgentExecutionLog(
        agent_name="Designer",
        step="Design Prompts",
        execution_time=execution_time,
        model_used="default",
        success=True
    ))
    return state

def validation_node(state: AgentState):
    print("--- FINAL SEO VALIDATION ---")
    
    model_tag = state.get("model_config", {}).get("planner", "gemini")
    model = resolve_model(model_tag)
    validator = get_seo_validator(model=model)
    
    content_to_validate = ""
    if state["draft"] and hasattr(state["draft"], "markdown_content"):
        content_to_validate = state["draft"].markdown_content
    else:
        content_to_validate = str(state["draft"])

    start_time = time.time()
    response = validator.run(
        f"Valide se este texto cumpre o plano de SEO: {content_to_validate}",
        response_model=ValidationScore
    )
    execution_time = time.time() - start_time
    
    state["validation"] = response.content
    # Check if we got a valid validation object
    if state["validation"] and hasattr(state["validation"], "is_validated"):
        state["is_validated"] = state["validation"].is_validated
    else:
        state["is_validated"] = False
        
    state["current_step"] = "validation"
    
    state["logs"].append(AgentExecutionLog(
        agent_name="SEO Validator",
        step="Final Validation",
        execution_time=execution_time,
        model_used=model_tag,
        success=True
    ))
    return state
    
def refinement_node(state: AgentState):
    print("--- REFINEMENT NODE ---")
    
    model_tag = state.get("model_config", {}).get("writer", "ollama")
    model = resolve_model(model_tag)
    writer = get_technical_writer(model=model)
    
    current_content = state["draft"].markdown_content if hasattr(state["draft"], "markdown_content") else str(state["draft"])
    
    # Verifica se há um pedido seletivo (via editor) ou chat geral
    edit_req = state.get("edit_request")
    
    if edit_req:
        target = edit_req.get("target_section")
        instruction = edit_req.get("instruction")
        prompt = f"""
        ARTIGO ATUAL:
        {current_content}
        
        PEDIDO DE REESCRITA SELETIVA:
        Foque na parte: "{target}"
        Instrução: {instruction}
        
        Reescreva APENAS este trecho mantendo a coesão com o restante do artigo. Retorne o artigo completo já integrado.
        """
    else:
        # Chat geral
        user_request = state["chat_history"][-1]["content"] if state["chat_history"] else "Melhore o artigo."
        prompt = f"""
        ARTIGO ATUAL:
        {current_content}
        
        PEDIDO DO USUÁRIO:
        {user_request}
        
        Reescreva o artigo ajustando o que foi pedido e mantendo a qualidade.
        """
    
    start_time = time.time()
    response = writer.run(prompt, response_model=Draft)
    execution_time = time.time() - start_time
    
    state["draft"] = response.content
    state["current_step"] = "refinement"
    state["iteration_count"] += 1
    state["edit_request"] = None # Limpa pedido após execução
    
    state["logs"].append(AgentExecutionLog(
        agent_name="Technical Writer (Refinement)",
        step=f"Refinement (It {state['iteration_count']})",
        execution_time=execution_time,
        model_used=model_tag,
        success=True
    ))
    return state
