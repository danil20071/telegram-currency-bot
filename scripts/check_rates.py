import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot
from api import ExchangeRateAPI
from database import Database

load_dotenv()


async def check_rates():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    
    if not token or not api_key:
        print("Missing environment variables")
        return
    
    bot = Bot(token=token)
    db = Database()
    await db.connect()
    
    api = ExchangeRateAPI(api_key)
    
    try:
        rate = await api.get_rub_cny_rate()
        if rate:
            await db.add_rate_history("RUB/CNY", rate)
            
            subscriptions = await db.get_subscriptions()
            target_rates = await db.get_target_rates()
            
            for sub in subscriptions:
                try:
                    await bot.send_message(
                        sub.chat_id,
                        f"📊 Обновление курса RUB/CNY:\n\n1 RUB = {rate:.4f} CNY\n1 CNY = {1/rate:.2f} RUB"
                    )
                except Exception as e:
                    print(f"Error sending to {sub.chat_id}: {e}")
            
            for target in target_rates:
                if target.currency == "CNY" and rate >= target.target_rate:
                    try:
                        await bot.send_message(
                            target.user_id,
                            f"🎯 Целевой курс достигнут!\n\n"
                            f"Текущий курс: {rate:.4f}\n"
                            f"Ваш целевой курс: {target.target_rate}"
                        )
                    except Exception as e:
                        print(f"Error sending target notification: {e}")
        
    finally:
        await api.close()
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(check_rates())