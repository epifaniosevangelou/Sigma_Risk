# Stock Report & Comparison Scripts

## Overview

This repository contains two scripts: `stock_report.py` and `stock_comparison.py`. They fetch historical stock data, compute financial metrics, and generate visual reports.

## `stock_report.py`

Generates detailed reports for each stock in the `tickers` list.

- **Data Source**: Fetches data from `yfinance`.
- **Metrics**: Calculates arithmetic returns, drawdowns, and risk statistics.
- **Visuals**:
  - Statistics table (`Riskfolio-Lib`)
  - Histogram of returns
  - Drawdown plot
- **Outputs**: Each ticker's results are saved in `outputs/Reporting/Stock Reporting/<ticker>`.

## `stock_comparison.py`

Compares multiple stocks against a benchmark.

- **Metrics**:
  - Sharpe Ratio
  - Beta and Alpha (via linear regression)
  - Correlation with portfolio stocks
- **Visuals**:
  - Bar charts for Sharpe Ratio, Beta, and Alpha
  - Correlation heatmaps
- **Data Source**: Fetches stock data from `yfinance` and portfolio data from a CSV file.

## Requirements

- `yfinance`, `pandas`, `matplotlib`, `riskfolio-lib`, `seaborn`, `scikit-learn`

## Output Structure

- **Stock Report**: Saved in `outputs/Reporting/Stock Reporting/<ticker>`.
- **Stock Comparison**: Saved in `outputs/Reporting/Stock Comparison`.
