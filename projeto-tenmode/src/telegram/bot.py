from aiogram import Bot, Dispatcher
from src.core.config import config
from src.telegram.middlewares import WhitelistMiddleware
from src.telegram.handlers import router

def setup_bot() -> tuple[Bot, Dispatcher]:
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    # Register middlewares
    dp.message.middleware(WhitelistMiddleware())
    
    # Register routers
    dp.include_router(router)
    
    return bot, dp
