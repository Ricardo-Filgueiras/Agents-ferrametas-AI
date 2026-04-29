import pydub
from fractions import Fraction


def adiciona_chunck_audio(frames_de_audio, audio_chunck):
    for frame in frames_de_audio:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels),
        )
        audio_chunck += sound
    return audio_chunck


def processa_audio_container(container_video, frames_de_audio, astream, a_start_time):
    if container_video and frames_de_audio:
        for frame in frames_de_audio:
            if astream is None:
                astream = container_video.add_stream('aac')
                astream.time_base = Fraction(1, frame.sample_rate)
                a_start_time = frame.time

            # Ajuste de PTS e Timebase
            frame.pts = int((frame.time - a_start_time) / astream.time_base)
            for packet in astream.encode(frame):
                packet.time_base = astream.time_base
                container_video.mux(packet)
    return astream, a_start_time
