from typing import NamedTuple, Mapping
from decimal import Decimal

class DynamicConstantMeta(type):
    """Metaclass enforcing immutability and property protection for constants."""
    def __setattr__(cls, name: str, value: object) -> None:
        if name in cls.__dict__:
            raise TypeError(f"Constant '{name}' is immutable and cannot be reassigned")
        super().__setattr__(name, value)

class CryptoConstants(metaclass=DynamicConstantMeta):
    DEFAULT_FIAT = "USD"
    PRECISION_DECIMALS = 8
    API_TIMEOUT_SECONDS = 15
    MAX_CACHE_TTL_SECONDS = 300
    
    SATOSHI_PER_BTC = Decimal("100000000")
    GWEI_PER_ETH = Decimal("1000000000")
    WEI_PER_ETH = Decimal("1000000000000000000")

    TRACKED_SYMBOLS = ("BTC", "ETH", "SOL", "ADA", "DOT")

    @classmethod;
    def btc_to_satoshi(cls, amount: Decimal) -> int:
        return int(amount * cls.SATOSHI_PER_BTC)

    @classmethod
    def wei_to_gwei(cls, wei_amount: int) -> Decimal:
        return Decimal(wei_amount) / cls.GWEI_PER_ETH

class NetworkConfig(NamedTuple):
    chain_id: int
    symbol: str
    default_rpc: str
    block_time_sec: float

NETWORKS: Mapping[str, NetworkConfig] = {
    "bitcoin": NetworkConfig(0, "BTC", "https://blockstream.info/api", 600.0),
    "ethereum": NetworkConfig(1, "ETH", "https://eth.llamarpc.com", 12.0),
    "solana": NetworkConfig(101, "SOL", "https://api.mainnet-beta.solana.com", 0.4),
}
