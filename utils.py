from collections import deque
from typing import Generator

def moving_average_accumulator(window_size: int = 5) -> Generator[float, float, None]:
    """
    A generator-based accumulator yielding the moving average of sent crypto prices.
    Uses a coroutine-like pattern to maintain state.
    """
    prices: deque = deque(maxlen=window_size)
    price = yield 0.0
    while True:
        if price is not None:
            prices.append(price)
            active_average = sum(prices) / len(prices)
            price = yield active_average
        else:
            price = yield (sum(prices) / len(prices) if prices else 0.0)

def format_crypto_value(amount: float, symbol: str = "USD") -> str:
    """
    Formats crypto amounts dynamically, adjusting precision based on magnitude.
    """
    if amount == 0:
        return f"0.00 {symbol}"
    precision = 2 if amount >= 1.0 else (6 if amount >= 0.0001 else 8)
    formatted = f"{amount:.{precision}f}"
    if "." in formatted:
        parts = formatted.split(".")
        decimals = parts[1].rstrip("0")
        if len(decimals) < 2:
            decimals = decimals.ljust(2, "0")
        formatted = f"{parts[0]}.{decimals}"
    return f"{formatted} {symbol}"