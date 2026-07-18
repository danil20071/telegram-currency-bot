import aiosqlite
from datetime import datetime
from typing import List, Optional
from .models import Subscription, TargetRate, RateHistory


class Database:
    def __init__(self, db_path: str = "bot.db"):
        self.db_path = db_path
        self.db: Optional[aiosqlite.Connection] = None

    async def connect(self):
        self.db = await aiosqlite.connect(self.db_path)
        await self._create_tables()

    async def close(self):
        if self.db:
            await self.db.close()

    async def _create_tables(self):
        await self.db.executescript("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                subscribed_at TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS target_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                currency TEXT,
                target_rate REAL,
                created_at TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS rate_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_pair TEXT,
                rate REAL,
                timestamp TIMESTAMP
            );
        """)
        await self.db.commit()

    async def add_subscription(self, user_id: int, chat_id: int) -> bool:
        try:
            await self.db.execute(
                "INSERT OR REPLACE INTO subscriptions (user_id, chat_id, subscribed_at) VALUES (?, ?, ?)",
                (user_id, chat_id, datetime.now())
            )
            await self.db.commit()
            return True
        except Exception:
            return False

    async def remove_subscription(self, user_id: int) -> bool:
        try:
            await self.db.execute(
                "DELETE FROM subscriptions WHERE user_id = ?",
                (user_id,)
            )
            await self.db.commit()
            return True
        except Exception:
            return False

    async def get_subscriptions(self) -> List[Subscription]:
        cursor = await self.db.execute("SELECT user_id, chat_id, subscribed_at FROM subscriptions")
        rows = await cursor.fetchall()
        return [Subscription(*row) for row in rows]

    async def add_target_rate(self, user_id: int, currency: str, target_rate: float) -> bool:
        try:
            await self.db.execute(
                "INSERT INTO target_rates (user_id, currency, target_rate, created_at) VALUES (?, ?, ?, ?)",
                (user_id, currency, target_rate, datetime.now())
            )
            await self.db.commit()
            return True
        except Exception:
            return False

    async def get_target_rates(self, user_id: Optional[int] = None) -> List[TargetRate]:
        if user_id:
            cursor = await self.db.execute(
                "SELECT id, user_id, currency, target_rate, created_at FROM target_rates WHERE user_id = ?",
                (user_id,)
            )
        else:
            cursor = await self.db.execute(
                "SELECT id, user_id, currency, target_rate, created_at FROM target_rates"
            )
        rows = await cursor.fetchall()
        return [TargetRate(*row) for row in rows]

    async def add_rate_history(self, currency_pair: str, rate: float) -> bool:
        try:
            await self.db.execute(
                "INSERT INTO rate_history (currency_pair, rate, timestamp) VALUES (?, ?, ?)",
                (currency_pair, rate, datetime.now())
            )
            await self.db.commit()
            return True
        except Exception:
            return False

    async def get_latest_rate(self, currency_pair: str) -> Optional[RateHistory]:
        cursor = await self.db.execute(
            "SELECT id, currency_pair, rate, timestamp FROM rate_history WHERE currency_pair = ? ORDER BY timestamp DESC LIMIT 1",
            (currency_pair,)
        )
        row = await cursor.fetchone()
        if row:
            return RateHistory(*row)
        return None