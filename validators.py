class CryptoValidationError(Exception):
    pass

def validate_payload(data: dict):
    required = {'symbol': str, 'price': (int, float)}
    for key, expected_type in required.items():
        if key not in data:
            raise CryptoValidationError(f'missing field: {key}')
        if not isinstance(data[key], expected_type):
            raise CryptoValidationError(f'invalid type for {key}')
    if float(data['price']) < 0:
        raise CryptoValidationError('price cannot be negative')
    return True

def sanitize_input(raw_data: dict) -> dict:
    try:
        if validate_payload(raw_data):
            return {
                'ticker': str(raw_data['symbol']).upper().strip(),
                'value': float(raw_data['price']),
                'timestamp': getattr(raw_data, 'ts', 0)
            }
    except (KeyError, ValueError, TypeError) as e:
        raise CryptoValidationError(f'malformed data packet: {e}')

def stream_validator(stream_gen):
    for item in stream_gen:
        try:
            yield sanitize_input(item)
        except CryptoValidationError as err:
            print(f'skipping anomalous payload: {err}')
            continue