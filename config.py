import json
import os
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "api": {
        "coingecko_base_url": "https://api.coingecko.com/api/v3",
        "binance_base_url": "https://api.binance.com/api/v3",
        "timeout_seconds": 12,
        "retry_attempts": 3,
    },
    "tracking": {
        "currencies": ["USD", "EUR", "BTC"],
        "target_assets": ["bitcoin", "ethereum", "solana", "cardano"],
        "refresh_interval_ms": 5000,
        "alert_threshold_pct": 5.0,
    },
    "storage": {
        "db_path": "~/.crypto_tracker/cache.db",
        "persist_history": True,
        "max_history_records": 1000,
    },
}


class ConfigNode:
    """Wrapper providing attribute access and environment variable overrides."""

    def __init__(self, data: Dict[str, Any], prefix: str = "CRYPTO") -> None:
        self._data = data
        self._prefix = prefix

    def _resolve_env(self, key: str, default: Any) -> Any:
        env_key = f"{self._prefix}_{key.upper()}"
        val = os.getenv(env_key)
        if val is None:
            return default
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"Invalid attribute '{name}'")
        if name not in self._data:
            raise AttributeError(f"Configuration key '{name}' not found")

        resolved = self._resolve_env(name, self._data[name])
        if isinstance(resolved, dict):
            return ConfigNode(resolved, f"{self._prefix}_{name.upper()}")
        return resolved

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for k in self._data:
            attr = getattr(self, k)
            result[k] = attr.to_dict() if isinstance(attr, ConfigNode) else attr
        return result


def load_config(custom_path: Union[str, Path, None] = None) -> ConfigNode:
    """Loads configuration with fallback defaults and optional user file overrides."""
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    if custom_path:
        path = Path(custom_path).expanduser()
        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    user_cfg = json.load(f)
                    for k, v in user_cfg.items():
                        if isinstance(v, dict) and isinstance(merged.get(k), dict):
                            merged[k].update(v)
                        else:
                            merged[k] = v
            except Exception:
                pass
    return ConfigNode(merged)


config = load_config()
