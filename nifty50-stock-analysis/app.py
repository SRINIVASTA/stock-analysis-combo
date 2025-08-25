import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.lines import Line2D
import io
from stock_analysis import get_data  # Your custom data fetch function

# ========== Function to build the Matplotlib dark mode figure ==========
def create_dark_mode_figure(df):
    plt.style.use('dark_background')

    fig, ax1 = plt.subplots(figsize=(15, 10), facecolor='black')
    ax1.set_facecolor('black')

    sns.barplot(x='Ticker', y='Current Price', data=df, color='#1f77b4', ax=ax1, width=0.6)

    ax1.plot(df['Ticker'], df['Book Value'], color='#2ca02c', linewidth=2, marker='o', label='Book Value')

    for i, txt in enumerate(df['Book Value']):
        ax1.annotate(f"{txt:.2f}", (i, txt), textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=8, rotation=90, color='white')

    ax2 = ax1.twinx()
    ax2.plot(df['Ticker'], df['P/B Ratio'], color='#d62728', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')

    ax1.set_title('Nifty 50 - Current Price, Book Value, and P/B Ratio Comparison', fontsize=16, color='white')
    ax1.set_xlabel('Ticker', fontsize=12, color='white')
    ax1.set_ylabel('Current Price / Book Value', fontsize=12, color='white')
    ax2.set_ylabel('P/B Ratio', fontsize=12, color='#d62728')

    ax1.tick_params(axis='x', colors='white', rotation=90, labelsize=10)
    ax1.tick_params(axis='y', colors='white', labelsize=10)
    ax2.tick_params(axis='y', colors='#d62728', labelsize=10)

    for spine in ax1.spines.values():
        spine.set_color('white')
    for spine in ax2.spines.values():
        spine.set_color('white')

    legend_elements = [
        Line2D([0], [0], color='#1f77b4', marker='s', linestyle='', label='Current Price'),
        Line2D([0], [0], color='#2ca02c', linewidth=2, marker='o', label='Book Value'),
        Line2D([0], [0], color='#d62728', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ]
    ax1.legend(handles=legend_elements, title='Metrics', loc='upper left',
               bbox_to_anchor=(1.05, 1), fontsize=10, title_fontsize=12,
               facecolor='#222222', edgecolor='white')

    ax1.text(0.05, 0.95, 'datasource: yfinance', transform=ax1.transAxes,
             ha='left', va='top', fontsize=10, color='white')

    plt.tight_layout(pad=2.0)
    return fig

# ========== Streamlit Main App ==========
def main():
    st.set_page_config(layout="wide")
    st.header("📊 Welcome to the Nifty50 Stock Analysis Dashboard")

    with st.spinner("Fetching stock data..."):
        df = get_data()

    # Ensure 'Ticker' is a column (not index)
    if df.index.name == 'Ticker':
        df = df.reset_index()

    st.success("Data loaded!")

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("🖼️ Dark Mode Chart (Matplotlib)")

    fig = create_dark_mode_figure(df)
    st.pyplot(fig)

    # Convert plot to PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor='black', edgecolor='black')
    buf.seek(0)

    st.download_button(
        label="📥 Download PNG (Dark Mode)",
        data=buf,
        file_name="nifty50_darkmode_matplotlib.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
