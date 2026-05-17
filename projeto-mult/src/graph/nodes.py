import time
from src.schemas.state import AgentState, AgentExecutionLog, ContentPlan, Draft, ReviewResult, DesignPrompts, ValidationScore
from src.agents.seo.agent import get_seo_planner, get_seo_validator
from src.agents.writer.agent import get_technical_writer
from src.agents.editor.agent import get_editor
from src.agents.designer.agent import get_designer

def planning_node(state: AgentState):
    print("--- SEO PLANNING ---")
    planner = get_seo_planner()
    
    start_time = time.time()
    # Passamos o response_model na chamada run
    response = planner.run(
        f"Ideia central: {state['topic']}. Keywords: {state['keywords']}",
        response_model=ContentPlan
    )
    execution_time = time.time() - start_time
    
    # No Agno v2.x com response_model, o conteúdo já vem como objeto se disponível
    state["plan"] = response.content
    state["current_step"] = "planning"
    
    state["logs"].append(AgentExecutionLog(
        agent_name="SEO Strategist",
        step="Planning",
        execution_time=execution_time,
        model_used=getattr(planner.model, "id", "unknown"),
        success=True
    ))
    return state

def writing_node(state: AgentState):
    print("--- TECHNICAL WRITING ---")
    writer = get_technical_writer()
    
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
        model_used=getattr(writer.model, "id", "unknown"),
        success=True
    ))
    return state

def editing_node(state: AgentState):
    print("--- EDITORIAL REVIEW ---")
    editor = get_editor()
    
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
        model_used=getattr(editor.model, "id", "unknown"),
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
        model_used=getattr(designer.model, "id", "unknown"),
        success=True
    ))
    return state

def validation_node(state: AgentState):
    print("--- FINAL SEO VALIDATION ---")
    validator = get_seo_validator()
    
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
        model_used=getattr(validator.model, "id", "unknown"),
        success=True
    ))
    return state
