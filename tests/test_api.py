import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from api import ExchangeRateAPI


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def api():
    return ExchangeRateAPI("test_api_key")


def _make_response(data):
    resp = MagicMock()
    resp.json.return_value = data
    resp.raise_for_status = MagicMock()
    return resp


@pytest.mark.asyncio
async def test_get_rates_success(api):
    mock_get = AsyncMock(return_value=_make_response({
        "result": "success",
        "conversion_rates": {"CNY": 7.2, "EUR": 0.85}
    }))

    with patch.object(api.client, "get", mock_get):
        rates = await api.get_rates("USD")
        assert rates is not None
        assert "CNY" in rates
        assert rates["CNY"] == 7.2


@pytest.mark.asyncio
async def test_convert(api):
    mock_get = AsyncMock(return_value=_make_response({
        "result": "success",
        "conversion_rates": {"CNY": 7.2}
    }))

    with patch.object(api.client, "get", mock_get):
        result = await api.convert(100, "USD", "CNY")
        assert result == 720.0


@pytest.mark.asyncio
async def test_get_rub_cny_rate(api):
    mock_get = AsyncMock(return_value=_make_response({
        "result": "success",
        "conversion_rates": {"CNY": 0.085}
    }))

    with patch.object(api.client, "get", mock_get):
        rate = await api.get_rub_cny_rate()
        assert rate == 0.085
