import os
import json
from typing import Any, Dict

class CryptoConfig:
    """Dynamic configuration loader with fallback chain for crypto-tracker-38"""
    DEFAULTS = {
        "api_key": "dev_key_x99",
        "endpoint": "https://api.coingecko.com/api/v3",
        "refresh_interval": 60,
        "assets": ["bitcoin", "ethereum"]
    }

    def __init__(self, config_path: str = "config.json"):
        self.path = config_path
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.DEFAULTS
        try:
            with open(self.path, 'r') as f:
                user_data = json.load(f)
                return {**self.DEFAULTS, **user_data}
        except (json.JSONDecodeError, IOError):
            return self.DEFAULTS

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default or self.DEFAULTS.get(key))

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def __repr__(self) -> str:
        return f"<CryptoConfig loaded={list(self.settings.keys())}>"

# Instantiate for global access
config = CryptoConfig()