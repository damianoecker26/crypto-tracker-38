import decimal
import functools
from datetime import datetime, timezone

def normalize_crypto_amount(val):
    """Converts varied inputs into high-precision Decimals for ledger safety."""
    ctx = decimal.Context(prec=28)
    return ctx.create_decimal(val).normalize()

def timestamp_utc():
    """Generates a structured UTC timestamp for blockchain alignment."""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

def retry_on_failure(retries=3):
    """Decorator for resilient interaction with unstable exchange APIs."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
            raise last_err
        return wrapper
    return decorator

def format_ticker_pair(base, quote):
    """Canonical string formatting for crypto asset pairs."""
    return f"{base.upper()}_{quote.upper()}"

def partition_stream(data, chunk_size=10):
    """Batch generator for high-volume market tick streams."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]