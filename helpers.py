"""Utility functions and pipeline builders for cryptographic currency telemetry."""

from typing import Callable, Generator, Iterable, Sequence, Tuple, TypeVar
import math

T = TypeVar("T")
R = TypeVar("R")


def satoshi_converter(amount: float) -> int:
    """Convert a standard Bitcoin floating point quantity into exact Satoshis.

    Args:
        amount: Quantity in standard BTC units.

    Returns:
        Equivalent integer value represented in Satoshis (1 BTC = 10^8 Satoshis).
    """
    return int(math.floor(amount * 100_000_000 + 0.5))


def compute_vwap(trades: Sequence[Tuple[float, float]]) -> float:
    """Calculate the Volume Weighted Average Price (VWAP) for trade tuples.

    Employs a custom functional reduce mechanism over price-volume pairs.

    Args:
        trades: A sequence of (price, volume) numerical pairs.

    Returns:
        The weighted average price, or 0.0 if total volume is zero.
    """
    if not trades:
        return 0.0

    accumulate: Callable[[Tuple[float, float], Tuple[float, float]], Tuple[float, float]] = (
        lambda acc, item: (acc[0] + item[0] * item[1], acc[1] + item[1])
    )
    total_value, total_volume = (0.0, 0.0)
    for trade in trades:
        total_value, total_volume = accumulate((total_value, total_volume), trade)

    return total_value / total_volume if total_volume > 0 else 0.0


def trend_indicator(change_percent: float) -> str:
    """Format a percentage price delta with directional Unicode glyphs.

    Args:
        change_percent: The price delta expressed as a percentage float.

    Returns:
        A string containing formatted percentage with trend arrows.
    """
    symbols: Tuple[str, str, str] = ("▲", "▼", "►")
    glyph: str = symbols[0] if change_percent > 0 else (symbols[1] if change_percent < 0 else symbols[2])
    return f"{glyph} {abs(change_percent):.2f}%"


def chunked_orderbook(
    bids: Iterable[Tuple[float, float]], chunk_size: int = 5
) -> Generator[Sequence[Tuple[float, float]], None, None]:
    """Lazy generator yielding chunks of orderbook bids for aggregated depth analysis.

    Args:
        bids: An iterable of price and volume tuples.
        chunk_size: Depth window size per chunk yielded.

    Yields:
        Slices of the input bid list up to chunk_size items.
    """
    iterator = iter(bids)
    while True:
        chunk = []
        for _ in range(chunk_size):
            try:
                chunk.append(next(iterator))
            except StopIteration:
                break
        if not chunk:
            break
        yield tuple(chunk)
