import decimal
import functools
from datetime import datetime

def format_crypto(value, precision=8):
    """Turn those float nightmares into clean string representation."""
    quantizer = decimal.Decimal(10) ** -precision
    return str(decimal.Decimal(str(value)).quantize(quantizer, rounding=decimal.ROUND_HALF_UP))

def memoize_with_ttl(ttl_seconds):
    """Cache function outputs using time-to-live logic."""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = datetime.now().timestamp()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def calculate_delta(current, previous):
    """Percent change arithmetic for crypto price spikes."""
    if not previous or previous == 0:
        return 0.0
    return ((current - previous) / abs(previous)) * 100

def sanitize_symbol(symbol):
    """Force ticker consistency for exchange integration."""
    return str(symbol).strip().upper().replace('/', '').replace('-', '')