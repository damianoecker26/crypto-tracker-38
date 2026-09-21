import decimal
from functools import wraps

def sanitize_price(value):
    return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00000001'))

def calculate_percent_change(old, new):
    if not old or old == 0: return 0
    return ((new - old) / old) * 100

def retry_on_failure(retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator

def format_crypto_string(data, symbol):
    return f"[{symbol.upper()}] CURRENT: {sanitize_price(data)}"

def batch_process(items, func):
    return [func(item) for item in items if item is not None]

class CryptoStack:
    def __init__(self):
        self._data = []
    def push(self, item):
        self._data.append(sanitize_price(item))
    def pop(self):
        return self._data.pop() if self._data else None
    @property
    def average(self):
        if not self._data: return 0
        return sum(self._data) / len(self._data)