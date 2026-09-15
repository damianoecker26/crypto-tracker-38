from enum import Enum
from typing import Final

class CryptoAsset(Enum):
    BTC = "bitcoin"
    ETH = "ethereum"
    SOL = "solana"
    LINK = "chainlink"

DEFAULT_API_TIMEOUT: Final[int] = 15
MAX_RETRIES: Final[int] = 3
CACHE_EXPIRATION_SECONDS: Final[int] = 60

BASE_URL: Final[str] = "https://api.coingecko.com/api/v3"

ERROR_MESSAGES = {
    "connection": "network connectivity issue detected",
    "rate_limit": "coingecko api rate limit exceeded",
    "timeout": "request execution time exceeded threshold"
}

def get_supported_ids() -> list[str]:
    return [asset.value for asset in CryptoAsset]

SUPPORTED_ASSETS: Final[list[str]] = get_supported_ids()