import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, path: str = 'config.json'):
        self.path = path
        self.defaults = {
            "api_key": "anonymous",
            "interval": 60,
            "symbols": ["BTC", "ETH", "SOL"],
            "base_currency": "USD",
            "debug": False
        }
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                raw = json.load(f)
                return {**self.defaults, **{k: v for k, v in raw.items() if k in self.defaults}}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str) -> Any:
        return self.data.get(key, self.defaults.get(key))

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

config = CryptoConfig()