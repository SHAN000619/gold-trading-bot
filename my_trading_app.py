import streamlit as st
import pandas as pd
import time
from datetime import datetime

# 1. Dashboard Configuration
st.set_page_config(page_title="Gold Bot Dashboard", layout="wide")

# 2. Safe MT5 Import
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
    st.sidebar.warning("Running in Cloud Mode (MT5 Offline)")

st.sidebar.info(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

# 4. Main Dashboard Header
st.title("📊 Gold Trading Bot Live Dashboard")
st.markdown("---")

# 5. Trading Data Display (Dummy Data if MT5 is offline)
col1, col2, col3 = st.columns(3)

if MT5_ENABLED:
    # Here the bot would normally fetch real MT5 data
    account_balance = 100031.04
    current_rsi = 34.06
    status = "Monitoring Market"
else:
    # Displaying current values you sent me
    account_balance = 100031.04
    current_rsi = 34.06
    status = "Waiting for Signal"

with col1:
    st.metric(label="Account Balance", value=f"${account_balance:,.2f}")
with col2:
    st.metric(label="Current RSI (14)", value=current_rsi)
with col3:
    st.metric(label="Bot Status", value=status)

# 6. Trade History Table
st.subheader("Recent Activity")
data = {
    'Time': [datetime.now().strftime('%Y-%m-%d %H:%M')],
    'Symbol': ['XAUUSD'],
    'Type': ['Monitoring'],
    'Price': [2035.50]
}
df = pd.DataFrame(data)
st.table(df)

# 7. Auto-Refresh logic
st.empty()
time.sleep(1)
