import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def run_pure_math_dashboard_ui():
    st.header("⚙️ Pure Math Technical Analytics Engine")
    st.caption("Runs localized mathematical indicators and advanced Shannon Entropy metrics entirely offline.")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        ticker_input = st.text_input("Stock Symbol (e.g., RELIANCE.NS, AAPL):", "RELIANCE.NS").strip().upper()
    with col_input2:
        period_choice = st.selectbox("Select Time Period Horizon:", [
            "1d", "5d", "1mo", "3mo", "1y", "5y", "10y", "MAX"
        ], index=3) # Default index pointing to 3mo
    
    if ticker_input:
        try:
            asset = yf.Ticker(ticker_input)
            
            # 1. Horizon Scale Ingestion Filters
            if period_choice in ["1d", "5d"]:
                raw_history = asset.history(period="1mo", interval="15m")
                target_lookback_days = 1 if period_choice == "1d" else 5
                unique_dates = pd.to_datetime(raw_history.index).date
                min_target_date = sorted(list(set(unique_dates)))[-target_lookback_days]
                display_mask = pd.to_datetime(raw_history.index).date >= min_target_date
            elif period_choice == "MAX":
                raw_history = asset.history(period="max", interval="1d")
                display_mask = pd.Series(True, index=raw_history.index)
            else:
                buffer_days = 60
                if period_choice == "1mo": total_days = buffer_days + 30
                elif period_choice == "3mo": total_days = buffer_days + 90
                elif period_choice == "1y": total_days = buffer_days + 365
                elif period_choice == "5y": total_days = buffer_days + (365 * 5)
                else: total_days = buffer_days + (365 * 10)
                
                raw_history = asset.history(period=f"{total_days}d", interval="1d")
                display_mask = raw_history.index >= raw_history.index[-1] - pd.Timedelta(days=total_days - buffer_days)

            if raw_history.empty:
                st.error(f"Ticker structure '{ticker_input}' returned empty arrays.")
                return

            # 2. Pure Technical Indicator Mathematics
            delta = raw_history['Close'].diff()
            gain = delta.clip(lower=0)
            loss = -1 * delta.clip(upper=0)
            avg_gain = gain.ewm(com=13, adjust=False).mean()
            avg_loss = loss.ewm(com=13, adjust=False).mean()
            rs = avg_gain / (avg_loss + 1e-10)
            raw_history['RSI'] = 100 - (100 / (1 + rs))

            raw_history['EMA12'] = raw_history['Close'].ewm(span=12, adjust=False).mean()
            raw_history['EMA26'] = raw_history['Close'].ewm(span=26, adjust=False).mean()
            raw_history['MACD'] = raw_history['EMA12'] - raw_history['EMA26']
            raw_history['Signal_Line'] = raw_history['MACD'].ewm(span=9, adjust=False).mean()
            raw_history['MACD_Diff'] = raw_history['MACD'] - raw_history['Signal_Line']

            # Isolate focused workspace array
            df = raw_history.loc[display_mask].copy()
            if df.empty:
                df = raw_history.tail(10).copy()

            # 3. CRITICAL SHANNON ENTROPY CALCULATION LOOP
            log_returns = np.log(df['Close'] / df['Close'].shift(1)).dropna()
            entropy_window = 10 if len(log_returns) > 15 else 3
            entropy_list = []
            
            for i in range(len(df)):
                if i < entropy_window:
                    entropy_list.append(0.0) # Pad cold initialization periods
                    continue
                
                slice_data = log_returns.iloc[max(0, i - entropy_window):i]
                counts, bin_edges = np.histogram(slice_data, bins=5, density=True)
                probs = counts / np.sum(counts) if np.sum(counts) > 0 else []
                probs = [p for p in probs if p > 0]
                
                shannon_ent = -np.sum(probs * np.log2(probs)) if probs else 0.0
                entropy_list.append(shannon_ent)

            # --- STAGE-GATE ALIGNMENT REPAIR (LINE 92 FIX) ---
            active_dates = df.index
            if len(entropy_list) != len(active_dates):
                entropy_list = entropy_list[-len(active_dates):]
            
            entropy_df = pd.DataFrame({"Shannon Entropy Value": list(entropy_list)}, index=active_dates)
            df['Entropy'] = entropy_df["Shannon Entropy Value"]

            # 4. Interface Rendering Pipeline Display Elements
            latest_price = df['Close'].iloc[-1]
            latest_rsi = df['RSI'].iloc[-1]
            latest_entropy = df['Entropy'].iloc[-1]
            overbought_days = int((df['RSI'] > 70).sum())
            oversold_days = int((df['RSI'] < 30).sum())

            col1, col2, col3 = st.columns(3)
            col1.metric("Current Close Price", f"₹{latest_price:.2f}" if ".NS" in ticker_input else f"${latest_price:.2f}")
            col2.metric("Trailing 14-Day RSI", f"{latest_rsi:.2f}")
            col3.metric("Current Shannon Entropy", f"{latest_entropy:.4f}")

            col4, col5 = st.columns(2)
            col4.metric("🔴 Overbought Periods Detected", f"{overbought_days} Blocks")
            col5.metric("🟢 Oversold Periods Detected", f"{oversold_days} Blocks")

            # 5. Multi-Pane Integrated Graphic Output Rendering
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(11, 10), sharex=True)
            
            # Panel A: Stock Prices
            window_size = 5 if period_choice in ["1d", "5d"] else (200 if period_choice in ["5y", "10y", "MAX"] else 20)
            df['SMA'] = df['Close'].rolling(window=window_size).mean()
            ax1.plot(df.index, df['Close'], color='dodgerblue', linewidth=1.5, label='Close Price')
            ax1.plot(df.index, df['SMA'], color='navy', linestyle='--', label=f'{window_size} SMA')
            if period_choice in ["5y", "10y", "MAX"]:
                ax1.set_yscale('log')
                ax1.set_title(f"{ticker_input} Financial Price Runway (Log Scale Enabled)", fontweight='bold')
            else:
                ax1.set_title(f"{ticker_input} Financial Price Runway", fontweight='bold')
            ax1.grid(True, alpha=0.15)
            ax1.legend()

            # Panel B: RSI Bounds
            ax2.plot(df.index, df['RSI'], color='darkorange', label='14-Day RSI')
            ax2.axhline(70, color='red', linestyle=':')
            ax2.axhline(30, color='green', linestyle=':')
            ax2.fill_between(df.index, df['RSI'], 70, where=(df['RSI'] > 70), color='red', alpha=0.2)
            ax2.fill_between(df.index, df['RSI'], 30, where=(df['RSI'] < 30), color='green', alpha=0.2)
            ax2.set_ylabel("RSI Range")
            ax2.set_ylim(10, 90)
            ax2.grid(True, alpha=0.15)

            # Panel C: MACD System
            ax3.plot(df.index, df['MACD'], color='blue', label='MACD')
            ax3.plot(df.index, df['Signal_Line'], color='orange', label='Signal')
            ax3.bar(df.index, df['MACD_Diff'], color=np.where(df['MACD_Diff'] >= 0, 'green', 'red'), alpha=0.4)
            ax3.set_ylabel("MACD Scale")
            ax3.grid(True, alpha=0.15)

            # Panel D: Shannon Entropy Disclosures
            ax4.plot(df.index, df['Entropy'], color='purple', linewidth=1.5, label='Shannon Entropy')
            ax4.set_ylabel("Entropy Bit Value")
            ax4.set_xlabel("Market Evaluation Timeline")
            ax4.grid(True, alpha=0.15)
            ax4.legend(loc='upper left')

            fig.autofmt_xdate()
            plt.tight_layout()
            st.pyplot(fig)

        except Exception as err:
            st.error(f"Execution Error within calculation layer: {err}")
