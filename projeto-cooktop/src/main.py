import sys
import os

# Adiciona o diretório raiz ao path antes de qualquer import do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_core.messages import HumanMessage
from src.graph.pipeline import app

def run_kitchen():
    print("\n" + "="*50)
    print("      🎂 BEM-VINDO À COZINHA DIGITAL 🎂")
    print("="*50 + "\n")
    
    # 1. Captura o pedido do usuário
    cake_order = input("Qual bolo deseja preparar hoje? (ex: Bolo de Chocolate): ")
    
    if not cake_order:
        print("Nenhum pedido feito. Fechando a cozinha...")
        return

    # 2. Inicializa o Estado da Tigela
    initial_state = {
        "messages": [HumanMessage(content=cake_order)],
        "tigela": [],
        "status_massa": "crua",
        "temperatura_forno": 0,
        "nota_inspetor": 0.0
    }

    # 3. Configuração de Execução (Ollama local por padrão)
    config = {"configurable": {"thread_id": "cozinha_01"}}

    print(f"\n🚀 Iniciando o preparo do: {cake_order}\n")
    print("-" * 30)

    # 4. Executa o Grafo e mostra a evolução em tempo real
    try:
        # Usamos stream para ver cada agente agindo
        for output in app.stream(initial_state, config):
            for node_name, result in output.items():
                print(f"\n👨‍🍳 AGENTE: {node_name.upper()}")
                
                # Se houver mensagens, mostra a última resposta da IA
                if "messages" in result:
                    last_msg = result["messages"][-1]
                    # Limita o texto para não poluir o terminal se for muito longo
                    content = last_msg.content[:200] + "..." if len(last_msg.content) > 200 else last_msg.content
                    print(f"💬 Resposta: {content}")
                
                # Mostra o status da tigela conforme ela evolui
                if "status_massa" in result:
                    print(f"🥣 Status da Massa: {result['status_massa']}")
                
                if "tigela" in result and result["tigela"]:
                    print(f"📦 Ingredientes na Tigela: {', '.join(result['tigela'])}")
                
                print("-" * 30)

        print("\n✅ PROCESSO FINALIZADO!")
        print("Verifique o arquivo 'data/caderno.md' para ver os registros do Inspetor.")

    except Exception as e:
        print(f"\n❌ ERRO NA COZINHA: {e}")

if __name__ == "__main__":
    # Garante que o diretório raiz está no path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    run_kitchen()
