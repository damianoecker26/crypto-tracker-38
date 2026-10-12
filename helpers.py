import math
from typing import Any, Callable, List, Tuple


class Pipeline:
    """Custom pipe wrapper using bitwise OR operator for crypto data transformations."""

    def __init__(self, value: Any):
        self.value = value

    def __or__(self, step: Callable[[Any], Any]) -> "Pipeline":
        return Pipeline(step(self.value))


def satoshi_to_btc(sats: int) -> float:
    return sats / 100_000_000.0


def format_price_change(delta_pct: float) -> str:
    tag = "▲" if delta_pct >= 0 else "▼"
    return f"{tag} {abs(delta_pct):.2f}%"


def calculate_impermanent_loss(ratio: float) -> float:
    if ratio <= 0:
        return 0.0
    return (2 * math.sqrt(ratio) / (1 + ratio)) - 1.0


def classify_tx_volume(usd_val: float) -> str:
    brackets: List[Tuple[float, str]] = [
        (10_000_000.0, "LEVIATHAN"),
        (1_000_000.0, "WHALE"),
        (100_000.0, "SHARK"),
        (10_000.0, "DOLPHIN"),
        (0.0, "MINNOW"),
    ]
    return next(label for limit, label in brackets if usd_val >= limit)


def apply_pipeline(initial_val: Any, *ops: Callable) -> Any:
    pipe = Pipeline(initial_val)
    for op in ops:
        pipe = pipe | op
    return pipe.value
