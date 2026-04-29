"""
MixedAudioCapture — captura microfone (WebRTC) e áudio do sistema (WASAPI)
simultaneamente, produzindo chunks mesclados via pydub.overlay().

Fluxo:
  1. Loop WebRTC chama add_mic_frames() a cada batch de frames (~20 ms cada).
  2. SystemAudioCapture chama add_system_chunk() a cada chunk de 10 s.
  3. Quando ambos os buffers têm >= chunk_duration_s segundos, _try_flush()
     corta, faz overlay e enfileira o segmento mesclado.
  4. O loop principal consome get_chunk() e envia para o Whisper.
"""

import queue
import threading
import pydub


class MixedAudioCapture:
    """
    Mistura áudio de microfone (frames WebRTC) e áudio do sistema (WASAPI)
    em chunks prontos para transcrição.

    Args:
        chunk_duration_s: Duração alvo de cada chunk de saída (segundos).
        mic_gain_db: Ganho aplicado ao microfone antes do mix (dB). Use 0 para neutro.
        sys_gain_db: Ganho aplicado ao áudio do sistema antes do mix (dB).
    """

    def __init__(
        self,
        chunk_duration_s: int = 5,
        mic_gain_db: float = 0.0,
        sys_gain_db: float = -3.0,  # sistema ligeiramente mais baixo por padrão
    ):
        self._chunk_duration_ms = chunk_duration_s * 1000
        self._mic_gain_db = mic_gain_db
        self._sys_gain_db = sys_gain_db

        self._mic_buffer = pydub.AudioSegment.empty()
        self._sys_buffer = pydub.AudioSegment.empty()
        self._output_queue: queue.Queue = queue.Queue()
        self._lock = threading.Lock()

    # ── Entrada de áudio ────────────────────────────────────────────────────

    def add_mic_frames(self, frames) -> None:
        """Alimenta o mixer com frames de áudio do WebRTC (av.AudioFrame)."""
        for frame in frames:
            segment = pydub.AudioSegment(
                data=frame.to_ndarray().tobytes(),
                sample_width=frame.format.bytes,
                frame_rate=frame.sample_rate,
                channels=len(frame.layout.channels),
            )
            with self._lock:
                self._mic_buffer += segment
        self._try_flush()

    def add_system_chunk(self, chunk: pydub.AudioSegment) -> None:
        """Alimenta o mixer com um chunk do SystemAudioCapture."""
        with self._lock:
            self._sys_buffer += chunk
        self._try_flush()

    # ── Mix interno ─────────────────────────────────────────────────────────

    def _try_flush(self) -> None:
        """
        Quando ambos os buffers têm dados suficientes, faz o mix e enfileira.
        Garante que nenhum buffer fique vazio antes do overlay.
        """
        with self._lock:
            mic_ms = len(self._mic_buffer)
            sys_ms = len(self._sys_buffer)
            cut_ms = min(mic_ms, sys_ms, self._chunk_duration_ms)

            if cut_ms < self._chunk_duration_ms:
                return  # Aguarda mais dados de ambas as fontes

            mic_slice = self._mic_buffer[:cut_ms]
            sys_slice = self._sys_buffer[:cut_ms]
            self._mic_buffer = self._mic_buffer[cut_ms:]
            self._sys_buffer = self._sys_buffer[cut_ms:]

        # Aplica ganho e normaliza para o mesmo sample rate / canais antes do mix
        mic_slice = self._normalizar(mic_slice + self._mic_gain_db)
        sys_slice = self._normalizar(sys_slice + self._sys_gain_db)

        # overlay: soma as duas ondas (sem clipping, pydub cuida disso)
        mixed = mic_slice.overlay(sys_slice)
        self._output_queue.put(mixed)

    @staticmethod
    def _normalizar(seg: pydub.AudioSegment) -> pydub.AudioSegment:
        """Converte para mono 16-bit 16kHz — formato ideal para o Whisper."""
        return (
            seg.set_channels(1)
               .set_sample_width(2)
               .set_frame_rate(16_000)
        )

    # ── Saída ────────────────────────────────────────────────────────────────

    def get_chunk(self) -> pydub.AudioSegment | None:
        """Retorna o próximo chunk mesclado ou None se não houver dados."""
        try:
            return self._output_queue.get_nowait()
        except queue.Empty:
            return None

    def flush_remaining(self) -> pydub.AudioSegment | None:
        """
        Chamado ao parar a gravação: força o mix do que restou nos buffers,
        mesmo que seja menos que chunk_duration_ms.
        """
        with self._lock:
            mic_ms = len(self._mic_buffer)
            sys_ms = len(self._sys_buffer)

            if mic_ms == 0 and sys_ms == 0:
                return None

            # Usa o buffer menor como corte
            cut_ms = min(mic_ms, sys_ms) if mic_ms > 0 and sys_ms > 0 else max(mic_ms, sys_ms)

            mic_slice = self._mic_buffer[:cut_ms] if mic_ms > 0 else pydub.AudioSegment.silent(cut_ms)
            sys_slice = self._sys_buffer[:cut_ms] if sys_ms > 0 else pydub.AudioSegment.silent(cut_ms)
            self._mic_buffer = pydub.AudioSegment.empty()
            self._sys_buffer = pydub.AudioSegment.empty()

        mic_slice = self._normalizar(mic_slice + self._mic_gain_db)
        sys_slice = self._normalizar(sys_slice + self._sys_gain_db)
        return mic_slice.overlay(sys_slice)
