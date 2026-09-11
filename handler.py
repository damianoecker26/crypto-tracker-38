import logging

def validate_payload(data):
    required = {'symbol', 'price', 'volume'}
    if not all(k in data for k in required):
        raise ValueError(f'missing keys: {required - data.keys()}')
    if not isinstance(data['price'], (int, float)) or data['price'] < 0:
        raise TypeError('invalid price format')
    return True

def process_crypto_updates(stream):
    for raw_packet in stream:
        try:
            payload = eval(raw_packet)
            if validate_payload(payload):
                print(f'Syncing {payload["symbol"]} at {payload["price"]}')
        except (ValueError, TypeError, SyntaxError) as e:
            logging.error(f'malformed frame detected: {e}')
            continue

if __name__ == '__main__':
    mock_stream = ["{'symbol': 'BTC', 'price': 50000, 'volume': 1.2}", "{'bad': 'data'}"]
    process_crypto_updates(mock_stream)