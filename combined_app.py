import streamlit as st
import importlib.util
import sys
import os

def import_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))

# Import apps by specifying exact paths
nifty_app = import_from_path("nifty_app", os.path.join(current_dir, "nifty50-stock-analysis", "app.py"))
quantum_app = import_from_path("quantum_app", os.path.join(current_dir, "Quantum-AI-Portfolio", "app.py"))
stock_app = import_from_path("stock_app", os.path.join(current_dir, "stock_analysis", "stock_analysis_app.py"))

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
