import os
import logging
import numpy as np
from faster_whisper import WhisperModel
from app.core.base import BaseSTT

class WhisperProvider(BaseSTT):
    def __init__(self):
        self.logger = logging.getLogger("WhisperProvider")
        model_size = os.getenv("STT_MODEL", "small")
        device = os.getenv("DEVICE", "cuda")
        compute_type = os.getenv("COMPUTE_TYPE", "float16")
        
        self.model = WhisperModel(
            model_size, 
            device=device, 
            compute_type=compute_type
        )
        self.logger.info(f"Whisper carregado no {device} com {compute_type}")

    def transcribe(self, audio_data: np.ndarray) -> str:
        language = os.getenv("STT_LANGUAGE", "pt")
        segments, _ = self.model.transcribe(audio_data, beam_size=5, language=language)
        return "".join([s.text for s in segments]).strip()
