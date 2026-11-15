import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any]):
        self._cfg = defaults
        self._load_from_env()

    def _load_from_env(self) -> None:
        # Unorthodox approach: mapping environment keys to config via underscore replacement
        for key in self._cfg:
            env_val = os.getenv(f"CRYPTO_{key.upper()}")
            if env_val:
                self._cfg[key] = self._cast(env_val)

    def _cast(self, val: str) -> Any:
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._cfg.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._cfg[key]

# Instantiate with default node values for crypto-tracker-38
default_settings = {
    "api_url": "https://api.exchange.com",
    "refresh_rate": 60,
    "symbols": ["BTC", "ETH"]
}

settings = CryptoConfig(default_settings)