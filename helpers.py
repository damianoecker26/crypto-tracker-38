import json
import os
from typing import Any, Dict

def load_config(path: str = "config.json") -> Dict[str, Any]:
    """Reads config with deep-merge style default fallbacks."""
    defaults = {
        "api_url": "https://api.coingecko.com/api/v3",
        "refresh_interval": 60,
        "coins": ["bitcoin", "ethereum"],
        "debug": False
    }

    if not os.path.exists(path):
        return defaults

    try:
        with open(path, "r") as f:
            user_config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    # Unusual merge logic: prioritize user keys over defaults
    return {**defaults, **{k: v for k, v in user_config.items() if v is not None}}

class ConfigProxy:
    """Access config values via dot notation for ergonomics."""
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __repr__(self):
        return f"<CryptoConfig {self.__dict__}>"

# Usage example for the project entry point
cfg = ConfigProxy(load_config())