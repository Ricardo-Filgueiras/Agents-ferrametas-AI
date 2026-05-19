import logging
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from app.user.models import Documentos_clientes
from app.user.services import process_document_file
from app.nova.tasks import ocr_and_markup_file



logger = logging.getLogger(__name__)

def run_processing_in_background(instance_id):
    """
    Runs ocr_and_markup_file in a background thread to prevent blocking the HTTP response.
    Closes the thread-local database connection when done.
    """
    try:
        ocr_and_markup_file(instance_id)
    except Exception as e:
        logger.error(f"[Background Thread] Falha ao processar arquivo via tasks: {e}", exc_info=True)
    finally:
        # Django thread-local database connection must be closed in background threads
        connection.close()

@receiver(post_save, sender=Documentos_clientes)
def post_save_documento_receptor(sender, instance, created, **kwargs):
    """
    Observer Signal Receiver: Listens for the post_save event of Documentos_clientes.
    When a new document instance is created, spawns a background thread to process it asynchronously.
    """
    if created:
        import sys
        if 'test' in sys.argv:
            logger.info("[Observer Signal] Modo de teste detectado. Executando processamento de forma síncrona para evitar locks no SQLite.")
            run_processing_in_background(instance.pk)
            return
            
        logger.info(f"[Observer Signal] Novo upload detectado para '{instance.nome}' (ID: {instance.pk}). Disparando thread de processamento...")
        
        # Spawn thread for asynchronous background execution
        thread = threading.Thread(
            target=run_processing_in_background,
            args=(instance.pk,),
            daemon=True
        )
        thread.start()
