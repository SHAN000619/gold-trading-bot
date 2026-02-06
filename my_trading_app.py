import streamlit as st
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- CORE ENGINE & MT5 CONNECTION ---
class GoldEyeMaster:
    def __init__(self):
        if not mt5.initialize():
            st.error("MT5 Connector Offline")

    def fetch_live_data(self, symbol="XAUUSD", timeframe=mt5.TIMEFRAME_M15):
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)
        if rates is None: return pd.DataFrame()
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # Technical Logic (Core)
        df['RSI'] = ta.rsi(df['close'], length=14)
        return df

    def get_account_summary(self):
        acc = mt5.account_info()
        return acc._asdict() if acc else None

    def get_positions(self):
        pos = mt5.positions_get()
        if pos:
            return pd.DataFrame(list(pos), columns=pos[0]._asdict().keys())
        return pd.DataFrame()

# --- UI INTERFACE ---
st.set_page_config(page_title="Gold Eye Terminal", layout="wide")

# MT5 Style UI Styling
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stMetric { background-color: #111; border: 1px solid #333; border-radius: 10px; padding: 10px; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def main():
    engine = GoldEyeMaster()
    
    # 1. Top Account Bar
    acc = engine.get_account_summary()
    if acc:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Balance", f"${acc['balance']:.2f}")
        c2.metric("Equity", f"${acc['equity']:.2f}")
        c3.metric("Floating P/L", f"${acc['profit']:.2f}", delta_color="normal")
        c4.metric("Margin Free", f"${acc['margin_free']:.2f}")

    # 2. Main Chart Section
    df = engine.fetch_live_data()
    if not df.empty:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
        # Candlestick
        fig.add_trace(go.Candlestick(x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'], name="Price"), row=1, col=1)
        # RSI
        fig.add_trace(go.Scatter(x=df['time'], y=df['RSI'], name="RSI", line=dict(color='#3498db')), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, margin=dict(l=0,r=30,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # 3. Trade Management Section
    st.subheader("Active Positions")
    trades = engine.get_positions()
    if not trades.empty:
        # Show selected columns like MT5 app
        st.dataframe(trades[['symbol', 'type', 'volume', 'price_open', 'price_current', 'profit']], use_container_width=True)
    else:
        st.info("No active positions. Scanning for Bot entry...")

if __name__ == "__main__":
    main()
    time.sleep(2)
    st.rerun()
