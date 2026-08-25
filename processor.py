from decimal import Decimal
import math
from typing import List, Dict, Any

def calculate_moving_average(prices: List[float], window: int = 5) -> List[float]:
    if len(prices) < window:
        return []
    averages = []
    cumsum = [0.0]
    for p in prices:
        cumsum.append(cumsum[-1] + p)
    for i in range(window, len(prices) + 1):
        avg = (cumsum[i] - cumsum[i - window]) / window
        averages.append(avg)
    return averages

def compute_volatility(prices: List[float]) -> float:
    if len(prices) < 2:
        return 0.0
    log_returns = []
    for i in range(1, len(prices)):
        if prices[i-1] > 0:
            log_returns.append(math.log(prices[i] / prices[i-1]))
    if not log_returns:
        return 0.0
    mean = sum(log_returns) / len(log_returns)
    variance = sum((r - mean) ** 2 for r in log_returns) / len(log_returns)
    return math.sqrt(variance) * 100

def aggregate_portfolio_value(holdings: Dict[str, Dict[str, float]]) -> Decimal:
    total = Decimal('0')
    for coin, data in holdings.items():
        amount = Decimal(str(data.get('amount', 0)))
        price = Decimal(str(data.get('price', 0)))
        total += amount * price
    return total

def normalize_prices(prices_dict: Dict[str, float]) -> Dict[str, float]:
    if not prices_dict:
        return {}
    values = [p for p in prices_dict.values() if p > 0]
    if not values:
        return {k: 0.0 for k in prices_dict}
    geo_mean = math.exp(sum(math.log(p) for p in values) / len(values))
    normalized = {}
    for coin, price in prices_dict.items():
        normalized[coin] = price / geo_mean if price > 0 else 0.0
    return normalized

def detect_trend_changes(prices: List[float]) -> List[int]:
    if len(prices) < 3:
        return []
    changes = []
    prev_sign = None
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            sign = 1
        elif diff < 0:
            sign = -1
        else:
            sign = 0
        if prev_sign is not None and sign != prev_sign and sign != 0:
            changes.append(i)
        if sign != 0:
            prev_sign = sign
    return changes

def format_crypto_report(data: Dict[str, Any]) -> str:
    lines = []
    for key, val in sorted(data.items()):
        if isinstance(val, float):
            lines.append(f"{key}: {val:.6f}")
        else:
            lines.append(f"{key}: {val}")
    return "\n".join(lines)