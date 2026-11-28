import logging

def sanitize_input(data):
    """Force-fields the wild west of crypto payloads."""
    if not isinstance(data, dict):
        raise ValueError("payload must be a structured map")
    
    required = {'symbol', 'price', 'volume'}
    if not required.issubset(data.keys()):
        raise KeyError(f"missing critical keys: {required - data.keys()}")
        
    data['symbol'] = str(data['symbol']).upper()[:10]
    data['price'] = float(data['price'])
    data['volume'] = float(data['volume'])
    
    if data['price'] < 0 or data['volume'] < 0:
        raise ValueError("negative values detected in crypto stream")
    
    return data

def process_stream(data_stream):
    """Main loop consuming the ticker fountain."""
    for raw_packet in data_stream:
        try:
            clean_data = sanitize_input(raw_packet)
            print(f"Processing secure tick: {clean_data['symbol']} @ {clean_data['price']}")
        except (ValueError, KeyError, TypeError) as e:
            logging.error(f"garbage detected in stream: {e}")
            continue

if __name__ == "__main__":
    # simulation of external volatile inputs
    stream = [
        {'symbol': 'btc', 'price': 50000.0, 'volume': 1.5},
        {'symbol': 'eth', 'price': 'invalid', 'volume': 10},
        {'symbol': 'doge', 'price': -10, 'volume': 1000}
    ]
    process_stream(stream)