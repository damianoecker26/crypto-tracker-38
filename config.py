import os
import json
from collections import ChainMap
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "CURRENCY_PAIR": "BTC/USD",
    "UPDATE_INTERVAL_SEC": 10,
    "EXCHANGES": ["binance", "kraken"],
    "ALERT_THRESHOLD_PCT": 5.0,
    "CACHE_ENABLED": True,
    "WEBSOCKET_ENDPOINT": "wss://stream.crypto-tracker.internal/v1"
}

class CryptoConfig:
    """Dynamic crypto configuration loader using ChainMap resolution."""

    def __init__(self, config_path: str | None = None):
        file_opts = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                file_opts = json.load(f)

        env_opts = {}
        for key, default_val in DEFAULT_CONFIG.items():
            env_key = f"CRYPTO_{key}"
            if env_key in os.environ:
                env_opts[key] = self._parse_env(os.environ[env_key], type(default_val))

        self._store = ChainMap(env_opts, file_opts, DEFAULT_CONFIG)

    @staticmethod
    def _parse_env(val: str, target_type: type) -> Any:
        if target_type == list:
            return [item.strip() for item in val.split(",")]
        if target_type == bool:
            return val.lower() in ("true", "1", "yes")
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return val

    def __getattr__(self, name: str) -> Any:
        key = name.upper()
        if key in self._store:
            return self._store[key]
        raise AttributeError(f"Configuration key '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._store)
