from collections import deque
from typing import Dict, List, Optional

class CryptoProcessor:
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.price_windows: Dict[str, deque] = {}
        self.running_sums: Dict[str, float] = {}
        self.current_prices: Dict[str, float] = {}
        self.prev_prices: Dict[str, float] = {}
        self.update_count = 0

    def add_price(self, symbol: str, price: float) -> float:
        if symbol not in self.price_windows:
            self.price_windows[symbol] = deque(maxlen=self.window_size)
            self.running_sums[symbol] = 0.0
        window = self.price_windows[symbol]
        if len(window) == self.window_size:
            old_price = window.popleft()
            self.running_sums[symbol] -= old_price
        window.append(price)
        self.running_sums[symbol] += price
        if symbol in self.current_prices:
            self.prev_prices[symbol] = self.current_prices[symbol]
        self.current_prices[symbol] = price
        self.update_count += 1
        count = len(window)
        return self.running_sums[symbol] / count

    def get_moving_average(self, symbol: str) -> float:
        if symbol not in self.running_sums:
            return 0.0
        count = len(self.price_windows.get(symbol, []))
        if count == 0:
            return 0.0
        return self.running_sums[symbol] / count

    def get_price_change(self, symbol: str) -> Optional[float]:
        if symbol not in self.prev_prices or symbol not in self.current_prices:
            return None
        prev = self.prev_prices[symbol]
        curr = self.current_prices[symbol]
        if prev == 0:
            return None
        return (curr - prev) / prev

    def process_batch(self, price_list: List[Dict[str, float]]) -> Dict[str, float]:
        results = {}
        for item in price_list:
            symbol = item.get("symbol")
            price = item.get("price")
            if symbol is not None and price is not None:
                avg = self.add_price(symbol, price)
                results[symbol] = avg
        return results

    def get_top_movers(self, min_change: float = 0.01) -> List[str]:
        movers = []
        for symbol in list(self.current_prices.keys()):
            change = self.get_price_change(symbol)
            if change is not None and abs(change) >= min_change:
                movers.append((symbol, abs(change)))
        movers.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in movers[:5]]

if __name__ == "__main__":
    processor = CryptoProcessor(5)
    data = [
        {"symbol": "BTC", "price": 65000.5},
        {"symbol": "ETH", "price": 2600.75},
        {"symbol": "BTC", "price": 65200.0},
        {"symbol": "ETH", "price": 2595.0},
        {"symbol": "BTC", "price": 65100.25},
        {"symbol": "LTC", "price": 70.5},
    ]
    print(processor.process_batch(data))
    print(processor.get_top_movers(0.005))
    print(processor.get_moving_average("BTC"))
