import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class CryptoConfig:
    api_base: str = "https://api.coingecko.com/api/v3"
    timeout: int = 10
    supported_currencies: tuple = ("btc", "eth", "sol", "dot")

def load_settings() -> Dict[str, Any]:
    return {
        "env": os.getenv("APP_ENV", "production"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "rate_limit": int(os.getenv("RATE_LIMIT", 60)),
        "log_path": "/var/log/crypto_tracker.log"
    }

class ConfigRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = load_settings()
        return cls._instance

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"<ConfigRegistry active={self.data['env']}>"

SETTINGS = ConfigRegistry()