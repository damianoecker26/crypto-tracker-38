import asyncio
from dataclasses import dataclass
from typing import Callable, Any, Dict, Optional, TypeVar

T = TypeVar('T')

@dataclass(frozen=True)
class TickerEvent:
    """Immutable representation of a real-time cryptocurrency ticker update."""
    symbol: str
    price: float
    volume: float
    timestamp: float

class PipelineStep:
    """Callable wrapper enabling pipe syntax for processing ticker events."""
    def __init__(self, func: Callable[[TickerEvent], Optional[TickerEvent]]) -> None:
        """Initialize the step with a transformer or filter function."""
        self.func = func

    def __call__(self, event: TickerEvent) -> Optional[TickerEvent]:
        """Execute the underlying transformation function on a ticker event."""
        return self.func(event)

    def __rshift__(self, next_step: 'PipelineStep') -> 'PipelineStep':
        """Chain two pipeline steps together using the bitwise right shift operator."""
        def combined(e: TickerEvent) -> Optional[TickerEvent]:
            res = self(e)
            return next_step(res) if res is not None else None
        return PipelineStep(combined)

class CryptoTickerHandler:
    """Reactive stream processor for handling crypto ticker events via custom pipelines."""

    def __init__(self) -> None:
        """Initialize the ticker handler with an empty registry of stream pipelines."""
        self._routes: Dict[str, PipelineStep] = {}

    def register(self, symbol: str, pipeline: PipelineStep) -> None:
        """Bind a specific ticker symbol to a processing pipeline."""
        self._routes[symbol.upper()] = pipeline

    def dispatch(self, raw_payload: Dict[str, Any]) -> Optional[TickerEvent]:
        """Parse raw dictionary payload and route through registered symbol pipeline."""
        symbol: str = str(raw_payload.get("symbol", "")).upper()
        if symbol not in self._routes:
            return None

        event = TickerEvent(
            symbol=symbol,
            price=float(raw_payload.get("price", 0.0)),
            volume=float(raw_payload.get("volume", 0.0)),
            timestamp=float(raw_payload.get("ts", 0.0))
        )
        return self._routes[symbol](event)