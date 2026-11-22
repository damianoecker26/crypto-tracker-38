# crypto-tracker-38

Crypto-tracker-38 is a lightweight Python command-line utility designed to monitor real-time cryptocurrency price fluctuations. It provides instant data streaming and historical tracking directly to your terminal.

## Features

*   **Live Price Streaming:** Fetches sub-second price updates for top-tier assets using the CoinGecko API.
*   **Custom Portfolio Monitoring:** Track your specific holdings and view instant P&L calculations based on current market rates.
*   **Price Alerts:** Set custom threshold notifications to receive terminal alerts when an asset hits a target buy or sell price.
*   **Data Export:** Save historical tracking logs to local CSV files for advanced technical analysis.

## Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38
pip install -r requirements.txt
```

## Usage

To start the tracker and monitor your specified assets, execute the main module:

```bash
python main.py --assets BTC,ETH,SOL --interval 10
```

To enable portfolio tracking, create a `portfolio.json` file in the root directory and run:

```bash
python main.py --portfolio portfolio.json
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.