import pytest
import pandas as pd
from marketanalysis.models import Stock

def test_stock_initialization():
    """Tests the successful creation of a Stock object."""
    stock = Stock(ticker="AAPL", sector="Technology")
    
    assert stock.ticker == "AAPL", f"Expected ticker 'AAPL', but got '{stock.ticker}'"
    assert stock.sector == "Technology", f"Expected sector 'Technology', but got '{stock.sector}'"
    assert stock.data.empty, "Stock data should be initialized as empty."

def test_stock_initialization_invalid_ticker():
    """Tests that initialization fails with an empty ticker."""

    with pytest.raises(ValueError, match="Ticker must be a non-empty string."):
        Stock(ticker="")

def test_get_latest_price_no_data():
    """Tests that getting a price fails if data is empty."""
    stock = Stock(ticker="AAPL")
    
    with pytest.raises(ValueError, match="No data available for this stock."):
        stock.get_latest_price()

def test_get_moving_average_no_data():
    """Tests that calculating MA fails if data is empty."""
    stock = Stock(ticker="AAPL")
    
    with pytest.raises(ValueError, match="No data available for this stock."):
        stock.get_moving_average(window=5)

def test_get_latest_price_with_data():
    """Tests getting the latest price from a populated DataFrame."""
    stock = Stock(ticker="AAPL")
    stock.data = pd.DataFrame({'Close': [150, 155, 160]})
    
    expected = 160
    actual = stock.get_latest_price()
    assert actual == expected, f"Expected latest price {expected}, but got {actual}"

def test_get_moving_average_with_data():
    """Tests calculating a moving average from a populated DataFrame."""
    stock = Stock(ticker="AAPL")
    stock.data = pd.DataFrame({'Close': [150, 155, 160]})
    
    moving_average = stock.get_moving_average(window=2)
    
    expected_ma = 157.5  # (155 + 160) / 2
    actual_ma = moving_average.iloc[-1]
    
    assert actual_ma == expected_ma, f"Expected MA(2) to be {expected_ma}, but got {actual_ma}"