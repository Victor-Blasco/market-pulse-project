import pandas as pd

class Stock:
    """Represents a stock with its historical data.
    Attributes:
        ticker (str): The stock ticker symbol.
        data (pd.DataFrame): Historical stock data with columns like 'Open', 'Close', 'High', 'Low', 'Volume'.
    
    """


    def __init__(self, ticker: str, data: pd.DataFrame):
        """Initializes the Stock with ticker and historical data."""
        self.ticker = ticker
        self.data = data

    def get_latest_price(self) -> float:
        """Returns the latest closing price of the stock."""
        return self.data['Close'].iloc[-1]

    def get_moving_average(self, window: int) -> pd.Series:
        """Calculates the moving average for the given window size."""
        return self.data['Close'].rolling(window=window).mean()