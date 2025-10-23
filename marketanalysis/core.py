import pandas as pd
import numpy as np
import yfinance as yf
from typing import List
from .models import Stock

class MarketAnalyzer:
    """Provides methods to analyze market data for multiple stocks.
    Attributes:
        name (str): The name of the market analyzer.
        stocks (List[Stock]): A list of Stock objects to analyze.
        results (pd.DataFrame): DataFrame to store analysis results.
    """

    def __init__(self, name: str, stocks: List[Stock]):
        """Initializes the MarketAnalyzer with a name and a list of Stock objects."""
        self.name = name
        self.stocks = stocks
        self.results = pd.DataFrame()
    
    def add_stock(self, stock: Stock):
        """Adds a new Stock object to the analyzer."""
        self.stocks.append(stock)

    def fetch_data(self, start_date: str, end_date: str):
        """Fetches historical data for all stocks in the analyzer."""
        for stock in self.stocks:
            data = yf.download(stock.ticker, start=start_date, end=end_date)
            stock.data = data