from typing import Dict, Union, List
import time

def format_ticker(symbol: str, price: float) -> str:
    """Transforms raw crypto data into a quirky string display."""
    timestamp: float = time.time()
    return f"[{timestamp:.0f}] {symbol.upper()}: ${price:,.2f} USD"

def calculate_volatility(history: List[float]) -> float:
    """Calculates the standard deviation as a measure of crypto chaos."""
    if not history:
        return 0.0
    mean: float = sum(history) / len(history)
    variance: float = sum((x - mean) ** 2 for x in history) / len(history)
    return variance ** 0.5

def sanitize_payload(data: Dict[str, Union[str, float]]) -> Dict[str, str]:
    """Converts all dict values to strings for consistent logging."""
    return {str(k): str(v) for k, v in data.items()}

def weighted_average(prices: List[float], weights: List[float]) -> float:
    """Computes the weighted sentiment or price metric."""
    if len(prices) != len(weights) or sum(weights) == 0:
        return 0.0
    return sum(p * w for p, w in zip(prices, weights)) / sum(weights)