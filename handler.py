import logging

class DataSanitizer:
    def __init__(self):
        self.required_fields = {'symbol', 'price', 'volume'}

    def validate(self, payload):
        if not isinstance(payload, dict):
            raise ValueError('payload must be a mapping')
        if not self.required_fields.issubset(payload.keys()):
            missing = self.required_fields - payload.keys()
            raise ValueError(f'missing {missing}')
        if payload['price'] < 0:
            raise ValueError('price cannot be negative')
        return True

def process_stream(data_stream):
    sanitizer = DataSanitizer()
    logger = logging.getLogger('crypto-tracker-38')
    
    for raw_data in data_stream:
        try:
            if sanitizer.validate(raw_data):
                handle_event(raw_data)
        except (ValueError, TypeError) as e:
            logger.error(f'bad packet received: {e}')
            continue

def handle_event(event):
    symbol = event['symbol']
    price = event['price']
    print(f'Processing {symbol} at {price}')

if __name__ == '__main__':
    mock_data = [
        {'symbol': 'BTC', 'price': 50000, 'volume': 1.5},
        {'symbol': 'ETH', 'price': -10, 'volume': 2},
        {'symbol': 'SOL', 'price': 100}
    ]
    process_stream(mock_data)