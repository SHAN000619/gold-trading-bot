import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# 1. Page Configuration
st.set_page_config(page_title="Gold Eye Pro", layout="wide")

# 2. Professional CSS Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="metric-container"] {
        background-color: #1f2630;
        border: 1px solid #34495e;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.title("🏆 Gold Eye Pro")
    st.success("Connection: Cloud Active")
    st.info(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown("---")
    st.write("Strategy: RSI Scalping")

# 4. Main Header
st.title("📊 Gold Eye Real-Time Dashboard")

# 5. Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Account Balance", "$100,031.04", "+0.05%")
with col2:
    st.metric("Current RSI", "34.06", "-1.2")
with col3:
    st.metric("Today's Profit", "$124.50", "+12%")
with col4:
    st.metric("Open Trades", "1", "XAUUSD")

st.markdown("---")

# 6. Live Gold Price Chart
st.subheader("📈 XAUUSD Live Market Trend")
chart_data = pd.DataFrame({
    'Time': pd.date_range(start=datetime.now(), periods=20, freq='min'),
    'Price': [2035 + random.uniform(-2, 5) for _ in range(20)]
})
fig = go.Figure()
fig.add_trace(go.Scatter(x=chart_data['Time'], y=chart_data['Price'], mode='lines+markers', line=dict(color='#f1c40f')))
fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

# 7. Trade History Table
st.subheader("📜 Recent Trade History")
history_data = {
    'Time': ['2026-02-05 10:15', '2026-02-05 11:30', '2026-02-05 12:45'],
    'Type': ['BUY', 'SELL', 'BUY'],
    'Lot Size': ['0.01', '0.02', '0.01'],
    'Entry Price': [2032.50, 2038.10, 2034.40],
    'Exit Price': [2036.00, 2035.20, 'Open'],
    'Profit/Loss': ['+$35.00', '+$58.00', '-$2.10']
}
df_history = pd.DataFrame(history_data)

def color_profit(val):
    if isinstance(val, str):
        if '+' in val: return 'color: #2ecc71'
        if '-' in val: return 'color: #e74c3c'
    return ''

st.table(df_history.style.applymap(color_profit, subset=['Profit/Loss']))

time.sleep(1)
