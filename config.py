import json
import os
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration provider with dynamic defaults"""
    
    DEFAULTS = {
        "api_base": "https://api.exchange.crypto",
        "timeout": 30,
        "rate_limit": 100,
        "symbols": ["BTC", "ETH"]
    }

    def __init__(self, path: str = "config.json"): 
        self.path = path
        self.data = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        config = self.DEFAULTS.copy()
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    user_data = json.load(f)
                    config.update({k: v for k, v in user_data.items() if k in self.DEFAULTS})
            except (json.JSONDecodeError, IOError):
                pass
        return config

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    @property
    def all(self) -> Dict[str, Any]:
        return self.data