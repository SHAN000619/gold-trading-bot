import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. Page Configuration & Professional MT5 Theme
st.set_page_config(page_title="Gold Eye MT5 Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    header { visibility: hidden; }
    .stTabs [data-baseweb="tab-list"] { 
        position: fixed; bottom: 0; width: 100%; background: #111; z-index: 999;
        justify-content: space-around; border-top: 1px solid #333; padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 10px; padding: 10px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    .stat-box { background: #111; border: 1px solid #222; border-radius: 4px; padding: 12px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Secure Data Engine (Simplified to prevent TypeErrors)
def get_live_market_data():
    try:
        # Fetching Gold Market Data (XAUUSD)
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if not data.empty:
            df = data.tail(60)
            # Manual RSI calculation to ensure stability
            close = df['Close']
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            return df, True
    except:
        pass
    return pd.DataFrame(), False

df, success = get_live_market_data()

# 3. Top Price Action Header (Fixed Line 48-64 Error)
if success and not df.empty:
    # Safely get current price as a float
    price_val = float(df['Close'].iloc[-1])
    
    # Using 3 columns for better stability instead of complex HTML f-strings
    c_sell, c_info, c_buy = st.columns([1, 1, 1])
    with c_sell:
        st.markdown(f"<div style='color:#ff3b30; font-size:18px;'><b>SELL</b><br>{price_val-0.10:.2f}</div>", unsafe_allow_html=True)
    with c_info:
        st.markdown("<div style='color:white; text-align:center; font-size:12px;'><b>XAUUSD</b><br>M15 | 0.01 Lot</div>", unsafe_allow_html=True)
    with c_buy:
        st.markdown(f"<div style='color:#34c759; font-size:18px; text-align:right;'><b>BUY</b><br>{price_val+0.10:.2f}</div>", unsafe_allow_html=True)
else:
    st.info("⌛ Waiting for live market feed...")

# 4. Navigation & Pro Content
tabs = st.tabs(["Quotes", "Charts", "Trade", "History"])

with tabs[1]: # Advanced Chart View
    if success and not df.empty:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
        
        # Professional Candlesticks
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     increasing_line_color='#26a69a', decreasing_line_color='#ef5350'), row=1, col=1)
        
        # RSI Indicator
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#2962FF', width=1.5)), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, 
                          margin=dict(l=0, r=40, t=5, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#111")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[2]: # Trade Page
    st.markdown("<div class='stat-box'><small style='color:#8e8e93;'>Balance</small><br><b style='font-size:22px;'>$5,111.28</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='stat-box'><small style='color:#8e8e93;'>Equity</small><br><b style='font-size:22px;'>$5,111.78</b> <span style='color:#34c759; font-size:12px;'>+0.50</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='stat-box'><small style='color:#8e8e93;'>Free Margin</small><br><b style='font-size:22px;'>$5,111.28</b></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("CLOSE ALL POSITIONS", type="primary", use_container_width=True):
        st.error("Action: Closing all trades...")

# 5. Real-Time Update
time.sleep(2)
st.rerun()
