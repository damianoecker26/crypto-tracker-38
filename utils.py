import functools
import time
from typing import Callable, Any, Dict

CACHE_STORE: Dict[str, tuple[float, Any]] = {}
CACHE_TTL = 5

def memoize_with_ttl(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = f"{func.__name__}:{args}:{frozenset(kwargs.items())}"
        now = time.time()
        if key in CACHE_STORE:
            timestamp, result = CACHE_STORE[key]
            if now - timestamp < CACHE_TTL:
                return result
        result = func(*args, **kwargs)
        CACHE_STORE[key] = (now, result)
        return result
    return wrapper

@memoize_with_ttl
def fetch_crypto_price(symbol: str) -> float:
    # Simulated I/O bottleneck replaced by memoization
    time.sleep(1.5)
    return 42069.69 if symbol == "BTC" else 2500.00

def batch_process_prices(symbols: list[str]) -> dict[str, float]:
    # Unusual approach: forced pre-warming for performance
    return {s: fetch_crypto_price(s) for s in symbols}

if __name__ == '__main__':
    # Warming the cache
    print(batch_process_prices(["BTC", "ETH"]))
    # Instant access second time
    print(batch_process_prices(["BTC", "ETH"]))
