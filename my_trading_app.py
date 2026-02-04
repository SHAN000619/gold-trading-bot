import streamlit as st
import MetaTrader5 as mt5
import pandas as pd

# --- Configuration ---
SYMBOL = "XAUUSD"
LOT_SIZE = 0.01
# 500 points = $5.00 for 0.01 lot in Gold
TP_POINTS = 500  
SL_POINTS = 500  

def get_rsi(symbol, periods=14):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
    if rates is None: return 50
    df = pd.DataFrame(rates)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

if not mt5.initialize():
    st.error("MT5 Initialization Failed!")
else:
    acc = mt5.account_info()
    st.sidebar.metric("Balance", f"${acc.balance:,.2f}")
    
    current_rsi = round(get_rsi(SYMBOL), 2)
    st.title(f"🤖 Pro Gold Bot | RSI: {current_rsi}")

    positions = mt5.positions_get(symbol=SYMBOL)

    if not positions:
        tick = mt5.symbol_info_tick(SYMBOL)
        
        # BUY Logic with SL/TP
        if current_rsi < 30:
            price = tick.ask
            sl = price - (SL_POINTS * 0.01)
            tp = price + (TP_POINTS * 0.01)
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": LOT_SIZE,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": sl,
                "tp": tp,
                "magic": 202401,
                "comment": "Auto Buy SL/TP",
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
            mt5.order_send(request)
            st.toast("🚀 Buy Order Placed with SL/TP!")

        # SELL Logic with SL/TP
        elif current_rsi > 70:
            price = tick.bid
            sl = price + (SL_POINTS * 0.01)
            tp = price - (TP_POINTS * 0.01)
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": LOT_SIZE,
                "type": mt5.ORDER_TYPE_SELL,
                "price": price,
                "sl": sl,
                "tp": tp,
                "magic": 202401,
                "comment": "Auto Sell SL/TP",
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
            mt5.order_send(request)
            st.toast("📉 Sell Order Placed with SL/TP!")

    # Monitoring Table
    if positions:
        st.subheader("📊 Active Trade Details")
        df_p = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
        st.table(df_p[['ticket', 'type', 'price_open', 'sl', 'tp', 'profit']])
# 7. EMERGENCY CLOSE BUTTON
    if positions:
        st.divider()
        if st.button("🔴 CLOSE ALL ACTIVE TRADES NOW"):
            for pos in positions:
                tick = mt5.symbol_info_tick(pos.symbol)
                # Determine close type (If Buy, close with Sell / If Sell, close with Buy)
                type_close = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
                price_close = tick.bid if pos.type == 0 else tick.ask
                
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": pos.symbol,
                    "volume": pos.volume,
                    "type": type_close,
                    "position": pos.ticket,
                    "price": price_close,
                    "magic": 202401,
                    "type_filling": mt5.ORDER_FILLING_FOK,
                }
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    st.toast(f"✅ Ticket {pos.ticket} closed successfully!")
            
            # Refresh dashboard after closing
            st.rerun()
