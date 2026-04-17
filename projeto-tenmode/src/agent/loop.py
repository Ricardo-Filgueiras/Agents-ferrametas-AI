import logging
from typing import List, Optional
from src.core.models import Message, Role, ToolCall
from src.core.config import config
from src.providers.factory import ProviderFactory
from src.tools.registry import global_tool_registry

logger = logging.getLogger(__name__)

class AgentLoop:
    def __init__(self, provider_name: str = config.DEFAULT_PROVIDER):
        self.provider = ProviderFactory.get_provider(provider_name)
        self.tools = global_tool_registry.get_all_tools()
        self.max_iterations = config.MAX_ITERATIONS

    async def run(self, messages: List[Message], system_prompt: Optional[str] = None) -> str:
        current_messages = list(messages)
        iterations = 0

        while iterations < self.max_iterations:
            iterations += 1
            logger.info(f"Agent Loop Iteration {iterations}/{self.max_iterations}")

            text_response, tool_call = await self.provider.generate_response(
                messages=current_messages,
                system_prompt=system_prompt,
                tools=self.tools if self.tools else None
            )

            if tool_call:
                logger.info(f"LLM requested tool: {tool_call.name} with args: {tool_call.arguments}")
                current_messages.append(Message(role=Role.ASSISTANT, content=f"Action: {tool_call.name}\nAction Input: {tool_call.arguments}"))
                
                tool = global_tool_registry.get_tool(tool_call.name)
                if tool:
                    try:
                        observation = await tool.execute(**tool_call.arguments)
                        logger.info(f"Tool {tool.name} returned: {observation}")
                    except Exception as e:
                        observation = f"Error executing tool: {str(e)}"
                        logger.error(observation)
                else:
                    observation = f"Tool {tool_call.name} not found."
                    logger.warning(observation)

                current_messages.append(Message(role=Role.USER, content=f"Observation: {observation}"))
            elif text_response:
                logger.info("Agent reached final answer.")
                return text_response
            else:
                logger.warning("Agent returned neither text nor tool call. Breaking loop.")
                break

        return "Desculpe, desisti ou deu timeout no processamento pois falhei nas chamadas em MAX iteracoes."
