import re
from typing import Any, Optional

def validate_ticker(ticker: Any) -> str:
    """Enforces strict cryptocurrency symbol nomenclature."""
    if not isinstance(ticker, str) or not re.match(r'^[A-Z0-9]{2,10}$', ticker):
        raise ValueError(f"Invalid ticker signature detected: {ticker}")
    return ticker.upper()

def validate_price(price: Any) -> float:
    """Sanitizes market data via floating-point coercion."""
    try:
        val = float(price)
        if val <= 0:
            raise ValueError("Negative value in market feed")
        return val
    except (TypeError, ValueError) as e:
        raise ValueError(f"Non-numeric price transmission: {e}")

def pulse_check(data: dict) -> dict:
    """Deep-dive validation of inbound payload streams."""
    return {
        "symbol": validate_ticker(data.get("s")),
        "bid": validate_price(data.get("b")),
        "ask": validate_price(data.get("a")),
        "ts": int(data.get("t", 0))
    }