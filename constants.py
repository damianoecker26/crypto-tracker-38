import enum
from typing import Final

class CryptoSymbols(enum.Enum):
    BTC = "bitcoin"
    ETH = "ethereum"
    SOL = "solana"
    DOGE = "dogecoin"

API_BASE_URL: Final[str] = "https://api.coingecko.com/api/v3"

class MarketStatus(enum.IntEnum):
    BULLISH = 1
    BEARISH = -1
    SIDEWAYS = 0

RATE_LIMIT_DELAY: Final[float] = 1.5

RETRIEVAL_SCHEMA: Final[dict] = {
    "vs_currency": "usd",
    "include_market_cap": "true",
    "include_24hr_vol": "true",
    "precision": 2
}

def get_symbol_map() -> dict:
    return {member.name: member.value for member in CryptoSymbols}

SUPPORTED_TOKENS: Final[list[str]] = list(get_symbol_map().values())

ERROR_MESSAGES: Final[dict[str, str]] = {
    "network": "provider connectivity failure",
    "parse": "invalid response payload structure",
    "auth": "missing api credentials"
}