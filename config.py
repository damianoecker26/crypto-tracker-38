import os
from typing import Any, Dict

class CryptoConfig:
    DEFAULT_SETTINGS = {
        "api_base": "https://api.coingecko.com/api/v3",
        "refresh_interval": 60,
        "tracked_pairs": ["BTC", "ETH", "SOL"],
        "db_path": "crypto_data.db",
        "verbosity": "INFO"
    }

    def __init__(self, env_prefix: str = "CT38_"):
        self._storage = self.DEFAULT_SETTINGS.copy()
        self._load_from_env(env_prefix)

    def _load_from_env(self, prefix: str) -> None:
        for key in self._storage.keys():
            env_key = f"{prefix}{key.upper()}"
            val = os.getenv(env_key)
            if val is not None:
                self._storage[key] = self._cast_type(key, val)

    def _cast_type(self, key: str, val: str) -> Any:
        default = self.DEFAULT_SETTINGS[key]
        if isinstance(default, int):
            return int(val)
        if isinstance(default, list):
            return [item.strip() for item in val.split(",")]
        return val

    def get(self, key: str) -> Any:
        return self._storage.get(key)

    def __getitem__(self, key: str) -> Any:
        return self._storage[key]

settings = CryptoConfig()