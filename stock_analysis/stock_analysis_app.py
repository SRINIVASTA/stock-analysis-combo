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

# ------------------- Main App -------------------

def main():
    st.sidebar.title("📋 Stock Controls")
    symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL, RELIANCE.NS):", value="RELIANCE.NS")
    period = st.sidebar.selectbox("Time Period", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'])
    fetch_button = st.sidebar.button("📥 Fetch Stock Data")

    st.title("📊 Stock Analysis Tool")

    if fetch_button:
        stock, hist, error = fetch_stock_data(symbol, period)
        if error:
            st.error(error)
            return

        info = stock.info
        longName = info.get('longName', 'Unknown Company')
        currency = info.get('currency', 'INR')
        currency_symbol = get_currency_symbol(currency)
        formatted_time = format_close_time(hist.index[-1], symbol)

        # Get values
        current_price = info.get('currentPrice', hist['Close'].iloc[-1])
        market_cap = info.get('marketCap')
        pe = info.get('trailingPE')
        dividend_yield = info.get('dividendYield')
        volume = info.get('volume')
        book_value = info.get('bookValue')
        eps = info.get('trailingEps')
        roe_raw = info.get('returnOnEquity')
        debt_equity = info.get('debtToEquity')
        op_margin = info.get('operatingMargins')

        # ROE calculation if missing
        if roe_raw is None or roe_raw == 0:
            if eps and book_value and book_value != 0:
                roe = (eps / book_value) * 100
            else:
                roe = None
        else:
            roe = roe_raw * 100

        # 📋 Display Summary without gaps
        st.subheader(f"🏢 {longName} ({symbol.upper()})")

        summary_lines = [
            f"**Current Price:** {currency_symbol}{current_price:.2f}",
            f"**{formatted_time}**"
        ]

        if market_cap:
            summary_lines.append(f"**Market Cap:** {currency_symbol}{market_cap / 1e12:.2f} T")
        if pe:
            summary_lines.append(f"**P/E Ratio:** {pe:.2f}")
        if dividend_yield:
            summary_lines.append(f"**Dividend Yield:** {dividend_yield * 100:.2f}%")
        if volume:
            summary_lines.append(f"**Volume:** {volume}")
        if book_value:
            summary_lines.append(f"**Book Value:** {currency_symbol}{book_value:.2f}")
        if eps:
            summary_lines.append(f"**EPS (TTM):** {eps:.2f}")
        if roe:
            summary_lines.append(f"**ROE:** {roe:.2f}%")
        if debt_equity:
            summary_lines.append(f"**Debt to Equity:** {debt_equity:.2f}")
        if op_margin:
            summary_lines.append(f"**Operating Margin:** {op_margin * 100:.2f}%")

        summary_block = "<br>".join(summary_lines)
        st.markdown(summary_block, unsafe_allow_html=True)

        # 📈 Charts
        st.markdown("---")
        st.subheader("🕯️ Candlestick Chart")
        plot_candlestick_chart(hist)

        st.subheader("📈 Price History with SMA")
        fig, ax = plt.subplots()
        ax.plot(hist.index, hist['Close'], label='Close', color='blue')
        ax.plot(hist.index, hist['SMA20'], label='SMA 20', color='green')
        ax.plot(hist.index, hist['SMA50'], label='SMA 50', color='red')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()
        st.pyplot(fig)

        st.subheader("📊 Volume Chart")
        fig, ax = plt.subplots()
        ax.bar(hist.index, hist['Volume'], color='gray')
        ax.set_title("Trading Volume")
        fig.autofmt_xdate()
        st.pyplot(fig)

        st.subheader("📉 RSI Indicator")
        fig, ax = plt.subplots()
        ax.plot(hist.index, hist['RSI'], color='purple')
        ax.axhline(70, color='red', linestyle='--', label='Overbought')
        ax.axhline(30, color='green', linestyle='--', label='Oversold')
        ax.set_title("RSI")
        ax.legend()
        fig.autofmt_xdate()
        st.pyplot(fig)

        st.subheader("📈 MACD Indicator")
        fig, ax = plt.subplots()
        ax.plot(hist.index, hist['MACD'], label='MACD', color='black')
        ax.plot(hist.index, hist['Signal'], label='Signal Line', color='orange')
        ax.axhline(0, color='gray', linestyle='--')
        ax.legend()
        fig.autofmt_xdate()
        st.pyplot(fig)

        # 📌 MACD difference
        diff = hist['MACD'].iloc[-1] - hist['Signal'].iloc[-1]
        st.subheader("📊 MACD - Signal Line Difference")
        st.write(f"Current difference: **{diff:.4f}**")

        # 🔔 Signal summary
        st.header("🔔 Signal Summary")
        summary_msg = generate_signal(hist['RSI'], hist['MACD'], hist['Signal'])
        st.info(summary_msg)

        # Long-term MACD trend
        trend_msg, trend_color = get_long_term_macd_trend(hist['MACD'])
        st.markdown(f"<h3 style='color:{trend_color}'>{trend_msg}</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
