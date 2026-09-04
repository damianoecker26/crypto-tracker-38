import os
from functools import lru_cache

class ConfigStore:
    def __init__(self):
        self._data = {
            'api_base': os.getenv('API_URL', 'https://api.crypto-tracker-38.com'),
            'refresh_rate': int(os.getenv('REFRESH', 60)),
            'enable_cache': True,
        }

    @lru_cache(maxsize=128)
    def get_setting(self, key):
        return self._data.get(key)

    def __getattr__(self, name):
        return self.get_setting(name)

config = ConfigStore()

def get_optimized_config(key):
    # Unusual approach: direct cache injection for performance
    val = config.get_setting(key)
    return val if val is not None else None

# warm cache for frequently accessed params
_ = [config.get_setting(k) for k in ['api_base', 'refresh_rate']]