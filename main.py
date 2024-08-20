import streamlit as st
import yfinance as yf
import time

# Streamlit app layout
st.title("Live Portfolio")

st.sidebar.title("Portfolio Settings")

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# Function to add a new stock to the portfolio
def add_stock():
    if stock_symbol and buy_price and quantity:
        st.session_state.portfolio[stock_symbol] = {'buy_price': buy_price, 'quantity': quantity}

# Sidebar inputs for adding a stock
stock_symbol = st.sidebar.text_input("Stock Symbol (Yahoo Finance format)", "")
buy_price = st.sidebar.number_input("Buying Price", min_value=0.0, format="%.2f")
quantity = st.sidebar.number_input("Quantity", min_value=1, step=1)

if st.sidebar.button("Add Stock"):
    add_stock()

# Function to fetch current stock prices
def get_stock_prices(portfolio):
    prices = {}
    for stock in portfolio:
        try:
            # Fetch the stock data
            ticker = yf.TTicker(stock)
            # Extract the last traded price
            prices[stock] = ticker.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            prices[stock] = f"Error: {e}"
    return prices

# Function to calculate profit or loss
def calculate_profit_or_loss(current_price, buy_price, quantity):
    return (current_price - buy_price) * quantity

# Live updating section of the app
placeholder = st.empty()

while True:
    if st.session_state.portfolio:
        stock_prices = get_stock_prices(st.session_state.portfolio)

        with placeholder.container():
            st.write("Your Portfolio:")
            for stock, data in st.session_state.portfolio.items():
                current_price = stock_prices[stock]
                buy_price = data['buy_price']
                quantity = data['quantity']
                if isinstance(current_price, str):
                    st.write(f"{stock}: {current_price}")
                else:
                    profit_or_loss = calculate_profit_or_loss(current_price, buy_price, quantity)
                    profit_or_loss_str = f"Profit" if profit_or_loss >= 0 else "Loss"
                    st.write(f"{stock}: ₹{current_price:.2f} | Bought at: ₹{buy_price:.2f} | Quantity: {quantity} | {profit_or_loss_str}: ₹{profit_or_loss:.2f}")
            st.write("-" * 40)
    else:
        st.write("Add stocks to your portfolio using the sidebar.")

    time.sleep(10)  # Update every 10 seconds
