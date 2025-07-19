import streamlit as st
import importlib.util
import os
import sys

def import_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))

# Import the main app modules from their respective folders
nifty_app = import_from_path("nifty_app", os.path.join(current_dir, "nifty50-stock-analysis", "app.py"))
quantum_app = import_from_path("quantum_app", os.path.join(current_dir, "Quantum-AI-Portfolio", "app.py"))
stock_app = import_from_path("stock_app", os.path.join(current_dir, "stock_analysis", "stock_analysis_app.py"))

st.title("📊 SRINIVASTA Combined Stock Dashboard")

# Sidebar menu for selecting apps
app_choice = st.sidebar.radio("Select an app:", [
    "Nifty50 Stock Analysis",
    "Quantum AI Portfolio",
    "Stock Analysis"
])

# Run the selected app's main function
if app_choice == "Nifty50 Stock Analysis":
    nifty_app.main()
elif app_choice == "Quantum AI Portfolio":
    quantum_app.main()
elif app_choice == "Stock Analysis":
    stock_app.main()
