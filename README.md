# Quantum-AI Portfolio & Stock Analysis

# 📊 SRINIVASTA Combined Stock Dashboard
### 🚀 Created by Srinivasta

A centralized, production-ready quantitative finance dashboard built with Streamlit. This application acts as a unified hub that dynamically routes and serves multiple specialized stock market analytics projects under a single web interface.

---

## 📂 Project Framework Architecture

The directory structure relies on absolute path isolation loops. This ensures internal script files or duplicate module assets (e.g., `app.py`) can co-exist inside sub-folders without namespace collisions.

```text
stock-analysis-combo/
├── Quantum-AI-Portfolio/          # [App Option] Modern Portfolio Optimization
│   └── app.py
├── nifty50-stock-analysis/        # [App Option] Regional Index Trackers
│   ├── app.py
│   └── nifty50_data.py            # Local Nifty Index Component Data Matrix
├── stock_analysis/                # [App Option] Fundamental Summary Analysis
│   └── stock_analysis_app.py
├── pure_math_analytics/           # [App Option] Advanced Local Analytics Folder
│   └── math_app.py                # Standalone pure math and entropy interface
├── plot_utils.py                  # Global Shared Chart Generation Workspace Utilities
├── combined_app.py                # Master Web Routing Hub Application
├── requirements.txt               # Unified Project Dependency Manifest
├── LICENSE                        # Project Licensing Documentation
└── README.md                      # Infrastructure Documentation
```

---

## 🛠️ Main Feature Options & Engines

1. **Stock Analysis**  
   Processes fundamental valuation records, company metrics, summary data, and shareholder breakdown tables.

2. **Quantum AI Portfolio**  
   Calculates institutional asset weighting modeling, alpha generation scripts, and risk-adjusted return spaces.

3. **Nifty50 Stock Analysis**  
   Tracks large-cap Indian securities performance matrices and components trading across regional market indexes using local tracking scripts.

4. **Pure Math Technical Analytics**  
   An API-free technical engine running completely locally without external AI tokens or premium platform restrictions. Features include:
   * **Adaptive Lookback Scaling:** Supports queries across timelines from **1 Day up to MAX history**. It automatically streams raw 15-minute bars for micro views (`1d`/`5d`) and handles massive lifetime datasets smoothly.
   * **Shannon Entropy Engine:** Computes localized information entropy algorithms over log returns to map statistical market disorder. Includes a stage-gate alignment patch to prevent runtime layout value mismatch dataframe crashes.
   * **Momentum Wave Tracking:** Computes localized 14-day trailing RSI and MACD signal arrays entirely offline, complete with dynamic translucent overbought (>70) and oversold (<30) zone charting colors.

---

## 🚀 Installation & Local Environment Setup

### 1. Clone the Source Repository
```bash
git clone https://github.com
cd stock-analysis-combo
```

### 2. Configure a Clean Virtual Environment (Recommended)
```bash
# Create environment
python -m venv venv

# Activate environment (Windows)
.\venv\Scripts\activate

# Activate environment (Mac/Linux)
source venv/bin/activate
```

### 3. Install Required Dependencies
Install the required quantitative processing frameworks. This step includes installing `scipy` to resolve runtime import errors:
```bash
pip install -r requirements.txt
```

### 4. Launch the Local Application Server
```bash
streamlit run combined_app.py
```

---

## ☁️ Streamlit Cloud Deployment Settings

When deploying this project to **Streamlit Cloud**, configure your settings exactly as shown below:

* **Main file path:** `combined_app.py`
* **Python Version:** `3.11` or higher is recommended

### Verified Core Dependencies (`requirements.txt`)
Ensure your root requirements file contains these precise version-agnostic handles to avoid hosting container errors:
```text
streamlit
pandas
numpy
yfinance
matplotlib
scipy
```

---

## ⚖️ Market Disclaimer
Investments in securities are subject to market risks. The value and returns on your investments may fluctuate due to news, economic events, corporate disclosures, or other macroeconomic factors. All calculations output by the dashboard are intended strictly for educational simulation and backtesting purposes.
