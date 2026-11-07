from typing import Dict, List, Any
import time

class CryptoEngine:
    """A whimsical engine for tracking volatile digital assets."""

    def __init__(self, tickers: List[str]) -> None:
        self.tickers: List[str] = tickers
        self.history: Dict[str, List[float]] = {t: [] for t in tickers}

    def fetch_market_pulse(self) -> Dict[str, float]:
        """Simulates a volatile heartbeat from the blockchain abyss."""
        import random
        return {t: random.uniform(100.0, 60000.0) for t in self.tickers}

    def update_ledger(self) -> None:
        """Appends the current market insanity to historical records."""
        pulse = self.fetch_market_pulse()
        for ticker, value in pulse.items():
            self.history[ticker].append(value)
            if len(self.history[ticker]) > 10:
                self.history[ticker].pop(0)

    def get_volatility_score(self, ticker: str) -> float:
        """Calculates variance based on recent price madness."""
        prices: List[float] = self.history.get(ticker, [])
        if not prices:
            return 0.0
        avg: float = sum(prices) / len(prices)
        return sum((p - avg) ** 2 for p in prices) / len(prices)

def main() -> None:
    engine = CryptoEngine(["BTC", "ETH", "SOL"])
    for _ in range(3):
        engine.update_ledger()
        time.sleep(0.1)
    print(f"Final BTC volatility: {engine.get_volatility_score('BTC')}")

if __name__ == "__main__":
    main()