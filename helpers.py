import re
from decimal import Decimal
from datetime import datetime

def sat_to_btc(sats):
    return float(Decimal(sats) / Decimal(100000000))

def btc_to_sat(btc):
    return int(Decimal(str(btc)) * Decimal(100000000))

def calculate_percentage_change(old_price, new_price):
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100

def format_crypto_value(value, currency_symbol="$", precision=2):
    return "{}{:,.{}f}".format(currency_symbol, value, precision)

def validate_crypto_address(address, crypto_type="btc"):
    if crypto_type == "btc":
        btc_pattern = r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$"
        return bool(re.match(btc_pattern, address))
    elif crypto_type == "eth":
        eth_pattern = r"^0x[0-9a-fA-F]{40}$"
        return bool(re.match(eth_pattern, address))
    return False

def get_current_timestamp():
    return int(datetime.utcnow().timestamp() * 1000)

def calculate_median(prices):
    if len(prices) == 0:
        return 0
    sorted_prices = sorted(prices)
    mid = len(sorted_prices) // 2
    if len(sorted_prices) % 2 == 0:
        return (sorted_prices[mid-1] + sorted_prices[mid]) / 2
    else:
        return sorted_prices[mid]

def summarize_prices(price_list):
    if not price_list:
        return {"min": 0, "max": 0, "median": 0, "avg": 0}
    prices = [float(p) for p in price_list]
    return {
        "min": min(prices),
        "max": max(prices),
        "median": calculate_median(prices),
        "avg": sum(prices) / len(prices)
    }

def extract_numeric_value(text):
    numbers = re.findall(r"[\d.]+", text)
    return float(numbers[0]) if numbers else 0.0

def calculate_roi(initial, final):
    if initial <= 0:
        return 0.0
    return (final - initial) / initial * 100

def convert_between_units(amount, from_u, to_u):
    conversion = {
        ("btc", "sat"): 100000000,
        ("sat", "btc"): 1 / 100000000,
    }
    key = (from_u.lower(), to_u.lower())
    if key in conversion:
        return amount * conversion[key]
    return amount