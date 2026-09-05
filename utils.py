import random
from typing import Generator, Tuple

def price_ticker(symbol: str, initial_price: float, volatility: float = 0.02) -> Generator[float, None, None]:
    price = initial_price
    while True:
        change_percent = random.uniform(-volatility, volatility)
        price += price * change_percent
        yield round(price, 4)

def track_trend(ticker: Generator[float, None, None]) -> Generator[Tuple[float, str], None, None]:
    prev_price = None
    for price in ticker:
        if prev_price is None:
            trend = 'initial'
        elif price > prev_price:
            trend = 'up'
        elif price < prev_price:
            trend = 'down'
        else:
            trend = 'flat'
        yield price, trend
        prev_price = price

def format_ticker_output(symbol: str, limit: int = 10) -> list:
    ticker = price_ticker(symbol, 100.0)
    tracker = track_trend(ticker)
    return [next(tracker) for _ in range(limit)]