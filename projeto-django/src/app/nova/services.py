import os
import logging
from django.core.files.base import ContentFile
from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)

class NovaAgentService:
    """
    Serviço central do agente Nova para processamento de documentos e inteligência.
    """

    def __init__(self):
        self.converter = DocumentConverter()

    def process_document(self, file_path):
        """
        Usa o IBM Docling para converter um arquivo (PDF, Word, etc.) em Markdown estruturado.
        """
        logger.info(f"[Nova Agent] Iniciando conversão Docling para: {file_path}")
        try:
            result = self.converter.convert(file_path)
            markdown_text = result.document.export_to_markdown()
            
            if markdown_text and markdown_text.strip():
                logger.info("[Nova Agent] Conversão concluída com sucesso.")
                return markdown_text
            else:
                logger.warning("[Nova Agent] Documento convertido resultou em texto vazio.")
                return ""
        except Exception as e:
            logger.error(f"[Nova Agent] Erro na conversão Docling: {e}", exc_info=True)
            raise e

def process_file_with_nova(documento):
    """
    Função auxiliar para processar um modelo Documentos_clientes usando o agente Nova.
    """
    if not documento.arquivo:
        return
        
    agent = NovaAgentService()
    file_path = documento.arquivo.path
    
    try:
        content = agent.process_document(file_path)
        
        # Salvar o markdown processado
        md_filename = os.path.basename(file_path)
        name_parts = os.path.splitext(md_filename)
        md_filename = f"{name_parts[0]}_processado.md"
        
        documento.arquivo_markdown.save(
            md_filename,
            ContentFile(content.encode('utf-8')),
            save=False
        )
        
        # O restante da lógica de análise (summary_card) pode permanecer no service original
        # ou ser migrado para cá se desejado.
        return content
    except Exception as e:
        logger.error(f"Falha ao processar arquivo com Nova: {e}")
        return None

def get_nova_ai_response(session, user_message):
    """
    Generates a response from the Nova AI using a local Ollama instance with RAG.
    Loads context from the associated markdown file, compiles the multi-turn conversational history,
    and queries the local Ollama API.
    """
    from .models import InteractionMessage
    import requests
    
    # 1. Retrieve context from the parsed markdown document
    context_content = ""
    if session.documento and session.documento.arquivo_markdown:
        try:
            with open(session.documento.arquivo_markdown.path, 'r', encoding='utf-8') as f:
                context_content = f.read()
        except Exception as e:
            logger.error(f"[Nova Agent] Erro ao ler arquivo markdown do documento: {e}")
            context_content = "Não foi possível carregar o arquivo markdown de contexto."

    # 2. Build system and conversation history messages for Ollama
    system_prompt = (
        "Você é a Nova, uma assistente virtual de inteligência artificial de alto nível. "
        "Seu objetivo é ajudar o usuário respondendo dúvidas com base EXCLUSIVAMENTE nas informações contidas no documento fornecido abaixo.\n\n"
        f"DOCUMENTO DE CONTEXTO:\n{context_content}\n\n"
        "Responda em formato Markdown, utilizando listas, tabelas e negritos de forma elegante. "
        "Seja profissional, clara, prestativa e objetiva. Responda em português do Brasil. "
        "Se a resposta não puder ser encontrada no documento de contexto, explique de forma educada que a informação não consta no documento fornecido."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add previous chat history in chronological order
    historic_messages = session.messages.all().order_by('created_at')
    for msg in historic_messages:
        role = "user" if msg.sender == "user" else "assistant"
        messages.append({"role": role, "content": msg.message})
        
    # Append active user message if not already persistent
    # Note: Some callers might save the user message to the DB before calling services.
    # We make sure it is in our request prompt payload.
    if not historic_messages.filter(sender='user', message=user_message).exists():
        messages.append({"role": "user", "content": user_message})

    # 3. Persist the User's message first
    user_msg_obj = InteractionMessage.objects.create(
        session=session,
        sender="user",
        message=user_message
    )

    # 4. Query Ollama local API
    model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    logger.info(f"[Nova Agent] Enviando requisição para Ollama. Modelo: {model_name}")
    
    url = "http://127.0.0.1:11434/api/chat"
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=45)
        if response.status_code == 200:
            res_json = response.json()
            response_text = res_json['message']['content']
            logger.info("[Nova Agent] Resposta gerada com sucesso pelo Ollama.")
        else:
            response_text = (
                f"Erro na API do Ollama (Status Code: {response.status_code}). "
                f"Detalhe: {response.text}"
            )
            logger.error(f"[Nova Agent] {response_text}")
    except requests.exceptions.RequestException as e:
        response_text = (
            f"O serviço local do Ollama não está respondendo. Certifique-se de que o Ollama está rodando localmente "
            f"(`ollama serve`) e o modelo `{model_name}` está baixado (`ollama run {model_name}`)."
        )
        logger.error(f"[Nova Agent] Falha ao conectar ao Ollama: {e}")

    # 5. Persist the Assistant's response
    InteractionMessage.objects.create(
        session=session,
        sender="assistant",
        message=response_text,
        context_used=context_content[:1000] # Limit size stored in context_used for metadata
    )
    
    return response_text
