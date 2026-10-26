import json
import os
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "base_currency": "USD",
    "refresh_rate_sec": 12,
    "tracked_assets": ["BTC", "ETH", "SOL"],
    "endpoints": {
        "coingecko": "https://api.coingecko.com/api/v3",
        "binance": "https://api.binance.com/api/v3"
    },
    "alerts_enabled": True,
    "min_volume_usd": 1000000.0,
}

class ConfigLoader:
    def __init__(self, filepath: Union[str, Path] = "crypto_config.json"):
        self.filepath = Path(filepath)
        self._store: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        loaded = {}
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
            except json.JSONDecodeError:
                pass
        self._store = self._deep_merge(DEFAULT_CONFIG, loaded)
        self._apply_env_overrides()

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        merged = base.copy()
        for k, v in override.items():
            if isinstance(v, dict) and isinstance(merged.get(k), dict):
                merged[k] = self._deep_merge(merged[k], v)
            else:
                merged[k] = v
        return merged

    def _apply_env_overrides(self) -> None:
        for k, v in os.environ.items():
            if k.startswith("CRYPTO_"):
                keys = k[7:].lower().split("__")
                target = self._store
                for key in keys[:-1]:
                    target = target.setdefault(key, {})
                target[keys[-1]] = json.loads(v) if v.lower() in ["true", "false"] or v.isdigit() else v

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._wrap(self._store[name])
        raise AttributeError(f"Configuration key '{name}' not found")

    @classmethod
    def _wrap(cls, val: Any) -> Any:
        if isinstance(val, dict):
            return type("ConfigProxy", (), {k: cls._wrap(v) for k, v in val.items()})()
        return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)
