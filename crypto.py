import streamlit as st
import pandas as pd
import requests

# --- Function to fetch real-time price ---
def get_crypto_data(coin_id="bitcoin", currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params)
    return response.json()

# --- Function to fetch historical data ---
def get_historical_data(coin="bitcoin", days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    res = requests.get(url, params=params).json()
    prices = res["prices"]
    df = pd.DataFrame(prices, columns=["Timestamp", "Price"])
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms")
    return df

# --- Streamlit App ---
st.set_page_config(page_title="Crypto Tracker", layout="centered")
st.title("📈 Real-Time Crypto Price Tracker")

coin = st.selectbox("Choose a cryptocurrency", ["bitcoin", "ethereum", "dogecoin", "solana", "litecoin"])
currency = "usd"

# Fetch current data
data = get_crypto_data(coin, currency)
price = data[coin][currency]
change = data[coin][f"{currency}_24h_change"]

# Display metrics
st.metric(label=f"{coin.title()} Price (USD)", value=f"${price}", delta=f"{change:.2f}%")

# Fetch and show historical data
st.subheader("📊 Price Trend Over Last 7 Days")
df = get_historical_data(coin)
st.line_chart(df.set_index("Date")["Price"])

st.caption("Data Source: CoinGecko API")
