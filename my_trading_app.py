import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime
import time

# 1. Page Configuration
st.set_page_config(page_title="Gold Eye MT5 Pro", layout="wide")

# 2. Advanced MT5 Style CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header {visibility: hidden;}
    .stMetric { background-color: #111111; border: 0.5px solid #333; border-radius: 8px; padding: 10px; }
    
    /* Top Trading Panel */
    .trade-container {
        display: flex;
        justify-content: space-between;
        background-color: #111111;
        padding: 12px;
        border-radius: 8px;
        border-bottom: 1px solid #333;
        margin-bottom: 5px;
    }
    .sell-side { color: #ff4b4b; text-align: left; font-size: 18px; font-weight: bold; }
    .buy-side { color: #00c853; text-align: right; font-size: 18px; font-weight: bold; }
    .pair-info { color: white; text-align: center; font-size: 12px; line-height: 1.2; }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 5px; }
    .stTabs [data-baseweb="tab"] { color: #8e8e93; font-size: 12px; padding: 10px; }
    .stTabs [aria-selected="true"] { color: #f1c40f !important; border-bottom: 2px solid #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Fetch Real-Time Data
def get_mt5_data():
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

df, success = get_mt5_data()

if success:
    curr = df['Close'].iloc[-1]
    bid, ask = curr - 0.10, curr + 0.10

    # 4. Top Price Display (Like your video)
    st.markdown(f"""
        <div class="trade-container">
            <div class="sell-side"><small>SELL</small><br>{bid:.2f}</div>
            <div class="pair-info"><b>XAUUSD</b><br>M15 | 0.01 Lot</div>
            <div class="buy-side"><small>BUY</small><br>{ask:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# 5. App Navigation
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

with tabs[1]: # Charts with RSI
    if success:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])
        # Price Chart
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                     low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        # RSI Chart
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI(14)", line=dict(color='#3498db')), row=2, col=1)
        
        # Fixing the Error: Syntax was fixed here
        fig.update_layout(template="plotly_dark", height=550, xaxis_rangeslider_visible=False, 
                          margin=dict(l=5, r=5, t=0, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#222")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.error("Connection Error. Retrying...")

with tabs[2]: # Account Info
    st.markdown("### Account Summary")
    st.metric("Balance", "$5,111.28")
    st.metric("Equity", f"${5111.28 + (0.50):.2f}", "+0.01%")
    st.write("---")
    st.info("🤖 Bot: Analyzing RSI Market Conditions...")

with tabs[3]: # History
    st.markdown("<center><br><br>Empty history</center>", unsafe_allow_html=True)

# 6. Auto-Refresh
time.sleep(3)
st.rerun()
