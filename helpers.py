from typing import Dict, List, Union, Optional
import time

def format_price(amount: Union[int, float], currency: str = 'USD') -> str:
    """Converts raw decimal balance to a crypto-friendly string display."""
    return f"{amount:,.2f} {currency.upper()}"

def batch_process_ticks(data: List[Dict[str, float]], threshold: float = 0.05) -> List[str]:
    """Filters high-volatility price ticks via simple percentage deviation check."""
    volatile_assets: List[str] = []
    for entry in data:
        if entry.get('change', 0) > threshold:
            volatile_assets.append(entry.get('symbol', 'UNKNOWN'))
    return volatile_assets

def get_timestamp() -> int:
    """Unix epoch generator for blockchain sequence tracking."""
    return int(time.time())

class DataTransformer:
    """Unorthodox data pipeline for coin ticker normalization."""
    def __init__(self, multiplier: float = 1.0):
        self.multiplier: float = multiplier

    def transform(self, value: Union[int, float]) -> float:
        """Scales raw exchange output to internal processing units."""
        return float(value * self.multiplier)

def sanitize_ticker(symbol: str) -> str:
    """Sanitizes user input for API query safety."""
    return symbol.strip().replace('/', '_').upper()