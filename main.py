import streamlit as st
import yfinance as yf
import time

# Define your watchlist of stocks (Yahoo Finance symbols) along with buying prices and quantities
watchlist = {
    'TATASTEEL.NS': {'buy_price': 149.30, 'quantity': 18},
    'IOC.NS': {'buy_price': 168.14, 'quantity': 7},
    'SAIL.NS': {'buy_price': 126.17, 'quantity': 1}
}

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

def calculate_profit_or_loss(current_price, buy_price, quantity):
    # Calculate profit or loss
    return (current_price - buy_price) * quantity

# Streamlit app layout
st.title("Live Stock Price Monitor with Profit/Loss Calculation")
st.write("Monitoring the following stocks: TATA Steel, IOCL, and SAIL")

placeholder = st.empty()  # Create an empty placeholder to update stock prices

while True:
    stock_prices = get_stock_prices(watchlist)
    
    with placeholder.container():
        st.write("Stock Prices and Profit/Loss:")
        for stock, data in watchlist.items():
            current_price = stock_prices[stock]
            buy_price = data['buy_price']
            quantity = data['quantity']
            if isinstance(current_price, str):  # If there's an error fetching the price
                st.write(f"{stock}: {current_price}")
            else:
                profit_or_loss = calculate_profit_or_loss(current_price, buy_price, quantity)
                profit_or_loss_str = f"Profit" if profit_or_loss >= 0 else "Loss"
                st.write(f"{stock}: ₹{current_price:.2f} | Bought at: ₹{buy_price:.2f} | Quantity: {quantity} | {profit_or_loss_str}: ₹{profit_or_loss:.2f}")
        st.write("-" * 40)
    
    time.sleep(10)  # Update every 10 seconds
