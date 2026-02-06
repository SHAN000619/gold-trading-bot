import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- STYLING (The MT5 Look) ---
st.set_page_config(page_title="Gold Eye MT5", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    header { visibility: hidden; }
    .stTabs [data-baseweb="tab-list"] { 
        position: fixed; bottom: 0; width: 100%; background: #111; z-index: 10;
        justify-content: space-around; border-top: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 12px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    .metric-card { background: #111; border: 1px solid #222; border-radius: 5px; padding: 10px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE DATA ENGINE ---
def get_mt5_data():
    try:
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if not data.empty:
            df = data.tail(50)
            # Simple RSI Calculation to avoid library errors
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain/loss)))
            return df, True
    except: pass
    return None, False

df, success = get_mt5_data()

# --- TOP PRICE HEADER ---
if success:
    last_price = df['Close'].iloc[-1]
    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; padding: 10px; background: #000; border-bottom: 1px solid #222;'>
            <div style='color: #ff4b4b; font-size: 18px;'><b>SELL</b><br>{last_price-0.15:.2f}</div>
            <div style='color: white; text-align: center; font-size: 14px;'><b>XAUUSD</b><br><small>M15 | 0.01 Lot</small></div>
            <div style='color: #00c853; font-size: 18px; text-align: right;'><b>BUY</b><br>{last_price+0.15:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tabs = st.tabs(["Quotes", "Charts", "Trade", "History"])

with tabs[1]: # Advanced Charts
    if success:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.75, 0.25])
        # Green/Red Candles like your video
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     increasing_line_color='#00ff00', decreasing_line_color='#ff0000'), row=1, col=1)
        # RSI Indicator
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#2962FF', width=1.2)), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, 
                          margin=dict(l=0, r=40, t=0, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#111")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[2]: # Trade Page
    st.markdown("<div class='metric-card'><small>Balance</small><br><b>$5,111.28</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-card'><small>Equity</small><br><b>$5,111.78</b> <span style='color:#00ff00; font-size:10px;'>+0.50</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-card'><small>Free Margin</small><br><b>$5,111.28</b></div>", unsafe_allow_html=True)
    st.button("Close All Positions", type="primary", use_container_width=True)

# --- AUTO REFRESH ---
time.sleep(2)
st.rerun()
