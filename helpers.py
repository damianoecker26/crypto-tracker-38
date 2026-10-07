import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=2):
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

def format_crypto_amount(value, precision=8):
    """Converts float to string with high precision, stripping trailing zeros."""
    val = Decimal(str(value)).normalize()
    return f"{val:.{precision}f}".rstrip('0').rstrip('.')

def calculate_profit_percentage(buy_price, current_price):
    if buy_price <= 0:
        return Decimal('0')
    profit = ((Decimal(str(current_price)) - Decimal(str(buy_price))) / Decimal(str(buy_price))) * 100
    return profit.quantize(Decimal('0.01'))

def sanitize_ticker(ticker):
    """Ensures ticker format matches common exchange patterns."""
    return str(ticker).upper().replace('-', '').replace('/', '').strip()

def get_timestamp_ms():
    return int(time.time() * 1000)