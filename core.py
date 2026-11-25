import requests
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class CoinSnapshot:
    symbol: str
    price: float

class CryptoOrchestrator:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, tickers: List[str]):
        self.tickers = [t.lower() for t in tickers]

    def _fetch_data(self) -> Dict:
        ids = ",".join(self.tickers)
        params = {"ids": ids, "vs_currencies": "usd"}
        response = requests.get(f"{self.BASE_URL}/simple/price", params=params)
        return response.json() if response.ok else {}

    def harvest_market_state(self) -> List[CoinSnapshot]:
        raw = self._fetch_data()
        return [CoinSnapshot(k, v['usd']) for k, v in raw.items()]

    def run_lifecycle(self) -> None:
        snapshot = self.harvest_market_state()
        for entry in snapshot:
            print(f"[TRACKER] {entry.symbol.upper()}: ${entry.price:,.2f}")

if __name__ == "__main__":
    tracker = CryptoOrchestrator(['bitcoin', 'ethereum', 'solana'])
    tracker.run_lifecycle()