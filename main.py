import asyncio
import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from bot import router
from bot.handlers import init_handlers
from api import ExchangeRateAPI
from database import Database

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    token = getenv("TELEGRAM_BOT_TOKEN")
    api_key = getenv("EXCHANGE_RATE_API_KEY")
    
    if not token or not api_key:
        logger.error("Missing required environment variables")
        return
    
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    
    db = Database()
    await db.connect()
    
    exchange_api = ExchangeRateAPI(api_key)
    init_handlers(exchange_api, db)
    
    dp.include_router(router)
    
    logger.info("Bot starting...")
    try:
        await dp.start_polling(bot)
    finally:
        await exchange_api.close()
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
