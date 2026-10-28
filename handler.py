"""Async event handler for real-time cryptocurrency tick streams."""

from typing import AsyncIterator, Dict, Protocol, TypedDict, Any
import asyncio
import time


class CryptoTick(TypedDict):
    symbol: str
    price: float
    timestamp: float


class EventSink(Protocol):
    """Protocol defining the asynchronous event emission interface."""
    async def emit(self, channel: str, payload: Dict[str, Any]) -> None:
        ...


class TickStreamHandler:
    """Dispatches crypto price ticks through transform pipelines to registered sinks."""

    def __init__(self, target_sink: EventSink, threshold_alert: float = 0.05) -> None:
        self.sink = target_sink
        self.threshold = threshold_alert
        self._last_prices: Dict[str, float] = {}

    async def __call__(self, tick_stream: AsyncIterator[CryptoTick]) -> int:
        """Process an incoming tick stream, calculating drift and dispatching events."""
        processed_count: int = 0
        async for tick in tick_stream:
            symbol, price = tick["symbol"], tick["price"]
            prev_price = self._last_prices.get(symbol, price)
            drift = abs(price - prev_price) / prev_price if prev_price else 0.0

            payload: Dict[str, Any] = {
                "tick": tick,
                "drift": round(drift, 4),
                "alert": drift >= self.threshold,
            }

            await self.sink.emit(f"crypto.ticks.{symbol.lower()}", payload)
            self._last_prices[symbol] = price
            processed_count += 1

        return processed_count


async def mock_tick_generator() -> AsyncIterator[CryptoTick]:
    """Yield synthetic ticker updates for stream verification."""
    ticks: list[CryptoTick] = [
        {"symbol": "BTC-USD", "price": 64000.0, "timestamp": time.time()},
        {"symbol": "BTC-USD", "price": 68000.0, "timestamp": time.time() + 1},
        {"symbol": "ETH-USD", "price": 3500.0, "timestamp": time.time() + 2},
    ]
    for tick in ticks:
        await asyncio.sleep(0.01)
        yield tick
