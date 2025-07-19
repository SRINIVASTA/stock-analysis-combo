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

# Add folders to sys.path if their modules need internal imports
sys.path.insert(0, os.path.join(current_dir, "Quantum-AI-Portfolio"))
sys.path.insert(0, os.path.join(current_dir, "stock_analysis"))
sys.path.insert(0, os.path.join(current_dir, "nifty50-stock-analysis"))

try:
    quantum_app = import_from_path("quantum_app", os.path.join(current_dir, "Quantum-AI-Portfolio", "app.py"))
    stock_app = import_from_path("stock_app", os.path.join(current_dir, "stock_analysis", "stock_analysis_app.py"))
    nifty_app = import_from_path("nifty_app", os.path.join(current_dir, "nifty50-stock-analysis", "app.py"))
except Exception as e:
    st.error(f"Error importing apps: {e}")
    st.stop()

st.title("📊 SRINIVASTA Combined Stock Dashboard")

app_choice = st.sidebar.radio("Select an app:", [
    "Stock Analysis",              # Should call stock_app
    "Quantum AI Portfolio",        # Should call quantum_app
    "Nifty50 Stock Analysis"       # Should call nifty_app
])

def run_app(module):
    if hasattr(module, "main"):
        module.main()
    else:
        st.error(f"The selected app ({module.__name__}) does not have a main() function.")

# Correct module-to-choice mapping
if app_choice == "Stock Analysis":
    run_app(stock_app)
elif app_choice == "Quantum AI Portfolio":
    run_app(quantum_app)
elif app_choice == "Nifty50 Stock Analysis":
    run_app(nifty_app)
