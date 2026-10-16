import json
import os
from pathlib import Path
from typing import Any, Dict


class DynamicCryptoConfig:
    """Creative dynamic configuration loader with default fallback cascading."""

    DEFAULTS: Dict[str, Any] = {
        "api_endpoint": "https://api.coingecko.com/api/v3",
        "update_interval_sec": 15,
        "default_currency": "usd",
        "tracked_symbols": ["btc", "eth", "sol"],
        "enable_websocket": False,
        "max_retries": 3,
        "alert_threshold_pct": 5.0,
    }

    def __init__(self, config_path: str = "config.json", env_prefix: str = "CRYPTO_"):
        self._path = Path(config_path)
        self._env_prefix = env_prefix
        self._file_data = self._load_file()

    def _load_file(self) -> Dict[str, Any]:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def get(self, key: str) -> Any:
        env_key = f"{self._env_prefix}{key.upper()}"
        if env_key in os.environ:
            return self._cast_value(os.environ[env_key], self.DEFAULTS.get(key))

        if key in self._file_data:
            return self._file_data[key]

        if key in self.DEFAULTS:
            return self.DEFAULTS[key]

        raise KeyError(f"Configuration option '{key}' not set.")

    def __getattr__(self, name: str) -> Any:
        try:
            return self.get(name)
        except KeyError as err:
            raise AttributeError(err) from None

    def _cast_value(self, val: str, reference: Any) -> Any:
        if reference is None:
            return val
        ref_type = type(reference)
        if ref_type is bool:
            return val.lower() in ("true", "1", "yes")
        if ref_type is list:
            return [item.strip() for item in val.split(",")]
        try:
            return ref_type(val)
        except (ValueError, TypeError):
            return val


config = DynamicCryptoConfig()
