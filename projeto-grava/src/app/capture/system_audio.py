import queue
import threading

import numpy as np
import pydub
import pyaudiowpatch as pyaudio

CHUNK_DURATION_S = 10
FRAMES_PER_READ = 1024


def listar_dispositivos_loopback() -> list[dict]:
    """Retorna dispositivos loopback WASAPI disponíveis."""
    result = []
    try:
        p = pyaudio.PyAudio()
        for d in p.get_loopback_device_info_generator():
            result.append({
                'id': d['index'],
                'nome': d['name'],
                'channels': d['maxInputChannels'],
                'rate': int(d['defaultSampleRate']),
            })
        p.terminate()
    except Exception:
        pass
    return result


class SystemAudioCapture:
    def __init__(self, device: dict):
        self._device = device
        self._chunk_queue: queue.Queue = queue.Queue()
        self._buffer: list[bytes] = []
        self._buffer_frames = 0
        self._target_frames = device['rate'] * CHUNK_DURATION_S
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    def _capture_loop(self):
        p = pyaudio.PyAudio()
        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=self._device['channels'],
                rate=self._device['rate'],
                input=True,
                input_device_index=self._device['id'],
                frames_per_buffer=FRAMES_PER_READ,
            )
            while self._running:
                data = stream.read(FRAMES_PER_READ, exception_on_overflow=False)
                self._buffer.append(data)
                self._buffer_frames += FRAMES_PER_READ
                if self._buffer_frames >= self._target_frames:
                    self._flush_buffer()
            stream.stop_stream()
            stream.close()
        except Exception:
            self._running = False
        finally:
            p.terminate()

    def _flush_buffer(self):
        if not self._buffer:
            return
        raw = b''.join(self._buffer)
        self._buffer.clear()
        self._buffer_frames = 0
        segment = pydub.AudioSegment(
            data=raw,
            sample_width=2,
            frame_rate=self._device['rate'],
            channels=self._device['channels'],
        )
        self._chunk_queue.put(segment)

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        self._flush_buffer()

    def get_chunk(self) -> pydub.AudioSegment | None:
        try:
            return self._chunk_queue.get_nowait()
        except queue.Empty:
            return None
