"""
MeetingCallbackHandler — observabilidade centralizada para todas as chamadas LLM.

Registra latência, uso de tokens e erros sem poluir o código de negócio.
Ativado automaticamente via config={"callbacks": [MeetingCallbackHandler()]}.
"""
import logging
import time

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

logger = logging.getLogger("projeto_grava.llm")


class MeetingCallbackHandler(BaseCallbackHandler):
    """Loga métricas de cada chamada ao LLM no logger 'projeto_grava.llm'."""

    def on_llm_start(self, serialized: dict, prompts: list[str], **kwargs) -> None:
        self._start_time = time.time()
        model_name = serialized.get("name", "desconhecido")
        logger.info("[LLM] Iniciando chamada | modelo=%s | prompts=%d", model_name, len(prompts))

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        elapsed = time.time() - self._start_time
        usage = {}
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
        logger.info(
            "[LLM] Concluído | latência=%.2fs | tokens_entrada=%s | tokens_saída=%s",
            elapsed,
            usage.get("prompt_tokens", "?"),
            usage.get("completion_tokens", "?"),
        )

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        logger.error("[LLM] ERRO: %s", error, exc_info=True)

    def on_chain_start(self, serialized: dict, inputs: dict, **kwargs) -> None:
        logger.debug("[Chain] Iniciando | inputs_keys=%s", list(inputs.keys()))

    def on_chain_error(self, error: Exception, **kwargs) -> None:
        logger.error("[Chain] ERRO: %s", error, exc_info=True)
