import os
import numpy as np
import pyaudio
import logging
import time
from dotenv import load_dotenv

load_dotenv()

class Listener:
    """Captura áudio baseada em detecção de voz (VAD simples)."""
    
    def __init__(self, wake_word="nova"):
        self.logger = logging.getLogger("Listener")
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        
        self.p = pyaudio.PyAudio()
        self.wake_word = wake_word.lower()
        self.threshold = 500 # Sensibilidade do microfone
        
        self.stream = None

    def start_stream(self):
        try:
            self.stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            self.logger.info("Microfone ativado. (Modo: Detecção de Voz)")
        except Exception as e:
            self.logger.error(f"Erro ao acessar microfone: {e}")
            raise e

    def stop_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def wait_for_wake_word(self) -> bool:
        """
        No modo simplificado, vamos apenas detectar se há som no microfone.
        A validação da palavra 'Nova' será feita pelo STT na Engine.
        """
        self.logger.info(f"Aguardando você chamar pela '{self.wake_word}'...")
        
        while True:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_data).mean()
            
            if amplitude > self.threshold:
                # Detectou som, agora captura o comando
                return True

    def capture_command(self, duration=4) -> np.ndarray:
        """Captura áudio por um tempo fixo após detectar som."""
        self.logger.info("Ouvindo...")
        frames = []
        
        # Captura por X segundos
        for _ in range(0, int(self.rate / self.chunk_size * duration)):
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(np.frombuffer(data, dtype=np.int16))
            
        return np.concatenate(frames).astype(np.float32) / 32768.0
