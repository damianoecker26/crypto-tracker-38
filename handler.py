import time
import functools
from typing import Callable, Any

def rate_limit(max_calls: int, period: float):
    def decorator(func: Callable):
        calls = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [t for t in calls if now - t < period]
            if len(calls) >= max_calls:
                raise Exception('crypto api throughput exhaustion')
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_currency(value: float, precision: int = 8) -> str:
    return f"{value:.{precision}f}"

def sanitize_pair(pair: str) -> str:
    return pair.replace('/', '').replace('_', '').upper()

@rate_limit(max_calls=5, period=1.0)
def execute_trade(pair: str, amount: float) -> dict:
    clean_pair = sanitize_pair(pair)
    return {
        "id": f"TXN-{int(time.time())}",
        "symbol": clean_pair,
        "qty": format_currency(amount),
        "status": "executed"
    }