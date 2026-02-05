import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Gold Eye Mobile", layout="wide")

# 2. MT5 Dark Style CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    /* Bottom Navigation Bar */
    .st-emotion-cache-183lyct { 
        padding-top: 0rem; 
    }
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #1c1c1e;
        border-radius: 10px;
        padding: 10px;
    }
    /* Bottom Nav Fix */
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1c1c1e;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        border-top: 0.5px solid #333;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Settings)
st.sidebar.title("Settings")
mode = st.sidebar.selectbox("Theme", ["Dark Mode", "Classic"])

# 4. Top Header (MT5 Style)
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1:
    st.subheader("Gold Eye Terminal")
with col_h2:
    st.write("🔴 Live")

# 5. Bottom Navigation Logic (Using Radio as Buttons)
selected_tab = st.sidebar.radio("Navigation", ["Quotes", "Charts", "Trade", "History"], index=2)

# 6. Page Content based on selection
if selected_tab == "Quotes":
    st.write("### Market Watch")
    st.table(pd.DataFrame({'Symbol': ['XAUUSD', 'EURUSD'], 'Bid': [2035.10, 1.0850], 'Ask': [2035.50, 1.0852]}))

elif selected_tab == "Charts":
    st.write("### XAUUSD, M15")
    fig = go.Figure(data=[go.Candlestick(x=[1,2,3,4], open=[2030,2032,2031,2034], high=[2035,2036,2033,2038], low=[2028,2030,2029,2032], close=[2032,2031,2034,2036])])
    fig.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Trade":
    st.write("### Positions")
    st.metric("Balance", "$100,031.04", "+0.05%")
    st.markdown("---")
    st.info("No Active Positions")

elif selected_tab == "History":
    st.write("### Trade History")
    # Empty state like your screenshot
    st.image("https://cdn-icons-png.flaticon.com/512/5058/5058432.png", width=100)
    st.write("Empty history")
