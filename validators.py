import hashlib
import re
from typing import Any


class CryptoAddressValidator:
    """Creative validation pipeline for cryptocurrency addresses."""

    _PATTERNS = {
        "btc_legacy": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        "btc_bech32": r"^bc1[a-0-z-1-9]{39,59}$",
        "eth": r"^0x[a-fA-F0-9]{40}$",
        "solana": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$",
    }

    def __init__(self, chain: str):
        if chain not in self._PATTERNS:
            raise ValueError(f"Unsupported chain target: {chain}")
        self.chain = chain
        self.pattern = re.compile(self._PATTERNS[chain])

    def __ror__(self, value: Any) -> bool:
        """Allow pipe operator syntax: address | CryptoAddressValidator('eth')"""
        return self.validate(value)

    def validate(self, address: Any) -> bool:
        if not isinstance(address, str) or not self.pattern.match(address):
            return False
        if self.chain == "eth":
            return self._verify_eip55(address)
        return True

    @staticmethod
    def _verify_eip55(address: str) -> bool:
        """Verify Ethereum address checksum without external web3 dependencies."""
        if address.islower() or address.isupper():
            return True

        clean_addr = address[2:].lower()
        addr_hash = hashlib.sha3_256(clean_addr.encode("utf-8")).hexdigest()

        for i, char in enumerate(clean_addr):
            if char.isalpha():
                hash_nibble = int(addr_hash[i], 16)
                expected_upper = hash_nibble >= 8
                if (address[2 + i].isupper()) != expected_upper:
                    return False
        return True


def validate_ticker(symbol: str) -> bool:
    """Validates unified crypto symbol syntax (e.g. BTC/USDT or ETH-PERP)."""
    clean = symbol.strip().upper()
    return bool(re.match(r"^[A-Z0-9]{2,10}([/_\-:][A-Z0-9]{2,10})?$", clean))
