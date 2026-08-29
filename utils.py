import re
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

def calculate_percentage_change(old_price: float, new_price: float) -> float:
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100

def format_large_number(number: float) -> str:
    if number >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.2f}K"
    return f"{number:.2f}"

def validate_crypto_address(address: str, coin_type: str = 'btc') -> bool:
    if coin_type == 'btc':
        pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
        return bool(re.match(pattern, address))
    elif coin_type == 'eth':
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, address))
    return False

def generate_short_hash(data: str) -> str:
    full_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return full_hash[16:32]

def get_current_timestamp() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def calculate_portfolio_value(holdings: Dict[str, float], prices: Dict[str, float]) -> float:
    total = 0.0
    for coin, amount in holdings.items():
        if coin in prices:
            total += amount * prices[coin]
    return total

def is_price_stable(prices: List[float], threshold: float = 0.05) -> bool:
    if len(prices) < 2:
        return True
    max_p = max(prices)
    min_p = min(prices)
    return (max_p - min_p) / min_p < threshold
