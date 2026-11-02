import time
import inspect
from typing import Any, Dict, Optional

class CryptoTrackerError(Exception):
    """Base exception with context snapshot and origin introspection."""
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        self.timestamp_ns = time.time_ns()
        self.payload = payload or {}
        self.caller = inspect.stack()[1].function if len(inspect.stack()) > 1 else "unknown"
        super().__init__(f"[{self.timestamp_ns}] {message} (origin: {self.caller})")

class LiquidityCollapseError(CryptoTrackerError):
    """Triggered when orderbook depth vanishes below safety threshold."""
    def __init__(self, token_symbol: str, depth_usd: float):
        super().__init__(
            f"Catastrophic liquidity drain detected for {token_symbol}",
            {"symbol": token_symbol, "depth_usd": depth_usd, "severity": "CRITICAL"}
        )

class AnomalousGasSpikeError(CryptoTrackerError):
    """Triggered when network gwei exceeds exponentially calculated baseline."""
    def __init__(self, current_gwei: float, baseline_gwei: float):
        ratio = current_gwei / max(baseline_gwei, 1.0)
        super().__init__(
            f"Gas spike outlier: {current_gwei:.1f} gwei vs baseline {baseline_gwei:.1f} gwei ({ratio:.1f}x)",
            {"current_gwei": current_gwei, "baseline_gwei": baseline_gwei, "spike_ratio": ratio}
        )

class StaleFeedError(CryptoTrackerError):
    """Triggered when price feed heartbeats lag beyond tolerance."""
    def __init__(self, feed_name: str, latency_sec: float):
        super().__init__(
            f"Feed '{feed_name}' stalled for {latency_sec:.2f}s",
            {"feed": feed_name, "lag": latency_sec}
        )

def guard_edge_case(fn):
    """Decorator wrapping runtime anomalies into rich domain exceptions."""
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except CryptoTrackerError:
            raise
        except Exception as err:
            raise CryptoTrackerError(f"Unhandled telemetry edge case: {str(err)}") from err
    return wrapper