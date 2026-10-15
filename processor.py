import logging

class CryptoProcessor:
    def __init__(self):
        self.valid_assets = {'BTC', 'ETH', 'SOL', 'DOT'}
        
    def process_data(self, incoming_stream):
        for raw_entry in incoming_stream:
            try:
                clean_data = self._sanitize(raw_entry)
                if not clean_data:
                    continue
                self._execute_trade(clean_data)
            except ValueError as e:
                logging.error(f'Skipping malformed packet: {e}')

    def _sanitize(self, entry):
        if not isinstance(entry, dict):
            raise ValueError('Input must be a dictionary')
        
        symbol = entry.get('ticker', '').upper()
        price = entry.get('price')

        if symbol not in self.valid_assets:
            return None
        
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(f'Invalid price detected for {symbol}')
            
        return {'ticker': symbol, 'price': float(price)}

    def _execute_trade(self, data):
        print(f'Processing {data['ticker']} at {data['price']}')

if __name__ == '__main__':
    processor = CryptoProcessor()
    stream = [{'ticker': 'BTC', 'price': 50000}, {'ticker': 'XRP', 'price': 1}, {'ticker': 'ETH', 'price': -5}]
    processor.process_data(stream)