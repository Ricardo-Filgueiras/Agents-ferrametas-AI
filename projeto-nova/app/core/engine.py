import time
import logging
import os
from app.core.state import AgentState
from app.core.controller import AgentController
from app.providers.stt_whisper import WhisperProvider
from app.providers.tts_piper import PiperProvider
from app.audio.listener import Listener
from app.audio.speaker import Speaker

class NovaEngine:
    """Orquestrador Slim do ciclo de vida da Nova Agent v2."""
    
    def __init__(self, state: AgentState):
        self.state = state
        self.logger = logging.getLogger("NovaEngine")
        
        # 1. Carrega Plugins (Providers)
        self.state.update_module("llm", "Carregando...")
        self.brain = AgentController()
        
        self.state.update_module("stt", "Carregando...")
        self.stt = WhisperProvider()
        
        self.state.update_module("tts", "Carregando...")
        self.tts = PiperProvider()
        
        # 2. Carrega Hardware
        self.state.update_module("audio", "Carregando...")
        self.listener = Listener(wake_word=os.getenv("WAKE_WORD", "nova"))
        self.speaker = Speaker()
        
        # Seta tudo como Idle
        for mod in ["llm", "stt", "tts", "audio"]:
            self.state.update_module(mod, "Idle")

    def start(self):
        self.logger.info("Nova Engine v2 (Modular) iniciada.")
        self.listener.start_stream()
        
        try:
            while self.state.is_running:
                self.state.set_action("Aguardando Wake Word...")
                
                if self.listener.wait_for_wake_word():
                    # Captura áudio
                    self.state.set_action("Ouvindo comando...")
                    audio_data = self.listener.capture_command(duration=4)
                    
                    self.run_cycle(audio_data)
        finally:
            self.listener.stop_stream()

    def run_cycle(self, audio_data):
        start_time = time.time()
        
        try:
            # 1. Transcrição (STT)
            self.state.update_module("stt", "Processando")
            stt_start = time.time()
            text = self.stt.transcribe(audio_data)
            self.state.update_module("stt", "OK", time.time() - stt_start)
            
            if not text: return

            # 2. Cérebro (LLM)
            self.state.update_module("llm", "Processando")
            llm_start = time.time()
            response = self.brain.ask(text)
            self.state.update_module("llm", "OK", time.time() - llm_start)
            
            # 3. Síntese (TTS)
            self.state.update_module("tts", "Processando")
            tts_start = time.time()
            wav_path = self.tts.synthesize(response)
            self.state.update_module("tts", "OK", time.time() - tts_start)
            
            # 4. Reprodução (Hardware)
            self.state.set_action("Falando...")
            self.speaker.play(wav_path)
            
            # Pequeno fôlego para o sistema não ouvir o eco da própria voz
            time.sleep(0.5)
            
            # Finaliza métricas
            self.state.log_interaction(text, response, time.time() - start_time)
            
        except Exception as e:
            self.logger.error(f"Erro no ciclo Engine: {e}")
            self.state.set_action(f"Erro: {str(e)}")
