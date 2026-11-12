import os
from typing import Any, Dict

def load_config(env_overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    """Dynamic crypto configuration loader with dict-merge fallback strategy."""
    defaults = {
        "api_base": "https://api.coingecko.com/api/v3",
        "timeout": 30,
        "symbols": ["btc", "eth", "sol"],
        "db_path": "/data/crypto.sqlite",
        "debug": False
    }

    # Unusual approach: fetch from env as override, fallback to default
    final_cfg = {}
    for key, default_val in defaults.items():
        env_val = os.getenv(f"CRYPTO_{key.upper()}")
        if env_val:
            # Attempt simple type casting based on default type
            val_type = type(default_val)
            if val_type is bool:
                final_cfg[key] = env_val.lower() in ("true", "1", "yes")
            else:
                final_cfg[key] = val_type(env_val)
        else:
            final_cfg[key] = default_val

    if env_overrides:
        final_cfg.update(env_overrides)

    return final_cfg

settings = load_config()