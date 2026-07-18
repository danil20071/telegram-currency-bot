import pytest
import asyncio
from datetime import datetime
from database import Database


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db():
    database = Database(":memory:")
    await database.connect()
    yield database
    await database.close()


@pytest.mark.asyncio
async def test_add_subscription(db):
    result = await db.add_subscription(123, 456)
    assert result is True
    
    subs = await db.get_subscriptions()
    assert len(subs) == 1
    assert subs[0].user_id == 123
    assert subs[0].chat_id == 456


@pytest.mark.asyncio
async def test_remove_subscription(db):
    await db.add_subscription(123, 456)
    result = await db.remove_subscription(123)
    assert result is True
    
    subs = await db.get_subscriptions()
    assert len(subs) == 0


@pytest.mark.asyncio
async def test_add_target_rate(db):
    result = await db.add_target_rate(123, "CNY", 12.5)
    assert result is True
    
    targets = await db.get_target_rates(123)
    assert len(targets) == 1
    assert targets[0].currency == "CNY"
    assert targets[0].target_rate == 12.5


@pytest.mark.asyncio
async def test_add_rate_history(db):
    result = await db.add_rate_history("RUB/CNY", 12.34)
    assert result is True
    
    latest = await db.get_latest_rate("RUB/CNY")
    assert latest is not None
    assert latest.rate == 12.34