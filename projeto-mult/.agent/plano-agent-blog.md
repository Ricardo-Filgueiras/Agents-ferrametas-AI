# Evolução para Multi-Agent Blog Engine (Lean Elite Team)

Este documento detalha o plano arquitetural para transformar o atual agente ReAct de chat genérico em um sistema multi-agente determinístico focado na criação de artigos otimizados para SEO. A abordagem utilizará "Equipes Enxutas de Elite" (uma pequena equipe de agentes super-especializados), contratos estritos com Pydantic e modelos locais (Ollama) para reduzir custos e garantir previsibilidade.

## ⚠️ User Review Required

Por favor, revise a nova topologia do grafo (abaixo) e as responsabilidades de cada agente. 
Se você aprovar, podemos iniciar a execução dessas etapas em nosso código.

## ❓ Open Questions

1. **Quais ferramentas de pesquisa (Tools)** você prefere que o Agente Pesquisador utilize? (ex: Tavily, DuckDuckGo, ou extração de dados locais/arquivos?)
2. Você já possui os **prompts específicos** para o redator de SEO e o revisor, ou quer que eu os crie seguindo as melhores práticas do mercado?
3. Há algum limite de iterações (loops de revisão) que devemos impor para evitar loops infinitos caso o texto não atinja a nota de SEO? (O padrão geralmente é máximo de 3 tentativas).

---

## 🏗️ Proposed Changes (Mudanças na Arquitetura)

Para suportar múltiplos agentes e fluxos determinísticos, a estrutura do projeto sofrerá as seguintes adaptações:

### 1. Separação do Estado e Contratos Rígidos (Pydantic)
Em vez de um estado genérico baseado apenas em um histórico de `messages`, adotaremos um estado central altamente tipado (Data-Driven Graph). 

#### [NEW] `src/core/schemas.py`
Definição de todos os contratos de dados que transitam pelo grafo usando Pydantic.
- `BlogState`: O estado global contendo os campos: `tema`, `pesquisa_bruta`, `rascunho`, `nota_seo`, `feedback_revisao`, `numero_revisoes`, `artigo_final`.
- `RevisorOutput`: Contrato de saída estruturada para o LLM do Revisor, obrigando-o a devolver (em JSON estrito): `nota_seo` (0-100) e `feedback` (lista de melhorias).

#### [MODIFY] `src/core/state.py`
Atualização da tipagem para refletir o novo modelo de estado.

---

### 2. Criação das "Equipes Enxutas" (Nós / Agentes Específicos)
Cada nó do grafo não será mais uma simples chamada "Genérica" de LLM, mas um agente especializado com uma Persona e objetivo único.

#### [NEW] `src/nodes/researcher.py`
- **Função:** Recebe o tema (topic) e usa ferramentas de busca para acumular contexto e keywords de SEO.
- **Saída no Estado:** Preenche a variável `pesquisa_bruta`.

#### [NEW] `src/nodes/writer.py`
- **Função:** Recebe o tema + a pesquisa bruta (e feedbacks anteriores, se houver) e escreve/refina o artigo focado em SEO.
- **Saída no Estado:** Preenche a variável `rascunho`.

#### [NEW] `src/nodes/reviewer.py`
- **Função:** Avalia o `rascunho` contra regras de SEO (Keywords, semântica, escaneabilidade, tamanho, H1/H2). **Crucial:** Utiliza o método `.with_structured_output(RevisorOutput)` para forçar o LLM local (Ollama) a responder um JSON determinístico ao invés de texto livre.
- **Saída no Estado:** Atualiza `nota_seo` e `feedback_revisao`.

#### [DELETE] `src/nodes/llm_nodes.py`
- Será removido/substituído pela estrutura fragmentada e especializada acima.

---

### 3. Topologia Determinística do Grafo

Em um MAS (Multi-Agent System) voltado à linha de produção, o grafo deixa de ser uma estrela reativa e passa a ser uma **Pipeline com Loop de Controle de Qualidade**.

#### [MODIFY] `src/agent.py` (ou `src/graphs/blog_graph.py`)
Novo Fluxo de Execução:
1. `START` ➡️ `Researcher`
2. `Researcher` ➡️ `Writer`
3. `Writer` ➡️ `Reviewer`
4. **Roteamento Condicional (`router_node`) pós Reviewer**:
   - Se `nota_seo` >= 85 ➡️ Vai para o nó `Publisher/Formatter` (ou `END`).
   - Se `nota_seo` < 85 e `numero_revisoes` < MAX_LIMIT ➡️ Volta para `Writer` (informando o `feedback_revisao`).
   - Se `numero_revisoes` >= MAX_LIMIT ➡️ Força a ida para `END` para evitar custo infinito.

---

### 4. Ajustes no Uso de Modelos Locais (Ollama)
Modelos locais (especialmente parâmetros menores como 8b/3b) precisam de truques extras para serem confiáveis com saídas JSON.
- **Ajuste:** Vamos configurar a flag `format="json"` nas invocações do nó Reviewer ou garantir que o LangChain esteja fazendo o parsing robusto do output do LLM para preencher o Pydantic corretamente.
- **Ajuste:** Prompts do sistema (System Messages) extremamente descritivos para cada agente (Persona Design).

---

### 5. Interface de Interação Escolhida (UX/UI)
Como o sistema se tornará um motor assíncrono e de múltiplas etapas, a CLI atual será substituída por uma interface web construída com **Streamlit**.

**Streamlit + LangGraph:** 
- **Por quê?** É a forma mais ágil de construir uma interface web visualmente rica usando puramente Python. Permite exibir claramente o "Chain of Thought" (processo de pensamento) dos agentes.
- **Como vai funcionar:** 
  1. O usuário insere o "Tema do Blog" e possíveis keywords no painel.
  2. O Streamlit intercepta os eventos gerados pelo LangGraph (streaming).
  3. A interface exibe blocos expansíveis atualizados em tempo real (ex: `🔄 Pesquisador buscando dados` -> `✍️ Redator criando rascunho` -> `🧐 Revisor validando SEO`).
  4. Após o loop de refinamento atingir a nota de corte, o artigo final será renderizado em Markdown junto com as métricas do motor.

## ✅ Verification Plan

Para validar se o novo motor está funcionando corretamente:

### Automated Tests
- Testar a serialização/deserialização do Pydantic State (validar se contratos não estão quebrando).
- `uv run test_workflow.py` com o mock de um modelo de linguagem que sempre reprova o SEO, para garantir que o grafo respeita o número máximo de repetições (Max Loops).

### Manual Verification
- Iniciar a CLI (`uv run main.py`) e pedir: *"Quero um artigo sobre O Impacto da IA na Arquitetura de Software"*.
- Monitorar os logs de streaming usando a interface rica (já existente) para ver claramente a transição: **Pesquisador -> Redator -> Revisor (Feedback gerado) -> Redator -> Resultado Final**.
