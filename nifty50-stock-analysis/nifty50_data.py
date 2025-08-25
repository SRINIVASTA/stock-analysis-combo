# nifty50_data.py

import yfinance as yf
import pandas as pd
import time
from datetime import date

TICKERS = [
    'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BRITANNIA.NS',
    'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS',
    'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS',
    'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS', 'ITC.NS',
    'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS',
    'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS',
    'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SUNPHARMA.NS',
    'TATACONSUM.NS', 'TCS.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS',
    'TITAN.NS', 'TRENT.NS', 'ULTRACEMCO.NS', 'WIPRO.NS'
]

def fetch_nifty50_data():
    all_data = []

    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            current_price = info.get("currentPrice")
            book_value = info.get("bookValue")
            eps = info.get("trailingEps")
            pe = info.get("trailingPE")
            revenue_growth = info.get("revenueGrowth")

            pb_ratio = (current_price / book_value) if current_price and book_value else None
            growth_rate = revenue_growth * 100 if revenue_growth else 0
            intrinsic_value = (eps * (8.5 + 2 * growth_rate)) if eps else None

            all_data.append({
                "Ticker": ticker,
                "Company Name": info.get("longName"),
                "Current Price": current_price,
                "Book Value": book_value,
                "EPS": eps,
                "P/E Ratio": pe,
                "Revenue Growth": revenue_growth,
                "P/B Ratio": pb_ratio,
                "Intrinsic Value": intrinsic_value
            })
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            all_data.append({
                "Ticker": ticker,
                "Company Name": None,
                "Current Price": None,
                "Book Value": None,
                "EPS": None,
                "P/E Ratio": None,
                "Revenue Growth": None,
                "P/B Ratio": None,
                "Intrinsic Value": None
            })
        time.sleep(1)

    df = pd.DataFrame(all_data)
    df.set_index("Ticker", inplace=True)
    df["Date"] = date.today()
    return df
