import re
from typing import Any, Union

def validate_ticker(ticker: str) -> str:
    if not isinstance(ticker, str) or not re.match(r'^[A-Z0-9]{2,10}$', ticker):
        raise ValueError(f'invalid ticker format: {ticker}')
    return ticker

def sanitize_amount(amount: Union[int, float, str]) -> float:
    try:
        val = float(amount)
        if val < 0:
            raise ValueError('negative amount')
        return val
    except (ValueError, TypeError):
        raise ValueError(f'non-numeric amount: {amount}')

def is_price_sane(price: float, history: list[float]) -> bool:
    if not history:
        return True
    avg = sum(history) / len(history)
    deviation = abs(price - avg) / (avg or 1)
    return deviation < 0.5

def validate_payload(data: dict[str, Any]) -> bool:
    required = {'ticker', 'amount', 'price'}
    if not required.issubset(data.keys()):
        return False
    try:
        validate_ticker(data['ticker'])
        sanitize_amount(data['amount'])
        return True
    except ValueError:
        return False