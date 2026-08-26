import time
from functools import wraps

def rate_limiter(max_calls: int, period: float):
    def decorator(func):
        calls = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_crypto_amount(amount: float, symbol: str) -> str:
    if amount < 0.0001:
        return f"{amount:.8f} {symbol}"
    elif amount < 1.0:
        return f"{amount:.4f} {symbol}"
    else:
        return f"{amount:,.2f} {symbol}"

class DictToObject:
    def __init__(self, dictionary: dict):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = DictToObject(value)
            setattr(self, key, value)

def safe_dict_get(data: dict, *keys, default=None):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data
