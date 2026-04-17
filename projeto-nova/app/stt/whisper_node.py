import os
import logging
from faster_whisper import WhisperModel
from dotenv import load_dotenv

load_dotenv()

class WhisperNode:
    """Nodo de processamento de áudio para texto usando Faster-Whisper."""
    
    def __init__(self):
        self.logger = logging.getLogger("WhisperNode")
        self.model_size = os.getenv("STT_MODEL", "tiny")
        self.device = os.getenv("DEVICE", "cpu")
        
        self.logger.info(f"Carregando modelo Whisper ({self.model_size}) no {self.device}...")
        
        # Carrega o modelo com quantização para economia de recursos
        self.model = WhisperModel(
            self.model_size, 
            device=self.device, 
            compute_type="int8"
        )
        self.logger.info("Modelo Whisper carregado com sucesso.")

    def transcribe(self, audio_path_or_array) -> str:
        """Transcreve um chunk de áudio ou arquivo para texto."""
        try:
            segments, info = self.model.transcribe(
                audio_path_or_array, 
                beam_size=5,
                language="pt",
                vad_filter=True # Remove silêncio automaticamente
            )
            
            text = "".join([segment.text for segment in segments]).strip()
            return text
        except Exception as e:
            self.logger.error(f"Erro na transcrição: {e}")
            return ""
