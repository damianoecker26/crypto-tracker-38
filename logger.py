import logging
import sys
import time
from decimal import Decimal
from typing import Any, Dict

def get_crypto_logger(name: str = "crypto_tracker") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        file_handler = logging.FileHandler("crypto_logs.txt", mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def log_price_update(logger: logging.Logger, symbol: str, price: Decimal, change_pct: float) -> None:
    emoji = "📈" if change_pct >= 0 else "📉"
    msg = f"{emoji} {symbol} price: {price} ({change_pct:+.2f}%)"
    logger.info(msg)

def log_trade_execution(logger: logging.Logger, side: str, symbol: str, quantity: Decimal, price: Decimal) -> None:
    total = quantity * price
    msg = f"TRADE {side.upper()}: {quantity} {symbol} at {price} total {total}"
    logger.info(msg)

def log_balance_update(logger: logging.Logger, asset: str, new_balance: Decimal, change: Decimal) -> None:
    msg = f"BALANCE: {asset} updated to {new_balance} change {change:+}"
    logger.debug(msg)

def log_api_call(logger: logging.Logger, endpoint: str, status: int, duration: float) -> None:
    status_str = "OK" if status < 400 else "FAIL"
    msg = f"API {endpoint} {status_str} ({status}) in {duration:.3f}s"
    if status >= 400:
        logger.warning(msg)
    else:
        logger.debug(msg)

def log_market_event(logger: logging.Logger, event_type: str, details: Dict[str, Any]) -> None:
    detail_str = " | ".join(f"{k}={v}" for k, v in details.items())
    msg = f"EVENT {event_type}: {detail_str}"
    logger.info(msg)
