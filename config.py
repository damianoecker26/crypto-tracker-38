import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigLoader:
    """Dynamic configuration cascade for crypto tracking parameters."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "base_currency": "USD",
        "tracked_symbols": ["BTC", "ETH", "SOL"],
        "update_interval": 15,
        "exchange": "coingecko",
        "alert_threshold_pct": 5.0,
        "enable_websocket": True,
        "cache_ttl_sec": 300,
    }

    ENV_PREFIX = "CRYPTO_"

    def __init__(self, config_path: str = "config.json"):
        self._path = Path(config_path)
        self._raw_data = self._load_cascade()

    def _cast_env_val(self, key: str, default_val: Any) -> Any:
        env_key = f"{self.ENV_PREFIX}{key.upper()}"
        val = os.getenv(env_key)
        if val is None:
            return default_val

        val_type = type(default_val)
        if val_type is bool:
            return val.lower() in ("true", "1", "yes")
        if val_type is list:
            return [item.strip() for item in val.split(",")] if val else []
        try:
            return val_type(val)
        except (ValueError, TypeError):
            return default_val

    def _load_cascade(self) -> Dict[str, Any]:
        file_config = {}
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
            except (json.JSONDecodeError, OSError):
                file_config = {}

        merged = {**self.DEFAULT_CONFIG, **file_config}
        return {
            k: self._cast_env_val(k, merged.get(k, v))
            for k, v in self.DEFAULT_CONFIG.items()
        }

    def __getattr__(self, name: str) -> Any:
        if name in self._raw_data:
            return self._raw_data[name]
        raise AttributeError(f"Configuration option '{name}' is not defined")

    def __getitem__(self, item: str) -> Any:
        return self._raw_data[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._raw_data)


config = ConfigLoader()
