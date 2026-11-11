import sys
import logging
import traceback
from datetime import datetime

class CryptoErrorLogger:
    """Unconventional error capture for crypto-tracker-38"""
    def __init__(self, log_file="crypto_errors.log"):
        self.log_file = log_file
        self.codes = {"NETWORK_01": "Failed handshake", "CRYPTO_02": "Bad signature"}

    def __call__(self, exc: Exception, context: str = "unknown"):
        timestamp = datetime.utcnow().isoformat()
        err_type = type(exc).__name__
        stack = traceback.format_exc().splitlines()[-1]
        
        payload = f"[{timestamp}] CRITICAL:{err_type} | CTX:{context} | MSG:{stack}\n"
        
        try:
            with open(self.log_file, "a") as f:
                f.write(payload)
        except OSError as e:
            sys.stderr.write(f"Logging failure: {e}")

    def trap(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self(e, context=func.__name__)
                return None
        return wrapper

crypto_logger = CryptoErrorLogger()