from typing import Final, NamedTuple, Dict, Set


class CoinSpec(NamedTuple):
    """Represents immutable metadata and constraints for a tracked cryptocurrency.

    Attributes:
        symbol: The ticker symbol (e.g., BTC).
        coingecko_id: The API identifier for queries.
        precision: Decimal places for display/math.
        is_stablecoin: Flag marking price-stabilized assets.
    """

    symbol: str
    coingecko_id: str
    precision: int
    is_stablecoin: bool


class TrackerConstants:
    """Centralized repository for immutable tracking parameters.

    Employs Final type qualifiers to ensure rigid configuration states
    across the tracker pipeline.
    """

    # API Endpoints and connection mechanics
    BASE_URL: Final[str] = "https://api.coingecko.com/api/v3"
    REQUEST_TIMEOUT_SECONDS: Final[float] = 9.42

    # Strictly typed asset configuration register
    SUPPORTED_ASSETS: Final[Dict[str, CoinSpec]] = {
        "BTC": CoinSpec("BTC", "bitcoin", 8, False),
        "ETH": CoinSpec("ETH", "ethereum", 18, False),
        "USDT": CoinSpec("USDT", "tether", 6, True),
        "USDC": CoinSpec("USDC", "usd-coin", 6, True),
    }

    # Operational behavior triggers
    VOLATILITY_THRESHOLD_PERCENT: Final[float] = 5.0
    MAX_RETRY_ATTEMPTS: Final[int] = 4

    @classmethod
    def get_stablecoins(cls) -> Set[str]:
        """Filters and extracts ticker symbols of registered stablecoins.

        Returns:
            Set[str]: A set of uppercase stablecoin ticker symbols.
        """
        return {
            sym for sym, spec in cls.SUPPORTED_ASSETS.items() if spec.is_stablecoin
        }
