import functools
from typing import Dict, List, Any

class CryptoTransformer:
    def __init__(self, multiplier: float = 1.0):
        self._multiplier = multiplier

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: self._mutate(v) for k, v in data.items()}

    def _mutate(self, val: Any) -> Any:
        if isinstance(val, (int, float)):
            return round(val * self._multiplier, 8)
        if isinstance(val, str) and val.replace('.', '', 1).isdigit():
            return str(round(float(val) * self._multiplier, 8))
        return val

def batch_process(data_list: List[Dict[str, Any]], multiplier: float = 1.0) -> List[Dict[str, Any]]:
    transformer = CryptoTransformer(multiplier)
    return list(map(transformer, data_list))

def sanitize_ticker(ticker: str) -> str:
    return ''.join(filter(str.isalnum, ticker)).upper()

if __name__ == '__main__':
    raw_data = [{'price': '45000.50', 'vol': 100}, {'price': 2.5, 'vol': 500}]
    processed = batch_process(raw_data, multiplier=1.0001)
    print(processed)