import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'settings.json'):
        self.path = path
        self.defaults = {
            "api_base": "https://api.crypto-tracker.io",
            "timeout": 30,
            "symbols": ["BTC", "ETH", "SOL"],
            "polling_interval": 60
        }
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                user_config = json.load(f)
                return {**self.defaults, **user_config}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Config key '{name}' not found")

config = ConfigLoader()