# 🐙 ten Agent (Tentaculo Mode)

**ten** é um Agente Pessoal de Inteligência Artificial desenhado para operar 100% localmente no desktop do usuário. Sua principal interface é o Telegram, criando uma experiência imersiva e sem fricções, livre de assinaturas em nuvem ou UIs complexas na web.

O agente processa suas requisições, pode rodar LLMs de ponta localmente (via **Ollama**), conectar-se a APIs de nuvem (Gemini/DeepSeek) e, principalmente, carregar "Skills" locais de forma dinâmica sem precisar de reinicialização (*Hot-Reload*).

## ✨ Principais Funcionalidades

- **Controle pelo Telegram:** Interaja com a IA enviando mensagens, áudios (Whister STT) ou arquivos (PDF extraction).
- **LLM Agnóstico:** Escolha qual "Cérebro" deseja usar. Suporte nativo para provedores locais via `Ollama` (`llama3.2`, `phi3`) ou via Nuvem (`Gemini 2.5`).
- **Engrenagem ReAct (Reasoning & Acting):** O agente não apenas fala; ele *pensa e usa ferramentas*. O loop autônomo permite chamamentos em cascata.
- **Memória Persistente Local:** Conversas armazenadas de forma enxuta e rápida com banco de dados `SQLite` utilizando WAL assíncrono.
- **Whitelist Restrita de Segurança:** Receba comandos exclusivamente do seu próprio ID do Telegram. Qualquer outro usuário ou bot crawler será ignorado na raiz, sem custo de API.
- **Sistema Customizado de Skills:** Crie pastas isoladas no repositório (ex. `.agents/skills/code_reviewer`) contendo as regras de ouro em um arquivo Markdown. O bot carrega as habilidades *on-the-fly*.

---

## 🚀 Casos de Uso (Exemplos Práticos)

1. **Code Reviewer e Helper Integrado:**
   - Em vez de abrir o ChatGPT, jogue o código do seu projeto no chat do Telegram. O agente lê a ferramenta *Code Reviewer* no diretório `.agents/skills/` e critica seu código verificando a PSR e PEP-8, tudo sem consumir contexto desnecessário até ser chamado de fato.

2. **Privacidade Total com Ollama Local (Desktop/Server):**
   - Transcreva um áudio de reunião confidencial enviando no Telegram. O arquivo nunca sai da sua máquina: é processado via Whisper local, resumido via modelo Ollama e a resposta retorna para seu celular de forma segura e imediata.

3. **Automação Pessoal em Background:**
   - Envie uma foto ou documento para o bot. O Agent Loop entende a requisição e, via Ferramentas Atuadoras (*Tools/Factory*), cria um relátorio textual em `.md` no seu Desktop.

---

## 🛠️ Instalação e Configuração

O projeto usa **Python** e o gerenciador ultrarrápido **uv**.

### 1. Requisitos
- Python 3.10+
- Gerenciador de dependências `uv`
- Conta no Telegram (BotFather para pegar um Token)

### 2. Configuração do `.env`
Renomeie ou crie um arquivo `.env` na raiz do projeto (como exemplo veja `.env-axample`):

```env
TELEGRAM_ALLOWED_USER_IDS=SEU_ID_TELEGRAM
TELEGRAM_BOT_TOKEN=TOKEN_CRIADO_NO_BOTFATHER
GEMINI_API_KEY=sua_API_key_aqui (Opcional)
DEEPSEEK_API_KEY=sua_API_key_aqui (Opcional)
OLLAMA_API_URL=http://localhost:11434
DEFAULT_LLM_PROVIDER=llama3.2:1b  # Ou gemini, qwen2.5, phi3...
```

### 3. Executando o motor
Com tudo configurado e a whitelist ativa, abra o terminal e deixe a magia acontecer:
```bash
uv run main.py
```

O bot efetuará *Polling* contínuo. Abra o Telegram no seu smartphone e comece a testar as habilidades!

---

## 📚 Documentação Adicional

Leia as especificações exatas na pasta `/docs`:
- `PRD.md`: Requisitos de escopo inicial do produto.
- `architecture.md`: Diagramas e definições de classes POO.
- `walkthrough.md`: Passos do esqueleto sistêmico para dev.
- `skill-user.md` e `agent-loop.md`: Especificações das mecânicas avançadas do núcleo ten.