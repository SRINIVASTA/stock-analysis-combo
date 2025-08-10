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
        if mh is None or mh.empty:
            return
        data = mh.iloc[:, 0].to_dict()
        st.subheader("Major Holders Breakdown:")
        if 'insidersPercentHeld' in data:
            st.write(f"🧑‍💼 Insiders Hold: **{data['insidersPercentHeld'] * 100:.2f}%**")
        if 'institutionsPercentHeld' in data:
            st.write(f"🏦 Institutions Hold: **{data['institutionsPercentHeld'] * 100:.2f}%**")
        if 'institutionsFloatPercentHeld' in data:
            st.write(f"📊 Float Held by Institutions: **{data['institutionsFloatPercentHeld'] * 100:.2f}%**")
        if 'institutionsCount' in data:
            st.write(f"🏢 Institutions Count: **{int(data['institutionsCount'])}**")
    except:
        pass

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
        msg = []
        if latest_rsi < 30:
            msg.append("🔼 RSI suggests the stock may be **oversold**.")
        elif latest_rsi > 70:
            msg.append("🔽 RSI suggests the stock may be **overbought**.")
        if latest_macd > latest_signal:
            msg.append("📈 MACD indicates a **bullish** crossover.")
        else:
            msg.append("📉 MACD indicates a **bearish** crossover.")
        return " ".join(msg)
    except:
        return "Unable to generate signal summary."

def get_long_term_macd_trend(macd_series):
    avg_macd = macd_series.tail(30).mean()
    latest_macd = macd_series.iloc[-1]
    if avg_macd < 0 and latest_macd < 0:
        return "📉 Long-Term MACD Trend: **Bearish**", "red"
    elif avg_macd > 0 and latest_macd > 0:
        return "📈 Long-Term MACD Trend: **Bullish**", "green"
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

def plot_line_chart(hist, y_col, title, color='blue', ref_lines=[]):
    fig, ax = plt.subplots()
    ax.plot(hist.index, hist[y_col], label=y_col, color=color)
    for yval, label, style, ref_color in ref_lines:
        ax.axhline(y=yval, linestyle=style, color=ref_color, label=label)
    ax.set_title(title)
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

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
        longName = info.get('longName', symbol)
        currency = info.get('currency', 'INR')
        currency_symbol = get_currency_symbol(currency)
        current_price = info.get('currentPrice', hist['Close'].iloc[-1])
        formatted_time = format_close_time(hist.index[-1], symbol)

        # Optional Fields
        book_value = info.get("bookValue")
        face_value = info.get("faceValue")
        eps = info.get("trailingEps")
        roe_raw = info.get("returnOnEquity")
        debt_equity = info.get("debtToEquity")
        op_margin = info.get("operatingMargins")
        pe = info.get('trailingPE')
        dividend_yield = info.get('dividendYield')
        volume = info.get('volume')
        market_cap = info.get('marketCap')

        if roe_raw is None or roe_raw == 0:
            if eps and book_value:
                roe = (eps / book_value) * 100
            else:
                roe = None
        else:
            roe = roe_raw * 100

        # Summary Info
        st.subheader(f"🏢 {longName} ({symbol.upper()})")
        st.markdown(f"- **Current Price:** {currency_symbol}{current_price:.2f}")
        st.markdown(f"- **{formatted_time}**")

        if market_cap:
            st.markdown(f"- **Market Cap:** {currency_symbol}{market_cap / 1e12:.2f} T")
        if pe:
            st.markdown(f"- **P/E Ratio:** {pe:.2f}")
        if dividend_yield:
            st.markdown(f"- **Dividend Yield:** {dividend_yield * 100:.2f}%")
        if volume:
            st.markdown(f"- **Volume:** {volume}")
        if book_value:
            st.markdown(f"- **Book Value:** {currency_symbol}{book_value:.2f}")
        if face_value:
            st.markdown(f"- **Face Value:** {currency_symbol}{face_value:.2f}")
        if eps:
            st.markdown(f"- **EPS (TTM):** {eps:.2f}")
        if roe:
            st.markdown(f"- **ROE:** {roe:.2f}%")
        if debt_equity:
            st.markdown(f"- **Debt to Equity:** {debt_equity:.2f}")
        if op_margin:
            st.markdown(f"- **Operating Margin:** {op_margin * 100:.2f}%")

        print_major_holders(stock)

        st.markdown("---")
        st.header("📈 Price Charts")

        plot_candlestick_chart(hist)

        st.subheader("Simple Moving Averages (SMA)")
        plot_line_chart(hist, 'Close', "Close Price with SMA", 'blue')
        plot_line_chart(hist, 'SMA20', "SMA 20", 'green')
        plot_line_chart(hist, 'SMA50', "SMA 50", 'red')

        st.subheader("Trading Volume")
        plot_line_chart(hist, 'Volume', "Trading Volume", 'gray')

        st.subheader("Relative Strength Index (RSI)")
        plot_line_chart(hist, 'RSI', "RSI", 'purple', ref_lines=[
            (70, 'Overbought', '--', 'red'),
            (30, 'Oversold', '--', 'green')
        ])

        st.subheader("MACD and Signal Line")
        plot_line_chart(hist, 'MACD', "MACD", 'black')
        plot_line_chart(hist, 'Signal', "Signal", 'orange', ref_lines=[(0, 'Zero Line', '--', 'gray')])

        # MACD Difference
        diff = hist['MACD'].iloc[-1] - hist['Signal'].iloc[-1]
        st.subheader("📊 MACD - Signal Line Difference")
        st.write(f"Current MACD - Signal: **{diff:.4f}**")

        # Signal Summary
        st.header("🔔 Signal Summary")
        st.info(generate_signal(hist['RSI'], hist['MACD'], hist['Signal']))

        # Long-term MACD trend
        trend_msg, trend_color = get_long_term_macd_trend(hist['MACD'])
        st.markdown(f"<h3 style='color:{trend_color}'>{trend_msg}</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
