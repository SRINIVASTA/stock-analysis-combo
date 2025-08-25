import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import io

def create_dark_mode_figure(df):
    with plt.style.context('dark_background'):
        fig, ax1 = plt.subplots(figsize=(15, 10), facecolor='black')
        ax1.set_facecolor('black')

        sns.barplot(x=df.index, y='Current Price', data=df, color='#1f77b4', ax=ax1, width=0.6)

        ax1.plot(df.index, df['Book Value'], color='#2ca02c', linewidth=2, marker='o', label='Book Value')

        for i, val in enumerate(df['Book Value']):
            ax1.annotate(f"{val:.2f}", (i, val), textcoords="offset points", xytext=(0, 10),
                         ha='center', fontsize=8, rotation=90, color='white')

        ax2 = ax1.twinx()
        ax2.plot(df.index, df['P/B Ratio'], color='#d62728', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')

        # Set tick labels to ticker names
        ax1.set_xticks(df.index)
        ax1.set_xticklabels(df['Ticker'], rotation=90, ha='right', fontsize=10, color='white')

        ax1.set_title('Nifty 50 - Current Price, Book Value, and P/B Ratio Comparison', fontsize=16, color='white')
        ax1.set_xlabel('Ticker', fontsize=12, color='white')
        ax1.set_ylabel('Current Price / Book Value', fontsize=12, color='white')
        ax2.set_ylabel('P/B Ratio', fontsize=12, color='#d62728')

        ax1.tick_params(axis='x', colors='white')
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

def main():
    st.set_page_config(layout="wide")
    st.header("📊 Nifty50 Stock Analysis Dashboard (Dark Mode)")

    # For demonstration: create a sample dataframe
    import pandas as pd
    df = pd.DataFrame({
        'Ticker': ['RELIANCE', 'TCS', 'HDFC', 'INFY', 'ICICI'],
        'Current Price': [2500, 3300, 2800, 1500, 900],
        'Book Value': [1500, 1200, 1400, 1100, 700],
        'P/B Ratio': [1.67, 2.75, 2.0, 1.36, 1.28]
    })
    df.index = range(len(df))

    fig = create_dark_mode_figure(df)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor='black')
    buf.seek(0)
    plt.close(fig)  # important!

    st.download_button(
        label="📥 Download Chart as PNG (Dark Mode)",
        data=buf,
        file_name="nifty50_darkmode_matplotlib.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
