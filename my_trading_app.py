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
    .stTabs [data-baseweb="tab"] { color: #8e8e93; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom-color: #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Fetching with Safety
def get_market_data():
    try:
        # Fetching Gold Futures (XAUUSD substitute)
        gold = yf.Ticker("GC=F")
        df = gold.history(period="1d", interval="15m")
        if df.empty:
            raise ValueError("No data found")
        return df, True
    except:
        # Fallback dummy data if internet or API fails
        dummy_df = pd.DataFrame({
            'Open': [2030, 2032, 2031, 2034],
            'High': [2035, 2036, 2033, 2038],
            'Low': [2028, 2030, 2029, 2032],
            'Close': [2032, 2031, 2034, 2036]
        }, index=pd.date_range(datetime.now(), periods=4, freq='15min'))
        return dummy_df, False

# Get data once at the start of the script
live_data, is_live = get_market_data()
current_price = live_data['Close'].iloc[-1]
price_diff = current_price - live_data['Close'].iloc[-2]

# Header
st.markdown(f"### Gold Eye Terminal")
status_icon = "🟢 Live" if is_live else "🟠 Offline Mode"
st.markdown(f"🕒 {datetime.now().strftime('%H:%M:%S')} | {status_icon}")

# 4. Navigation Tabs
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

with tabs[0]: # Quotes
    st.write("Market Watch")
    st.table(pd.DataFrame({
        'Symbol': ['XAUUSD (Gold)', 'EURUSD', 'BTCUSD'],
        'Price': [f"{current_price:.2f}", "1.0852", "42,500.20"],
        'Change': [f"{price_diff:+.2f}", "-0.0001", "+150.40"]
    }))

with tabs[1]: # Charts
    st.write("XAUUSD, M15 (Real-time Feed)")
    fig = go.Figure(data=[go.Candlestick(
        x=live_data.index,
        open=live_data['Open'], high=live_data['High'],
        low=live_data['Low'], close=live_data['Close'],
        increasing_line_color= '#2ecc71', decreasing_line_color= '#e74c3c'
    )])
    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]: # Trade
    st.write("Positions")
    c1, c2 = st.columns(2)
    c1.metric("Balance", "$100,031.04", f"{price_diff:+.2f}")
    c2.metric("Equity", f"${100031.04 + price_diff:,.2f}")
    st.markdown("---")
    st.warning("🤖 Bot Status: Monitoring RSI Signals...")

with tabs[3]: # History
    st.write("Trade History")
    st.markdown("<br><center><img src='https://cdn-icons-png.flaticon.com/512/5058/5058432.png' width='80'><br>Empty history</center>", unsafe_allow_html=True)

# Refresh
time.sleep(2)
