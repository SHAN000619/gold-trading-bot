import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Custom Styling to mimic MT5 App
st.set_page_config(page_title="Gold Eye Terminal", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    header { visibility: hidden; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000; border-bottom: 1px solid #333; }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 14px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# Function to fetch highly accurate data
def fetch_fast_data():
    try:
        data = yf.download("GC=F", period="1d", interval="1m", progress=False).tail(50)
        return data
    except:
        return None

# MT5 Header UI
st.markdown("""
    <div style='display: flex; justify-content: space-between; padding: 10px; background: #111; border-radius: 10px;'>
        <div style='color: #ff4b4b;'><b>SELL</b><br>4825.34</div>
        <div style='color: white; text-align: center;'><b>XAUUSD</b><br><small>M15 | 0.01 Lot</small></div>
        <div style='color: #00c853;'><b>BUY</b><br>4826.64</div>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["Quotes", "Charts", "Trade", "History"])

with tabs[1]: # The Real MT5 Chart Look
    df = fetch_fast_data()
    if df is not None:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.75, 0.25])
        
        # Professional Green/Red Candles
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#00ff00', decreasing_line_color='#ff0000', name="Price"
        ), row=1, col=1)
        
        # Adding Indicator (RSI) like your video
        df['RSI'] = 50 # Placeholder for demo
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#2962FF', width=1.5)), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False, 
                          margin=dict(l=0, r=40, t=0, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#222")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with tabs[2]: # Trade Page
    st.markdown("### Account Summary")
    st.metric("Balance", "$5,111.28")
    st.metric("Equity", "$5,111.78", "+0.50")
    st.button("Close All Positions", type="primary", use_container_width=True)

time.sleep(1)
st.rerun()
