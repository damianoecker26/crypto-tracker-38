import time
import sys

def validate_ticker(ticker):
    if not isinstance(ticker, str) or len(ticker) < 2 or len(ticker) > 5:
        raise ValueError(f"Invalid ticker format: {ticker}")
    return ticker.upper()

def process_market_data(stream):
    for raw_input in stream:
        try:
            sanitized = validate_ticker(raw_input.strip())
            print(f"Processing secure feed for {sanitized}")
        except (ValueError, AttributeError) as e:
            print(f"Security protocol alert: {e}", file=sys.stderr)
            continue

def main():
    mock_stream = ["btc", "eth", "longtickername", "x", "sol", 123]
    process_market_data(mock_stream)

if __name__ == "__main__":
    main()