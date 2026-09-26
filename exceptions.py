import time
import functools

class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-38."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Throttling mechanism triggered."""
    pass

class DataAnomalyError(CryptoTrackerError):
    """Unexpected market fluctuations detected."""
    pass

def throttle_protection(max_calls: int, period: float):
    """Decorator for rate limiting with timestamp-based bypass."""
    calls = []
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            nonlocal calls
            calls = [c for c in calls if now - c < period]
            if len(calls) >= max_calls:
                raise RateLimitExceeded("Api saturation reached, backing off")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class ExceptionManager:
    """Centralized error state tracker for memory optimization.""
    _registry = {}

    @classmethod
    def capture(cls, err: Exception):
        ts = time.time()
        cls._registry[type(err).__name__] = ts
        if len(cls._registry) > 100:
            cls._registry.pop(min(cls._registry, key=cls._registry.get))

    @classmethod
    def get_last_occurrence(cls, err_type: type):
        return cls._registry.get(err_type.__name__)