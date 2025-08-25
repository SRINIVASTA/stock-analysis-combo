import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import io

from stock_analysis import get_data  # Import from your module

def main():
    st.set_page_config(layout="wide")
    st.header("📊 Nifty50 Stock Analysis Dashboard")

    # Load stock data
    with st.spinner("Fetching stock data..."):
        df = get_data()
    st.success("Data loaded successfully!")

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("📈 Price vs Book Value & P/B Ratio (Plotly - Dark Theme)")

    # Plotly line/bar chart
    fig = go.Figure()

    # Bar: Current Price
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Current Price'],
        name='Current Price',
        marker_color='skyblue',
        text=[f"₹{p:,.2f}" if p else "" for p in df['Current Price']],
        hoverinfo='text+x+y'
    ))

    # Line: Book Value
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Book Value'],
        name='Book Value',
        mode='lines+markers',
        line=dict(color='limegreen', width=2),
        marker=dict(symbol='circle', size=8),
        hoverinfo='text+x+y'
    ))

    # Line: P/B Ratio
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['P/B Ratio'],
        name='P/B Ratio',
        mode='lines+markers',
        yaxis="y2",
        line=dict(color='red', dash='dash', width=2),
        marker=dict(symbol='x', size=8),
        hoverinfo='text+x+y'
    ))

    # Layout with dark template
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(title="Ticker", tickangle=45),
        yaxis=dict(title="Price / Book Value"),
        yaxis2=dict(title="P/B Ratio", overlaying="y", side="right"),
        legend=dict(x=1.02, y=1, bgcolor="rgba(0,0,0,0)", bordercolor="gray"),
        margin=dict(l=40, r=40, t=60, b=150),
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

    # Download button (as PNG)
    st.subheader("📥 Download Chart as PNG")
    buf = io.BytesIO()
    fig.write_image(buf, format="png", engine="kaleido", scale=2)
    buf.seek(0)

    st.download_button(
        label="Download Image",
        data=buf,
        file_name="nifty50_stock_analysis_dark.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
