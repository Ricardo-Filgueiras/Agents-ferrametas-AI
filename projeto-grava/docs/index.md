# Projeto-Grava

Gravador de reuniões local-first com transcrição automática offline (Whisper) e geração de atas inteligentes via Ollama ou OpenAI. Captura tela, áudio e webcam — sem dados deixando a máquina.

**Privacidade:** Quando usando Ollama, toda a IA é executada localmente. Nenhum dado é enviado para a nuvem.

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [Instalação](instalacao.md) | Pré-requisitos, instalação, configuração inicial |
| [Guia do Usuário](guia-usuario.md) | Como usar: gravação, histórico, modos de áudio |
| [Arquitetura](arquitetura.md) | Módulos, pipelines de dados, decisões técnicas |
| [API & Módulos](api-modulos.md) | Referência de classes e funções públicas |
| [FAQ & Troubleshooting](faq.md) | Erros comuns, limitações, roadmap |

---

## 🚀 Início rápido

```bash
# Clonar e instalar
git clone https://github.com/Ricardo-Filgueiras/Agents-ferrametas-AI.git
cd Agents-ferrametas-AI/projeto-grava
uv sync

# Rodar (Ollama deve estar executando)
streamlit run src/app/main.py
```

Acesse `http://localhost:8501` e clique no botão vermelho para começar a gravar.

---

## 📋 Versão

- **Versão:** 0.1.0
- **Python:** 3.12+
- **Dependências:** Ollama (local) ou OpenAI (cloud), FFmpeg
