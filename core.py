import math
from datetime import datetime, timezone
from typing import NamedTuple


class Tick(NamedTuple):
    symbol: str
    price: float
    volume: float
    timestamp: float


class MomentumVector(NamedTuple):
    magnitude: float
    direction: int


def calculate_momentum(ticks: list[Tick]) -> MomentumVector:
    """Computes a dimensional momentum vector using dynamic time decay weights.

    Args:
        ticks: Sequence of chronological trade ticks.

    Returns:
        A tuple containing directional velocity magnitude and market bias.
    """
    if not ticks:
        return MomentumVector(0.0, 0)

    now = datetime.now(timezone.utc).timestamp()
    weighted_sum = 0.0
    total_weight = 0.0

    for tick in ticks:
        age = max(1.0, now - tick.timestamp)
        weight = tick.volume / math.sqrt(age)
        weighted_sum += tick.price * weight
        total_weight += weight

    weighted_avg = weighted_sum / (total_weight or 1.0)
    baseline = ticks[0].price
    delta = weighted_avg - baseline

    return MomentumVector(
        magnitude=abs(delta),
        direction=1 if delta > 0 else (-1 if delta < 0 else 0)
    )


class CryptoPipeline:
    """Reactive stream pipeline transforming raw tick data into metrics."""

    def __init__(self, window_size: int = 10) -> None:
        """Initialize the pipeline with a target sliding window size."""
        self._window_size: int = window_size
        self._buffer: list[Tick] = []

    def feed(self, tick: Tick) -> tuple[MomentumVector, float]:
        """Ingest a single tick and yield updated momentum and running VWAP.

        Args:
            tick: Incoming cryptocurrency tick update.

        Returns:
            Tuple of current MomentumVector and calculated VWAP float.
        """
        self._buffer.append(tick)
        if len(self._buffer) > self._window_size:
            self._buffer.pop(0)

        momentum = calculate_momentum(self._buffer)
        total_vol = sum(t.volume for t in self._buffer) or 1.0
        vwap = sum(t.price * t.volume for t in self._buffer) / total_vol

        return momentum, vwap
