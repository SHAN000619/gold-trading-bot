import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Gold Eye MT5 Pro", layout="wide")

# Custom Professional Dark Theme (MT5 Style)
st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    header { visibility: hidden; }
    .stTabs [data-baseweb="tab-list"] { 
        position: fixed; bottom: 0; width: 100%; background: #111; z-index: 100;
        justify-content: space-around; border-top: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 11px; padding: 10px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    .metric-container { background: #111; border: 0.5px solid #222; border-radius: 4px; padding: 8px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURE DATA FETCHING ---
def fetch_market_data():
    try:
        # Fetching Gold Spot (XAUUSD equivalent)
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if not data.empty:
            df = data.tail(60)
            # RSI Calculation Logic
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            df['RSI'] = 100 - (100 / (1 + (gain/loss)))
            return df, True
    except:
        pass
    return pd.DataFrame(), False

df, success = fetch_market_data()

# --- TOP INTERACTIVE HEADER (SELL/BUY) ---
if success and not df.empty:
    current_val = df['Close'].iloc[-1]
    # Fixed the TypeError by ensuring current_val is valid
    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; padding: 12px; background: #000; border-bottom: 1px solid #222;'>
            <div style='color: #ff4b4b; font-size: 20px; font-weight: bold;'><small style='font-size:10px; color:#8e8e93;'>SELL</small><br>{current_val-0.12:.2f}</div>
            <div style='color: white; text-align: center; font-size: 14px;'><b>XAUUSD</b><br><small style='color:#8e8e93;'>M15 | 0.01 Lot</small></div>
            <div style='color: #00c853; font-size: 20px; font-weight: bold; text-align: right;'><small style='font-size:10px; color:#8e8e93;'>BUY</small><br>{current_val+0.12:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Connecting to Liquidity Provider...")

# --- NAVIGATION & CONTENT ---
tabs = st.tabs(["Quotes", "Charts", "Trade", "History"])

with tabs[1]: # Advanced Charts Section (MT5 Style)
    if success and not df.empty:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.75, 0.25])
        
        # Professional Candlesticks
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
                                     increasing_fillcolor='#26a69a', decreasing_fillcolor='#ef5350'), row=1, col=1)
        
        # RSI(14) Indicator
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#2962FF', width=1.2), name="RSI(14)"), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, 
                          margin=dict(l=0, r=40, t=5, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#111")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[2]: # Trade Tab
    st.markdown("<div class='metric-container'><small style='color:#8e8e93;'>Balance</small><br><b style='font-size:20px;'>$5,111.28</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-container'><small style='color:#8e8e93;'>Equity</small><br><b style='font-size:20px;'>$5,111.78</b> <span style='color:#00ff00; font-size:12px;'>+0.50</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-container'><small style='color:#8e8e93;'>Free Margin</small><br><b style='font-size:20px;'>$5,111.28</b></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Close All Positions", type="primary", use_container_width=True):
        st.info("Executing Batch Close Order...")

# --- REAL-TIME REFRESH ---
time.sleep(2)
st.rerun()
