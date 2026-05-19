import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.signal import find_peaks

def calculate_fourier_trends(close_prices, harmonics=3):
    """Applies Fourier Transform to isolate structural cyclical wavelengths."""
    n = len(close_prices)
    fft_coeffs = np.fft.fft(close_prices)
    frequencies = np.fft.fftfreq(n)
    
    # Filter high-frequency noise by zeroing out minor coefficients
    amplitudes = np.abs(fft_coeffs)
    top_indices = np.argsort(amplitudes)[::-1][:harmonics + 1]
    
    filtered_fft = np.zeros(n, dtype=complex)
    for idx in top_indices:
        filtered_fft[idx] = fft_coeffs[idx]
        
    return np.fft.ifft(filtered_fft).real

def calculate_shannon_entropy(close_prices, windows=14):
    """Measures system disorder and unpredictable price phases using Shannon Entropy."""
    returns = pd.Series(close_prices).pct_change().dropna()
    
    def rolling_entropy(window_data):
        prob_dist, _ = np.histogram(window_data, bins=10, density=True)
        prob_dist = prob_dist[prob_dist > 0]
        return -np.sum(prob_dist * np.log2(prob_dist))
        
    return returns.rolling(window=windows).apply(rolling_entropy).fillna(0).to_numpy()

def run_pure_math_dashboard_ui():
    st.header("🧮 Pure Math Technical Analytics Engine")
    st.write("Deterministic quantitative analysis bypassing machine learning biases.")
    
    # User Control Sidebar Parameters
    ticker = st.text_input("Enter Quant Ticker Symbol (e.g., ^NSEI, RELIANCE.NS):", value="^NSEI")
    col1, col2 = st.columns(2)
    with col1:
        lookback_days = st.slider("Lookback Evaluation Window (Days)", 60, 730, 365)
    with col2:
        harmonics = st.slider("Fourier Cycle Harmonics", 1, 10, 3)

    if st.button("Execute Mathematical Pass"):
        with st.spinner("Processing Matrix Transformations..."):
            # Fetch Ticker Data
            df = yf.download(ticker, period=f"{lookback_days}d")
            
            if df.empty:
                st.error("Matrix generation failure: Invalid ticker or empty dataset.")
                return

            # Clean Multi-index columns if present in newer yfinance versions
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            close_prices = df['Close'].dropna().to_numpy()
            dates = df.index[-len(close_prices):]

            # 1. Fourier Series Extrapolation
            fourier_signal = calculate_fourier_trends(close_prices, harmonics=harmonics)

            # 2. Local Peak and Trough Detection (SciPy Signals)
            peaks, _ = find_peaks(close_prices, distance=10, prominence=np.std(close_prices)*0.2)
            troughs, _ = find_peaks(-close_prices, distance=10, prominence=np.std(close_prices)*0.2)

            # 3. Structural Shannon Entropy Calculation
            entropy_series = calculate_shannon_entropy(close_prices)

            # --- Visual Layout Injection ---
            st.subheader("🌐 Frequency Domain Cycle Extrapolation (Fourier Series)")
            chart_df = pd.DataFrame({
                "Historical Close": close_prices,
                f"Fourier Model (Harmonics: {harmonics})": fourier_signal
            }, index=dates)
            st.line_chart(chart_df)

            # Metrics Panel Layout
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Mathematical Extrapolated Peaks Detected", len(peaks))
            with m2:
                st.metric("Mathematical Extrapolated Troughs Detected", len(troughs))
            with m3:
                current_entropy = entropy_series[-1] if len(entropy_series) > 0 else 0
                st.metric("System Shannon Entropy (14D)", f"{current_entropy:.4f}")

            # Statistical Breakdown
            st.subheader("📊 Dynamic Entropy Vector (Market Chaos Evaluation)")
            entropy_df = pd.DataFrame({"Shannon Entropy Value": entropy_series}, index=dates)
            st.area_chart(entropy_df)
            
            # Risk State Flag Matrix
            st.subheader("📋 Algorithmic Phase Determination")
            if current_entropy > 2.5:
                st.warning("⚠️ High Entropy Alert: Price movements are highly chaotic. Breakdown or breakout risk imminent.")
            else:
                st.success("✅ Stable Mathematical Regime: Price cycle conforms cleanly to standard wave harmonics.")

if __name__ == "__main__":
    # Fallback to allow execution as a direct standalone test script
    st.set_page_config(layout="wide")
    run_pure_math_dashboard_ui()
