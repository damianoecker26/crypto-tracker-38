import sys

def validate_crypto_input(data):
    if not isinstance(data, dict):
        raise ValueError('data must be dict')
    required = {'symbol', 'price'}
    if not required.issubset(data.keys()):
        raise KeyError(f'missing keys: {required - data.keys()}')
    if data['price'] < 0:
        raise ValueError('price cannot be negative')
    return True

def process_stream(data_stream):
    for entry in data_stream:
        try:
            if validate_crypto_input(entry):
                print(f"Processing {entry['symbol']} at {entry['price']}")
        except (ValueError, KeyError) as e:
            print(f"Skipping malformed packet: {e}", file=sys.stderr)

if __name__ == '__main__':
    raw_feed = [
        {'symbol': 'BTC', 'price': 65000},
        {'symbol': 'ETH', 'price': -1},
        {'symbol': 'SOL', 'price': 150},
        "invalid_data"
    ]
    process_stream(raw_feed)