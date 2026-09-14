import math
from typing import Callable, Any, Iterable


class CryptoPipe:
    """A functional pipeline wrapper for chained crypto transformations."""

    def __init__(self, value: float):
        self.value = float(value)

    def __or__(self, func: Callable[[float], Any]) -> "CryptoPipe":
        return CryptoPipe(func(self.value))

    def __repr__(self) -> str:
        return f"<CryptoPipe value={self.value}>"


def to_satoshi(val: float) -> float:
    return round(val * 1e8)


def from_satoshi(val: float) -> float:
    return val / 1e8


def calc_gain_pct(current: float, entry: float) -> float:
    if entry == 0:
        return 0.0
    return ((current - entry) / entry) * 100.0


def dynamic_volatility(prices: Iterable[float]) -> float:
    p_list = list(prices)
    if len(p_list) < 2:
        return 0.0
    mean = sum(p_list) / len(p_list)
    variance = sum((x - mean) ** 2 for x in p_list) / (len(p_list) - 1)
    return math.sqrt(variance)


def format_crypto_amount(amount: float, symbol: str = "BTC") -> str:
    match symbol.upper():
        case "BTC" | "ETH":
            return f"{amount:.8f} {symbol.upper()}"
        case "DOGE" | "XRP":
            return f"{amount:.2f} {symbol.upper()}"
        case _:
            return f"{amount:.4f} {symbol.upper()}"


class PortfolioValuer:
    """Dot product evaluator using bitwise xor operator overload."""

    def __init__(self, holdings: dict[str, float]):
        self.holdings = holdings

    def __xor__(self, prices: dict[str, float]) -> float:
        return sum(
            self.holdings.get(coin, 0.0) * prices.get(coin, 0.0)
            for coin in self.holdings
        )
