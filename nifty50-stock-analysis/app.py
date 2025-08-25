import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from stock_analysis import get_data
import io

def main():
    st.set_page_config(layout="wide")
    st.header("📊 Welcome to the Nifty50 Stock Analysis Dashboard")

    with st.spinner("Fetching stock data..."):
        df = get_data()
    st.success("Data loaded!")

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("📈 Price vs Book Value & P/B Ratio Chart")

    # Prepare x-axis labels and indices
    tickers = df.index.tolist()
    x_vals = list(range(len(tickers)))

    # Create figure
    fig = go.Figure()

    # Bar trace for Current Price
    fig.add_trace(go.Bar(
        x=x_vals,
        y=df['Current Price'],
        name='Current Price',
        marker_color='skyblue',
        text=[f"{v:.2f}" if v is not None else "" for v in df['Current Price']],
        textposition='outside',
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>" +
            "Current Price: %{y}<br>" +
            "Book Value: %{customdata[1]}<br>" +
            "P/B Ratio: %{customdata[2]}<extra></extra>"
        ),
        customdata=list(zip(df['Book Value'], df['Book Value'], df['P/B Ratio'])),
    ))

    # Line trace for Book Value
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df['Book Value'],
        mode='lines+markers+text',
        name='Book Value',
        line=dict(color='limegreen', width=3),
        text=[f"{v:.2f}" if v is not None else "" for v in df['Book Value']],
        textposition='top center',
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>" +
            "Book Value: %{y}<br>" +
            "Current Price: %{customdata[1]}<extra></extra>"
        ),
        customdata=list(zip(tickers, df['Current Price']))
    ))

    # Line trace for P/B Ratio on secondary y-axis
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df['P/B Ratio'],
        mode='lines+markers+text',
        name='P/B Ratio',
        line=dict(color='red', width=3, dash='dash'),
        text=[f"{v:.2f}" if v is not None else "" for v in df['P/B Ratio']],
        textposition='top center',
        yaxis='y2',
        hovertemplate="<b>%{x}</b><br>P/B Ratio: %{y}<extra></extra>"
    ))

    # Update layout for dark theme
    fig.update_layout(
        template='plotly_dark',
        xaxis=dict(
            tickmode='array',
            tickvals=x_vals,
            ticktext=tickers,
            title="Ticker",
            tickangle=45
        ),
        yaxis=dict(
            title="Current Price / Book Value",
            side='left'
        ),
        yaxis2=dict(
            title="P/B Ratio",
            overlaying='y',
            side='right'
        ),
        legend=dict(
            title="Metrics",
            bgcolor='#222222',
            bordercolor='white',
            borderwidth=1
        ),
        margin=dict(l=60, r=60, t=60, b=100),
        height=600,
        hovermode='x unified',
    )

    st.plotly_chart(fig, use_container_width=True)

    # Download PNG button
    buf = fig.to_image(format="png", width=1200, height=700, scale=2)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf,
        file_name="nifty50_stock_analysis_plotly_dark.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
