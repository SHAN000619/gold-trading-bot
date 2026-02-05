import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random

# 1. Page Configuration
st.set_page_config(page_title="Gold Eye Terminal", layout="wide")

# 2. MT5 Dark Mobile CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    header {visibility: hidden;}
    
    /* Metric Styling */
    div[data-testid="stMetric"] {
        background-color: #1c1c1e;
        border-radius: 12px;
        padding: 15px !important;
        border: 0.5px solid #333;
    }

    /* Professional Text */
    h3 { color: #ffffff !important; font-size: 22px !important; }
    .stMarkdown p { color: #8e8e93; }
    
    /* Navigation Simulation */
    .nav-box {
        background-color: #1c1c1e;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Top Status Bar
col_t1, col_t2 = st.columns([0.7, 0.3])
with col_t1:
    st.markdown(f"### Gold Eye Terminal")
with col_t2:
    st.markdown("🔴 **Live**")

st.markdown("---")

# 4. Mobile Navigation (Simple Tabs for Mobile)
tabs = st.tabs(["📊 Quotes", "📈 Charts", "💼 Trade", "📜 History"])

# 5. Tab Content
with tabs[0]:
    st.write("Market Watch")
    prices = {'Symbol': ['XAUUSD', 'EURUSD', 'GBPUSD'], 'Bid': [2035.10, 1.0852, 1.2640], 'Ask': [2035.55, 1.0854, 1.2642]}
    st.table(pd.DataFrame(prices))

with tabs[1]:
    st.write("XAUUSD, M15")
    fig = go.Figure(data=[go.Candlestick(x=list(range(10)),
                open=[2030+i for i in range(10)], high=[2035+i for i in range(10)],
                low=[2028+i for i in range(10)], close=[2032+i for i in range(10)])])
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.write("Positions")
    st.metric("Balance", "$100,031.04", "+0.05%")
    st.info("No Active Positions")

with tabs[3]:
    # Matching your screenshot
    st.write("Trade History")
    st.markdown("<br><br><center><img src='https://cdn-icons-png.flaticon.com/512/5058/5058432.png' width='80'></center>", unsafe_allow_html=True)
    st.markdown("<center>Empty history</center>", unsafe_allow_html=True)
