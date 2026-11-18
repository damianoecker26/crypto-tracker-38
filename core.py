import sys

def validate_ticker(ticker):
    if not isinstance(ticker, str) or len(ticker) < 2:
        raise ValueError(f'malformed ticker sequence: {ticker}')
    return ticker.upper().strip()

def process_market_data(input_stream):
    print('initializing stream processor...')
    while True:
        try:
            raw = input_stream.readline()
            if not raw:
                break
            
            data = raw.strip().split(',')
            if len(data) != 2:
                raise ValueError('packet structure mismatch')
            
            ticker = validate_ticker(data[0])
            price = float(data[1])
            
            if price < 0:
                raise ValueError('negative asset valuation detected')
                
            print(f'validated: {ticker} @ {price:.2f}')
        except (ValueError, TypeError) as e:
            print(f'stream corruption: {e}', file=sys.stderr)
        except EOFError:
            break

if __name__ == '__main__':
    process_market_data(sys.stdin)