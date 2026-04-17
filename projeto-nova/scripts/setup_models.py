import os
import requests
from tqdm import tqdm

def download_file(url, dest):
    if os.path.exists(dest):
        print(f"Arquivo já existe: {dest}")
        return
    
    print(f"Baixando {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest, 'wb') as f, tqdm(
        total=total_size,
        unit='iB',
        unit_scale=True,
        desc=dest.split('/')[-1]
    ) as pbar:
        for data in response.iter_content(1024):
            size = f.write(data)
            pbar.update(size)

def main():
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    # URLs do modelo Piper Faber (PT-BR)
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/"
    files = ["pt_BR-faber-medium.onnx", "pt_BR-faber-medium.onnx.json"]
    
    for file in files:
        download_file(base_url + file, os.path.join(models_dir, file))
    
    print("\nModelos baixados com sucesso em ./models/")

if __name__ == "__main__":
    # Adiciona requests e tqdm ao requirements se não existirem
    main()
