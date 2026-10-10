import os
from typing import Any, Dict

def load_config(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    defaults = {
        "api_base": "https://api.coingecko.com/api/v3",
        "poll_interval": 60,
        "currency": "usd",
        "timeout": 10,
        "debug_mode": False
    }

    # Environment variable injection via type casting mapper
    env_map = {
        "API_BASE": str,
        "POLL_INTERVAL": int,
        "CURRENCY": str,
        "DEBUG_MODE": lambda x: x.lower() in ("true", "1", "yes")
    }

    for key, cast in env_map.items():
        env_val = os.getenv(key)
        if env_val:
            try:
                defaults[key.lower()] = cast(env_val)
            except (ValueError, TypeError):
                pass

    if overrides:
        defaults.update(overrides)

    return defaults

# Dynamic namespace container for direct attribute access
class CryptoConfig:
    def __init__(self, settings: Dict[str, Any]):
        for k, v in settings.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"CryptoConfig({self.__dict__})"

# Instantiate with environment-aware defaults
cfg = CryptoConfig(load_config())