import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Add repo folders to sys.path so imports work
sys.path.append(os.path.join(current_dir, "nifty50-stock-analysis"))
sys.path.append(os.path.join(current_dir, "Quantum-AI-Portfolio"))
sys.path.append(os.path.join(current_dir, "stock_analysis"))

# Import main app functions from each repo
# Adjust these imports if the main app files or function names differ

import app as nifty_app          # from nifty50-stock-analysis/app.py
import app as quantum_app       # from Quantum-AI-Portfolio/app.py
import stock_analysis_app as stock_app  # from stock_analysis/stock_analysis_app.py

st.title("SRINIVASTA Combined Stock Analysis")

choice = st.sidebar.selectbox("Choose app", [
    "Nifty50 Stock Analysis",
    "Quantum AI Portfolio",
    "Stock Analysis"
])

if choice == "Nifty50 Stock Analysis":
    nifty_app.main()   # Make sure nifty50-stock-analysis/app.py has main()
elif choice == "Quantum AI Portfolio":
    quantum_app.main() # Make sure Quantum-AI-Portfolio/app.py has main()
else:
    stock_app.main()   # Make sure stock_analysis/stock_analysis_app.py has main()
