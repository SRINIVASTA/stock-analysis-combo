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

    # Current Price bars in light blue (similar to Views line color)
    sns.barplot(x='Ticker', y='Current Price', data=df, color='#8ecae6', label='Current Price', width=0.6, ax=ax1)
    ax1.set_ylim(0, max(df['Current Price'].max(), df['Book Value'].max()) * 1.1)

    # Book Value line in cyan (#219ebc)
    ax1.plot(range(len(df)), df['Book Value'], color='#219ebc', linewidth=2, marker='o', linestyle='-', label='Book Value')

    # Annotate Book Value with white color
    for i, txt in enumerate(df['Book Value']):
        ax1.annotate(f"{txt:.2f}", (i, txt), textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=8, rotation=90, color='white')

    # P/B Ratio on secondary axis in coral (#fb8500)
    ax2 = ax1.twinx()
    ax2.plot(range(len(df)), df['P/B Ratio'], color='#fb8500', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ax2.set_ylabel('P/B Ratio', color='#fb8500', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='#fb8500', labelsize=10)

    # X-axis labels in white
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df.index, rotation=90, ha='right', fontsize=10, color='white')

    # Y-axis label and ticks in white for primary axis
    ax1.set_ylabel('Current Price / Book Value', color='white', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='white', labelsize=10)

    # Faint grid lines for better readability
    ax1.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.2)

    # Legend with dark background and white text
    legend_elements = [
        Line2D([0], [0], color='#8ecae6', marker='s', linestyle='', label='Current Price'),
        Line2D([0], [0], color='#219ebc', linewidth=2, marker='o', linestyle='-', label='Book Value'),
        Line2D([0], [0], color='#fb8500', linewidth=2, linestyle='--', marker='x', label='P/B Ratio')
    ]
    ax1.legend(handles=legend_elements, title='Metrics', loc='upper left', bbox_to_anchor=(1.05, 1),
               fontsize=10, facecolor='#000000', edgecolor='white', title_fontsize=12)

    fig.tight_layout(pad=2.0)
    st.pyplot(fig)

    # Download button for the plot as PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf,
        file_name="nifty50_stock_analysis_dark_colored.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
