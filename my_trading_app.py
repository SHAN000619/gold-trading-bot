import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime
import time

# 1. Page Config
st.set_page_config(page_title="Gold Eye MT5 Pro", layout="wide")

# 2. MT5 Ultra-Dark CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header {visibility: hidden;}
    
    /* Top Trading Panel Styling */
    .trade-container {
        display: flex;
        justify-content: space-between;
        background-color: #111111;
        padding: 15px;
        border-radius: 10px;
        border: 0.5px solid #333;
        margin-bottom: 10px;
    }
    .sell-side { color: #ff4b4b; text-align: left; font-size: 20px; font-weight: bold; }
    .buy-side { color: #00c853; text-align: right; font-size: 20px; font-weight: bold; }
    .pair-info { color: white; text-align: center; font-size: 14px; }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 0.5px solid #333; }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Live Data Fetching Logic
def fetch_mt5_data():
    try:
        gold = yf.Ticker("GC=F")
        df = gold.history(period="1d", interval="1m").tail(60)
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        return df, True
    except:
        return pd.DataFrame(), False

df, success = fetch_mt5_data()

if success:
    curr = df['Close'].iloc[-1]
    bid = curr - 0.15
    ask = curr + 0.15

    # 4. Top Price Panel (Exactly like your video)
    st.markdown(f"""
        <div class="trade-container">
            <div class="sell-side"><small>SELL</small><br>{bid:.2f}</div>
            <div class="pair-info"><b>XAUUSD</b><br><small>M15 | 0.01 Lot</small></div>
            <div class="buy-side"><small>BUY</small><br>{ask:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# 5. Bottom Navigation Tabs
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

with tabs[1]: # Advanced Chart Section
    if success:
        # Creating Subplots for Chart + RSI
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # Candlestick Chart
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name="Price"
        ), row=1, col=1)

        # RSI Indicator
        fig.add_trace(go.Scatter(
            x=df.index, y=df['RSI'], name="RSI(14)", line=dict(color='#3498db', width=1.5)
        ), row=2, col=1)

        # RSI Levels (30, 70)
        fig.add_hline(y=70, line_dash="dash", line_color="rgba(255,255,255,0.2)", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="rgba(255,255,255,0.2)", row=2, col=1)

        fig.update_layout(template="plotly_dark", height=600, 
                          xaxis_ranges
