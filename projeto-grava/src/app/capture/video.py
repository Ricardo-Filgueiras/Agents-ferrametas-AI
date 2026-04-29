from fractions import Fraction

import av
import cv2
import numpy as np

# 90kHz é o clock padrão para H.264 — resolução suficiente para representar
# qualquer frame rate sem truncamento que cause PTS duplicado.
_TIME_BASE = Fraction(1, 90000)
_PTS_STEP_30FPS = int(_TIME_BASE.denominator / 30)  # 3000 ticks por frame


def bgr_para_av_frame(bgr: np.ndarray, capture_time: float) -> av.VideoFrame:
    """Converte um frame BGR (numpy) capturado pelo MSS num av.VideoFrame yuv420p."""
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    frame = av.VideoFrame.from_ndarray(rgb, format='rgb24')
    frame = frame.reformat(format='yuv420p')
    frame.pts = int(capture_time * _TIME_BASE.denominator)
    frame.time_base = _TIME_BASE
    return frame


def _configurar_stream(vstream, frame):
    """
    Configura o codec H.264 para gravação real-time sem buffering.

    Três configurações eliminam o problema de freeze juntas:
      1. max_b_frames = 0  → desativa B-frames (causa principal do buffer).
      2. tune=zerolatency  → desativa o lookahead do x264.
      3. gop_size = 30     → keyframe a cada 1 s (30 frames).
    """
    ctx = vstream.codec_context
    ctx.width = frame.width
    ctx.height = frame.height
    ctx.pix_fmt = 'yuv420p'
    ctx.time_base = _TIME_BASE
    ctx.framerate = 30
    ctx.max_b_frames = 0
    ctx.gop_size = 30
    ctx.bit_rate = 4_000_000 if frame.height > 720 else 2_000_000
    ctx.options = {'preset': 'ultrafast', 'tune': 'zerolatency'}


def processa_video_container(container_video, frames_de_video, vstream, v_start_time, last_pts=-1):
    if not frames_de_video:
        return vstream, v_start_time, last_pts

    for frame in frames_de_video:
        if vstream is None:
            vstream = container_video.add_stream('libx264')
            _configurar_stream(vstream, frame)
            v_start_time = frame.time if frame.time is not None else 0.0

        if frame.time is not None:
            pts = int((frame.time - v_start_time) / _TIME_BASE)
        else:
            pts = last_pts + _PTS_STEP_30FPS

        pts = max(pts, last_pts + 1)
        last_pts = pts

        if frame.format.name != 'yuv420p':
            frame = frame.reformat(format='yuv420p')

        frame.pts = pts
        frame.time_base = _TIME_BASE

        for packet in vstream.encode(frame):
            packet.time_base = _TIME_BASE
            if packet.dts is None:
                packet.dts = packet.pts
            container_video.mux(packet)

    return vstream, v_start_time, last_pts


def flush_container(container_video, vstream, astream):
    if container_video:
        if vstream:
            for packet in vstream.encode():
                packet.time_base = vstream.time_base
                if packet.dts is None:
                    packet.dts = packet.pts
                container_video.mux(packet)
        if astream:
            for packet in astream.encode():
                packet.time_base = astream.time_base
                container_video.mux(packet)
        container_video.close()
