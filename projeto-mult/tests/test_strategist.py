"""
🧪 TEST & INTEGRATION - STRATEGIST AGENT
========================================
Scripts de teste para o agente Strategist.

Como usar:
    python tests/test_strategist.py
"""

import sys
import os
from pathlib import Path

# Adicionar path do projeto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.strategist.agent import get_strategist, get_llm_strategist
from src.workflows.strategist_workflow import run_strategist_workflow


# ============================================================================
# TEST 1: Verificar configuração de modelos
# ============================================================================

def test_model_configuration():
    """Testa se os modelos estão configurados corretamente."""
    
    print("\n" + "="*70)
    print("🧪 TEST 1: Model Configuration")
    print("="*70)
    
    print("\n📋 Variáveis de Ambiente:")
    print(f"  OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'NÃO DEFINIDO')}")
    print(f"  BASE_MODEL: {os.getenv('BASE_MODEL', 'NÃO DEFINIDO')}")
    print(f"  GOOGLE_API_KEY: {'✅ Definida' if os.getenv('GOOGLE_API_KEY') else '❌ Não definida'}")
    print(f"  OPENAI_API_KEY: {'✅ Definida' if os.getenv('OPENAI_API_KEY') else '❌ Não definida'}")
    
    print("\n🔍 Testando obtenção de LLM...")
    try:
        llm = get_llm_strategist()
        print(f"✅ LLM obtido com sucesso!")
        print(f"   Tipo: {type(llm).__name__}")
        return True
    except Exception as e:
        print(f"❌ Erro ao obter LLM: {e}")
        return False


# ============================================================================
# TEST 2: Criar agente Strategist
# ============================================================================

def test_strategist_creation():
    """Testa criação do agente."""
    
    print("\n" + "="*70)
    print("🧪 TEST 2: Strategist Creation")
    print("="*70)
    
    print("\n🔨 Criando agente Strategist...")
    try:
        strategist = get_strategist()
        print(f"✅ Agente criado com sucesso!")
        print(f"   Nome: {strategist.name}")
        print(f"   Role: {strategist.role}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# TEST 3: Análise simples
# ============================================================================

def test_simple_analysis():
    """Testa análise simples com o agente."""
    
    print("\n" + "="*70)
    print("🧪 TEST 3: Simple Analysis")
    print("="*70)
    
    strategist = get_strategist()
    
    prompt = """
    Tema: Introdução a LangGraph
    Keywords: langgraph, agentes, workflows, llm
    
    Faça uma análise rápida de 3 parágrafos sobre a viabilidade deste tema para conteúdo.
    Seja direto e prático.
    """
    
    print("\n⏳ Executando análise (pode levar alguns segundos)...\n")
    
    try:
        result = strategist.run(prompt)
        response = result.content if hasattr(result, 'content') else result
        
        print("✅ Análise completada!")
        print("\n📝 Resposta:")
        print("-" * 70)
        print(str(response)[:500])  # Primeiros 500 caracteres
        print("-" * 70)
        return True
    
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# TEST 4: Workflow completo
# ============================================================================

def test_complete_workflow():
    """Testa o workflow completo."""
    
    print("\n" + "="*70)
    print("🧪 TEST 4: Complete Workflow")
    print("="*70)
    
    print("\n⏳ Executando workflow completo...\n")
    
    try:
        result = run_strategist_workflow(
            topic="Python e Machine Learning",
            keywords=["python ml", "machine learning", "data science"],
            target_audience="Desenvolvedores interessados em ML"
        )
        
        print("\n" + "="*70)
        print("✅ Workflow Completado!")
        print("="*70)
        
        print(f"\nFase Final: {result['current_phase']}")
        print(f"Iterações: {result['iteration_count']}")
        print(f"Histórico de Análises: {len(result['analysis_history'])} etapas")
        
        if result["error_message"]:
            print(f"⚠️  Erro: {result['error_message']}")
            return False
        
        if result["strategy_plan"]:
            plan = result["strategy_plan"]
            print(f"\n✅ Plano Estratégico Gerado:")
            
            # Tenta acessar atributos de forma segura
            try:
                attrs = {}
                for attr in ['title', 'category', 'outline', 'primary_keywords', 'estimated_word_count']:
                    if hasattr(plan, attr):
                        attrs[attr] = getattr(plan, attr)
                
                for key, value in attrs.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} itens")
                    else:
                        print(f"   {key}: {str(value)[:60]}...")
            except:
                print(f"   {str(plan)[:200]}...")
            
            return True
        
        return False
    
    except Exception as e:
        print(f"❌ Erro no workflow: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# RUNNER
# ============================================================================

def run_all_tests():
    """Executa todos os testes."""
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + "TESTE DO AGENTE STRATEGIST".center(68) + "║")
    print("║" + " ReAct Pattern com LangGraph".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Model Configuration", test_model_configuration),
        ("Strategist Creation", test_strategist_creation),
        ("Simple Analysis", test_simple_analysis),
        ("Complete Workflow", test_complete_workflow),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"  {test_name:<30} {status}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    print("="*70 + "\n")
    
    return passed == total


# ============================================================================
# QUICK START
# ============================================================================

def quick_start():
    """Início rápido: usa o agente sem testes."""
    
    print("\n🚀 QUICK START - STRATEGIST AGENT\n")
    
    strategist = get_strategist()
    
    tema = input("📝 Digite um tema: ").strip()
    if not tema:
        tema = "Python Performance Optimization"
    
    keywords_str = input("🔑 Digite keywords (separadas por vírgula): ").strip()
    if not keywords_str:
        keywords = ["python", "performance", "optimization"]
    else:
        keywords = [k.strip() for k in keywords_str.split(",")]
    
    print(f"\n⏳ Analisando '{tema}'...\n")
    
    prompt = f"""
    Tema: {tema}
    Keywords: {', '.join(keywords)}
    
    Realize uma análise estratégica breve (2-3 parágrafos) sobre:
    1. Viabilidade do tema
    2. Potencial de mercado
    3. Como se diferenciar
    """
    
    try:
        result = strategist.run(prompt)
        response = result.content if hasattr(result, 'content') else result
        print("✅ Análise Concluída!\n")
        print(response)
    except Exception as e:
        print(f"❌ Erro: {e}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            quick_start()
        elif command == "test":
            success = run_all_tests()
            sys.exit(0 if success else 1)
        else:
            print(f"Comando desconhecido: {command}")
            print("\nUsos:")
            print("  python tests/test_strategist.py test      # Executar testes")
            print("  python tests/test_strategist.py quick     # Quick start interativo")
    else:
        # Padrão: executar todos os testes
        run_all_tests()
