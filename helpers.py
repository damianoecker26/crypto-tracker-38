import decimal
from typing import Union, List

def sanitize_amount(value: Union[str, float, int]) -> decimal.Decimal:
    """convert inputs to precise decimal objects for ledger safety"""
    return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00000001'))

def calculate_roi(initial: decimal.Decimal, current: decimal.Decimal) -> float:
    """percentage gain calculation for portfolio analysis"""
    if initial == 0:
        return 0.0
    return float(((current - initial) / initial) * 100)

def chunk_symbols(symbols: List[str], size: int = 50) -> List[List[str]]:
    """batching mechanism for api rate limit compliance"""
    return [symbols[i:i + size] for i in range(0, len(symbols), size)]

def format_currency(amount: decimal.Decimal, symbol: str = '$') -> str:
    """human readable currency string generation"""
    return f"{symbol}{amount:,.8f}"

def hex_to_wei(hex_val: str) -> int:
    """evm hex conversion for blockchain smart contract values"""
    return int(hex_val, 16)

def is_bullish(prices: List[float]) -> bool:
    """simple trend detection via mean delta check"""
    if len(prices) < 2:
        return False
    return prices[-1] > prices[0]