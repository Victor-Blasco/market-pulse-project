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

    def __init__(self, name: str):
        """Initializes the MarketAnalyzer with a name and a list of Stock objects."""
        self.name = name
        self.stocks : List[Stock] = []
        self.results = pd.DataFrame()
    
    def add_stock(self, stock: Stock):
        """Adds a new Stock object to the analyzer."""
        self.stocks.append(stock)

    def fetch_data(self, start_date: str, end_date: str):
        """Fetches historical data for all stocks in the analyzer."""
        try:
            all_data = yf.download(
                tickers=[stock.ticker for stock in self.stocks],
                start=start_date,
                end=end_date,
                group_by='ticker'
            )
            for stock in self.stocks:
                stock.data = all_data[stock.ticker].dropna()
        except Exception as e:
            print(f"Error fetching data: {e}")
    
    def analyze_moving_averages(self, window: int):
        """Analyzes moving averages for all stocks and stores results."""
        analysis_results = []
        for stock in self.stocks:
            try:
                ma_series = stock.get_moving_average(window)
                latest_ma = ma_series.iloc[-1] if ma_series is not None else np.nan
                analysis_results.append({
                    'Ticker': stock.ticker,
                    'Sector': stock.sector,
                    f'MA_{window}': latest_ma
                })
            except ValueError as ve:
                print(f"Skipping {stock.ticker}: {ve}")
        
        self.results = pd.DataFrame(analysis_results)
    
    def get_results(self) -> pd.DataFrame:
        """Returns the analysis results."""
        return self.results
    
    def save_results(self, filepath: str):
        """Saves the analysis results to a CSV file."""
        self.results.to_csv(filepath, index=False)
    
    def load_results(self, filepath: str):
        """Loads analysis results from a CSV file."""
        self.results = pd.read_csv(filepath)
    
    def summarize(self) -> pd.DataFrame:
        """Provides a summary of the analysis results."""
        return self.results.describe()
    
    def calculate_daily_returns(self):
        """Calculates daily returns for all stocks."""
        for stock in self.stocks:
            if not stock.data.empty:
                stock.data['daily_return'] = stock.data['Close'].pct_change()

    def calculate_volatility(self) -> pd.Series | None:
        """Calculates volatility (standard deviation of daily returns) for all stocks."""
        volatility_results = {}
        for stock in self.stocks:
            if 'daily_return' in stock.data.columns:
                volatility = np.std(stock.data['daily_return'].dropna())
                volatility_results[stock.ticker] = volatility
            else:
                print(f"Daily returns not calculated for {stock.ticker}. Skipping volatility calculation.")
        
        if volatility_results:
            return pd.Series(volatility_results, name='Volatility')
        return None

    def get_correlation_matrix(self) -> pd.DataFrame | None:
        """Calculates the correlation matrix of daily returns for all stocks."""
        returns_data = {}
        for stock in self.stocks:
            if 'daily_return' in stock.data.columns:
                returns_data[stock.ticker] = stock.data['daily_return']
            else:
                print(f"Daily returns not calculated for {stock.ticker}. Skipping correlation calculation.")
        
        if returns_data:
            returns_df = pd.DataFrame(returns_data)
            return returns_df.corr()
        return None