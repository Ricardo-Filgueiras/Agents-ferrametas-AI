"""
Captura a tela em tempo real durante a gravação da reunião via MSS.
Os frames são entregues como tuplas (bgr_array, capture_time) numa queue
thread-safe para consumo pelo loop principal do PyAV.
"""

import queue
import threading
import time

import cv2
import mss
import numpy as np


class ScreenRecorder:
    def __init__(self, fps: int = 15, monitor_idx: int = 1):
        self.fps = fps
        self.monitor_idx = monitor_idx
        self.frame_queue: queue.Queue = queue.Queue(maxsize=fps * 2)
        self.recording = False
        self._thread: threading.Thread | None = None

    def start(self):
        self.recording = True
        self._thread = threading.Thread(target=self._record, daemon=True)
        self._thread.start()

    def stop(self):
        self.recording = False
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _record(self):
        interval = 1.0 / self.fps
        with mss.mss() as sct:
            monitor = sct.monitors[self.monitor_idx]
            while self.recording:
                t0 = time.monotonic()

                img = np.array(sct.grab(monitor))
                bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                capture_time = time.monotonic()

                # Descarta o frame mais antigo se a queue estiver cheia
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass

                try:
                    self.frame_queue.put_nowait((bgr, capture_time))
                except queue.Full:
                    pass

                sleep_time = interval - (time.monotonic() - t0)
                if sleep_time > 0:
                    time.sleep(sleep_time)
