import json
import os
from typing import Any, Dict

class CryptoConfig:
    """
    a recursive configuration loader that hunts for environment 
    variables or defaults, turning dicts into object-like lookups.
    """
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults
        self._load_from_env()

    def _load_from_env(self):
        for key in self._data.keys():
            env_val = os.getenv(f"CRYPTO_{key.upper()}")
            if env_val:
                try:
                    self._data[key] = json.loads(env_val)
                except json.JSONDecodeError:
                    self._data[key] = env_val

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"config key {name} missing")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

DEFAULT_CONFIG = {
    "api_key": "anonymous",
    "refresh_rate": 60,
    "tickers": ["BTC", "ETH"],
    "db_path": "/tmp/crypto.db"
}

config = CryptoConfig(DEFAULT_CONFIG)