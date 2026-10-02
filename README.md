# crypto-tracker-38

Crypto-tracker-38 is a lightweight Python command-line utility designed to monitor real-time cryptocurrency price fluctuations. It utilizes high-frequency data streams to provide users with instant portfolio valuations and market trend analysis.

## Features

*   **Real-Time Price Tracking:** Fetch live market data for over 500+ assets via the CoinGecko API.
*   **Portfolio Management:** Track your holdings by specifying asset quantities to see real-time P&L calculations.
*   **Price Alerts:** Configure custom threshold notifications to alert you when a coin hits a target buy or sell price.
*   **Historical Data Visualization:** Generate simple terminal-based sparkline charts to visualize 24-hour price trends.

## Installation

Ensure you have Python 3.9+ installed. Clone the repository and install the dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38
pip install -r requirements.txt
```

## Usage

You can start monitoring the market by running the main entry point with your selected ticker symbols:

```bash
# Track current price of Bitcoin and Ethereum
python main.py --symbols BTC ETH

# Track a portfolio with custom quantities
python main.py --portfolio '{"BTC": 0.5, "ETH": 10.2}'
```

To enable desktop notifications for price alerts, use the alert flag:

```bash
python main.py --symbol BTC --alert 50000
```

## Configuration
Update the `config.json` file in the root directory to adjust polling intervals or switch between different API endpoints if you possess an enterprise key.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.