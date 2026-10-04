"""Crypto stream processing engine with pipeline transformations."""

from typing import Callable, Generator, Iterable, Any, TypeVar, Dict, Union
from dataclasses import dataclass
import time

T = TypeVar('T')
R = TypeVar('R')


@dataclass(frozen=True)
class TickerPrice:
    """Immutable payload for live cryptographic asset price ticks."""
    symbol: str
    price: float
    timestamp: float = 0.0

    def __post_init__(self) -> None:
        if self.timestamp == 0.0:
            object.__setattr__(self, 'timestamp', time.time())


class StreamPipeline:
    """Pipeline operator wrapper transforming streams using bitwise OR composition."""

    def __init__(self, source: Iterable[Any]) -> None:
        """Initialize stream processor pipeline with source sequence."""
        self._source = source

    def __or__(self, transform: Callable[[Iterable[Any]], Any]) -> 'StreamPipeline':
        """Chain a transformation function onto the current pipeline output."""
        return StreamPipeline(transform(self._source))

    def collect(self) -> list[Any]:
        """Evaluate and materialise the processing pipeline results into a list."""
        return list(self._source)


def parse_raw_ticks(raw_data: Iterable[Dict[str, Union[str, float]]]) -> Generator[TickerPrice, None, None]:
    """Parses raw stream dictionaries into strongly-typed TickerPrice objects."""
    for item in raw_data:
        symbol, price = item.get("symbol"), item.get("price")
        if isinstance(symbol, str) and isinstance(price, (int, float)):
            yield TickerPrice(symbol=symbol.upper(), price=float(price))


def compute_moving_averages(ticks: Iterable[TickerPrice], window_size: int = 3) -> Generator[Dict[str, Union[str, float]], None, None]:
    """Calculates running simple moving price averages per asset symbol."""
    history: Dict[str, list[float]] = {}
    for tick in ticks:
        buf = history.setdefault(tick.symbol, [])
        buf.append(tick.price)
        if len(buf) > window_size:
            buf.pop(0)
        yield {
            "symbol": tick.symbol,
            "sma": round(sum(buf) / len(buf), 4),
            "count": len(buf)
        }
