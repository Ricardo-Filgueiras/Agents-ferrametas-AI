# Base com CUDA 11.8 (compatível com GTX 1660)
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 1. Instalar dependências de sistema (Áudio, Python, FFmpeg)
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    portaudio19-dev \
    python3-pyaudio \
    libsndfile1 \
    ffmpeg \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar Piper TTS (Binário)
RUN wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz \
    && tar -xvf piper_amd64.tar.gz \
    && mv piper/piper /usr/local/bin/ \
    && mv piper/*.so* /usr/local/lib/ \
    && rm -rf piper piper_amd64.tar.gz
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# 3. Atualiza pip e instala requirements
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o código e modelos
COPY . .

# Garante permissões de execução
RUN chmod +x main.py

CMD ["python3", "main.py"]
