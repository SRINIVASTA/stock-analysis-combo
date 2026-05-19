import streamlit as st
import importlib.util
import os
import sys

# 1. FORCE PAGE CONFIG FIRST (Must be the very first Streamlit command)
st.set_page_config(page_title="SRINIVASTA Dashboard", layout="wide")

def import_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))

# Prevent internal app routing imports from throwing ModuleNotFoundError
sys.path.insert(0, os.path.join(current_dir, "Quantum-AI-Portfolio"))
sys.path.insert(0, os.path.join(current_dir, "stock_analysis"))
sys.path.insert(0, os.path.join(current_dir, "nifty50-stock-analysis"))
sys.path.insert(0, os.path.join(current_dir, "pure_math_analytics")) # Added path

# 2. CLEAR ARGV TO PREVENT SUB-APP CONFLICTS
sys.argv = [sys.argv] 

try:
    quantum_app = import_from_path("quantum_app", os.path.join(current_dir, "Quantum-AI-Portfolio", "app.py"))
    stock_app = import_from_path("stock_app", os.path.join(current_dir, "stock_analysis", "stock_analysis_app.py"))
    nifty_app = import_from_path("nifty_app", os.path.join(current_dir, "nifty50-stock-analysis", "app.py"))
    # FIXED: Added the math app to the try-except import block
    math_app = import_from_path("math_app", os.path.join(current_dir, "pure_math_analytics", "math_app.py"))
except Exception as e:
    st.error(f"Error importing apps: {e}")
    st.stop()

# Main Title Header
st.markdown(
    """
    <h1 style='text-align: center; color: #3366cc;'>
        📊 SRINIVASTA <span style='color:#00cc99;'>Combined Stock Dashboard</span>
    </h1>
    <p style='text-align: center; font-size: 14px; color: #666666;'>
        Market Disclaimer: Investments in securities are subject to market risks.
    </p>
    """,
    unsafe_allow_html=True
)

# Navigation
app_choice = st.sidebar.radio("Select an app:", [
    "Stock Analysis",
    "Quantum AI Portfolio",
    "Nifty50 Stock Analysis",
    "Pure Math Technical Analytics"
])

def run_app(module, entry_function="main"):
    # 3. PURGE SUB-APP PAGE CONFIGS TO PREVENT STREAMLIT CRASHES
    if hasattr(st, "_is_running_with_streamlit"):
        ctx = st.runtime.scriptrunner.script_run_context.get_script_run_context()
        if ctx:
            ctx.page_config_set = False 
            
    if hasattr(module, entry_function):
        func = getattr(module, entry_function)
        func()
    else:
        st.error(f"The selected app ({module.__name__}) does not have a {entry_function}() function.")

# Execute routing
if app_choice == "Stock Analysis":
    run_app(stock_app)
elif app_choice == "Quantum AI Portfolio":
    run_app(quantum_app)
elif app_choice == "Nifty50 Stock Analysis":
    run_app(nifty_app)
elif app_choice == "Pure Math Technical Analytics":
    # FIXED: Points to the imported math module and calls its specific UI function
    run_app(math_app, entry_function="run_pure_math_dashboard_ui")
