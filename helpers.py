"""Cryptocurrency metric conversion and streaming analysis pipeline helpers."""

from typing import TypeVar, Callable, Any, Generator, Union
from decimal import Decimal, ROUND_HALF_UP

T = TypeVar("T")
R = TypeVar("R")


class CryptoPipe:
    """Composable data pipe wrapper for chaining crypto transformations using bitwise right shift."""

    def __init__(self, func: Callable[[Any], Any]) -> None:
        """Initialize the pipe with a transformation function.

        Args:
            func: The single-argument callable to wrap into a pipe node.
        """
        self.func = func

    def __rshift__(self, other: Union["CryptoPipe", Callable[[Any], Any]]) -> "CryptoPipe":
        """Chain another function or CryptoPipe onto this pipeline.

        Args:
            other: Target function or pipe to execute next.

        Returns:
            A new CryptoPipe instance representing the combined execution chain.
        """
        next_func = other.func if isinstance(other, CryptoPipe) else other
        return CryptoPipe(lambda x: next_func(self.func(x)))

    def __call__(self, value: Any) -> Any:
        """Execute the underlying function pipeline on a given input value."""
        return self.func(value)


def satoshi_to_btc(sats: Union[int, str]) -> Decimal:
    """Convert Satoshi integer quantity into exact Bitcoin Decimal representation.

    Args:
        sats: Amount in Satoshis.

    Returns:
        Decimal representation of the amount in BTC.
    """
    return Decimal(str(sats)) / Decimal("100000000")


def format_currency(symbol: str = "$") -> Callable[[Union[float, Decimal]], str]:
    """Generate a closure that formats numbers into fixed-precision currency strings.

    Args:
        symbol: Currency prefix symbol.

    Returns:
        Callable formatting input amounts to formatted strings.
    """
    def formatter(amount: Union[float, Decimal]) -> str:
        val = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{symbol}{val:,.2f}"

    return formatter


def stream_moving_average(alpha: float = 0.2) -> Generator[Decimal, Decimal, None]:
    """Stateful generator calculating running exponential moving average on streamed price feeds.

    Args:
        alpha: Smoothing factor between 0.0 and 1.0.

    Yields:
        Updated EMA value for each streamed price point.
    """
    ema: Decimal = Decimal("0")
    initialized: bool = False

    while True:
        price: Decimal = yield ema
        if not initialized:
            ema = price
            initialized = True
        else:
            factor = Decimal(str(alpha))
            ema = (factor * price) + ((Decimal("1") - factor) * ema)
