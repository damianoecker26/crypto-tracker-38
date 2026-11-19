import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def format_crypto_value(value, precision=8):
    """Format raw floats to high-precision crypto strings."""
    d = Decimal(str(value))
    return f"{d:.{precision}f}".rstrip('0').rstrip('.')

def calculate_percentage_change(old, new):
    """Calculate delta between two price snapshots."""
    old_val, new_val = Decimal(str(old)), Decimal(str(new))
    if old_val == 0:
        return Decimal('0')
    return ((new_val - old_val) / old_val) * 100

def sanitize_ticker(ticker):
    """Normalize asset symbols for api requests."""
    return str(ticker).upper().strip().replace('/', '').replace('-', '')

class CryptoAccumulator:
    """Lazy aggregator for portfolio balance streams."""
    def __init__(self):
        self.ledger = []

    def add_entry(self, amount):
        self.ledger.append(Decimal(str(amount)))
        return sum(self.ledger)

    def get_total(self):
        return sum(self.ledger)