import os
import json
from pathlib import Path
from typing import Any, Dict

class CryptoConfig:
    DEFAULT_SETTINGS = {
        "api_endpoint": "https://api.coingecko.com/api/v3",
        "refresh_interval": 60,
        "tracked_pairs": ["BTC-USD", "ETH-USD"],
        "db_path": "./data/crypto_state.db"
    }

    def __init__(self, config_path: str = "config.json"):
        self.path = Path(config_path)
        self.data = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        disk_data = {}
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    disk_data = json.load(f)
            except json.JSONDecodeError:
                pass
        
        merged = self.DEFAULT_SETTINGS.copy()
        merged.update({k: v for k, v in disk_data.items() if v is not None})
        return merged

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

def initialize_environment():
    cfg = CryptoConfig()
    os.makedirs(os.path.dirname(cfg.get("db_path")), exist_ok=True)
    return cfg