import os
import json
from pathlib import Path
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, path: str = 'settings.json') -> None:
        self.path = Path(path)
        self.defaults = {
            "api_key": "anonymous",
            "refresh_rate": 30,
            "symbols": ["BTC", "ETH", "SOL"],
            "debug": False
        }
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                user_cfg = json.load(f)
            return {**self.defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key, self.defaults.get(key))

    def get_env_override(self) -> None:
        for key in self.defaults:
            env_val = os.getenv(f"CRYPTO_{key.upper()}")
            if env_val:
                self.data[key] = type(self.defaults[key])(env_val)

config = CryptoConfig()