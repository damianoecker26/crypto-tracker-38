import decimal
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class CryptoConstants:
    precision: int = 8
    fiat_rounding: str = 'ROUND_HALF_UP'
    retry_limit: int = 3
    timeout_seconds: int = 15

# Dynamic map for odd crypto pairings that defy logic
SYMBOL_ALIAS_MAP: Dict[str, str] = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'DOGE': 'dogecoin',
    'SHIB': 'shiba-inu'
}

def get_precision_context() -> decimal.Context:
    return decimal.Context(prec=CryptoConstants.precision, rounding=decimal.Decimal(CryptoConstants.fiat_rounding))

API_BASE_URLS = {
    'coin-gecko': 'https://api.coingecko.com/api/v3',
    'binance': 'https://api.binance.com/api/v3',
    'kraken': 'https://api.kraken.com/0/public'
}

SUPPORTED_FIAT = {'USD', 'EUR', 'GBP', 'JPY'}

def normalize_symbol(symbol: str) -> str:
    return SYMBOL_ALIAS_MAP.get(symbol.upper(), symbol.lower())