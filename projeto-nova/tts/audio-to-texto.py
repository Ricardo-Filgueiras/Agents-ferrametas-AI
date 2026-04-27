import whisper
import os
import sys
from datetime import datetime

def transcribe_audio(audio_path):
    """
    Transcreve um arquivo de áudio para texto e salva em um arquivo .md
    """
    if not os.path.exists(audio_path):
        print(f"❌ Erro: Arquivo '{audio_path}' não encontrado.")
        return

    try:
        # O modelo 'base' é um bom equilíbrio entre velocidade e precisão.
        # Opções: 'tiny', 'base', 'small', 'medium', 'large'
        print(f"📦 Carregando modelo Whisper (base)...")
        model = whisper.load_model("base")

        print(f"🎙️ Transcrevendo: {os.path.basename(audio_path)}...")
        # fp16=False é usado para evitar avisos em CPUs sem suporte a meia precisão
        result = model.transcribe(audio_path, fp16=False)
        
        text = result['text'].strip()
        
        # Gerar nome do arquivo de saída .md
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_file = f"{base_name}_transcricao.md"
        output_path = os.path.join(os.path.dirname(audio_path), output_file)
        
        # Criar conteúdo Markdown formatado
        md_content = f"""# Transcrição de Áudio
---
**Arquivo Original:** `{os.path.basename(audio_path)}`
**Data da Transcrição:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
**Modelo Utilizado:** `Whisper (base)`

## 📝 Texto Transcrito

{text}

---
*Gerado automaticamente por Agents-ferrametas-AI*
"""
        
        # Salvar o arquivo
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"✅ Sucesso! Transcrição salva em: {output_file}")
        
    except Exception as e:
        print(f"⚠️ Ocorreu um erro durante a transcrição: {e}")
        print("\nCertifique-se de que o 'ffmpeg' está instalado no seu sistema.")

if __name__ == "__main__":
    # Verifica se um arquivo foi passado como argumento
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        # Busca automática por arquivos de áudio comuns no diretório atual
        extensions = ('.ogg', '.mp3', '.wav', '.m4a', '.flac')
        files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]
        
        if files:
            # Ordena por data de modificação para pegar o mais recente
            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            audio_file = files[0]
            print(f"ℹ️ Nenhum arquivo especificado. Usando o mais recente encontrado: {audio_file}")
        else:
            print("❌ Nenhum arquivo de áudio encontrado no diretório.")
            print("Uso: python audio-to-texto.py <caminho_do_audio>")
            sys.exit(1)

    transcribe_audio(audio_file)
