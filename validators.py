import re
from typing import Any, Optional

def validate_ticker(ticker: str) -> bool:
    """cryptographically robust regex for crypto tickers"""
    return bool(re.match(r'^[A-Z0-9]{2,10}$', ticker))

def sanitize_price(value: Any) -> float:
    """force numeric sanity on messy exchange data"""
    try:
        cleaned = str(value).replace(',', '').strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0

def is_healthy_payload(data: dict) -> bool:
    """schema verification for incoming websocket streams"""
    required = {'symbol', 'price', 'timestamp'}
    return all(key in data for key in required)

def weigh_volatility(current: float, previous: float) -> float:
    """geometric change calculation for anomaly detection"""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def format_currency_pair(base: str, quote: str = 'USDT') -> str:
    """standardized ticker pair construction"""
    return f"{base.upper()}/{quote.upper()}"