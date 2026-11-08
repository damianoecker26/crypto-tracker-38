from typing import Dict, List, Union, Optional
import time

CryptoData = Dict[str, Union[str, float]]

def normalize_ticker(symbol: str) -> str:
    """Converts ticker to canonical uppercase format.

    Args:
        symbol: The raw cryptocurrency ticker string.

    Returns:
        The formatted ticker string.
    """
    return symbol.strip().upper()

def calculate_volatility(prices: List[float], window: int = 24) -> Optional[float]:
    """Computes rolling price variance for the asset.

    Args:
        prices: List of historical price points.
        window: Number of periods for variance calculation.

    Returns:
        The calculated volatility value or None if insufficient data.
    """
    if len(prices) < window:
        return None
    mean_price = sum(prices[-window:]) / window
    variance = sum((x - mean_price) ** 2 for x in prices[-window:]) / window
    return variance ** 0.5

def format_timestamp(ts: Optional[float] = None) -> str:
    """Generates a human-readable UTC timestamp for logs.

    Args:
        ts: Unix timestamp or current time if None.

    Returns:
        ISO format string.
    """
    t = ts or time.time()
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t))