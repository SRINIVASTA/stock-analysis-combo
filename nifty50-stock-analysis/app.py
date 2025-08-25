import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import io

from stock_analysis import get_data  # Only importing get_data function

def main():
    st.set_page_config(layout="wide")
    st.header("📊 Welcome to the Nifty50 Stock Analysis dashboard")

    with st.spinner("Fetching stock data..."):
        df = get_data()
    st.success("Data loaded!")

    st.subheader("📋 Data Table")
    st.dataframe(df)

    st.subheader("📈 Price vs Book Value & P/B Ratio Chart")

    # Set dark background style
    plt.style.use('dark_background')

    fig, ax1 = plt.subplots(figsize=(15, 10))

    # Reset index so 'Ticker' is a column for seaborn
    df_plot = df.reset_index()

    sns.barplot(x='Ticker', y='Current Price', data=df_plot, color='skyblue', label='Current Price', width=0.6, ax=ax1)
    ax1.set_ylim(0, max(df['Current Price'].max(), df['Book Value'].max()) * 1.1)

    # Annotate Book Value with white color
    for i, txt in enumerate(df_plot['Book Value']):
        ax1.annotate(f"{txt:.2f}", (i, txt), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, rotation=90, color='white')

    # Book Value line - lighter green for visibility
    ax1.plot(range(len(df_plot)), df_plot['Book Value'], color='limegreen', linewidth=2, marker='o', linestyle='-', label='Book Value')

    ax2 = ax1.twinx()
    ax2.plot(range(len(df_plot)), df_plot['P/B Ratio'], color='red', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ax2.set_ylabel('P/B Ratio', color='red', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='red', labelsize=10)

    ax1.set_xticks(range(len(df_plot)))
    ax1.set_xticklabels(df_plot['Ticker'], rotation=90, ha='right', fontsize=10, color='white')

    # Set axis label colors to white
    ax1.set_ylabel('Current Price / Book Value', color='white', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='white', labelsize=10)

    legend_elements = [
        Line2D([0], [0], color='skyblue', marker='s', linestyle='', label='Current Price'),
        Line2D([0], [0], color='limegreen', linewidth=2, marker='o', linestyle='-', label='Book Value'),
        Line2D([0], [0], color='red', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ]
    ax1.legend(handles=legend_elements, title='Metrics', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10, facecolor='#222222', edgecolor='white', title_fontsize=12)

    fig.tight_layout(pad=2.0)
    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf,
        file_name="nifty50_stock_analysis_dark.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
