"""
Main bot entry point
"""
import asyncio
import logging
from aiogram import Dispatcher, Bot, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers import router
from admin import admin_router
from admin_init import setup_admin  # Initialize admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """Set bot commands"""
    commands = [
        BotCommand(command='start', description='Botni boshlash'),
        BotCommand(command='help', description='Yordam'),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Main bot function"""
    
    # Initialize admin
    setup_admin()
    
    # Check if token is set
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN not set in .env file!")
        print("❌ BOT_TOKEN not set in .env file!")
        print("   Please create .env file with: BOT_TOKEN=your_token_here")
        return
    
    # Initialize bot and dispatcher
    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    
    # Include routers
    dp.include_router(admin_router)  # Admin commands first (higher priority)
    dp.include_router(router)         # Regular user commands
    
    # Set bot commands
    await set_commands(bot)
    
    logger.info("✅ Bot started successfully")
    print("✅ Bot started successfully!")
    print("   Waiting for messages...")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Bot stopped")
        logger.info("Bot stopped by user")
