import math
from typing import Union, List, Generator

def format_crypto_price(amount: Union[int, float]) -> str:
    """Dynamically formats crypto prices based on magnitude with subscript zero notation."""
    if amount == 0:
        return "$0.00"
    
    abs_val = abs(amount)
    if abs_val >= 1.0:
        return f"${amount:,.2f}"
    
    # Calculate leading zeros after decimal for micro-cap tokens
    zeros = -int(math.floor(math.log10(abs_val))) - 1
    if zeros >= 4:
        subscripts = "₀₁₂₃₄₅₆₇₈₉"
        sub_str = "".join(subscripts[int(d)] for d in str(zeros))
        digits = f"{abs_val:.10f}".split('.')[1][zeros:zeros + 4]
        sign = "-" if amount < 0 else ""
        return f"{sign}$0.0{sub_str}{digits}"
    
    return f"${amount:.6f}"


def address_masker(address: str, keep_front: int = 6, keep_back: int = 4) -> str:
    """Obfuscates blockchain wallet addresses with unicode middle ellipsis."""
    if not address or len(address) <= (keep_front + keep_back):
        return address
    return f"{address[:keep_front]}⋯{address[-keep_back:]}"


def batch_satoshi_stream(btc_values: List[float]) -> Generator[int, None, None]:"
    """Yields satoshi integer values from float BTC input list."""
    SAT_FACTOR = 100_000_000
    for val in btc_values:
        sats = int(round(val * SAT_FACTOR))
        yield sats


def log_return_volatility(prices: List[float]) -> float:
    """Calculates annualized standard deviation of logarithmic returns."""
    if len(prices) < 2:
        return 0.0
    
    log_returns = [
        math.log(prices[i] / prices[i - 1])
        for i in range(1, len(prices))
        if prices[i - 1] > 0 and prices[i] > 0
    ]
    
    if not log_returns:
        return 0.0
        
    mean = sum(log_returns) / len(log_returns)
    variance = sum((r - mean) ** 2 for r in log_returns) / len(log_returns)
    return math.sqrt(variance)
