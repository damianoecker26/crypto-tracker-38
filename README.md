# crypto-tracker-38

Crypto-tracker-38 is a lightweight, high-performance Python CLI tool designed to provide real-time cryptocurrency market data and portfolio monitoring. It aggregates data from multiple exchange APIs to deliver instant price updates and historical performance tracking directly to your terminal.

## Features

*   **Real-time Price Engine:** Fetches live market data using optimized asynchronous requests for sub-second latency.
*   **Portfolio Tracking:** Automatically calculates the current valuation of your holdings by syncing with user-defined asset lists.
*   **Alert System:** Configure custom price threshold triggers that send desktop notifications when assets hit specific targets.
*   **Data Export:** Supports seamless exporting of market trends and portfolio history into CSV format for offline analysis.

## Installation

Ensure you have Python 3.9+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38
pip install -r requirements.txt
```

## Usage

To view the current market status of top assets, run the tracker directly from your terminal:

```bash
python main.py --fetch --limit 10
```

To monitor a specific portfolio file and enable price alerts:

```bash
python main.py --portfolio my_assets.json --alerts --threshold 5.0
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.