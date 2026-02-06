import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- CUSTOM THEME (MT5 BLACK) ---
st.set_page_config(page_title="Gold Eye MT5 Pro", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    header { visibility: hidden; }
    .stTabs [data-baseweb="tab-list"] { 
        position: fixed; bottom: 0; width: 100%; background: #111; z-index: 999;
        justify-content: space-around; border-top: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 11px; padding: 10px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    .metric-box { background: #111; border: 1px solid #222; border-radius: 5px; padding: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE DATA FETCHING ---
def fetch_data():
    try:
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if not data.empty:
            df = data.tail(60)
            # RSI Calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain/loss)))
            return df, True
    except:
        pass
    return pd.DataFrame(), False

df, success = fetch_data()

# --- TOP PRICE HEADER (SELL/BUY) ---
if success and not df.empty:
    price = df['Close'].iloc[-1]
    # Fixed the TypeError issue by simplifying the display
    col_s, col_i, col_b = st.columns([1, 1, 1])
    with col_s:
        st.markdown(f"<div style='color:#ff3b30; font-size:20px;'><b>SELL</b><br>{price-0.10:.2f}</div>", unsafe_allow_html=True)
    with col_i:
        st.markdown("<div style='color:white; text-align:center; font-size:14px;'><b>XAUUSD</b><br><small>M15 | 0.01 Lot</small></div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div style='color:#34c759; font-size:20px; text-align:right;'><b>BUY</b><br>{price+0.10:.2f}</div>", unsafe_allow_html=True)
else:
    st.info("🔄 Synchronizing with Global Markets...")

# --- BOTTOM NAVIGATION TABS ---
tabs = st.tabs(["Quotes", "Charts", "Trade", "History"])

with tabs[1]: # Advanced Live Chart
    if success and not df.empty:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
        # Green/Red Candles like your MT5 video
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     increasing_line_color='#26a69a', decreasing_line_color='#ef5350'), row=1, col=1)
        # RSI Indicator
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#2962FF', width=1.5), name="RSI"), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=550, xaxis_rangeslider_visible=False, 
                          margin=dict(l=0, r=40, t=5, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#111")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[2]: # Trade Page
    st.markdown("<div class='metric-box'><small style='color:#8e8e93;'>Balance</small><br><b style='font-size:22px;'>$5,111.28</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-box'><small style='color:#8e8e93;'>Equity</small><br><b style='font-size:22px;'>$5,111.78</b> <span style='color:#34c759; font-size:12px;'>+0.50</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-box'><small style='color:#8e8e93;'>Free Margin</small><br><b style='font-size:22px;'>$5,111.28</b></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("CLOSE ALL POSITIONS", type="primary", use_container_width=True):
        st.warning("Sending request to MT5 server...")

# --- REAL-TIME REFRESH ---
time.sleep(2)
st.rerun()
