import threading
import signal
import sys
import logging
import os
from dotenv import load_dotenv
from app.core.state import AgentState
from app.core.engine import NovaEngine
from app.ui.dashboard import Dashboard

# Carrega configurações do .env
load_dotenv()

# Configuração de Logging para arquivo (Observabilidade para o Desenvolvedor)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nova.log", encoding='utf-8')
    ]
)
logger = logging.getLogger("NovaMain")

def main():
    """Ponto de entrada principal da Nova Agent v2."""
    logger.info("Sistema Nova Agent v2 iniciando...")
    
    # 1. Inicializa o Estado Compartilhado (Ponto de Verdade Único)
    state = AgentState()
    
    # 2. Instancia os Componentes Principais
    try:
        # A Engine coordena STT, LLM (via AgentController), TTS e Hardware
        engine = NovaEngine(state)
        # O Dashboard observa o 'state' e renderiza a TUI
        dashboard = Dashboard(state)
    except Exception as e:
        logger.error(f"Falha crítica na inicialização dos componentes: {e}", exc_info=True)
        print(f"Erro ao iniciar o sistema. Verifique o arquivo nova.log para detalhes.")
        sys.exit(1)
    
    # 3. Handler para encerramento gracioso (Ctrl+C)
    def signal_handler(sig, frame):
        logger.info("Sinal de encerramento recebido.")
        state.is_running = False
        state.set_action("Encerrando sistema...")
        # Pequeno delay para a TUI mostrar o status de encerramento
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    # 4. Inicia a Inteligência (Engine) em uma Thread separada
    # Isso permite que o Dashboard (Rich) rode na thread principal
    engine_thread = threading.Thread(target=engine.start, name="EngineThread", daemon=True)
    engine_thread.start()
    
    logger.info("Threads de execução iniciadas com sucesso.")

    # 5. Inicia a Interface de Status (Bloqueante)
    try:
        # dashboard.run() manterá o terminal ocupado renderizando o estado
        dashboard.run()
    except KeyboardInterrupt:
        state.is_running = False
    except Exception as e:
        logger.error(f"Erro na thread de interface: {e}")
    finally:
        logger.info("Nova Agent encerrada.")

if __name__ == "__main__":
    main()
