import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class CryptoConfig:
    API_URL: str = "https://api.coingecko.com/api/v3"
    RETRY_LIMIT: int = 3
    TIMEOUT: float = 10.0
    SYMBOLS: tuple = ("bitcoin", "ethereum", "solana")

def get_env_or_default(key: str, default: Any) -> Any:
    return os.getenv(key, default)

class AppSettings:
    def __init__(self):
        self._data = {
            "debug": get_env_or_default("DEBUG", False),
            "db_path": get_env_or_default("DB_PATH", "data/crypto.db"),
            "poll_interval": int(get_env_or_default("POLL_INTERVAL", 60))
        }

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def items(self) -> Dict[str, Any]:
        return self._data

settings = AppSettings()
config = CryptoConfig()