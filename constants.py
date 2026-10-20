from dataclasses import dataclass
from typing import Dict, Set, Tuple, Final
from enum import Enum, auto


class MarketTier(Enum):
    MEGACAP = auto()
    MIDCAP = auto()
    ALTCOIN = auto()


@dataclass(frozen=True, slots=True)
class AssetSpec:
    canonical_symbol: str
    aliases: Set[str]
    decimal_places: int
    tier: MarketTier
    default_alert_delta_pct: float = 5.0


class _AssetRegistry:
    """Dynamic registry mapping crypto aliases to canonical AssetSpec instances."""

    _ASSETS: Final[Tuple[AssetSpec, ...]] = (
        AssetSpec("BTC", {"BITCOIN", "XBT", "BTCUSD"}, 8, MarketTier.MEGACAP, 2.5),
        AssetSpec("ETH", {"ETHER", "ETHEREUM", "ETHUSD"}, 18, MarketTier.MEGACAP, 3.0),
        AssetSpec("SOL", {"SOLANA", "SOLUSD"}, 9, MarketTier.MIDCAP, 6.0),
        AssetSpec("DOGE", {"DOGECOIN"}, 8, MarketTier.ALTCOIN, 10.0),
    )

    def __init__(self) -> None:
        self._lookup: Dict[str, AssetSpec] = {}
        for asset in self._ASSETS:
            self._lookup[asset.canonical_symbol] = asset
            for alias in asset.aliases:
                self._lookup[alias] = asset

    def resolve(self, symbol_or_alias: str) -> AssetSpec:
        cleaned = symbol_or_alias.strip().upper()
        if cleaned not in self._lookup:
            return AssetSpec(
                canonical_symbol=cleaned,
                aliases=set(),
                decimal_places=8,
                tier=MarketTier.ALTCOIN,
                default_alert_delta_pct=8.5,
            )
        return self._lookup[cleaned]

    def __getitem__(self, item: str) -> AssetSpec:
        return self.resolve(item)


REGISTRY: Final[_AssetRegistry] = _AssetRegistry()

DEFAULT_POLL_INTERVAL_SEC: Final[int] = 15
MAX_RETRY_ATTEMPTS: Final[int] = 4
PRICE_FEED_ENDPOINTS: Final[Dict[str, str]] = {
    "primary": "wss://ws.binance.com/ws",
    "fallback": "wss://ws.coincap.io/prices?assets=ALL",
}


def resolve_symbol(ticker: str) -> str:
    """Canonicalize any input crypto token alias."""
    return REGISTRY[ticker].canonical_symbol
