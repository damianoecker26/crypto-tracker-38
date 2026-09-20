import os
import json
from typing import Any, Dict

DEFAULTS: Dict[str, Any] = {
    "api": {
        "coingecko_url": "https://api.coingecko.com/api/v3",
        "rate_limit_delay": 1.5,
        "retry_attempts": 3
    },
    "tracker": {
        "symbols": ["BTC", "ETH", "SOL"],
        "update_interval_sec": 30,
        "alert_threshold_percentage": 5.0
    },
    "logging": {
        "level": "INFO",
        "save_to_file": False
    }
}

class CryptoConfig:
    def __init__(self, filepath: str = "config.json"):
        self._raw = DEFAULTS.copy()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    self._merge(self._raw, json.load(f))
                except json.JSONDecodeError:
                    pass
        self._apply_env_overrides(self._raw, "CRYPTO")

    def _merge(self, base: dict, override: dict) -> None:
        for k, v in override.items():
            if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                self._merge(base[k], v)
            else:
                base[k] = v

    def _apply_env_overrides(self, current: dict, prefix: str) -> None:
        for k, v in list(current.items()):
            env_key = f"{prefix}_{k.upper()}"
            if isinstance(v, dict):
                self._apply_env_overrides(v, env_key)
            else:
                env_val = os.environ.get(env_key)
                if env_val is not None:
                    try:
                        current[k] = json.loads(env_val.lower())
                    except json.JSONDecodeError:
                        current[k] = type(v)(env_val) if v is not None else env_val

    def __truediv__(self, path: str) -> Any:
        parts = [p for p in path.split("/") if p]
        val = self._raw
        try:
            for part in parts:
                val = val[part]
            return val
        except (KeyError, TypeError) as err:
            raise KeyError(f"Configuration path '{path}' not found") from err

    def __repr__(self) -> str:
        return f"CryptoConfig({self._raw})"

config = CryptoConfig()
