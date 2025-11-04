import pandas as pd

class Stock:
    """Represents a single stock.
    Attributes:
        ticker (str): The stock ticker symbol.
        sector (str, optional): Sector of the stock.
    
    """


    def __init__(self, ticker: str, sector: str = "N/A" ):
        """Initializes the Stock with ticker and sector."""
        if not isinstance(ticker, str) or not ticker:
            raise ValueError("Ticker must be a non-empty string.")
        self.ticker = ticker
        self.sector = sector
        self.data: pd.DataFrame = pd.DataFrame()

    def get_latest_price(self) -> float:
        """Returns the latest closing price of the stock."""
        if self.data.empty:
            raise ValueError("No data available for this stock.")
        return self.data['Close'].iloc[-1]

    def get_moving_average(self, window: int) -> pd.Series | None:
        """Calculates the moving average for the given window size."""
        if self.data.empty:
            raise ValueError("No data available for this stock.")
        return self.data['Close'].rolling(window=window).mean()