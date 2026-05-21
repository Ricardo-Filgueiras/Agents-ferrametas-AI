# Plano de Implementação: Workspace Copilot Avançado

Este documento detalha a transição da interface simples do Blog Engine para um ambiente de trabalho tipo "Copilot", permitindo interação em tempo real, visualização do fluxo de agentes e edição iterativa.

## 🏗️ Nova Arquitetura de UI (Streamlit)

Dividiremos a tela principal em um layout de duas colunas principais para simular o ambiente de um Workspace de IA moderno.

### 1. Coluna de Interação (Chat & Status) - 40% da tela
- **Chat History:** Utilizará `st.chat_message` para manter o contexto da conversa com o agente mestre.
- **Streaming de Status:** Usaremos o componente `st.status` (disponível no Streamlit moderno) para exibir as etapas do LangGraph em tempo real:
    - `🔍 Pesquisando tendências...`
    - `✍️ Redigindo rascunho...`
    - `🧐 Revisando SEO e qualidade...`
- **Input:** `st.chat_input` sempre visível no rodapé desta coluna.

### 2. Coluna de Resultado (Preview & Editor) - 60% da tela
- **Tabs Dinâmicas:** 
    - `📖 Preview`: Renderização do Markdown final com CSS customizado para leitura.
    - `📝 Editor`: Um campo `st.text_area` ou `st_ace` que carrega o `draft` atual, permitindo que o usuário faça ajustes manuais finos.
- **Sincronização:** Alterações no Editor atualizam o `st.session_state["draft"]`, que pode ser lido pelos agentes no chat para próximas iterações.

---

## 🛠️ Contornando as Restrições de Seleção

Como o Streamlit não detecta nativamente a seleção de texto com o mouse para disparar ações:
- **Estratégia:** Adotaremos o padrão de **"Referência por Contexto"**.
- O usuário dirá no chat: *"No parágrafo sobre 'Custos de Nuvem', adicione um exemplo real"*.
- O agente receberá o `draft` completo + o pedido do usuário e usará o nó `Writer` para realizar a edição cirúrgica.

---

## ❓ Perguntas para Decisão Técnica

1. **Modelo de Edição:** Deseja que o Chat seja a ÚNICA forma de editar (Agente faz tudo) ou quer o "Modelo Misto" (O Agente escreve, mas você pode apagar uma vírgula ou trocar uma palavra manualmente no lado direito)?
2. **Histórico Global:** O chat deve ser limpo a cada novo artigo ou devemos manter uma sidebar com "Conversas Recentes"?
3. **Visibilidade do Grafo:** Além do texto (status), você gostaria de um pequeno diagrama Mermaid estático mostrando o caminho que o agente percorreu?

## ⚠️ Alerta de Performance
O streaming de eventos do LangGraph para o Streamlit exige o uso de `queue` ou `generators` para não bloquear a thread principal da UI. Precisaremos refatorar o `run_blog_pipeline` para ser uma função assíncrona que produz yields de estado.
