import json
import os
from typing import Dict, Any, Optional

def deep_update(source: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in overrides.items():
        if isinstance(value, dict) and key in source and isinstance(source[key], dict):
            source[key] = deep_update(source[key], value)
        else:
            source[key] = value
    return source

def load_crypto_config(
    config_path: Optional[str] = None,
    defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if defaults is None:
        defaults = {
            "base_api_url": "https://api.coingecko.com/api/v3",
            "default_coins": ["bitcoin", "ethereum", "solana"],
            "update_frequency_seconds": 300,
            "max_retries": 3,
            "timeout": 10,
            "enable_logging": True,
            "price_alerts": {
                "enabled": True,
                "threshold_percent": 2.5
            }
        }
    file_config = {}
    path = config_path or os.getenv("CRYPTO_TRACKER_CONFIG", "config.json")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
        except (json.JSONDecodeError, IOError):
            file_config = {}
    env_config = {}
    for env_key, env_val in os.environ.items():
        if env_key.startswith("CRYPTO_"):
            key = env_key[7:].lower()
            parts = key.split("__")
            current = env_config
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            try:
                current[parts[-1]] = json.loads(env_val)
            except (json.JSONDecodeError, TypeError):
                current[parts[-1]] = env_val
    result = dict(defaults)
    for layer in [file_config, env_config]:
        result = deep_update(result, layer)
    if isinstance(result.get("update_frequency_seconds"), str):
        try:
            result["update_frequency_seconds"] = int(result["update_frequency_seconds"])
        except ValueError:
            pass
    return result

class ConfigLoader:
    def __init__(self, config_path: Optional[str] = None):
        self._data = load_crypto_config(config_path)
    def __getitem__(self, key: str) -> Any:
        return self._data[key]
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no '{name}'")
    def reload(self, config_path: Optional[str] = None) -> None:
        self._data = load_crypto_config(config_path)

def get_config() -> ConfigLoader:
    return ConfigLoader()