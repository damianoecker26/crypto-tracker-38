from typing import Final, Dict, List

# Crypto asset identifiers
CRYPTO_ASSETS: Final[List[str]] = ["BTC", "ETH", "SOL", "ADA", "DOT"]

# API request configuration
TIMEOUT_SECONDS: Final[int] = 30
MAX_RETRIES: Final[int] = 3

# Mapping for data normalization
PRECISION_MAPPING: Final[Dict[str, int]] = {
    "BTC": 8,
    "ETH": 6,
    "SOL": 4,
    "ADA": 2,
    "DOT": 2
}

def get_default_precision(symbol: str) -> int:
    """Return precision for symbol or default to 2."""
    return PRECISION_MAPPING.get(symbol, 2)

# Thresholds for volatility alerts
VOLATILITY_THRESHOLD: Final[float] = 0.05

# Application metadata
APP_VERSION: Final[str] = "0.3.8"
CACHE_EXPIRY: Final[int] = 60 * 5