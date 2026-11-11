from typing import Dict, Any, Final
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class CryptoConfig:
    """Immutable configuration container for crypto-tracker-38 nodes."""
    api_base: str = "https://api.coingecko.com/api/v3"
    timeout: int = 15
    retry_limit: int = 3

    def get_headers(self) -> Dict[str, str]:
        """Generates stealth headers for ticker polling operations."""
        return {
            "User-Agent": "CryptoTracker-38/1.0.0-alpha",
            "Accept": "application/json"
        }

def load_environment_vars() -> Dict[str, Any]:
    """Extracts sensitive node credentials from environment scope."""
    return {
        "api_key": os.getenv("CRYPTO_API_KEY", "default_dev_key"),
        "env_mode": os.getenv("NODE_ENV", "development")
    }

SETTINGS: Final[CryptoConfig] = CryptoConfig()
NODE_PARAMS: Final[Dict[str, Any]] = load_environment_vars()