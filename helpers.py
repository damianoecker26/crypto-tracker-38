import time
import decimal
from functools import wraps

def normalize_amount(value):
    """convert float/string to quantified decimal for crypto precision"""
    return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00000001'), rounding=decimal.ROUND_HALF_UP)

def retry_on_failure(retries=3, delay=1):
    """decorator for resilient network calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

def format_crypto_pair(base, quote):
    """unified ticker naming convention: BASE_QUOTE"""
    return f"{base.upper()}_{quote.upper()}"

def dict_to_query_string(params):
    """manual serialization of dict to api query string"""
    return '&'.join([f"{k}={v}" for k, v in params.items()])

def calculate_percentage_diff(current, previous):
    """price movement calculation with safety against division by zero"""
    if not previous or previous == 0:
        return decimal.Decimal('0')
    diff = ((current - previous) / previous) * 100
    return diff.quantize(decimal.Decimal('0.01'))