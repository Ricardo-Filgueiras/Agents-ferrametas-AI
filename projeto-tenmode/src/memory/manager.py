from typing import List, Optional
from src.core.models import Conversation, Message
from src.database.repositories import ConversationRepository, MessageRepository
from src.core.config import config

class MemoryManager:
    def __init__(self):
        self.conv_repo = ConversationRepository()
        self.msg_repo = MessageRepository()

    async def get_or_create_conversation(self, user_id: str, provider: str = None) -> Conversation:
        target_provider = provider or config.DEFAULT_PROVIDER
        conv = await self.conv_repo.get_latest_for_user(user_id)
        if not conv:
            conv = await self.conv_repo.create(user_id=user_id, provider=target_provider)
        elif conv.provider != target_provider:
            # Create a new conversation if the default provider changed in ENV
            conv = await self.conv_repo.create(user_id=user_id, provider=target_provider)
            
        return conv

    async def load_context(self, conversation_id: str) -> List[Message]:
        return await self.msg_repo.get_messages(conversation_id, limit=config.MEMORY_WINDOW_SIZE)

    async def save_turn(self, conversation_id: str, user_msg: Message, assistant_msg: Message):
        await self.msg_repo.add_message(conversation_id, user_msg)
        await self.msg_repo.add_message(conversation_id, assistant_msg)
        
    async def add_message(self, conversation_id: str, message: Message):
        await self.msg_repo.add_message(conversation_id, message)
