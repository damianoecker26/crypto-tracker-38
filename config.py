import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults
        self._load_env()

    def _load_env(self) -> None:
        # Map ENV_VARS to dictionary keys dynamically
        mapping = {
            'CRYPTO_API_KEY': 'api_key',
            'CRYPTO_SYMBOL': 'ticker',
            'CRYPTO_INTERVAL': 'interval'
        }
        for env_key, config_key in mapping.items():
            if val := os.getenv(env_key):
                self._data[config_key] = val

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"CryptoConfig({self._data})"

def get_config() -> ConfigLoader:
    defaults = {
        'api_key': 'default_test_key',
        'ticker': 'BTC/USD',
        'interval': '1m',
        'db_path': 'ledger.db'
    }
    return ConfigLoader(defaults)

# Usage pattern: cfg = get_config(); print(cfg['ticker'])