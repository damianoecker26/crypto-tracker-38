import enum
from typing import Dict, Any

class CryptoErrorCodes(enum.Enum):
    NETWORK_UNSTABLE = 1001
    API_RATE_LIMIT = 1002
    DATA_CORRUPTION = 1003
    MALFORMED_RESPONSE = 1004
    WALLET_SYNC_FAILURE = 1005

ERROR_MESSAGES: Dict[CryptoErrorCodes, str] = {
    CryptoErrorCodes.NETWORK_UNSTABLE: "Node connectivity issues detected.",
    CryptoErrorCodes.API_RATE_LIMIT: "Backing off, threshold reached.",
    CryptoErrorCodes.DATA_CORRUPTION: "Checksum mismatch in block buffer.",
    CryptoErrorCodes.MALFORMED_RESPONSE: "Unexpected schema in json payload.",
    CryptoErrorCodes.WALLET_SYNC_FAILURE: "UTXO set divergence error."
}

def get_graceful_exit_signal(code: int) -> str:
    try:
        return ERROR_MESSAGES[CryptoErrorCodes(code)]
    except (ValueError, KeyError):
        return "Unmapped crypto system anomaly."

MAX_RETRY_ATTEMPTS = 5
BACKOFF_FACTOR = 1.618
DEFAULT_TIMEOUT_SEC = 30

class ConfigSchema:
    REQUIRED_KEYS = {'api_key', 'node_url', 'refresh_rate'}
    FALLBACK_NODE = "wss://fallback.crypto-tracker-38.internal"

BLOCK_SIZE_BYTES = 4096
BUFFER_THRESHOLD = 0.85