import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, CallbackQuery, User, Chat
from bot.handlers import (
    cmd_start, cmd_rates, cmd_convert, callback_convert,
    cmd_subscribe, cmd_target, cmd_exchange, init_handlers
)


@pytest.fixture
def mock_api():
    api = AsyncMock()
    api.get_rub_cny_rate.return_value = 0.085
    api.convert.return_value = 720.0
    return api


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add_subscription.return_value = True
    db.add_target_rate.return_value = True
    return db


@pytest.fixture
def mock_message():
    message = MagicMock(spec=Message)
    message.from_user = MagicMock(spec=User)
    message.from_user.id = 123
    message.chat = MagicMock(spec=Chat)
    message.chat.id = 456
    message.text = "/start"
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_callback():
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock(spec=User)
    callback.from_user.id = 123
    callback.message = MagicMock(spec=Message)
    callback.message.chat = MagicMock(spec=Chat)
    callback.message.chat.id = 456
    callback.data = "rates"
    callback.answer = AsyncMock()
    callback.message.edit_text = AsyncMock()
    return callback


@pytest.mark.asyncio
async def test_cmd_start(mock_message):
    await cmd_start(mock_message)
    mock_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_cmd_rates_success(mock_message, mock_api):
    init_handlers(mock_api, AsyncMock())
    await cmd_rates(mock_message)
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args[0][0]
    assert "0.085" in call_args


@pytest.mark.asyncio
async def test_cmd_convert_success(mock_message, mock_api):
    init_handlers(mock_api, AsyncMock())
    mock_message.text = "/convert 1000 RUB CNY"
    await cmd_convert(mock_message)
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args[0][0]
    assert "720.00" in call_args
