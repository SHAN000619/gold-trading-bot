import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime
import time

# 1. Page Config
st.set_page_config(page_title="Gold Eye Pro Terminal", layout="wide")

# 2. MT5 Dark Mobile CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header {visibility: hidden;}
    div[data-testid="stMetric"] {
        background-color: #1c1c1e;
        border-radius: 12px;
        padding: 15px !important;
        border: 0.5px solid #333;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1c1c1e;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8e8e93;
    }
    .stTabs [aria-selected="true"] {
        color: #f1c40f !important;
        border-bottom-color: #f1c40f !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Fetching Function (Live Gold Price)
def get_gold_data():
    gold = yf.Ticker("GC=F") # Gold Futures
    data = gold.history(period="1d", interval="15m")
    return data

try:
    live_data = get_gold_data()
    current_price = live_data['Close'].iloc[-1]
    prev_price = live_data['Close'].iloc[-2]
    price_diff = current_price - prev_price
except:
    current_price, price_diff = 2035.50, 0.45

# Header
st.markdown(f"### Gold Eye Terminal")
st.markdown(f"🕒 {datetime.now().strftime('%H:%M:%S')} | 🟢 Live")

# 4. Navigation Tabs
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

with tabs[0]: # Quotes
    st.write("Market Watch")
    st.table(pd.DataFrame({
        'Symbol': ['XAUUSD (Gold)', 'EURUSD', 'BTCUSD'],
        'Price': [f"{current_price:.2f}", "1.0852", "42,500.20"],
        'Change': [f"{price_diff:+.2f}", "-0.0001", "+150.40"]
    }))

with tabs[1]: # Charts (Real Data)
    st.write("XAUUSD, M15 (Live Feed)")
    fig = go.Figure(data=[go.Candlestick(
        x=live_data.index,
        open=live_data['Open'],
        high=live_data['High'],
        low=live_data['Low'],
        close=live_data['Close'],
        increasing_line_color= '#2ecc71', decreasing_line_color= '#e74c3c'
    )])
    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    

with tabs[2]: # Trade (Bot Logic)
    st.write("Positions")
    c1, c2 = st.columns(2)
    c1.metric("Balance", "$100,031.04", f"{price_diff:+.2f}")
    c2.metric("Equity", f"${100031.04 + price_diff:,.2f}")
    
    st.markdown("---")
    # Simulate a Bot Trade
    st.warning("🤖 Bot Status: Scanning for RSI signals...")
    st.write("Current RSI: **34.06**")

with tabs[3]: # History
    st.write("Trade History")
    history_data = {
        'Time': ['10:15', '11:30'],
        'Type': ['BUY', 'SELL'],
        'Profit': ['+$35.00', '+$58.00']
    }
    st.table(pd.DataFrame(history_data))

# Auto-refresh
time.sleep(2)
