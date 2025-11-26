# Market Pulse Project

Object-oriented Python financial analysis system designed to explore market behaviors. This project fetches historical stock data, calculates key risk metrics like volatility, and analyzes correlations between different market sectors using professional visualizations.

## Project Overview

**Market Pulse** is designed to answer key questions about financial data through descriptive analysis. Instead of predicting future prices, it focuses on understanding past performance and relationships between assets.

**Key Objectives:**
* **Data Acquisition:** Efficiently fetch historical market data using the Yahoo Finance API (`yfinance`).
* **Risk Assessment:** Calculate and visualize the annualized or daily volatility of stocks.
* **Correlation Analysis:** Determine how different stocks and sectors move in relation to each other.
* **Professional Visualization:** Present findings using clear, high-quality charts (Bar Charts, Heatmaps, Line Plots).

## Features

* **Modular Architecture:** Built as an installable Python package (`marketanalysis`) separating logic from presentation.
* **Efficient Data Pipeline:** Downloads data for multiple tickers in a single API call to optimize performance.
* **Statistical Analysis:**
    * Daily Returns calculation.
    * Volatility (Standard Deviation) computation using `NumPy`.
    * Correlation Matrix generation using `Pandas`.
* **Test-Driven Development (TDD):** Core logic is verified with a comprehensive suite of unit and integration tests using `pytest` and `unittest.mock`.
* **Interactive Presentation:** Results are delivered via a structured Jupyter Notebook.

## Project Structure

```text
market_pulse_project/
├── marketanalysis/          # Core Python Package (The "Engine")
│   ├── __init__.py
│   ├── core.py              # Main logic (MarketAnalyzer class)
│   ├── models.py            # Data structures (Stock class)
│   └── utils.py             # Helper functions
├── presentation/            # Analysis & Reports (The "Client")
│   └── financial_analysis.ipynb
├── tests/                   # Test Suite
│   ├── test_core.py         # Integration tests for MarketAnalyzer
│   └── test_models.py       # Unit tests for Stock model
├── pyproject.toml           # Package build configuration
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```
## Installation and Setup

1. Clone the repository
```bash
git clone https://github.com/Victor-Blasco/market-pulse-project.git
cd market-pulse-proyect
```
2. Create virtual environment
Windows (Git Bash):
```bash
python -m venv venv
source venv/Scripts/activate
```
macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies & The Package
```bash
# Install libraries (pandas, numpy, yfinance, matplotlib, seaborn, pytest, etc.)
pip install -r requirements.txt

# Install the 'marketanalysis' package in editable mode
pip install -e .
```