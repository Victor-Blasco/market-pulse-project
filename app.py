import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

from marketanalysis.core import MarketAnalyzer
from marketanalysis.models import Stock

# --- Page Configuration ---
st.set_page_config(
    page_title="Market Pulse Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Title and Description ---
st.title("📈 Market Pulse: Financial Analysis")
st.markdown("""
This application allows you to analyze the volatility and correlation of financial assets 
using real-time data from Yahoo Finance.
""")

# --- Sidebar: User Configuration ---
st.sidebar.header("Analysis Configuration")

# 1. Date Selection
# Default to last 12 months
end_date_default = datetime.today()
start_date_default = end_date_default - timedelta(days=365)

start_date = st.sidebar.date_input("Start Date", start_date_default)
end_date = st.sidebar.date_input("End Date", end_date_default)

# 2. Ticker Selection (Stocks)
default_tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "PFE", "TSLA"]
selected_tickers = st.sidebar.multiselect(
    "Select Stocks (Tickers)",
    options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "BAC", "PFE", "JNJ", "KO"],
    default=default_tickers
)

custom_tickers = st.sidebar.text_input("Or type other tickers (comma separated)", "")
if custom_tickers:
    # Clean and add manual tickers
    manual_list = [t.strip().upper() for t in custom_tickers.split(",") if t.strip()]
    selected_tickers.extend(manual_list)
    # Remove duplicates
    selected_tickers = list(set(selected_tickers))

run_button = st.sidebar.button("Run Analysis", type="primary")

# --- Main Logic ---

# Cached function to avoid downloading data every time a visual tab is changed
@st.cache_data
def run_market_analysis(tickers, start, end):
    if not tickers:
        return None
    
    # Instantiate market analyzer
    analyzer = MarketAnalyzer(name="Streamlit Analysis")
    
    # Add stocks
    for ticker in tickers:
        analyzer.add_stock(Stock(ticker=ticker, sector="Unknown"))
        
    # Download and process 
    analyzer.fetch_data(str(start), str(end))
    analyzer.calculate_daily_returns()
    
    return analyzer

# --- Rendering ---

if run_button:
    if not selected_tickers:
        st.error("Please select at least one stock.")
    else:
        with st.spinner('Downloading data and calculating metrics...'):
            try:
                # Run the analysis using the cached function
                analyzer = run_market_analysis(selected_tickers, start_date, end_date)
                
                # Verify if there is data
                if not analyzer.stocks or analyzer.stocks[0].data.empty:
                    st.error("No data found for the selected tickers in this date range.")
                else:
                    st.success("Analysis complete!")
                    
                    # --- Tabs to organize the visualization ---
                    tab1, tab2, tab3, tab4 = st.tabs(["Risk (Volatility)", "Correlation", "Prices", "Raw Data"])
                    
                    # Tab 1: Volatility
                    with tab1:
                        st.subheader("Risk Analysis: Daily Volatility")
                        volatility = analyzer.calculate_volatility()
                        
                        if volatility is not None:
                            # Show highlight metric (the most volatile stock)
                            max_vol_stock = volatility.idxmax()
                            max_vol_val = volatility.max()
                            st.metric("Most Volatile Stock", max_vol_stock, f"{max_vol_val:.2%}")
                            
                            # Chart
                            fig_vol, ax_vol = plt.subplots(figsize=(10, 5))
                            vol_sorted = volatility.sort_values(ascending=False)
                            ax_vol.bar(vol_sorted.index, vol_sorted.values, color='steelblue')
                            ax_vol.set_ylabel("Standard Deviation")
                            ax_vol.set_title("Volatility (Higher = More Risk)")
                            st.pyplot(fig_vol)
                        else:
                            st.warning("Could not calculate volatility.")

                    # Tab 2: Correlation
                    with tab2:
                        st.subheader("Correlation Matrix")
                        st.write("How do stocks move in relation to each other?")
                        corr_matrix = analyzer.get_correlation_matrix()
                        
                        if corr_matrix is not None:
                            fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
                            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f", ax=ax_corr)
                            st.pyplot(fig_corr)

                    # Tab 3: Prices
                    with tab3:
                        st.subheader("Price Evolution (Normalized Base 100)")
                        # Build DataFrame of normalized prices for the chart
                        price_data = pd.DataFrame()
                        for stock in analyzer.stocks:
                            if not stock.data.empty:
                                first_price = stock.data['Close'].iloc[0]
                                price_data[stock.ticker] = (stock.data['Close'] / first_price) * 100
                        
                        st.line_chart(price_data)

                    # Tab 4: Raw Data
                    with tab4:
                        st.subheader("Latest market data")
                        # Show data for the first stock as an example
                        if analyzer.stocks:
                            stock_example = analyzer.stocks[0]
                            st.write(f"Data for **{stock_example.ticker}**:")
                            st.dataframe(stock_example.data.tail())

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

else:
    st.info("Select your stocks and dates in the sidebar and click 'Run Analysis'.")