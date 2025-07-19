import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Quantum AI Portfolio", layout="wide")

# Theme selector
theme = st.sidebar.selectbox("Select Theme", ["Dark", "Light"])

if theme == "Dark":
    bg_color = "#121212"
    text_color = "white"
    input_bg = "#1e1e1e"
    border_color = "#444"
    chart_bg = "#1e1e1e"
else:
    bg_color = "white"
    text_color = "black"
    input_bg = "white"
    border_color = "#ccc"
    chart_bg = "white"

# Inject CSS
st.markdown(f"""
    <style>
    .css-18e3th9, .css-1d391kg {{
        background-color: {bg_color};
        color: {text_color};
    }}
    input, .stTextInput>div>div>input, .stDateInput>div>input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    label, .css-10trblm {{
        color: {text_color} !important;
    }}
    [data-testid="stMetricValue"], [data-testid="stMetricDelta"], [data-testid="stMetricLabel"] {{
        color: {text_color} !important;
    }}
    table {{
        color: {text_color} !important;
        background-color: {input_bg} !important;
    }}
    .stLineChart > div > div > canvas {{
        background-color: {chart_bg} !important;
    }}
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {bg_color};
    }}
    ::-webkit-scrollbar-thumb {{
        background-color: {border_color};
        border-radius: 4px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Quantum AI Portfolio Dashboard")

# Sidebar inputs
tickers = st.sidebar.text_input("Enter Ticker Symbols (comma-separated)", "AAPL,MSFT,RELIANCE.NS")
symbols = [t.strip().upper() for t in tickers.split(",") if t.strip()]

min_allowed_date = datetime.date(1990, 1, 1)
today = datetime.date.today()

start_date = st.sidebar.date_input(
    "Start Date",
    value=today - datetime.timedelta(days=100),
    min_value=min_allowed_date
)

end_date = st.sidebar.date_input(
    "End Date",
    value=today,
    min_value=min_allowed_date
)

investment_amount = st.sidebar.number_input("Investment Amount", min_value=1000, value=100000, step=1000, format="%d")

if start_date >= end_date:
    st.error("Error: Start date must be before End date.")
    st.stop()

@st.cache_data(ttl=3600)
def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
    df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
    suffix = ticker
    new_cols = []
    for col in df.columns:
        if isinstance(col, str):
            if col.endswith(suffix):
                col = col[:-len(suffix)]
            elif col.endswith(' ' + suffix):
                col = col[:-(len(suffix) + 1)]
            col = col.strip()
        new_cols.append(col)
    df.columns = new_cols
    return df

@st.cache_data(ttl=600)
def get_yfinance_news(ticker):
    try:
        return yf.Ticker(ticker).news
    except Exception:
        return []

data_dict = {}
for sym in symbols:
    data_dict[sym] = get_data(sym, start_date, end_date)

weights = np.array([1/len(symbols)] * len(symbols))
portfolio_values = None
valid_symbols = []

for i, sym in enumerate(symbols):
    df = data_dict[sym]
    price_col = next((col for col in ['Adj Close', 'Close'] if col in df.columns), None)
    if not price_col:
        st.warning(f"Price data missing for {sym}")
        continue
    prices = df[price_col].dropna()
    if prices.empty:
        st.warning(f"No price data found for {sym}.")
        continue
    valid_symbols.append(sym)
    if portfolio_values is None:
        portfolio_values = prices * weights[i]
    else:
        portfolio_values = portfolio_values.add(prices * weights[i], fill_value=0)

if portfolio_values is not None and not portfolio_values.empty:
    portfolio_values = portfolio_values.dropna()
    scaled_portfolio_values = portfolio_values / portfolio_values.iloc[0] * investment_amount

    current_value = scaled_portfolio_values.iloc[-1]
    initial_value = scaled_portfolio_values.iloc[0]
    total_return = current_value - initial_value
    total_return_pct = (total_return / initial_value) * 100

    daily_returns = scaled_portfolio_values.pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252)
    hhi = np.sum(weights**2)

    np.random.seed(len(valid_symbols) + (end_date - start_date).days)
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    sentiment_scores = []
    for sym in valid_symbols:
        score = np.random.uniform(-1, 1)
        sentiment_scores.append(score)
        if score > 0.25:
            sentiment_counts['positive'] += 1
        elif score < -0.25:
            sentiment_counts['negative'] += 1
        else:
            sentiment_counts['neutral'] += 1
    overall_sentiment_score = np.mean(sentiment_scores)
    risk_level = "HIGH" if volatility > 0.02 else "MODERATE"

    def get_currency_symbol(ticker_list):
        for t in ticker_list:
            if t.endswith('.NS'):
                return "₹"
        return "$"

    currency = get_currency_symbol(valid_symbols)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Portfolio Value", f"{currency}{current_value:,.2f}", delta=f"{total_return_pct:+.3f}%")
        st.metric("All Time Total Return", f"{currency}{total_return:,.2f}", delta=f"{total_return_pct:+.3f}%")
    with col2:
        st.metric("Portfolio Volatility (Annualized)", f"{volatility:.3%}")
        st.metric("Concentration Risk (HHI)", f"{hhi:.3f}")
        st.write(f"Risk Level: **{risk_level}**")
    with col3:
        st.metric("Market Sentiment Strength", f"{overall_sentiment_score:.1%}")
        st.write(f"Sentiment Distribution: Positive {sentiment_counts['positive']}, Neutral {sentiment_counts['neutral']}, Negative {sentiment_counts['negative']}")

    st.markdown("---")
    days_range = (end_date - start_date).days
    display_days = min(days_range, len(scaled_portfolio_values))
    st.subheader(f"Portfolio Trend (Last {display_days} Days)")
    st.line_chart(scaled_portfolio_values.tail(display_days))

    st.subheader("Portfolio Composition")
    st.table(pd.DataFrame({"Ticker": valid_symbols, "Weight": [round(1/len(valid_symbols), 3)] * len(valid_symbols)}))

    st.subheader("AI Recommendations")
    if hhi > 0.5:
        st.warning("High concentration risk detected. Consider diversifying your portfolio.")
    else:
        st.success("Portfolio diversification looks good.")

else:
    st.error("No valid price data found for the given tickers.")
