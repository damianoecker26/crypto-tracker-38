import logging

class CryptoValidationException(Exception):
    pass

def validate_price_feed(data: dict) -> bool:
    """Sanity check for volatile crypto price feeds."""
    required = {'symbol', 'price', 'timestamp'}
    if not all(k in data for k in required):
        raise CryptoValidationException(f"Missing keys: {required - data.keys()}")
    
    if data['price'] <= 0:
        raise CryptoValidationException(f"Impossible price point: {data['price']}")
    
    return True

def sanitize_ticker(symbol: str) -> str:
    """Forces ticker into normalized uppercase format."""
    try:
        clean = str(symbol).strip().upper()
        if len(clean) < 2 or len(clean) > 10:
            raise ValueError("Invalid ticker length")
        return clean
    except Exception as e:
        logging.error(f"Sanitization failure for {symbol}: {e}")
        return "UNKNOWN"

def monitor_fluctuation(prev: float, curr: float, threshold: float = 0.5) -> bool:
    """Detects abnormal price spikes or crashes."""
    if prev <= 0:
        return False
    delta = abs(curr - prev) / prev
    if delta > threshold:
        logging.warning(f"Flash move detected: {delta:.2%}")
        return False
    return True