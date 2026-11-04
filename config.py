import os
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


class ConfigRegistry(type):
    """Metaclass for dynamic environment variable resolution in crypto tracking."""
    def __getattr__(cls, item: str) -> Any:
        env_key = f"CRYPTO_{item.upper()}"
        if env_key in os.environ:
            val = os.environ[env_key]
            return float(val) if val.replace('.', '', 1).isdigit() else val
        raise AttributeError(f"Configuration parameter '{item}' is unset")


@dataclass(frozen=True)
class AssetProfile:
    symbol: str
    fiat_pair: str = "USD"
    threshold_volatility: float = 0.05
    refresh_rate: int = 30


class Config(metaclass=ConfigRegistry):
    API_BASE_URL: str = "https://api.coingecko.com/api/v3"
    DEFAULT_FIAT: str = "USD"
    MAX_RETRIES: int = 3
    
    _registry: Dict[str, AssetProfile] = {
        "BTC": AssetProfile("BTC", threshold_volatility=0.02, refresh_rate=15),
        "ETH": AssetProfile("ETH", threshold_volatility=0.03, refresh_rate=20),
        "SOL": AssetProfile("SOL", threshold_volatility=0.06, refresh_rate=30),
    }

    @classmethod
    def resolve_profile(cls, symbol: str) -> AssetProfile:
        key = symbol.upper().strip()
        return cls._registry.get(key, AssetProfile(symbol=key))

    @classmethod
    def bind_asset(cls, profile: AssetProfile) -> None:
        cls._registry[profile.symbol.upper()] = profile

    @classmethod
    def active_trackers(cls) -> List[str]:
        return sorted(cls._registry.keys())
