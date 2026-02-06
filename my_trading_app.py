import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. Page Config to hide default Streamlit elements
st.set_page_config(page_title="Gold Eye MT5", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced CSS to mimic Native MT5 App look
st.markdown("""
    <style>
    /* Hide Streamlit Header and Footer */
    header {visibility: hidden;}
    [data-testid="stHeader"] {visibility: hidden;}
    .main { background-color: #000000 !important; padding-top: 0px !important; }
    
    /* Custom Navigation Bar at the Bottom (Like MT5) */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #121212;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        border-top: 1px solid #333;
        z-index: 999;
    }
    .nav-item { color: #8e8e93; font-size: 10px; text-align: center; }
    .nav-item.active { color: #f1c40f; }

    /* Top Price Header Styling */
    .top-panel {
        display: flex;
        justify-content: space-between;
        padding: 10px 15px;
        background-color: #121212;
        border-bottom: 1px solid #222;
        margin-top: -50px; /* Adjusting for hidden header */
    }
    .bid-ask { font-size: 22px; font-weight: bold; line-height: 1; }
    .pair-name { text-align: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Engine
def get_mt5_live_data():
    data = yf.download("GC=F", period="1d", interval="1m", progress=False).tail(40)
    return data

# 4. Main App Render
def render_terminal():
    df = get_mt5_live_data()
    
    if not df.empty:
        curr_price = df['Close'].iloc[-1]
        
        # Top MT5 Price Bar
        st.markdown(f"""
            <div class="top-panel">
                <div class="bid-ask" style="color:#ff3b30;"><small style='font-size:10px;'>SELL</small><br>{curr_price-0.10:.2f}</div>
                <div class="pair-name"><b>XAUUSD</b><br><small style='color:#8e8e93;'>M15 | 0.01 LOT</small></div>
                <div class="bid-ask" style="color:#34c759; text-align:right;"><small style='font-size:10px;'>BUY</small><br>{curr_price+0.10:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        # Professional MT5 Chart
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.02, row_heights=[0.75, 0.25])
        
        # Candles with MT5 colors
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#34c759', decreasing_line_color='#ff3b30',
            increasing_fillcolor='#34c759', decreasing_fillcolor='#ff3b30'
        ), row=1, col=1)
        
        # RSI Indicator at Bottom
        df['RSI'] = 45 # Mock RSI for logic
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#007aff', width=1.5)), row=2, col=1)

        fig.update_layout(template="plotly_dark", height=550, xaxis_rangeslider_visible=False,
                          margin=dict(l=0, r=40, t=5, b=0), paper_bgcolor='black', plot_bgcolor='black')
        fig.update_yaxes(side="right", gridcolor="#1a1a1a")
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Bottom MT5 Navigation Simulation
    st.markdown("""
        <div class="nav-bar">
            <div class="nav-item">📊<br>Quotes</div>
            <div class="nav-item active">📈<br>Charts</div>
            <div class="nav-item">💼<br>Trade</div>
            <div class="nav-item">📜<br>History</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_terminal()
    time.sleep(2)
    st.rerun()
