import os
from typing import Any, Dict, Type, get_type_hints


class CryptoConfig:
    """Dynamically resolved configuration for the crypto-tracker-38 application.

    Utilizes class-level type annotations to automatically parse and cast
    environment variables into runtime attributes.
    """

    # Type-annotated config values with defaults
    API_URL: str = "https://api.coingecko.com/v3"
    COIN_IDS: list = ["bitcoin", "ethereum", "solana"]
    UPDATE_INTERVAL_SEC: int = 60
    DEBUG_MODE: bool = False

    def __init__(self) -> None:
        """Initialize config and immediately synchronize with environment variables."""
        self._sync_env()

    def _cast_value(self, value: str, target_type: Type[Any]) -> Any:
        """Cast a string value from environment to the targeted type hint."""
        if target_type is bool:
            return value.lower() in ("true", "1", "yes")
        if target_type is list:
            return [item.strip() for item in value.split(",") if item.strip()]
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return value

    def _sync_env(self) -> None:
        """Overwrites defaults with matching uppercase environment variables."""
        hints = get_type_hints(self.__class__)
        for key, expected_type in hints.items():
            env_val = os.getenv(f"CRYPTO_{key}")
            if env_val is not None:
                casted = self._cast_value(env_val, expected_type)
                setattr(self, key, casted)

    def dump_config(self) -> Dict[str, Any]:
        """Export active configuration state as a dictionary."""
        return {
            key: getattr(self, key)
            for key in get_type_hints(self.__class__).keys()
        }
