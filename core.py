import time
import sys

def validate_payload(data):
    required = {'symbol': str, 'price': (int, float)}
    if not isinstance(data, dict) or not all(k in data and isinstance(data[k], v) for k, v in required.items()):
        raise ValueError(f"malformed crypto packet: {data}")
    return True

def process_ticker(stream):
    while True:
        try:
            payload = next(stream)
            if validate_payload(payload):
                print(f"processing {payload['symbol']} at {payload['price']}")
        except (ValueError, TypeError) as e:
            print(f"skip corrupt data: {e}")
        except StopIteration:
            break

def mock_stream():
    data = [
        {'symbol': 'BTC', 'price': 65000},
        {'symbol': 'ETH', 'price': 'invalid'},
        {'symbol': 'SOL', 'price': 140},
        None
    ]
    for item in data:
        yield item

if __name__ == '__main__':
    process_ticker(mock_stream())