import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Add each repo folder to sys.path
sys.path.append(os.path.join(current_dir, "nifty50-stock-analysis"))
sys.path.append(os.path.join(current_dir, "Quantum-AI-Portfolio"))
sys.path.append(os.path.join(current_dir, "stock_analysis"))

# Import main app scripts using their folder-qualified names
from nifty50_stock_analysis import app as nifty_app
from Quantum_AI_Portfolio import app as quantum_app
from stock_analysis import stock_analysis_app as stock_app

st.title("SRINIVASTA Combined Stock Analysis")

choice = st.sidebar.selectbox("Choose app", [
    "Nifty50 Stock Analysis",
    "Quantum AI Portfolio",
    "Stock Analysis"
])

if choice == "Nifty50 Stock Analysis":
    nifty_app.main()
elif choice == "Quantum AI Portfolio":
    quantum_app.main()
else:
    stock_app.main()
