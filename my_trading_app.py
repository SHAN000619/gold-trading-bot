import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. MT5 Professional Dark Theme Configuration
st.set_page_config(page_title="Gold Eye MT5 Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* MT5 Pure Black Background */
    .main { background-color: #000000 !important; }
    header { visibility: hidden; }
    
    /* Bottom Navigation Bar like MT5 Mobile */
    .stTabs [data-baseweb="tab-list"] { 
        position: fixed; bottom: 0; width: 100%; background: #111; z-index: 1000;
        justify-content: space-around; border-top: 1px solid #333; padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 10px; padding: 10px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    
    /* Trade Page Styling */
    .trade-card { background: #111; border: 1px solid #222; border-radius: 4px; padding: 15px; margin-bottom: 8px; }
    .balance-text { color: #8e8e93; font-size: 12px; }
    .value-text { color: white; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Market Data Loader
def fetch_mt5_market_data():
    try:
        # Fetching Gold Spot Data
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if not data.empty:
            df = data.tail(60)
            # RSI Calculation for the bottom chart
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain/loss)))
            return df, True
    except:
        pass
    return pd.DataFrame(), False

df, success = fetch_mt5_market_data()

# 3. Top Bid/Ask Panel (Fixed Line 48 Error)
if success and not df.empty:
    price = float(df['Close'].iloc[-1])
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown(f"<div style='color:#ff3b30; font-size:18px;'><b>SELL</b><br>{price-0.12:.2f}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='color:white; text-align:center; font-size:12px;'><b>XAUUSD</b><br>M15 | 0.01 Lot</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='color:#34c759; font-size:18px; text-align:right;'><b>BUY</b><br>{price+0.12:.2f}</div>", unsafe_allow_html=True)

# 4. Main App Navigation
tabs = st.tabs(["Quotes", "Charts", "Trade", "History"])

with tabs[1]: # 📈 The Professional Chart View
    if success and not df.empty:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
        
        # MT5 Style Candlesticks
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
                                     increasing_fillcolor='#26a69a', decreasing_fillcolor='#ef5350'), row=1, col=1)
        
        # RSI Indicator
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#2962FF', width=1.5)), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, 
                          margin=dict(l=0, r=40, t=5, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#111")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[2]: # 💼 Trade & Account Summary
    st.markdown("""
        <div class='trade-card'><span class='balance-text'>Balance</span><br><span class='value-text'>$5,111.28</span></div>
        <div class='trade-card'><span class='balance-text'>Equity</span><br><span class='value-text'>$5,111.78</span> <span style='color:#34c759; font-size:12px;'>+0.50</span></div>
        <div class='trade-card'><span class='balance-text'>Free Margin</span><br><span class='value-text'>$5,111.28</span></div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("CLOSE ALL POSITIONS", type="primary", use_container_width=True):
        st.error("Requesting Batch Close...")

# 5. Live Refresh
time.sleep(2)
st.rerun()
