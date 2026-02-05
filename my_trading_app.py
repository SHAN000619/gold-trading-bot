import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import time
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Gold Eye Live", layout="wide")

# 2. Ultra-Dark UI Styling (MT5 Inspired)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header {visibility: hidden;}
    div[data-testid="stMetric"] {
        background-color: #111111;
        border: 0.5px solid #333;
        border-radius: 10px;
        padding: 10px !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Live Data Simulation Logic
@st.cache_data(ttl=1) # තත්පරයකින් දත්ත අලුත් කරයි
def fetch_live_gold():
    try:
        # Fetching Gold Futures (XAUUSD)
        gold = yf.Ticker("GC=F")
        df = gold.history(period="1d", interval="1m").tail(30) # අවසන් විනාඩි 30 ක දත්ත
        return df, True
    except:
        # Fallback dummy data logic
        dates = [datetime.now() - timedelta(minutes=i) for i in range(30)]
        prices = np.random.normal(2035, 2, 30).cumsum()
        df = pd.DataFrame({'Open': prices-1, 'High': prices+2, 'Low': prices-2, 'Close': prices}, index=dates)
        return df, False

live_df, is_online = fetch_live_gold()
current_price = live_df['Close'].iloc[-1]
price_diff = current_price - live_df['Close'].iloc[-2]

# --- Header Section ---
st.markdown(f"### 🟨 Gold Eye Live Terminal")
st.caption(f"Server Time: {datetime.now().strftime('%H:%M:%S')} | Connection: {'🟢 Active' if is_online else '🟠 Simulation Mode'}")

# 4. Main Tabs
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

with tabs[1]: # Chart Tab
    st.write(f"**XAUUSD, M1 (Real-time Feed)**")
    
    # Creating the Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=live_df.index,
        open=live_df['Open'], high=live_df['High'],
        low=live_df['Low'], close=live_df['Close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
        increasing_fillcolor='#26a69a', decreasing_fillcolor='#ef5350'
    )])
    
    # Adding a moving price line (Current Price Label)
    fig.add_hline(y=current_price, line_dash="dash", line_color="#ffffff", 
                 annotation_text=f"Live: {current_price:.2f}", annotation_position="right")

    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=10, r=50, t=10, b=10),
        xaxis_rangeslider_visible=False,
        yaxis=dict(side="right", gridcolor="#1f1f1f"),
        xaxis=dict(gridcolor="#1f1f1f")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[0]: # Quotes Tab
    st.write("Market Watch")
    st.table(pd.DataFrame({
        'Symbol': ['XAUUSD', 'EURUSD', 'BTCUSD'],
        'Price': [f"{current_price:.2f}", "1.0854", "96,240.50"],
        'Change': [f"{price_diff:+.2f}", "-0.0001", "+245.10"]
    }))

with tabs[2]: # Trade Tab
    st.metric("Total Balance", "$100,031.04", f"{price_diff:+.2f}")
    st.markdown("---")
    st.write("Current Positions: **None**")
    st.warning("🤖 Bot is scanning for entry points...")

with tabs[3]: # History Tab
    st.markdown("<center><br>Empty history</center>", unsafe_allow_html=True)

# 5. The "Magic" for live movement
# මෙමගින් තත්පර කිහිපයකට වරක් පිටුව ඉබේම Refresh වේ
st.empty()
time.sleep(2)
st.rerun()
