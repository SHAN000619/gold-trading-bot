import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime
import time

# 1. Page Configuration
st.set_page_config(page_title="Gold Eye Pro", layout="wide")

# 2. Advanced MT5 Style CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header {visibility: hidden;}
    .stMetric { background-color: #111111; border: 0.5px solid #333; border-radius: 8px; padding: 10px; }
    /* Top Price Buttons */
    .price-box { display: flex; justify-content: space-around; background: #111; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .sell-btn { color: #ef5350; font-weight: bold; }
    .buy-btn { color: #26a69a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Live Data Fetching
def get_live_data():
    try:
        data = yf.Ticker("GC=F").history(period="1d", interval="1m").tail(50)
        # RSI Calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        return data
    except:
        return pd.DataFrame()

df = get_live_data()
if not df.empty:
    current_price = df['Close'].iloc[-1]
    bid = current_price - 0.20
    ask = current_price + 0.20

# 4. Top Trading Panel
st.markdown(f"""
    <div class="price-box">
        <div class="sell-btn">SELL<br>{bid:.2f}</div>
        <div style="color:white; font-size:12px;">XAUUSD<br>0.01</div>
        <div class="buy-btn">BUY<br>{ask:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# 5. Navigation Tabs
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

with tabs[1]: # Charts with RSI
    # Subplots: Chart on top, RSI on bottom
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])
    
    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                 low=df['Low'], close=df['Close'], name="Gold"), row=1, col=1)
    
    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI(14)", line=dict(color='#3498db')), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="gray", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="gray", row=2, col=1)

    fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False, margin=dict(l=10,r=10,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]: # Trade Page
    st.write("### Account Info")
    st.metric("Balance", "5,111.28")
    st.metric("Equity", f"{5111.28 + (current_price - 2035):.2f}")
    st.write("---")
    st.info("No active positions")

# Refresh every 5 seconds
time.sleep(5)
st.rerun()
