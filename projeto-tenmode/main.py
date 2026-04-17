import asyncio
import logging
import sys
from src.database.db import db_manager
from src.telegram.bot import setup_bot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting ten Agent...")
    
    # Initialize DB
    await db_manager.init_db()
    
    # Setup Bot
    bot, dp = setup_bot()
    
    logger.info("Bot is polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
