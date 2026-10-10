import functools

class CryptoValidator:
    def __init__(self):
        self._cache = {}

    def memoize_validation(func):
        @functools.wraps(func)
        def wrapper(self, ticker):
            if ticker not in self._cache:
                self._cache[ticker] = func(self, ticker)
            return self._cache[ticker]
        return wrapper

    @memoize_validation
    def is_valid_ticker(self, ticker: str) -> bool:
        if not isinstance(ticker, str) or len(ticker) < 2:
            return False
        return ticker.isupper() and ticker.isalpha()

    def batch_validate(self, tickers: list[str]) -> dict[str, bool]:
        return {t: self.is_valid_ticker(t) for t in tickers}

    def clear_validation_cache(self) -> None:
        self._cache.clear()

    def __repr__(self):
        return f"CryptoValidator(cache_size={len(self._cache)})"

    def __call__(self, ticker: str) -> bool:
        return self.is_valid_ticker(ticker)