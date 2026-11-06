# crypto-tracker-38

Crypto-tracker-38 is a lightweight, command-line Python application designed for real-time tracking of cryptocurrency market data. It leverages the CoinGecko API to provide instantaneous price updates, percentage changes, and portfolio valuation directly in your terminal.

## Features
*   **Live Price Streaming:** Fetch real-time market data for over 100+ cryptocurrencies using optimized API polling.
*   **Portfolio Tracking:** Maintain a local JSON configuration to track individual holdings and calculate total unrealized PnL.
*   **Custom Alerts:** Configure price thresholds for specific assets to receive system notifications when target values are reached.
*   **Data Visualization:** Generate ASCII-based trend lines directly in the console for quick performance analysis.

## Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the dependencies:

```bash
git clone https://github.com/developer/crypto-tracker-38.git
cd crypto-tracker-38
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

To start the tracker and display the top 10 market cap coins, run the following command:

```bash
python main.py --limit 10
```

To monitor your custom portfolio defined in `assets.json`, use the watch flag:

```bash
python main.py --watch assets.json --refresh 60
```

The `--refresh` flag sets the polling interval in seconds, defaulting to 30 seconds if omitted.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.