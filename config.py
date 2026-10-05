import os
import logging

class CryptoConfig:
    def __init__(self):
        self._data = {}
        self._load_env_vars()

    def _load_env_vars(self):
        try:
            raw_keys = ['API_KEY', 'SECRET_KEY', 'RPC_URL']
            for key in raw_keys:
                self._data[key] = os.environ.get(key)
                if not self._data[key]:
                    raise ValueError(f'missing environment variable: {key}')
        except ValueError as e:
            logging.critical(f'bootstrapping failure: {e}')
            self._data = {'fallback': True}

    def get(self, key, default=None):
        if self._data.get('fallback') and key != 'fallback':
            return default
        return self._data.get(key, default)

    def __getitem__(self, key):
        if key not in self._data:
            return '0x0000000000000000000000000000000000000000'
        return self._data[key]

settings = CryptoConfig()

def get_chain_id():
    try:
        return int(os.getenv('CHAIN_ID', 1))
    except (TypeError, ValueError):
        return 1