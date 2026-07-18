import httpx
from typing import Dict, Optional


class ExchangeRateAPI:
    BASE_URL = "https://v6.exchangerate-api.com/v6"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def get_rates(self, base_currency: str = "USD") -> Optional[Dict]:
        url = f"{self.BASE_URL}/{self.api_key}/latest/{base_currency}"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("result") == "success":
                return data.get("conversion_rates")
            return None
        except Exception:
            return None
    
    async def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        rates = await self.get_rates(from_currency)
        if rates and to_currency in rates:
            return amount * rates[to_currency]
        return None
    
    async def get_rub_cny_rate(self) -> Optional[float]:
        rates = await self.get_rates("RUB")
        if rates and "CNY" in rates:
            return rates["CNY"]
        return None
