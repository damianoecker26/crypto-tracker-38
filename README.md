# crypto-tracker-38

`crypto-tracker-38` is a lightweight, high-performance Python utility designed to monitor real-time cryptocurrency price fluctuations. It provides developers and traders with a streamlined CLI interface to track market trends and analyze asset performance without the bloat of web-based dashboards.

### Features

*   **Real-time Data Streaming:** Fetches live price updates from leading exchanges using optimized asynchronous API requests.
*   **Portfolio Snapshot:** Generates instant terminal-based reports on your current holdings, including 24h percentage changes and total valuation.
*   **Price Alerts:** Configurable threshold monitoring that triggers desktop notifications when assets hit specific support or resistance levels.
*   **Data Persistence:** Automatically logs tracking history to a local SQLite database for future trend analysis and historical price visualization.

### Installation

Ensure you have Python 3.9+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-38.git
cd crypto-tracker-38
pip install -r requirements.txt
```

### Usage

To start tracking your favorite assets, simply provide the ticker symbols as command-line arguments:

```bash
# Monitor Bitcoin and Ethereum prices
python main.py --assets BTC,ETH --interval 30
```

To view a summary of your portfolio from a saved configuration file:

```bash
python main.py --portfolio config.json
```

### License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.