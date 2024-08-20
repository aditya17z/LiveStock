import streamlit as st
import yfinance as yf
import time

# Define your watchlist of stocks (Yahoo Finance symbols)
watchlist = ['TATASTEEL.NS', 'IOC.NS']

def get_stock_prices(watchlist):
    prices = {}
    for stock in watchlist:
        try:
            # Fetch the stock data
            ticker = yf.Ticker(stock)
            # Extract the last traded price
            prices[stock] = ticker.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            prices[stock] = f"Error: {e}"
    return prices

# Streamlit app layout
st.title("Live Stock Price Monitor")
st.write("Monitoring the following stocks: TATA Steel and IOCL")

while True:
    stock_prices = get_stock_prices(watchlist)
    st.write("Stock Prices:")
    for stock, price in stock_prices.items():
        st.write(f"{stock}: ₹{price:.2f}")
    st.write("-" * 40)
    time.sleep(1)
    st.experimental_rerun()  # Rerun the Streamlit app to update the prices
