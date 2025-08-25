import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import io
import pandas as pd  # needed for NaN checks

from stock_analysis import get_data  # Only importing get_data function

def main():
    st.set_page_config(layout="wide")
    st.header("📊 Welcome to the Nifty50 Stock Analysis dashboard")  # Changed to st.header (title is in combined app)

    with st.spinner("Fetching stock data..."):
        df = get_data()
    st.success("Data loaded!")

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("📈 Price vs Book Value & P/B Ratio Chart")

    # Set dark background style
    plt.style.use('dark_background')

    fig, ax1 = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#121212')  # Dark figure bg
    ax1.set_facecolor('#121212')         # Dark axes bg

    # Use bright colors for bars and lines
    sns.barplot(x='Ticker', y='Current Price', data=df, color='deepskyblue', label='Current Price', width=0.6, ax=ax1)
    ax1.set_ylim(0, max(df['Current Price'].max(), df['Book Value'].max()) * 1.1)

    for i, txt in enumerate(df['Book Value']):
        if not pd.isna(txt):
            ax1.annotate(f"{txt:.2f}", (i, txt), textcoords="offset points", xytext=(0, 10),
                         ha='center', fontsize=8, rotation=90, color='white')

    ax1.plot(range(len(df)), df['Book Value'], color='lime', linewidth=2, marker='o', linestyle='-', label='Book Value')

    ax2 = ax1.twinx()
    ax2.set_facecolor('#121212')  # Dark bg for second y-axis
    ax2.plot(range(len(df)), df['P/B Ratio'], color='orange', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ax2.set_ylabel('P/B Ratio', color='orange', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='orange', labelsize=10)

    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df.index, rotation=90, ha='right', fontsize=10)
    ax1.tick_params(colors='white', axis='x', rotation=90, labelsize=10)
    ax1.tick_params(colors='white', axis='y', labelsize=10)

    legend_elements = [
        Line2D([0], [0], color='deepskyblue', marker='s', linestyle='', label='Current Price'),
        Line2D([0], [0], color='lime', linewidth=2, marker='o', linestyle='-', label='Book Value'),
        Line2D([0], [0], color='orange', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ]
    ax1.legend(handles=legend_elements, title='Metrics', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10,
               facecolor='#121212', edgecolor='white', title_fontsize=12)

    fig.tight_layout(pad=2.0)
    st.pyplot(fig)

    # Download button - save with dark background
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf,
        file_name="nifty50_stock_analysis_dark.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
