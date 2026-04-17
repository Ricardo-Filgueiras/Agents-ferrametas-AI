import uuid
from typing import List, Optional
from src.core.models import Conversation, Message, Role
from src.database.db import db_manager

class ConversationRepository:
    async def create(self, user_id: str, provider: str) -> Conversation:
        conn = await db_manager.get_connection()
        conv_id = str(uuid.uuid4())
        await conn.execute(
            "INSERT INTO conversations (id, user_id, provider) VALUES (?, ?, ?)",
            (conv_id, user_id, provider)
        )
        await conn.commit()
        return Conversation(id=conv_id, user_id=user_id, provider=provider)

    async def get_by_id(self, conv_id: str) -> Optional[Conversation]:
        conn = await db_manager.get_connection()
        async with conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return Conversation(id=row['id'], user_id=row['user_id'], provider=row['provider'])
        return None

    async def get_latest_for_user(self, user_id: str) -> Optional[Conversation]:
        conn = await db_manager.get_connection()
        async with conn.execute(
            "SELECT * FROM conversations WHERE user_id = ? ORDER BY rowid DESC LIMIT 1", 
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return Conversation(id=row['id'], user_id=row['user_id'], provider=row['provider'])
        return None

class MessageRepository:
    async def add_message(self, conversation_id: str, message: Message):
        conn = await db_manager.get_connection()
        await conn.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, message.role.value, message.content)
        )
        await conn.commit()

    async def get_messages(self, conversation_id: str, limit: int = 50) -> List[Message]:
        conn = await db_manager.get_connection()
        async with conn.execute(
            "SELECT * FROM (SELECT * FROM messages WHERE conversation_id = ? ORDER BY id DESC LIMIT ?) ORDER BY id ASC",
            (conversation_id, limit)
        ) as cursor:
            rows = await cursor.fetchall()
            return [Message(role=Role(row['role']), content=row['content']) for row in rows]
