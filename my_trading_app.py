import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# 1. Page Configuration
st.set_page_config(page_title="Gold Eye Pro", layout="wide")

# 2. Advanced Professional CSS (Mobile Responsive Fix)
st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #0e1117; }
    
    /* Styling the Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1f2630;
        border: 1px solid #34495e;
        padding: 15px !important;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Force 2 columns per row on Mobile */
    @media (max-width: 640px) {
        div[data-testid="column"] {
            width: 48% !important;
            flex: 1 1 48% !important;
            min-width: 48% !important;
            display: inline-block !important;
            margin-bottom: 10px;
        }
        div[data-testid="stVerticalBlock"] > div {
            flex-direction: row !important;
            flex-wrap: wrap !important;
        }
    }
    
    /* Clean headers */
    h1, h2, h3 { color: #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2500/2500158.png", width=80)
    st.title("Gold Eye Control")
    st.success("System: Active")
    st.info(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown("---")
    st.write("Strategy: RSI Scalper v2.0")

# 4. Main Title
st.title("📊 Gold Eye Trading Terminal")

# 5. Live Metrics (Optimized for Mobile)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Sample Data
account_balance = 100031.04
current_rsi = 34.06
today_profit = 124.50

with col1:
    st.metric("Balance", f"${account_balance:,.2f}", "+0.05%")
with col2:
    st.metric("RSI (14)", current_rsi, "-1.2", delta_color="inverse")
with col3:
    st.metric("Daily Profit", f"${today_profit:,.2f}", "+12%")
with col4:
    st.metric("Status", "Monitoring", "XAUUSD")

st.markdown("---")

# 6. Interactive Live Chart
st.subheader("📈 Market Trend (XAUUSD)")
chart_data = pd.DataFrame({
    'Time': pd.date_range(start=datetime.now(), periods=20, freq='min'),
    'Price': [2035 + random.uniform(-2, 5) for _ in range(20)]
})
fig = go.Figure()
fig.add_trace(go.Scatter(x=chart_data['Time'], y=chart_data['Price'], 
                         mode='lines+markers', 
                         line=dict(color='#f1c40f', width=3),
                         marker=dict(size=6)))
fig.update_layout(template="plotly_dark", height=350, 
                  margin=dict(l=10, r=10, t=10, b=10),
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# 7. Trade History
st.subheader("📜 Recent Trade History")
history_data = {
    'Time': ['22:15', '23:30', '00:45'],
    'Type': ['BUY', 'SELL', 'BUY'],
    'Lots': ['0.01', '0.02', '0.01'],
    'Price': [2032.50, 2038.10, 2034.40],
    'Profit': ['+$35.00', '+$58.00', '-$2.10']
}
df_history = pd.DataFrame(history_data)

def style_profit(val):
    color = '#2ecc71' if '+' in str(val) else '#e74c3c'
    return f'color: {color}; font-weight: bold'

st.table(df_history.style.applymap(style_profit, subset=['Profit']))

# 8. Refresh Logic
time.sleep(1)
