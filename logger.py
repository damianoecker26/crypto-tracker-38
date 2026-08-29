import logging
import sys
from typing import Dict, Any

class CryptoEdgeLogger:
    def __init__(self, log_file: str = "crypto-tracker-38.log"):
        self.logger = logging.getLogger("crypto-tracker-38")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(fh)
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(logging.Formatter("CRYPTO: %(message)s"))
            self.logger.addHandler(ch)

    def safe_log(self, level: str, msg: str, data: Dict[str, Any] = None) -> None:
        if data is None:
            data = {}
        try:
            if not msg or not isinstance(msg, str):
                self.logger.warning("Edge case: empty or invalid log message")
                msg = "Invalid message provided"
            if "price" in data:
                price = data["price"]
                if not isinstance(price, (int, float)):
                    self.logger.error(f"Edge case: non-numeric price {price}")
                    return
                if price <= 0:
                    self.logger.error(f"Edge case: non-positive price {price} for {data.get('symbol', 'unknown')}")
                    if price < 0:
                        price = 1 / abs(price)
                    else:
                        price = 0.0001
                    data["price"] = price
                    msg += " (corrected)"
            extra = {"data": data} if data else {}
            log_func = getattr(self.logger, level.lower(), self.logger.info)
            log_func(msg, extra=extra)
        except Exception as e:
            self.logger.critical(f"Logger edge case failure: {str(e)}")
            print(f"CRITICAL FALLBACK: {level} - {msg}")

    def handle_edge_case(self, exc: Exception, symbol: str = "BTC") -> None:
        exc_str = str(exc).lower()
        try:
            if "timeout" in exc_str or "connection" in exc_str:
                self.safe_log("warning", f"Network edge case for {symbol}", {"error": str(exc)})
            elif "rate" in exc_str or "limit" in exc_str:
                self.safe_log("warning", f"Rate limit edge case for {symbol} - pausing", {"error": str(exc)})
            elif "value" in exc_str or "invalid" in exc_str:
                self.safe_log("error", f"Data validation edge case for {symbol}", {"error": str(exc)})
            elif "key" in exc_str:
                self.safe_log("critical", f"API key edge case for {symbol}", {"error": str(exc)})
            else:
                self.safe_log("error", f"General crypto error for {symbol}: {exc}")
        except Exception as inner:
            print(f"Unhandled logger error: {inner}")

if __name__ == "__main__":
    logger = CryptoEdgeLogger()
    logger.safe_log("info", "Tracking started", {"symbol": "ETH", "price": 3000.5})
    logger.safe_log("info", "Tracking started", {"symbol": "BTC", "price": -45000})
    logger.safe_log("info", "Tracking started", {"symbol": "SOL", "price": 0})
    try:
        raise ConnectionError("timeout")
    except Exception as e:
        logger.handle_edge_case(e, "ETH")
    try:
        raise ValueError("invalid price")
    except Exception as e:
        logger.handle_edge_case(e, "XRP")