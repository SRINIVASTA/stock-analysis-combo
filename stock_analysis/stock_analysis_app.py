import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import ta
import pytz
from datetime import datetime, time

st.set_page_config(page_title="📈 Stock Analysis App", layout="wide")

# ------------------- Utilities -------------------

def get_currency_symbol(currency_code):
    symbols = {'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
    return symbols.get(currency_code, '')

def format_close_time(last_date, symbol):
    try:
        symbol_lower = symbol.lower()
        if symbol_lower.endswith('.ns'):
            local_tz = pytz.timezone('Asia/Kolkata')
            close_time = time(15, 30)
        elif symbol_lower.endswith('.hk'):
            local_tz = pytz.timezone('Asia/Hong_Kong')
            close_time = time(16, 0)
        elif symbol_lower.endswith('.us') or symbol_lower.endswith('.nasdaq') or symbol_lower.endswith('.nyse'):
            local_tz = pytz.timezone('US/Eastern')
            close_time = time(16, 0)
        else:
            local_tz = pytz.UTC
            close_time = time(16, 0)

        dt_naive = datetime.combine(last_date.date(), close_time)
        dt_localized = local_tz.localize(dt_naive)
        offset = dt_localized.strftime('%z')
        offset_formatted = f"GMT{offset[:3]}:{offset[3:]}"
        return f"At close: {dt_localized.strftime('%B %d at %I:%M:%S %p')} {offset_formatted}"
    except Exception as e:
        return f"At close: (time formatting unavailable: {e})"

def print_major_holders(stock):
    try:
        mh = stock.major_holders
        ih = stock.institutional_holders

        if mh is None or mh.empty:
            st.warning("⚠️ Major holders data not available for this stock via yfinance.")
        else:
            st.subheader("Major Holders Breakdown:")
            # mh is a DataFrame with index and values, show as % with no gaps
            for idx, val in mh.iloc[:, 0].items():
                # some values are in decimals, convert accordingly
                try:
                    if 'PercentHeld' in idx:
                        display_val = f"{val*100:.2f}%"
                    else:
                        display_val = f"{val}"
                except:
                    display_val = str(val)
                st.write(f"{idx.replace('_', ' ').title()}: {display_val}")

        if ih is None or ih.empty:
            st.warning("⚠️ Institutional holders data not available via yfinance.")
        else:
            st.subheader("Top Institutional Holders:")
            st.dataframe(ih)

        with st.expander("📘 Learn More about Major Holders"):
            st.markdown("""
            **Major Holders** are large shareholders that can influence stock price and company decisions:
            - **Insiders:** Company executives and employees holding shares.
            - **Institutions:** Investment firms, mutual funds, pension funds owning shares.
            - **Float:** Shares available for trading (excluding locked-in shares).
            """)
    except Exception as e:
        st.error(f"Error fetching major holders: {e}")

def fetch_stock_data(symbol, period):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    if hist.empty:
        return None, None, "No historical data found."

    hist.dropna(inplace=True)
    hist['SMA20'] = hist['Close'].rolling(window=20).mean()
    hist['SMA50'] = hist['Close'].rolling(window=50).mean()
    hist['RSI'] = ta.momentum.RSIIndicator(hist['Close'], window=14).rsi()
    macd = ta.trend.MACD(hist['Close'])
    hist['MACD'] = macd.macd()
    hist['Signal'] = macd.macd_signal()

    return stock, hist, None

def generate_signal(rsi, macd, signal_line):
    try:
        latest_rsi = rsi.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_signal = signal_line.iloc[-1]

        messages = []
        if latest_rsi < 30:
            messages.append("🔼 RSI suggests the stock may be **oversold**.")
        elif latest_rsi > 70:
            messages.append("🔽 RSI suggests the stock may be **overbought**.")

        if latest_macd > latest_signal:
            messages.append("📈 MACD indicates a **bullish** crossover.")
        else:
            messages.append("📉 MACD indicates a **bearish** crossover.")

        return " ".join(messages)
    except:
        return "Unable to generate signal summary."

def get_long_term_macd_trend(macd_series):
    recent_macd = macd_series.tail(30)
    avg_macd = recent_macd.mean()
    latest_macd = macd_series.iloc[-1]

    if avg_macd < 0 and latest_macd < 0:
        return "📉 Long-Term MACD Trend: **Bearish**", "red"
    elif avg_macd > 0 and latest_macd > 0:
        return "📈 Long-Term MACD Trend: **Bullish**", "green"
    else:
        return "⚖️ Long-Term MACD Trend: **Neutral / Uncertain**", "orange"

def plot_candlestick_chart(hist):
    fig = go.Figure(data=[go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close']
    )])
    fig.update_layout(title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📘 Learn More about Candlestick Charts"):
        st.markdown("""
        Candlestick charts display stock price movements within a specific period:
        - **Body:** Shows open and close prices (green = close > open, red = close < open).
        - **Wicks (Shadows):** Indicate high and low prices.
        They help visualize market sentiment, trends, and reversals.
        """)

def plot_sma_chart(hist):
    fig, ax = plt.subplots()
    ax.plot(hist.index, hist['Close'], label='Close', color='blue')
    ax.plot(hist.index, hist['SMA20'], label='SMA 20', color='green')
    ax.plot(hist.index, hist['SMA50'], label='SMA 50', color='red')
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()
    st.pyplot(fig)

    with st.expander("📘 Learn More about Simple Moving Averages (SMA)"):
        st.markdown("""
        SMAs smooth out price data by averaging closing prices over a set period:
        - **SMA20:** Short-term trend indicator.
        - **SMA50:** Medium-term trend indicator.
        Crossovers between SMAs can signal potential buy or sell points.
        """)

def plot_volume_chart(hist):
    fig, ax = plt.subplots()
    ax.bar(hist.index, hist['Volume'], color='gray')
    ax.set_title("Trading Volume")
    fig.autofmt_xdate()
    st.pyplot(fig)

    with st.expander("📘 Learn More about Trading Volume"):
        st.markdown("""
        Volume shows the number of shares traded during a specific time.
        High volume often confirms price movements; low volume may indicate weak interest.
        """)

def plot_rsi_chart(hist):
    fig, ax = plt.subplots()
    ax.plot(hist.index, hist['RSI'], color='purple')
    ax.axhline(70, color='red', linestyle='--', label='Overbought')
    ax.axhline(30, color='green', linestyle='--', label='Oversold')
    ax.set_title("RSI")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

    with st.expander("📘 Learn More about RSI (Relative Strength Index)"):
        st.markdown("""
        RSI measures speed and change of price movements on a scale of 0 to 100.
        - Above 70: Overbought (possible sell signal).
        - Below 30: Oversold (possible buy signal).
        RSI helps identify momentum shifts.
        """)

def plot_macd_chart(hist):
    fig, ax = plt.subplots()
    ax.plot(hist.index, hist['MACD'], label='MACD', color='black')
    ax.plot(hist.index, hist['Signal'], label='Signal Line', color='orange')
    ax.axhline(0, color='gray', linestyle='--')
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

    with st.expander("📘 Learn More about MACD and Signal Line"):
        st.markdown("""
        The MACD (Moving Average Convergence Divergence) shows the relationship between two EMAs:
        - **MACD line:** Difference between 12-day and 26-day EMAs.
        - **Signal line:** 9-day EMA of the MACD line.
        Crossovers indicate buy or sell signals:
        - MACD crossing above Signal = Bullish.
        - MACD crossing below Signal = Bearish.
        """)

def explain_macd_difference(macd_series, signal_series):
    diff = macd_series.iloc[-1] - signal_series.iloc[-1]
    st.subheader("📊 MACD - Signal Line Difference")
    st.write(f"Current difference between MACD and Signal Line: **{diff:.4f}**")

    with st.expander("📘 Learn More about MACD Difference"):
        st.markdown("""
        The difference between MACD and Signal line helps confirm momentum strength:
        - Positive difference: Bullish momentum.
        - Negative difference: Bearish momentum.
        Larger magnitude = stronger momentum.
        """)

# ------------------- Main App -------------------

def main():
    st.sidebar.title("📋 Stock Controls")
    symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL, RELIANCE.NS):", value="RELIANCE.NS")
    period = st.sidebar.selectbox("Time Period", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'])
    fetch_button = st.sidebar.button("📥 Fetch Stock Data")

    st.title("📊 Welcome to Stock Analysis Tool")

    if fetch_button:
        stock, hist, error = fetch_stock_data(symbol, period)
        if error:
            st.error(error)
            return

        info = stock.info
        longName = info.get('longName', 'Unknown Company')
        currency = info.get('currency', 'INR')
        currency_symbol = get_currency_symbol(currency)
        current_price = info.get('currentPrice', hist['Close'].iloc[-1])
        book_value = info.get("bookValue", "N/A")
        face_value = info.get("faceValue", "N/A")
        isin = info.get("isin", "N/A")
        formatted_time = format_close_time(hist.index[-1], symbol)

        # Summary Info - no gaps, aligned, consistent
        st.subheader(f"🏢 {longName} ({symbol})")
        st.markdown(f"""
- **Current Price:** {currency_symbol}{current_price:.2f}
- **{formatted_time}**
- **Market Cap:** {currency_symbol}{info.get('marketCap', 0)/1e12:.2f} T
- **P/E Ratio:** {info.get('trailingPE', 'N/A')}
- **Dividend Yield:** {info.get('dividendYield', 0) * 100:.2f}%
- **Volume:** {info.get('volume', 'N/A')}
- **Book Value:** {currency_symbol}{book_value}
- **EPS (TTM):** {info.get('trailingEps', 'N/A')}
- **ROE:** {info.get('returnOnEquity', 0) * 100:.2f}%
- **Debt to Equity:** {info.get('debtToEquity', 'N/A')}
- **Operating Margin:** {info.get('operatingMargins', 0) * 100:.2f}%
        """)

        with st.expander("📘 Learn More about Summary Metrics"):
            st.markdown("""
- **Market Cap:** Total value of a company’s outstanding shares.
- **P/E Ratio:** Price-to-Earnings ratio; valuation metric.
- **Dividend Yield:** Annual dividends paid divided by stock price.
- **Volume:** Number of shares traded in a period.
- **Book Value:** Net asset value per share.
- **EPS (TTM):** Earnings per share for last 12 months.
- **ROE:** Return on equity; profitability relative to shareholders’ equity.
- **Debt to Equity:** Financial leverage indicator.
- **Operating Margin:** Profitability from operations.
            """)

        # Short-Term Signal
        signal_text = generate_signal(hist['RSI'], hist['MACD'], hist['Signal'])
        st.info(signal_text)
        with st.expander("📘 Learn More about Short-Term Signals"):
            st.markdown("""
- **RSI:** Indicates if stock is overbought or oversold.
- **MACD Crossover:** Bullish or bearish momentum shifts.
            """)

        # Long-Term MACD Meter
        trend_text, trend_color = get_long_term_macd_trend(hist['MACD'])
        st.markdown(f"<h4 style='color:{trend_color}'>{trend_text}</h4>", unsafe_allow_html=True)
        with st.expander("📘 Learn More about Long-Term MACD Trend"):
            st.markdown("""
This looks at average MACD over past 30 periods to indicate overall market sentiment:
- Positive = Bullish trend.
- Negative = Bearish trend.
- Neutral = Mixed signals.
            """)

        # Major Holders and Institutional Holders with missing checks
        print_major_holders(stock)

        # Candlestick Chart
        st.subheader("🕯️ Candlestick Chart")
        plot_candlestick_chart(hist)

        # SMA Plot
        st.subheader("📈 Price History with SMA")
        plot_sma_chart(hist)

        # Volume Chart
        st.subheader("📊 Volume Chart")
        plot_volume_chart(hist)

        # RSI Plot
        st.subheader("📉 RSI Indicator")
        plot_rsi_chart(hist)

        # MACD Plot
        st.subheader("📈 MACD Indicator")
        plot_macd_chart(hist)

        # MACD vs Signal difference
        explain_macd_difference(hist['MACD'], hist['Signal'])

        # CSV Download
        csv = hist.to_csv()
        st.download_button("📥 Download Historical Data", data=csv, file_name=f"{symbol}_{period}_data.csv", mime='text/csv')

        # Live price refresh
        if st.button("🔄 Refresh Current Price"):
            try:
                live_price = yf.Ticker(symbol).info.get('currentPrice')
                st.metric("Live Price", f"{currency_symbol}{live_price:.2f}")
            except:
                st.error("Could not fetch live price.")

if __name__ == "__main__":
    main()
