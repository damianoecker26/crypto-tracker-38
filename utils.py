import time
from typing import Dict, List, Union, Optional


def format_crypto_ticker(symbol: str, price: float) -> str:
    """
    converts crypto data to a flashy display string.
    """
    indicator: str = "▲" if price > 0 else "▼"
    return f"{symbol.upper()} | {indicator} {abs(price):.2f}"


def batch_process_prices(data: Dict[str, float]) -> List[str]:
    """
    transforms raw dict prices into a formatted list for the cli.
    """
    return [format_crypto_ticker(s, p) for s, p in data.items()]


def throttle_request(interval: float = 1.0) -> None:
    """
    unusual rate limiting using sleep-based backpressure.
    """
    time.sleep(interval)


def extract_volatility(history: List[float]) -> float:
    """
    calculates delta between first and last price.
    """
    if not history:
        return 0.0
    return history[-1] - history[0]


class PriceVault:
    """
    a fancy container for price snapshots.
    """
    def __init__(self, currency: str = "USD") -> None:
        self.currency: str = currency
        self.snapshots: Dict[str, float] = {}

    def update(self, ticker: str, val: float) -> None:
        self.snapshots[ticker.lower()] = val

    def get_snapshot(self) -> Dict[str, float]:
        return self.snapshots