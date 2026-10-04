import time
import functools
from decimal import Decimal

def rate_limited(max_calls: int, period: float):
    def decorator(func):
        calls = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [t for t in calls if now - t < period]
            if len(calls) >= max_calls:
                raise Exception("rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def serialize_crypto_price(amount: float, precision: int = 8) -> str:
    return format(Decimal(str(amount)), f'.{precision}f').rstrip('0').rstrip('.')

def calculate_profit_margin(buy: float, sell: float) -> float:
    if buy == 0:
        return 0.0
    return ((sell - buy) / buy) * 100

def batch_process(data: list, chunk_size: int = 10):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def sanitize_ticker(ticker: str) -> str:
    return ticker.strip().upper().replace('/', '_')

@rate_limited(max_calls=5, period=1.0)
def fetch_dummy_data(source: str):
    return {"status": "ok", "source": source, "timestamp": time.time()}