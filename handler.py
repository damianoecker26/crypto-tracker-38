import asyncio
import random
from typing import AsyncGenerator, Dict, List, Union


class CryptoStreamHandler:

    def __init__(self, tickers: List[str]):
        self.tickers = [t.upper() for t in tickers]
        self._active = False

    async def _fetch_mock_price(self, ticker: str) -> Dict[str, Union[str, float]]:
        await asyncio.sleep(random.uniform(0.1, 0.5))
        base_price = {"BTC": 65000.0, "ETH": 3500.0, "SOL": 140.0}.get(
            ticker, 1.0
        )
        change = random.uniform(-0.02, 0.02)
        return {
            "ticker": ticker,
            "price": round(base_price * (1 + change), 2),
            "timestamp": asyncio.get_event_loop().time(),
        }

    async def stream_prices(self) -> AsyncGenerator[Dict[str, Union[str, float]], None]:
        self._active = True
        while self._active:
            tasks = [self._fetch_mock_price(ticker) for ticker in self.tickers]
            for completed_task in asyncio.as_completed(tasks):
                try:
                    yield await completed_task
                except Exception as exc:
                    yield {
                        "error": str(exc),
                        "timestamp": asyncio.get_event_loop().time(),
                    }
            await asyncio.sleep(2.0)

    def stop(self) -> None:
        self._active = False
