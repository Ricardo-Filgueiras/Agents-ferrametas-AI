import os
import asyncio
import whisper
import logging
from edge_tts import Communicate

logger = logging.getLogger(__name__)

_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        logger.info("Loading Whisper model 'base'...")
        _whisper_model = whisper.load_model("base")
    return _whisper_model

class AudioService:
    @staticmethod
    async def text_to_speech(text: str, output_path: str, voice: str = "pt-BR-ThalitaNeural"):
        """Generates an audio file from text using edge-tts."""
        communicate = Communicate(text, voice)
        await communicate.save(output_path)
        return output_path

    @staticmethod
    async def speech_to_text(audio_path: str) -> str:
        """Transcribes audio file to text using local Whisper model. Runs non-blocking."""
        loop = asyncio.get_event_loop()
        def _transcribe():
            model = get_whisper_model()
            result = model.transcribe(audio_path, language="pt")
            return result["text"]
        
        return await loop.run_in_executor(None, _transcribe)
