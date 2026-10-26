import time
import decimal
from functools import wraps

def format_crypto(value, precision=8):
    """Format high-precision crypto decimals into strings."""
    quant = decimal.Decimal(10) ** -precision
    return str(decimal.Decimal(str(value)).quantize(quant, rounding=decimal.ROUND_HALF_UP))

def retry_on_failure(retries=3, delay=1):
    """Decorator for resilience against network hiccups."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def sanitize_ticker(ticker):
    """Normalize asset names for API requests."""
    return str(ticker).upper().replace('/', '_').strip()

def batch_process(items, batch_size=10):
    """Generator for chunking large order books."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def calculate_roi(entry, exit_price):
    """Percentage change calculation for trades."""
    entry_dec = decimal.Decimal(str(entry))
    exit_dec = decimal.Decimal(str(exit_price))
    return float(((exit_dec - entry_dec) / entry_dec) * 100)