import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import io

from stock_analysis import get_data  # Only importing get_data function

# st.set_page_config(layout="wide")
# st.title("📊 Nifty 50 Stock Analysis")

# This will be called by `combined_app.py` to run the app
def main():
    with st.spinner("Fetching stock data..."):
        df = get_data()
    st.success("Data loaded!")

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("📈 Price vs Book Value & P/B Ratio Chart")
    fig, ax1 = plt.subplots(figsize=(15, 10))

    sns.barplot(x='Ticker', y='Current Price', data=df, color='skyblue', label='Current Price', width=0.6, ax=ax1)
    ax1.set_ylim(0, max(df['Current Price'].max(), df['Book Value'].max()) * 1.1)

    for i, txt in enumerate(df['Book Value']):
        ax1.annotate(f"{txt:.2f}", (i, txt), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, rotation=90)

    ax1.plot(range(len(df)), df['Book Value'], color='darkgreen', linewidth=2, marker='o', linestyle='-', label='Book Value')

    ax2 = ax1.twinx()
    ax2.plot(range(len(df)), df['P/B Ratio'], color='red', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ax2.set_ylabel('P/B Ratio', color='red', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='red', labelsize=10)

    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df.index, rotation=90, ha='right', fontsize=10)

    legend_elements = [
        Line2D([0], [0], color='skyblue', marker='s', linestyle='', label='Current Price'),
        Line2D([0], [0], color='darkgreen', linewidth=2, marker='o', linestyle='-', label='Book Value'),
        Line2D([0], [0], color='red', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ]
    ax1.legend(handles=legend_elements, title='Metrics', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

    fig.tight_layout(pad=2.0)
    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf,
        file_name="nifty50_stock_analysis.png",
        mime="image/png"
    )
