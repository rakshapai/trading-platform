# trading-platform

[![GitHub license](https://img.shields.io/github/license/rakshapai/trading-platform)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/rakshapai/trading-platform)](https://github.com/rakshapai/trading-platform/issues)

## Overview

The **Trading Platform** is an automated stock and cryptocurrency trading solution built to facilitate seamless trading strategies. It integrates with **Gemini** and leverages functionalities from [`robin_stocks`](https://www.robin-stocks.com/en/latest/gemini.html) for API interactions.

> **Note**: The `robin_stocks` module used in this project is adapted from the open-source repository mentioned above.


## Overview

The **Trading Platform** is designed as a modular and extensible trading bot that interacts with cryptocurrency exchanges, particularly **Gemini**. It leverages `robin_stocks` for API interaction and includes customizable trading strategies.

## Features

- **Automated Trading**: Execute trades based on predefined strategies.
- **Gemini API Integration**: Real-time data fetching and order execution.
- **Portfolio Management**: Track assets, balances, and transactions.
- **Extensible Architecture**: Customize trading algorithms and integrate with other exchanges.

## Architecture

- **Core Modules:**
  - `main.py` → Entry point for the trading bot.
  - `trading_engine.py` → Manages order execution and trade logic.
  - `strategies/` → Contains various trading strategies.
  - `data_fetcher.py` → Fetches market data in real time.
  - `config.py` → Stores user configurations and risk parameters.

- **External Dependencies:**
  - `robin_stocks` for API interaction.
  - `dotenv` for managing environment variables.
  - `pandas`, `numpy` for data processing.

## Data Flow

1. **Market Data Collection**  [WIP]
   - `data_fetcher.py` pulls real-time market data from Gemini.
  
2. **Strategy Execution**  [WIP]
   - `strategies/` analyzes the data and decides whether to buy, sell, or hold.
  
3. **Trade Execution**  [WIP]
   - `trading_engine.py` sends orders via `robin_stocks`.

4. **Logging & Reporting**  [WIP]
   - All transactions and logs are stored in `logs/` for analysis.

## Future Enhancements
- Add support for additional exchanges (e.g., Binance, Coinbase).
- Implement a web-based dashboard for visualization and reporting.
- Introduce machine learning for predictive analysis.

## References

- [Robin Stocks - Gemini API](https://www.robin-stocks.com/en/latest/gemini.html)

