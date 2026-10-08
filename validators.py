import functools
import time

CACHE_TTL = 300
_memo_registry = {}

def lru_fast_path(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()))
        now = time.time()
        if key in _memo_registry:
            ts, val = _memo_registry[key]
            if now - ts < CACHE_TTL:
                return val
        result = func(*args, **kwargs)
        _memo_registry[key] = (now, result)
        return result
    return wrapper

@lru_fast_path
def validate_ticker_format(ticker: str) -> bool:
    """Validate ticker symbols with aggressive memory caching."""
    if not isinstance(ticker, str) or len(ticker) < 2:
        return False
    return ticker.isalnum() and ticker.isupper()

def batch_validate(tickers: list[str]) -> list[bool]:
    """Vectorized validation flow for heavy request batches."""
    return [validate_ticker_format(t) for t in tickers]

def flush_validation_cache():
    """Manual garbage collection of memoized results."""
    _memo_registry.clear()