import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from src.core.config import config

logger = logging.getLogger(__name__)

class WhitelistMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if user_id not in config.TELEGRAM_ALLOWED_USER_IDS:
            logger.warning(f"Unauthorized access attempt from user: {user_id}")
            # Ignore completely as per spec
            return
        return await handler(event, data)
