import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from marketanalysis.core import MarketAnalyzer
from marketanalysis.models import Stock

@pytest.fixture
def sample_analyzer():
    """Fixture that provides a MarketAnalyzer with sample stocks"""
    analyzer = MarketAnalyzer("Test Analyzer")
    analyzer.add_stock(Stock("AAPL", "Technology"))
    analyzer.add_stock(Stock("MSFT", "Technology"))
    return analyzer

@pytest.fixture
def mock_stock_data():
    """Fixture that provides mock stock data"""
    dates = pd.date_range(start='2023-01-01', end='2023-01-10')
    data = {
        'AAPL': pd.DataFrame({
            'Close': [100, 102, 101, 103, 105, 104, 107, 106, 108, 110]
        }, index=dates),
        'MSFT': pd.DataFrame({
            'Close': [200, 202, 201, 203, 205, 204, 207, 206, 208, 210]
        }, index=dates)
    }
    return data

def test_analyzer_initialization():
    """Tests the correct initialization of the MarketAnalyzer"""
    analyzer = MarketAnalyzer("Test")
    assert analyzer.name == "Test"
    assert len(analyzer.stocks) == 0
    assert analyzer.results.empty

def test_add_stock(sample_analyzer):
    """Tests adding stocks to the analyzer"""
    new_stock = Stock("GOOGL", "Technology")
    initial_count = len(sample_analyzer.stocks)
    sample_analyzer.add_stock(new_stock)
    assert len(sample_analyzer.stocks) == initial_count + 1
    assert sample_analyzer.stocks[-1].ticker == "GOOGL"

@patch('yfinance.download')
def test_fetch_data(mock_yf_download, sample_analyzer, mock_stock_data):
    """Tests fetching historical data using a mock"""
    mock_yf_download.return_value = mock_stock_data
    
    sample_analyzer.fetch_data('2023-01-01', '2023-01-10')
    
    assert not sample_analyzer.stocks[0].data.empty
    assert not sample_analyzer.stocks[1].data.empty
    assert len(sample_analyzer.stocks[0].data) == 10
    assert len(sample_analyzer.stocks[1].data) == 10

def test_analyze_moving_averages(sample_analyzer, mock_stock_data):
    """Tests the moving averages analysis"""
    # Set up the test data
    sample_analyzer.stocks[0].data = mock_stock_data['AAPL']
    sample_analyzer.stocks[1].data = mock_stock_data['MSFT']
    
    # Run the analysis
    sample_analyzer.analyze_moving_averages(window=3)
    
    # Verify the results
    assert not sample_analyzer.results.empty
    assert 'MA_3' in sample_analyzer.results.columns
    assert len(sample_analyzer.results) == 2

def test_save_and_load_results(sample_analyzer, tmp_path):
    """Tests saving and loading results"""
    # Create some test results
    test_data = pd.DataFrame({
        'Ticker': ['AAPL', 'MSFT'],
        'MA_3': [105.0, 205.0]
    })
    sample_analyzer.results = test_data
    
   # Save and load the results
    filepath = tmp_path / "test_results.csv"
    sample_analyzer.save_results(filepath)
    
    # Clear results and reload
    sample_analyzer.results = pd.DataFrame()
    sample_analyzer.load_results(filepath)
    
    # Verify that the data was maintained
    pd.testing.assert_frame_equal(sample_analyzer.results, test_data)

def test_summarize(sample_analyzer):
    """Tests the generation of the results summary"""
    # Set up test data
    sample_analyzer.results = pd.DataFrame({
        'Ticker': ['AAPL', 'MSFT'],
        'MA_3': [105.0, 205.0]
    })
    
    summary = sample_analyzer.summarize()
    assert isinstance(summary, pd.DataFrame)
    assert 'MA_3' in summary.columns


def test_calculate_daily_returns(sample_analyzer, mock_stock_data):
    """Tests that daily returns are calculated correctly."""
    # Set up the test data
    sample_analyzer.stocks[0].data = mock_stock_data['AAPL']
    sample_analyzer.stocks[1].data = mock_stock_data['MSFT']

    sample_analyzer.calculate_daily_returns()
    
    aapl_returns = sample_analyzer.stocks[0].data['daily_return'].dropna()
    expected_returns = mock_stock_data['AAPL']['Close'].pct_change().dropna()

    assert np.isclose(aapl_returns.values, expected_returns.values).all(), f"Expected {expected_returns.values}, got {aapl_returns.values}"



def test_calculate_volatility(sample_analyzer, mock_stock_data):
    """Tests that volatility (std deviation of daily returns) is calculated correctly."""
    # Set up the test data
    sample_analyzer.stocks[0].data = mock_stock_data['AAPL']
    sample_analyzer.stocks[1].data = mock_stock_data['MSFT']

    sample_analyzer.calculate_daily_returns()
    
    aapl_returns = sample_analyzer.stocks[0].data['daily_return'].dropna()

    expected_vol_aapl = np.std(aapl_returns)

    volatilities = sample_analyzer.calculate_volatility()
    
    assert isinstance(volatilities, pd.Series)
    assert 'AAPL' in volatilities.index
    
    
    print(f"AAPL Volatility: {volatilities['AAPL']}, Expected: {expected_vol_aapl}")
    assert np.isclose(volatilities['AAPL'], expected_vol_aapl)

def test_get_correlation_matrix(sample_analyzer, mock_stock_data):
    """Tests the calculation of the correlation matrix of daily returns."""
    # Set up the test data
    sample_analyzer.stocks[0].data = mock_stock_data['AAPL']
    sample_analyzer.stocks[1].data = mock_stock_data['MSFT']

    sample_analyzer.calculate_daily_returns()
    
    returns_data = {
        stock.ticker: stock.data['daily_return'] for stock in sample_analyzer.stocks
    }
    returns_df = pd.DataFrame(returns_data)

    expected_corr = returns_df.corr()

    corr_matrix = sample_analyzer.get_correlation_matrix()
    
    pd.testing.assert_frame_equal(corr_matrix, expected_corr)