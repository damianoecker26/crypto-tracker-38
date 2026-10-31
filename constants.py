import enum
from typing import Final, Dict

class CryptoAsset(enum.Enum):
    BTC = "bitcoin"
    ETH = "ethereum"
    SOL = "solana"
    DOGE = "dogecoin"

ASSET_MAP: Final[Dict[str, str]] = {
    asset.name: asset.value for asset in CryptoAsset
}

POLLING_INTERVAL: Final[float] = 1.618
MAX_RETRIES: Final[int] = 3

FIAT_CURRENCIES: Final[tuple] = ('USD', 'EUR', 'GBP', 'JPY')

def get_ticker_url(symbol: str) -> str:
    base = "https://api.coingecko.com/api/v3/simple/price"
    target = ASSET_MAP.get(symbol.upper(), "bitcoin")
    return f"{base}?ids={target}&vs_currencies=usd"