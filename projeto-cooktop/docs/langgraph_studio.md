# 🎨 Visualizando com LangGraph Studio

O LangGraph Studio permite que você visualize a "Tigela" (Estado) evoluindo e os agentes conversando em uma interface gráfica em tempo real.

## 🛠️ Preparação

### 1. Requisitos
*   **LangGraph Studio** instalado (disponível para macOS e Windows).
*   **Docker** rodando no seu computador (necessário para o Studio).
*   **Ollama** configurado para aceitar conexões externas (se rodando fora do Docker).

### 2. Configuração do Ollama para o Studio
Como o Studio roda dentro de um container Docker, ele precisa conseguir "enxergar" o seu Ollama local.
*   No Windows, certifique-se de que a variável de ambiente `OLLAMA_HOST` está definida como `0.0.0.0`.
*   No seu arquivo `.env`, use:
    ```env
    OLLAMA_API_URL=http://host.docker.internal:11434
    ```

## 🚀 Como Abrir

1.  Abra o aplicativo **LangGraph Studio**.
2.  Clique em **"Select a directory"** e escolha a pasta raiz deste projeto.
3.  O Studio lerá o arquivo `langgraph.json` e carregará o grafo `kitchen`.

## 🥣 O que observar no Studio

*   **Graph View**: Você verá o fluxo: `START -> sous_chef -> confeiteiro -> inspector -> quality_check`.
*   **State View**: À direita, você pode abrir a "Tigela" e ver a lista de `ingredients` e o `status_massa` mudando conforme os agentes agem.
*   **Threads**: Você pode pausar, voltar no tempo e editar o estado da tigela manualmente para testar cenários (ex: "E se eu tirar os ovos agora?").

## 📝 Solução de Problemas
*   **Erro de Conexão com LLM**: Verifique se o `OLLAMA_API_URL` está usando `host.docker.internal`.
*   **Dependências**: O Studio criará um ambiente isolado. Se faltar algum pacote, verifique se ele está listado no `requirements.txt`.
