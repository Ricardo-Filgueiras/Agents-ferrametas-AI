from kokoro import KPipeline
import pyaudio
import numpy as np

# Inicialização global do pipeline
_pipeline = KPipeline(lang_code='p', repo_id='hexgrad/Kokoro-82M')

class KokoroPlayer:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.rate = 24000

    def start(self):
        """Abre o hardware de áudio uma única vez."""
        if self.stream is None:
            self.stream = self.pa.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.rate,
                output=True
            )

    def stop(self):
        """Fecha o hardware de áudio."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.pa.terminate()

    def play_text(self, texto):
        """Gera o áudio e envia para o stream já aberto."""
        if not texto.strip():
            return

        if self.stream is None:
            self.start()

        try:
            # Speed 1.1 para mais fluidez
            generator = _pipeline(texto, voice='pf_dora', speed=1.1)
            for _, _, audio in generator:
                if audio is not None:
                    if not isinstance(audio, np.ndarray):
                        audio = audio.detach().cpu().numpy()
                    # Envia para o stream aberto
                    self.stream.write(audio.astype(np.float32).tobytes())
        except Exception as e:
            print(f"❌ Erro na reprodução de áudio: {e}")

# Instância global para facilitar o uso
player = KokoroPlayer()

def stream_kokoro_local(texto):
    """Função de compatibilidade que usa o player persistente."""
    player.play_text(texto)

if __name__ == "__main__":
    player.start()
    player.play_text("Olá! Este é um teste com stream persistente.")
    player.play_text("Agora as pausas entre as frases devem sumir.")
    player.stop()