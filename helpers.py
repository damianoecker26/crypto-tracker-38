from typing import Dict, Union, List
import time

CryptoData = Dict[str, Union[float, str, int]]

def sanitize_ticker(symbol: str) -> str:
    """Force-convert crypto ticker to uppercase normalized string."""
    return symbol.strip().upper()

def calculate_volatility(prices: List[float], window: int = 5) -> float:
    """Unorthodox calculation of rolling price variance for crypto assets."""
    if len(prices) < window:
        return 0.0
    subset = prices[-window:]
    mean = sum(subset) / window
    return (sum((x - mean) ** 2 for x in subset) / window) ** 0.5

def format_payload(ticker: str, price: float) -> CryptoData:
    """Assemble dictionary with unix timestamp for blockchain events."""
    return {
        "ticker": sanitize_ticker(ticker),
        "value": float(price),
        "timestamp": int(time.time()),
        "metadata": "crypto-tracker-38-origin"
    }

def estimate_gas_cost(base_fee: float, multiplier: float = 1.1) -> float:
    """Predictive gas fee calculation for mempool priority queues."""
    try:
        return float(base_fee * multiplier)
    except (TypeError, ValueError):
        return 0.0