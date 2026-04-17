import aiosqlite
import logging
from typing import Optional
from src.core.config import config

logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    async def get_connection(self) -> aiosqlite.Connection:
        if self.connection is None:
            self.connection = await aiosqlite.connect(config.DB_PATH)
            # Enable WAL mode for better concurrency
            await self.connection.execute('PRAGMA journal_mode=WAL;')
            self.connection.row_factory = aiosqlite.Row
        return self.connection

    async def init_db(self):
        conn = await self.get_connection()
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                provider TEXT NOT NULL
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')
        await conn.commit()
        logger.info("Database initialized successfully.")

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None

db_manager = DatabaseManager()
