# Planejamento de Atualização e Evolução - Docstóteles

Este documento detalha a avaliação técnica sobre a modernização do projeto utilizando Docker, Django e a expansão do ecossistema LangChain, com base nos requisitos de escalabilidade e visão de produto.

---

### 1. 🚀 Migração para Django (Interface e Backend)
Atualmente em Streamlit, a migração para Django transforma o projeto de um script de teste em uma aplicação web robusta.

*   **Gestão de Usuários e Privacidade:** Implementação de autenticação nativa para garantir que cada usuário gerencie suas próprias coleções e históricos de chat de forma isolada.
*   **Persistência de Dados (ORM):** Substituição do estado temporário (`st.session_state`) por um banco de dados relacional (PostgreSQL/SQLite), permitindo que o histórico de conversas sobreviva a recarregamentos de página.
*   **Tarefas Assíncronas (Celery + Redis):** Otimização do processo de scraping. O usuário inicia a raspagem de um site e pode continuar navegando, recebendo uma notificação quando a coleção estiver indexada e pronta.
*   **Arquitetura de API:** Preparação do sistema para ser consumido por outros clientes (Apps mobile, bots de Telegram/Discord) via Django REST Framework.

### 2. 🤖 Expansão do LangChain (Agentes e Memória)
Evolução do RAG passivo para um Agente Inteligente ativo.

*   **Scraping como "Tool":** Transformar a lógica do Firecrawl em uma ferramenta que o agente pode decidir usar autonomamente quando não encontrar a resposta na base de dados local.
*   **Memória Conversacional Nativa:** Uso de `ConversationalRetrievalChain` e `ConversationBufferMemory` para manter o contexto fluido de uma conversa de múltiplos turnos.
*   **Abstração de Provedores:** Facilidade para alternar entre Groq (velocidade), OpenAI (raciocínio complexo) ou Anthropic sem alterar a lógica de negócio.

### 3. 🐳 Containerização com Docker
Tornar o ambiente de desenvolvimento e produção idêntico e isolado.

*   **Padronização de Ambiente:** Resolve conflitos de caminhos de arquivos e dependências de sistema (especialmente críticas para bibliotecas como FAISS e HuggingFace).
*   **Orquestração de Serviços:** Uso de `docker-compose` para gerenciar simultaneamente a aplicação, o banco de dados vetorial, o banco de dados relacional e as filas de processamento assíncrono.

---

### 📊 Veredito de Implementação

| Perfil de Uso | Recomendação Técnica |
| :--- | :--- |
| **Estudo e POC** | Manter Streamlit + FAISS local. Foco em refinar os prompts e o fatiamento de documentos. |
| **Produto/SaaS** | **Migrar para Django + Docker + LangChain Agents.** Soluciona gargalos de UI, privacidade e estabilidade. |

### 🛠️ Próximos Passos Sugeridos
1.  **Imediato:** Adicionar Docker ao projeto atual para garantir portabilidade.
2.  **Curto Prazo:** Implementar a persistência do índice FAISS em disco para evitar re-indexação constante.
3.  **Médio Prazo:** Migrar para Django se houver necessidade de múltiplos usuários e controle de acesso.
