# crypto-tracker-38

A lightweight, high-performance command-line interface for monitoring real-time cryptocurrency market data. Built in Python, this tool provides instant access to price feeds, historical trends, and portfolio valuation directly from your terminal.

## Features
* **Live Price Ticker:** Fetches real-time price updates for over 500+ cryptocurrencies using the CoinGecko API.
* **Portfolio Tracking:** Calculate your total holdings value by simply defining your assets and quantities in a local configuration file.
* **Price Alerts:** Set custom threshold triggers to receive terminal notifications when an asset hits your target buy or sell price.
* **Data Export:** Generate clean CSV reports of your current watchlist and historical price data for further analysis.

## Installation

Ensure you have Python 3.8+ installed on your system.

```bash
# Clone the repository
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38

# Install dependencies
pip install -r requirements.txt
```

## Usage

Configure your assets in `portfolio.json`, then run the tracker to see your dashboard:

```bash
# Start the live monitor
python tracker.py --monitor

# Get a one-time snapshot of specific coins
python tracker.py --assets BTC,ETH,SOL
```

You can also set a price alert for a specific currency:

```bash
python tracker.py --alert BTC --target 50000
```

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.