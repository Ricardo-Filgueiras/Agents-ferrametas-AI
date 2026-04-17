import os
import requests
import site

def download_alexa():
    # Tenta localizar a pasta da biblioteca
    packages = site.getsitepackages()
    target_dir = None
    for p in packages:
        test_path = os.path.join(p, "openwakeword", "resources", "models")
        if os.path.exists(os.path.dirname(test_path)):
            target_dir = test_path
            break
    
    if not target_dir:
        print("Não foi possível localizar a pasta do openwakeword.")
        return

    os.makedirs(target_dir, exist_ok=True)
    url = "https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/alexa_v0.1.onnx"
    dest = os.path.join(target_dir, "alexa_v0.1.onnx")
    
    print(f"Baixando modelo para {dest}...")
    r = requests.get(url)
    with open(dest, 'wb') as f:
        f.write(r.content)
    print("Download concluído.")

if __name__ == "__main__":
    download_alexa()
