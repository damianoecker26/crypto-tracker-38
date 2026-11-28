import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy for crypto-tracker-38 configuration."""
    _defaults = {
        "api_base": "https://api.coingecko.com/api/v3",
        "refresh_rate": 60,
        "watch_list": ["bitcoin", "ethereum"],
        "debug": False
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self.settings = self._defaults.copy()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    user_config = json.load(f)
                    self.settings.update(user_config)
                except json.JSONDecodeError:
                    pass

    def __getattr__(self, name: str) -> Any:
        return self.settings.get(name)

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.settings, f, indent=4)

config = ConfigLoader()