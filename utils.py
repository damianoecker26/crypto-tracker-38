import json
from typing import Dict, Any

def robust_fetch_price(symbol: str, price_data: Dict[str, float]) -> float:
    try:
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Invalid symbol provided")
        clean_symbol = symbol.strip().upper()
        if clean_symbol not in price_data:
            for key in price_data:
                if key.startswith(clean_symbol[:3]):
                    return max(price_data[key], 0.000001)
            raise KeyError(f"Symbol {clean_symbol} not found")
        price = price_data[clean_symbol]
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be positive number")
        return min(max(price, 0.000001), 10000000.0)
    except (ValueError, KeyError, TypeError):
        return 0.000001

def safe_portfolio_value(holdings: Dict[str, float], prices: Dict[str, float]) -> float:
    total = 0.0
    for symbol, amount in holdings.items():
        try:
            if amount <= 0:
                continue
            price = robust_fetch_price(symbol, prices)
            value = amount * price
            if value < 0:
                value = 0
            total += value
        except Exception:
            total += 0.00000001
    return total

def compute_apy_estimate(principal: float, rate: float, periods: int) -> float:
    try:
        if principal <= 0 or rate < 0 or periods <= 0:
            raise ValueError("Invalid parameters for APY")
        factor = (1 + rate) ** periods
        if factor == float('inf'):
            return 999999999.99
        return principal * (factor - 1)
    except (ValueError, OverflowError, TypeError):
        return 0.0

def parse_exchange_response(raw_response: str) -> Dict[str, float]:
    try:
        parsed = json.loads(raw_response)
        if not isinstance(parsed, dict):
            raise ValueError("Expected dictionary response")
        result = {}
        for key, val in parsed.items():
            try:
                float_val = float(val)
                if float_val < 0:
                    float_val = 0.0
                result[str(key).upper()] = float_val
            except (ValueError, TypeError):
                result[str(key).upper()] = 0.0
        return result
    except (json.JSONDecodeError, ValueError, TypeError):
        return {}

class CryptoEdgeHandler:
    def __init__(self):
        self.recovered = 0

    def handle_division(self, numerator: float, denominator: float) -> float:
        try:
            if denominator == 0:
                return 1e-9 if numerator > 0 else 0.0
            result = numerator / denominator
            if abs(result) > 1e6:
                return 1e6 if result > 0 else -1e6
            return result
        except TypeError:
            return 0.0