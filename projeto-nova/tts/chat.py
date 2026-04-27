import sys
import os
import threading
import queue
import time
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from ollama_utils import get_ollama_models
from kokoro_stream import player, stream_kokoro_local

# Fila para gerenciar as frases a serem faladas
audio_queue = queue.Queue()

def limpar_texto_para_tts(texto):
    """Prepara o texto para ser falado, tratando siglas e limpando markdown."""
    # 1. Limpeza de Markdown e Quebras de linha excessivas
    texto = texto.replace('*', '').replace('#', '').replace('`', '').replace('**', '')
    texto = texto.replace('\n', ' ') # Transforma quebras de linha em espaços para fluidez
    
    # 2. Dicionário Fonético (Ajuste Fino de Pronúncia)
    substituicoes = {
        "SQL": "ésse quê éle",
        "BI": "bê í",
        "Python": "paiton",
        "AI": "ai",
        "IA": "i á",
        "LLM": "éle éle éme",
        "Ollama": "olama",
        "Alura": "alura",
        "Nova": "nôva",
    }
    
    for sigla, fonetica in substituicoes.items():
        texto = texto.replace(f" {sigla} ", f" {fonetica} ")
        texto = texto.replace(f"{sigla} ", f"{fonetica} ")
        texto = texto.replace(f" {sigla}", f" {fonetica}")
    
    return texto.strip()

def tts_worker():
    """Worker que fica em segundo plano processando a fila de áudio."""
    while True:
        texto = audio_queue.get()
        if texto is None: 
            break
        
        texto_para_falar = limpar_texto_para_tts(texto)
        
        if texto_para_falar:
            # Reduzimos o delay para quase zero, pois a pontuação já cuida das pausas
            stream_kokoro_local(texto_para_falar)
            
        audio_queue.task_done()

def load_system_prompt(filepath):
    """Carrega o prompt de sistema de um arquivo externo."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            print(f"⚠️ Aviso: Arquivo de sistema '{filepath}' não encontrado. Usando prompt padrão.")
            return "Você é um assistente útil."
    except Exception as e:
        print(f"❌ Erro ao ler arquivo de sistema: {e}")
        return "Você é um assistente útil."

def main():
    print("\n" + "="*50)
    print("      🤖 BEM-VINDO AO TERMINAL CHAT (LLM LOCAL)      ")
    print("="*50 + "\n")

    # 1. Carregar Prompt de Sistema (SYSTEM.md)
    # Tenta carregar SYSTEM.md da pasta atual ou da pasta tts/
    prompt_path = "tts/SYSTEM.md" if os.path.exists("tts/SYSTEM.md") else "SYSTEM.md"
    system_content = load_system_prompt(prompt_path)
    
    # 2. Listar e escolher o modelo
    modelos = get_ollama_models()
    
    if not modelos:
        print("❌ Nenhum modelo encontrado no Ollama. Saindo...")
        return

    print("📦 Modelos disponíveis:")
    for i, model in enumerate(modelos):
        print(f"  [{i}] {model}")
    
    try:
        escolha = int(input("\n👉 Escolha o número do modelo para o chat: "))
        if 0 <= escolha < len(modelos):
            model_name = modelos[escolha]
        else:
            print("❌ Escolha inválida. Usando o primeiro da lista.")
            model_name = modelos[0]
    except ValueError:
        print("❌ Entrada inválida. Usando o primeiro da lista.")
        model_name = modelos[0]

    print(f"\n✅ Iniciando chat com o modelo: {model_name}")
    print(f"📝 Prompt de sistema carregado de: {prompt_path}")
    print("--- Digite 'sair' para encerrar o chat ---\n")

    # Inicializa o hardware de áudio
    player.start()

    # Iniciar a thread de TTS
    worker_thread = threading.Thread(target=tts_worker, daemon=True)
    worker_thread.start()

    # 3. Configurar LangChain
    llm = ChatOllama(model=model_name)
    
    # Adiciona a mensagem de sistema no início do histórico
    chat_history = [SystemMessage(content=system_content)]

    # 4. Loop de Chat
    try:
        while True:
            user_input = input("👤 Você: ")
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até logo!")
                audio_queue.put(None) # Encerra o worker
                player.stop() # Fecha o hardware de áudio
                break

            if not user_input.strip():
                continue

            chat_history.append(HumanMessage(content=user_input))

            print(f"🤖 {model_name}: ", end="", flush=True)
            
            full_response = ""
            sentence_buffer = ""
            
            try:
                for chunk in llm.stream(chat_history):
                    content = chunk.content
                    print(content, end="", flush=True)
                    
                    full_response += content
                    sentence_buffer += content
                    
                    # 1. Limpeza agressiva de markdown no buffer para evitar quebras erradas
                    # Removemos asteriscos e hashtags antes de procurar o ponto final
                    temp_clean = sentence_buffer.replace('*', '').replace('#', '').replace('**', '')

                    # 2. Lógica de streaming de áudio por sentença
                    # Só quebra se houver pontuação E se não for uma lista numerada (ex: "1. ")
                    if any(punct in temp_clean for punct in ['. ', '! ', '? ', '. \n', '! \n', '? \n']):
                        
                        # Regex simples ou lógica para evitar quebra em "1. ", "2. ", etc.
                        # Se o que vem antes do ponto for apenas números, não quebramos.
                        last_punct_idx = max(temp_clean.rfind('. '), temp_clean.rfind('! '), temp_clean.rfind('? '))
                        
                        if last_punct_idx != -1:
                            potential_sentence = temp_clean[:last_punct_idx+1].strip()
                            
                            # Verifica se é apenas um número seguido de ponto (ex: "1.")
                            # Se for, não enviamos para o áudio ainda, esperamos a frase completa.
                            if not (potential_sentence.isdigit() or (len(potential_sentence) <= 3 and potential_sentence[:-1].isdigit())):
                                audio_queue.put(potential_sentence)
                                # Limpamos do buffer original apenas o que já foi enviado
                                # (Aproximação baseada no tamanho do texto limpo)
                                sentence_buffer = sentence_buffer[len(sentence_buffer) - (len(temp_clean) - last_punct_idx - 1):]

                # Enviar o que sobrou no final
                final_clean = limpar_texto_para_tts(sentence_buffer)
                if final_clean:
                    audio_queue.put(final_clean)
                
                print("\n")
                chat_history.append(AIMessage(content=full_response))
                
            except Exception as e:
                print(f"\n❌ Erro ao processar resposta: {e}")
    except KeyboardInterrupt:
        print("\n👋 Chat interrompido.")
        audio_queue.put(None)

if __name__ == "__main__":
    main()
