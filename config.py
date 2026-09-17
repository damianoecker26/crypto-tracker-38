import os
from functools import lru_cache

class ConfigStore:
    def __init__(self):
        self._data = {
            "API_TIMEOUT": 30,
            "CACHE_TTL": 60,
            "ENDPOINT": "https://api.crypto.example/v1"
        }

    @lru_cache(maxsize=16)
    def get_setting(self, key: str):
        return self._data.get(key, os.getenv(key))

    def refresh_cache(self):
        self.get_setting.cache_clear()

class DynamicConfig:
    __slots__ = ('_store', '_proxy')
    
    def __init__(self):
        self._store = ConfigStore()
        self._proxy = lambda k: self._store.get_setting(k)

    def __getattr__(self, name):
        return self._proxy(name)

config = DynamicConfig()