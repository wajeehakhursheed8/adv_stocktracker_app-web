import streamlit as st
import pandas as pd

# Your original stocks data
stocks = {
    # Technology
    "AAPL": {"price": 178.5, "quantity": 10},    # Apple
    "MSFT": {"price": 329.8, "quantity": 5},     # Microsoft
    "TSLA": {"price": 244.3, "quantity": 8},     # Tesla
    "GOOGL": {"price": 132.7, "quantity": 12},   # Alphabet
    "AMZN": {"price": 138.5, "quantity": 7},     # Amazon
    "NVDA": {"price": 452.2, "quantity": 4},     # NVIDIA
    "META": {"price": 298.1, "quantity": 6},     # Meta Platforms
    
    # Banking & Finance
    "JPM": {"price": 145.9, "quantity": 9},      # JPMorgan Chase
    "BAC": {"price": 28.4, "quantity": 20},      # Bank of America
    "GS": {"price": 345.2, "quantity": 3},       # Goldman Sachs
    
    # Energy
    "XOM": {"price": 108.7, "quantity": 15},     # ExxonMobil
    "CVX": {"price": 164.1, "quantity": 7},      # Chevron
    "BP": {"price": 36.9, "quantity": 18},       # BP plc
    
    # Pharmaceuticals / Healthcare
    "PFE": {"price": 38.2, "quantity": 20},      # Pfizer
    "JNJ": {"price": 165.3, "quantity": 6},      # Johnson & Johnson
    "MRK": {"price": 110.6, "quantity": 8},      # Merck & Co.
    
    # Consumer Goods
    "KO": {"price": 60.7, "quantity": 14},       # Coca-Cola
    "PEP": {"price": 181.5, "quantity": 5},      # PepsiCo
    "NKE": {"price": 109.4, "quantity": 9},      # Nike
    "MCD": {"price": 287.3, "quantity": 4}       # McDonald's
}

# Your original functions (unchanged)
def get_price(stockname):
    if stockname in stocks:
        return stocks[stockname]["price"]
    else:
        return None

def total(stocks):
    total_invest = 0
    for stock in stocks:
        price = stocks[stock]['price']
        quantity = stocks[stock]['quantity']
        total_invest += price * quantity
    return total_invest

# Initialize session state for results
if 'results' not in st.session_state:
    st.session_state.results = []

# Streamlit GUI
st.title(" WELCOME TO STOCK INFO!")
st.markdown("---")

# Sidebar for stock information
st.sidebar.header("Available Stocks")
st.sidebar.markdown("### Technology")
tech_stocks = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "NVDA", "META"]
for stock in tech_stocks:
    st.sidebar.text(f"{stock}: ${stocks[stock]['price']}")

st.sidebar.markdown("### Banking & Finance")
finance_stocks = ["JPM", "BAC", "GS"]
for stock in finance_stocks:
    st.sidebar.text(f"{stock}: ${stocks[stock]['price']}")

st.sidebar.markdown("### Energy")
energy_stocks = ["XOM", "CVX", "BP"]
for stock in energy_stocks:
    st.sidebar.text(f"{stock}: ${stocks[stock]['price']}")

st.sidebar.markdown("### Healthcare")
health_stocks = ["PFE", "JNJ", "MRK"]
for stock in health_stocks:
    st.sidebar.text(f"{stock}: ${stocks[stock]['price']}")

st.sidebar.markdown("### Consumer Goods")
consumer_stocks = ["KO", "PEP", "NKE", "MCD"]
for stock in consumer_stocks:
    st.sidebar.text(f"{stock}: ${stocks[stock]['price']}")

# Main interface
st.header("Stock Calculator")

col1, col2 = st.columns(2)

with col1:
    stockname1 = st.selectbox(
        "Select a stock:",
        options=list(stocks.keys()),
        index=0
    )

with col2:
    quantity = st.number_input(
        "Enter quantity:",
        min_value=1,
        value=1,
        step=1
    )

# Custom CSS for green button
st.markdown("""
<style>
.stButton > button[kind="primary"] {
    background-color: #556B2F !important;
    color: white !important;
    border: none !important;
    border-radius: 5px !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #3D4F21 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

if st.button("Calculate Stock Value", type="primary"):
    price = get_price(stockname1)
    if price is not None:
        total_value = price * quantity
        
        st.success(f" The price of {stockname1} is ${price}")
        st.info(f" Total value for {quantity} shares: ${total_value}")
        
        # Add to results (your original logic)
        st.session_state.results.append({
            "Stock": stockname1,
            "Quantity": quantity,
            "Price": price,
            "Total Value": total_value
        })
    else:
        st.error(" Error 404: Stock not found!")

# Display current results
if st.session_state.results:
    st.markdown("---")
    st.header("Your Stock Calculations")
    df_results = pd.DataFrame(st.session_state.results)
    st.dataframe(df_results, use_container_width=True)
    
    # Clear results button
    if st.button("Clear All Results"):
        st.session_state.results = []
        st.rerun()

# Total investment calculation section
st.markdown("---")
st.header("Total Investment Calculator")

col3, col4 = st.columns(2)

with col3:
    if st.button("Calculate Total Investment", type="secondary"):
        total_investment = total(stocks)
        st.success(f" The total investment of all stocks is: ${total_investment:,.2f}")

with col4:
    if st.session_state.results:
        user_total = sum([result["Total Value"] for result in st.session_state.results])
        st.metric("Your Calculated Total", f"${user_total:,.2f}")

# CSV download section
if st.session_state.results:
    st.markdown("---")
    st.header("Export Results")
    
    df_download = pd.DataFrame(st.session_state.results)
    csv_data = df_download.to_csv(index=False)
    
    st.download_button(
        label=" Download Results as CSV",
        data=csv_data,
        file_name="stock_results.csv",
        mime="text/csv",
        type="primary"
    )

# Footer
st.markdown("---")
st.markdown("*Thank you for using Stock Info! *")