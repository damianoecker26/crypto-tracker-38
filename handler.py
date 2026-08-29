import re
def validate_symbol(symbol):
    if not isinstance(symbol, str):
        return False
    return bool(re.match(r'^[A-Z]{1,10}$', symbol))

def validate_price(price):
    if isinstance(price, (int, float)):
        price = str(price)
    try:
        p = float(price)
        return 0 < p < 1000000
    except (ValueError, TypeError):
        return False

class CryptoHandler:
    def __init__(self):
        self.tracked = []

    def process_loop(self, data_stream):
        for idx, item in enumerate(data_stream):
            if not isinstance(item, dict):
                continue
            sym = item.get('symbol', item.get('sym', '')).upper()
            pr = item.get('price', item.get('pr', ''))
            if validate_symbol(sym) and validate_price(pr):
                entry = {'symbol': sym, 'price': float(pr)}
                self.tracked.append(entry)
        return self.tracked

    def get_summary(self):
        if not self.tracked:
            return "No valid data"
        prices = [d['price'] for d in self.tracked]
        avg = sum(prices) / len(prices)
        return f"Tracked {len(prices)} coins, avg price {avg:.2f}"

if __name__ == "__main__":
    handler = CryptoHandler()
    sample = [
        {'symbol': 'BTC', 'price': 65000},
        {'sym': 'ETH', 'pr': 2500},
        {'symbol': 'bad!', 'price': 100},
        {'symbol': 'LTC', 'price': 'abc'},
        {'symbol': 'XRP', 'price': 0.5}
    ]
    result = handler.process_loop(sample)
    print(handler.get_summary())
    print("First entry:", result[0] if result else "none")
