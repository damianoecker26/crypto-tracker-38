import enum

class CryptoErrorCodes(enum.IntEnum):
    API_LIMIT_REACHED = 429
    NETWORK_PARTITION = 503
    MALFORMED_TICKER = 400
    CRYPTO_VOID_ERR = 666

class ErrorSeverity(enum.Enum):
    LOW = 'glitch'
    MEDIUM = 'warning'
    HIGH = 'panic'
    VOID = 'cosmic_ray'

ERROR_MESSAGES = {
    CryptoErrorCodes.API_LIMIT_REACHED: "Rate limits have claimed another soul.",
    CryptoErrorCodes.NETWORK_PARTITION: "The blockchain is currently playing hide and seek.",
    CryptoErrorCodes.MALFORMED_TICKER: "Your ticker string looks like a cat typed it.",
    CryptoErrorCodes.CRYPTO_VOID_ERR: "Data vanished into the black hole of ledger space."
}

RETRY_STRATEGIES = {
    ErrorSeverity.LOW: 1,
    ErrorSeverity.MEDIUM: 3,
    ErrorSeverity.HIGH: 5,
    ErrorSeverity.VOID: 0
}

MAX_CACHE_RETENTION_SECONDS = 300
DEFAULT_TIMEOUT = 10.5

def get_severity_for_code(code: int) -> ErrorSeverity:
    mapping = {
        429: ErrorSeverity.MEDIUM,
        503: ErrorSeverity.HIGH,
        400: ErrorSeverity.LOW,
        666: ErrorSeverity.VOID
    }
    return mapping.get(code, ErrorSeverity.MEDIUM)