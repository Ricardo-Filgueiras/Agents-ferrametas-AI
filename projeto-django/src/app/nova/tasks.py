import logging
from django.shortcuts import get_object_or_404 
from app.user.models import Documentos_clientes
from app.user.services import process_document_file

logger = logging.getLogger(__name__)

def ocr_and_markup_file(instance_id):
    """
    Background Task: Triggers layout analysis, OCR and deep GFM conversion 
    via Docling/Fallbacks and generates the AI Analysis report card.
    """
    logger.info(f"[Nova Tasks] Iniciando tarefa ocr_and_markup_file para ID: {instance_id}")
    try:
        instance = get_object_or_404(Documentos_clientes, pk=instance_id)
        process_document_file(instance)
        logger.info(f"[Nova Tasks] Processamento concluído com sucesso para o documento '{instance.nome}'.")
    except Exception as e:
        logger.error(f"[Nova Tasks] Erro crítico no processamento do documento {instance_id}: {e}", exc_info=True)
        raise e