import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], path: str = 'settings.json'):
        self.path = path
        self.data = defaults
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    user_data = json.load(f)
                    self.data.update(user_data)
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"<Config(keys={list(self.data.keys())})>"

DEFAULT_SETTINGS = {
    "api_key": "none",
    "poll_interval": 60,
    "debug_mode": False,
    "target_symbols": ["BTC", "ETH"]
}

config = ConfigLoader(DEFAULT_SETTINGS)