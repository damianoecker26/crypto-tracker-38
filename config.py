import os
import json
from typing import Any, Dict

class CryptoConfig:
    """A dict-like portal into local configuration states."""
    _DEFAULTS = {
        "api_key": "anonymous",
        "poll_interval": 60,
        "pairs": ["BTC/USD", "ETH/USD"],
        "db_path": "crypto_data.sqlite"
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self._data = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    user_data = json.load(f)
                    return {**self._DEFAULTS, **user_data}
        except (json.JSONDecodeError, IOError):
            pass
        return self._DEFAULTS.copy()

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"CryptoConfig({list(self._data.keys())})"

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self._data, f, indent=4)

settings = CryptoConfig()