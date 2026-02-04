import streamlit as st
import pandas as pd
import time
from datetime import datetime

# 1. Dashboard Configuration (This sets the Browser Tab Name)
st.set_page_config(page_title="Gold Eye", layout="wide")

# 2. Safe MT5 Import Logic
try:
    import MetaTrader5 as mt5
    MT5_ENABLED = True
except ImportError:
    MT5_ENABLED = False

# 3. Sidebar Information
st.sidebar.title("Bot Status")
if MT5_ENABLED:
    st.sidebar.success("MT5 Library Loaded")
else:
    st.sidebar.warning("Running in Cloud Mode")

st.sidebar.info(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

# 4. Main Dashboard Header (This is the ONLY title displayed)
st.title("📊 Gold Eye Dashboard")
st.markdown("---")

# 5. Trading Metrics (Using your latest values)
col1, col2, col3 = st.columns(3)

# Data values from your screenshot
account_balance = 100031.04
current_rsi = 34.06
bot_status = "Waiting for Signal"

with col1:
    st.metric(label="Account Balance", value=f"${account_balance:,.2f}")
with col2:
    st.metric(label="Current RSI (14)", value=current_rsi)
with col3:
    st.metric(label="System Status", value=bot_status)

# 6. Recent Activity Table
st.subheader("Recent Activity")
data = {
    'Time': [datetime.now().strftime('%Y-%m-%d %H:%M')],
    'Symbol': ['XAUUSD'],
    'Action': ['Monitoring'],
    'Price': [2035.50]
}
df = pd.DataFrame(data)
st.table(df)

# 7. Auto-Refresh
time.sleep(1)
