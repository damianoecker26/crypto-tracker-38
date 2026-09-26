import time
import functools
from decimal import Decimal

def format_crypto_val(value: float, precision: int = 8) -> str:
    return f"{Decimal(str(value)):.{precision}f}".rstrip('0').rstrip('.')

def rate_limited(calls: int, period: int):
    def decorator(func):
        history = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            history[:] = [t for t in history if now - t < period]
            if len(history) >= calls:
                time.sleep(period - (now - history[0]))
            history.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

class CryptoTransformer:
    @staticmethod
    def to_satoshis(btc_amount: float) -> int:
        return int(btc_amount * 10**8)

    @staticmethod
    def calculate_pnl(entry: float, current: float, size: float) -> float:
        return (current - entry) * size

def sanitize_ticker(ticker: str) -> str:
    return ''.join(filter(str.isalnum, ticker)).upper()