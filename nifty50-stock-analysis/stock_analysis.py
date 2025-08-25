import json
import os
import yfinance as yf
import pandas as pd
import time
from datetime import date
import streamlit as st

# --- Stock Data Functions ---

tickers = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BHARTIARTL.NS",
    "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "ETERNAL.NS",
    "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS",
    "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS",
    "ITC.NS", "JIOFIN.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SHRIRAMFIN.NS",
    "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "TECHM.NS", "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

def fetch_ticker_data(ticker):
    try:
        stock_data = yf.Ticker(ticker)
        info = stock_data.info

        company_name = info.get("longName")
        current_price = info.get("currentPrice")
        book_value = info.get("bookValue")
        earnings_per_share = info.get("trailingEps")
        price_to_earnings = info.get("trailingPE")
        debt_to_equity = info.get("debtToEquity")
        return_on_equity = info.get("returnOnEquity")
        dividend_yield = info.get("dividendYield")
        current_ratio = info.get("currentRatio")
        quick_ratio = info.get("quickRatio")
        operating_cashflow = info.get("operatingCashflow")
        revenue_growth = info.get("revenueGrowth")

        pb_ratio = (current_price / book_value) if (current_price is not None and book_value not in [None, 0]) else None
        growth_rate = revenue_growth * 100 if revenue_growth is not None else 0
        intrinsic_value = (earnings_per_share * (8.5 + 2 * growth_rate)) if earnings_per_share is not None else None

        return [
            ticker, company_name, current_price, book_value, earnings_per_share,
            price_to_earnings, debt_to_equity, return_on_equity, dividend_yield,
            current_ratio, quick_ratio, operating_cashflow, revenue_growth, pb_ratio,
            intrinsic_value, None, None, None, None
        ]
    except Exception:
        return None

@st.cache_data(ttl=3600)  # Cache results for 1 hour to reduce API calls
def get_data():
    all_data = []
    for tic in tickers:
        data = fetch_ticker_data(tic)
        all_data.append(data if data else [tic] + [None]*18)
        time.sleep(1)

    columns = [
        'Ticker', 'Company Name', 'Current Price', 'Book Value', 'Earnings Per Share',
        'Price-to-Earnings Ratio', 'Debt-to-Equity Ratio', 'Return on Equity', 'Dividend Yield',
        'Current Ratio', 'Quick Ratio', 'Operating Cashflow', 'Revenue Growth', 'P/B Ratio',
        'Intrinsic Value', 'Competitive Advantage', 'Market Share', 'Brand Recognition',
        'Corporate Governance'
    ]

    df = pd.DataFrame(all_data, columns=columns)
    df.set_index('Ticker', inplace=True)

    tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    while tickers_to_retry:
        time.sleep(5)
        for tic in tickers_to_retry:
            data = fetch_ticker_data(tic)
            if data:
                for i, col in enumerate(df.columns):
                    if pd.isna(df.at[tic, col]) and data[i + 1] is not None:
                        df.at[tic, col] = data[i + 1]
            time.sleep(1)
        tickers_to_retry = df[(df['Current Price'].isna()) | (df['Earnings Per Share'].isna())].index.tolist()

    df['Date'] = date.today()
    df.sort_index(inplace=True)
    return df

# You can now just call get_data() and display it however you want:
if __name__ == "__main__":
    st.title("Stock Data")
    df = get_data()
    st.dataframe(df)
