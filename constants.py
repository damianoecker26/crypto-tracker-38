import enum

class CryptoErrorCodes(enum.IntEnum):
    API_LIMIT_EXCEEDED = 429
    NETWORK_PARTITION = 503
    MALFORMED_RESPONSE = 502
    DECRYPTION_FAILURE = 403
    UNSUPPORTED_ASSET = 404

ERROR_MESSAGES = {
    CryptoErrorCodes.API_LIMIT_EXCEEDED: "rate limited by exchange server",
    CryptoErrorCodes.NETWORK_PARTITION: "node connectivity failure detected",
    CryptoErrorCodes.MALFORMED_RESPONSE: "unexpected schema in payload",
    CryptoErrorCodes.DECRYPTION_FAILURE: "corrupt secure transmission block",
    CryptoErrorCodes.UNSUPPORTED_ASSET: "ticker symbol unavailable for monitoring"
}

RETRY_STRATEGY = {
    CryptoErrorCodes.API_LIMIT_EXCEEDED: {"max_retries": 5, "backoff_factor": 2.0},
    CryptoErrorCodes.NETWORK_PARTITION: {"max_retries": 3, "backoff_factor": 1.5},
    CryptoErrorCodes.MALFORMED_RESPONSE: {"max_retries": 1, "backoff_factor": 0.1}
}

DEFAULT_TIMEOUT_SECONDS = 30
HEARTBEAT_INTERVAL = 60

def get_error_context(code: int) -> str:
    return ERROR_MESSAGES.get(code, "unknown protocol anomaly encountered")