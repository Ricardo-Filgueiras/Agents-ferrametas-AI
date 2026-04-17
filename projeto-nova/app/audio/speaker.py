import subprocess
import logging
import os
import sounddevice as sd
import soundfile as sf

class Speaker:
    """Responsável pela reprodução de áudio no hardware local."""
    
    def __init__(self):
        self.logger = logging.getLogger("Speaker")

    def play(self, wav_path: str):
        """Reproduz um arquivo WAV usando ffplay ou sounddevice como backup."""
        if not wav_path or not os.path.exists(wav_path):
            return

        # Tenta FFPLAY primeiro (mais eficiente)
        try:
            cmd = f"ffplay -nodisp -autoexit -loglevel quiet \"{wav_path}\""
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            self._cleanup(wav_path)
            return
        except Exception:
            self.logger.warning("ffplay falhou. Usando sounddevice como backup.")

        # Backup: sounddevice (roda puramente em Python)
        try:
            data, fs = sf.read(wav_path, dtype='float32')
            sd.play(data, fs)
            sd.wait() # Espera terminar de tocar
        except Exception as e:
            self.logger.error(f"Falha total ao reproduzir som: {e}")
        finally:
            self._cleanup(wav_path)

    def _cleanup(self, path):
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
