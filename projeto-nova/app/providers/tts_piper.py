import os
import subprocess
import logging
import tempfile
import pyttsx3
import threading
from app.core.base import BaseTTS

class PiperProvider(BaseTTS):
    def __init__(self):
        self.logger = logging.getLogger("PiperProvider")
        model_name = os.getenv("TTS_MODEL", "pt_BR-faber-medium")
        self.model_path = f"models/{model_name}.onnx"
        self._lock = threading.Lock() # Garante thread-safety para o pyttsx3

    def synthesize(self, text: str) -> str:
        """Gera áudio usando Piper ou Voz Nativa sem bloquear."""
        
        # 1. Tenta Piper
        if os.path.exists(self.model_path):
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_wav.close()
            try:
                cmd = f'piper --model {self.model_path} --output_file "{temp_wav.name}"'
                subprocess.run(cmd, input=text.encode('utf-8'), shell=True, check=True, capture_output=True)
                if os.path.exists(temp_wav.name) and os.path.getsize(temp_wav.name) > 0:
                    return temp_wav.name
            except Exception as e:
                self.logger.warning(f"Piper falhou. Erro: {e}")

        # 2. Backup Nativo (Thread-safe)
        return self._synthesize_native(text)

    def _synthesize_native(self, text: str) -> str:
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_wav.close()
        
        try:
            # Precisamos inicializar o engine dentro do lock para evitar colisões
            with self._lock:
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                for voice in voices:
                    if "brazil" in voice.name.lower() or "portuguese" in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                
                engine.save_to_file(text, temp_wav.name)
                engine.runAndWait()
                # Importante: destruir o engine para liberar o recurso
                del engine
                
            return temp_wav.name
        except Exception as e:
            self.logger.error(f"Falha na voz nativa: {e}")
            return ""
