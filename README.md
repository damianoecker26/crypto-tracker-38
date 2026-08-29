# crypto-tracker-38

crypto-tracker-38 is a Python tool for monitoring cryptocurrency market data and managing personal investment portfolios. It delivers up-to-date pricing information and performance metrics directly from the terminal to support informed trading decisions.

## Features

- Fetches real-time prices and 24-hour changes for any cryptocurrency via the CoinGecko API
- Tracks custom portfolios with quantity, purchase price, and automatic profit/loss calculations
- Monitors price movements and outputs alerts for user-defined thresholds
- Exports portfolio summaries and price snapshots to CSV for further analysis

## Installation

```bash
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Track current prices:

```bash
python main.py --coins bitcoin ethereum solana
```

Track a portfolio defined in JSON:

```bash
python main.py --portfolio portfolio.json
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)