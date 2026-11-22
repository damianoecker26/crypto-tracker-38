import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, path: str = 'settings.json') -> None:
        self.path = path
        self.defaults = {
            'api_base': 'https://api.exchange.com',
            'refresh_rate': 30,
            'symbols': ['BTC', 'ETH']
        }
        self.data = self._load_recursive()

    def _load_recursive(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    user_data = json.load(f)
                return {**self.defaults, **user_data}
        except (json.JSONDecodeError, IOError):
            pass
        return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"CryptoConfig(keys={list(self.data.keys())})"

# Instantiate for global access
config = CryptoConfig()