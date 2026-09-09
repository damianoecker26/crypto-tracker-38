[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# crypto-tracker-38

crypto-tracker-38 is a lightweight Python command-line utility designed to monitor real-time cryptocurrency prices, market capitalization, and volume changes across major trading pairs. Powered by public exchange REST APIs, it provides instant market insights and local portfolio tracking directly inside your terminal.

## Key Features

- **Live Market Streaming:** Fetches spot prices, 24-hour volume, and percentage fluctuations for over 500 digital assets.
- **Automated Price Alerts:** Configurable threshold notifications that trigger desktop alerts when a coin hits a specified target price.
- **Portfolio P&L Tracking:** Calculates real-time profit and loss metrics based on local CSV transaction logs.
- **Data Exporting:** Exports time-series price snapshots into formatted JSON or CSV files for quantitative analysis.

## Installation

Ensure Python 3.9+ is installed on your machine.

```bash
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

Run the CLI tool directly to fetch live price data for target assets:

```bash
python main.py --coins bitcoin,ethereum,solana --currency usd
```

Alternatively, import the core library directly into your Python script:

```python
from tracker import CryptoTracker

tracker = CryptoTracker(currency="usd")
data = tracker.get_spot_prices(coins=["bitcoin", "ethereum"])

for coin, info in data.items():
    print(f"{coin.capitalize()}: ${info['price']:.2f} ({info['change_24h']:.2f}%)")
```

## License

This project is open-source and available under the [MIT License](LICENSE).