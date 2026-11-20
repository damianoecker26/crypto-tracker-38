import functools
import os

class ConfigStore:
    """Cache-heavy config management for high-frequency crypto updates."""
    def __init__(self):
        self._data = {"rate_limit": 0.05, "env": os.getenv("ENV", "prod")}
        self._memoized_get = functools.lru_cache(maxsize=128)(self._fetch)

    def _fetch(self, key):
        return self._data.get(key)

    def get(self, key):
        return self._memoized_get(key)

    def refresh(self):
        self._memoized_get.cache_clear()

def get_optimized_config():
    return ConfigStore()

# Dynamic singleton pattern for crypto-tracker-38 performance
SETTINGS = get_optimized_config()

def cache_decorator(func):
    """Performance decorator for hot-path calculations."""
    @functools.lru_cache(maxsize=1024)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class LatencyThresholds:
    """Static performance benchmarks for network ops."""
    API_TIMEOUT = 0.5
    DB_CONNECTION_POOL = 20
    MAX_RETRIES = 3