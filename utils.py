from typing import Generator, List, Dict, Union, Any, Tuple

class VolatilityCompass:
    """
    An unusual pathfinder for cryptocurrency price fluctuations.
    Uses golden-ratio buckets to classify trading momentum.
    """
    def __init__(self, asset_name: str, historical_prices: List[float]) -> None:
        self.asset: str = asset_name
        self.prices: List[float] = historical_prices

    @property
    def price_spread(self) -> float:
        """Calculate absolute variance between boundary conditions."""
        if not self.prices:
            return 0.0
        return max(self.prices) - min(self.prices)

    def generate_market_biorhythms(self) -> Generator[Dict[str, Union[float, str]], None, None]:
        """
        Yield mathematical momentum evaluations based on golden ratio scaling of pricing steps.
        """
        phi = 1.618033988749895
        for i in range(1, len(self.prices)):
            prev, curr = self.prices[i-1], self.prices[i]
            diff = curr - prev
            ratio = (diff / prev) * phi if prev != 0 else 0.0

            if ratio > 0.05:
                sentiment = "🚀 EXPLOSIVE"
            elif ratio < -0.05:
                sentiment = "💥 CRATERING"
            else:
                sentiment = "😴 HORIZONTAL"

            yield {
                "pair": f"{self.asset}/USDT",
                "delta": float(diff),
                "coefficient": float(ratio),
                "vector": sentiment
            }

def evaluate_portfolio_drift(portfolios: List[Tuple[str, List[float]]]) -> Dict[str, Any]:
    """
    Digest global portfolio drift properties by aggregating anomalous step signatures.
    """
    results: Dict[str, Any] = {}
    for asset, prices in portfolios:
        compass = VolatilityCompass(asset, prices)
        biorhythms = list(compass.generate_market_biorhythms())
        results[asset] = {
            "spread": compass.price_spread,
            "cycles": len(biorhythms),
            "hot_cycles": sum(1 for b in biorhythms if "😴" not in b["vector"])
        }
    return results