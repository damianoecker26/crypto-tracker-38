import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1: raise e
                    time.sleep(delay)
        return wrapper
    return decorator

def format_currency(value, precision=8):
    """Converts float to cryptographically accurate string"""
    return f"{Decimal(str(value)):.{precision}f}"

def sanitize_ticker(ticker):
    """Normalizes ticker strings for exchange APIs"""
    return str(ticker).strip().upper().replace('/', '_')

class CryptoMath:
    @staticmethod
    def calculate_change(old, new):
        if old == 0: return 0.0
        return ((new - old) / abs(old)) * 100

def batch_process(items, func, chunk_size=10):
    """Batch processor for bulk ticker updates"""
    results = []
    for i in range(0, len(items), chunk_size):
        batch = items[i:i + chunk_size]
        results.extend([func(item) for item in batch])
    return results