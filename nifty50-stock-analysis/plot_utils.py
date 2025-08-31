import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def plot_dark_mode(df):
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(15, 10))

    # Bar plot for Current Price
    sns.barplot(x=df.index, y='Current Price', data=df, color='#1f77b4', ax=ax1)
    ax1.set_ylim(0, max(df['Current Price'].max(), df['Book Value'].max()) * 1.1)

    # Annotate Book Value on bar plot
    for i, txt in enumerate(df['Book Value']):
        ax1.annotate(f"{txt:.2f}", (i, df['Book Value'].iloc[i]),
                     textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=8, rotation=90, color='white')

    # Line plot for Book Value (primary y-axis)
    ax1.plot(df.index, df['Book Value'], color='#2ca02c', linewidth=2, marker='o', linestyle='-')

    # Secondary y-axis for P/B Ratio
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['P/B Ratio'], color='#d62728', linewidth=2, linestyle='--', marker='x')
    ax2.set_ylabel('P/B Ratio', color='#d62728')
    ax2.tick_params(axis='y', labelcolor='#d62728')

    # Third y-axis for ROE (%)
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 60))  # Shift third axis to the right
    ax3.plot(df.index, df['ROE (%)'], color='#ff7f0e', linewidth=2, linestyle=':', marker='D')
    ax3.set_ylabel('ROE (%)', color='#ff7f0e')
    ax3.tick_params(axis='y', labelcolor='#ff7f0e')

    # Titles and labels
    ax1.set_title('Nifty 50 - Current Price, Book Value, P/B Ratio & ROE (%)', color='white')
    ax1.set_xlabel('Ticker', color='white')
    ax1.set_ylabel('Price / Book Value', color='white')

    # X-axis labels styling
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df.index, rotation=90, ha='right', fontsize=9, color='white')

    # Color ticks and spines
    ax1.tick_params(axis='y', colors='white')
    for spine in ax1.spines.values():
        spine.set_color('white')
    for spine in ax2.spines.values():
        spine.set_color('white')
    for spine in ax3.spines.values():
        spine.set_color('#ff7f0e')

    # Legend
    legend_elements = [
        Line2D([0], [0], color='#1f77b4', marker='s', linestyle='', label='Current Price'),
        Line2D([0], [0], color='#2ca02c', linewidth=2, marker='o', linestyle='-', label='Book Value'),
        Line2D([0], [0], color='#d62728', linewidth=2, linestyle='--', marker='x', label='P/B Ratio'),
        Line2D([0], [0], color='#ff7f0e', linewidth=2, linestyle=':', marker='D', label='ROE (%)')
    ]
    ax1.legend(handles=legend_elements, loc='upper left')

    fig.tight_layout()
    return fig
