import streamlit as st
import importlib.util
import os
import sys

# =====================================================================
# MODULE PATH ROUTING & IMPORTS
# =====================================================================
def import_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

current_dir = os.path.dirname(os.path.abspath(__file__))

# Add application sub-folders to core Python environment search paths
sys.path.insert(0, os.path.join(current_dir, "Quantum-AI-Portfolio"))
sys.path.insert(0, os.path.join(current_dir, "stock_analysis"))
sys.path.insert(0, os.path.join(current_dir, "nifty50-stock-analysis"))
sys.path.insert(0, os.path.join(current_dir, "pure_math_analytics"))

try:
    quantum_app = import_from_path("quantum_app", os.path.join(current_dir, "Quantum-AI-Portfolio", "app.py"))
    stock_app = import_from_path("stock_app", os.path.join(current_dir, "stock_analysis", "stock_analysis_app.py"))
    nifty_app = import_from_path("nifty_app", os.path.join(current_dir, "nifty50-stock-analysis", "app.py"))
    # Dynamically mounting the math_app as a clean, separated dependency module
    math_app = import_from_path("math_app", os.path.join(current_dir, "pure_math_analytics", "math_app.py"))
except Exception as e:
    st.error(f"Error importing infrastructure sub-apps: {e}")
    st.stop()

# =====================================================================
# RENDER VISUAL BRAND HEADERS
# =====================================================================
st.markdown(
    """
    <h1 style='text-align: center; color: #3366cc;'>
        📊 SRINIVASTA <span style='color:#00cc99;'>Combined Stock Dashboard</span>
    </h1>
    <p style='text-align: center; font-size: 14px; color: #666666;'>
        Market Disclaimer: Investments in securities are subject to market risks. The value and returns on your investments may fluctuate due to news, economic events, or other market factors.
    </p>
    """,
    unsafe_allow_html=True
)

# Sidebar application choice options
app_choice = st.sidebar.radio("Select an app:", [
    "Stock Analysis",
    "Quantum AI Portfolio",
    "Nifty50 Stock Analysis",
    "Pure Math Technical Analytics"
])

def run_app(module, entry_function="main"):
    if hasattr(module, entry_function):
        func = getattr(module, entry_function)
        func()
    else:
        st.error(f"The selected module does not have a '{entry_function}()' execution block.")

# =====================================================================
# GLOBAL TRAFFIC ROUTER TRIGGER MATCHES
# =====================================================================
if app_choice == "Stock Analysis":
    run_app(stock_app, entry_function="main")
elif app_choice == "Quantum AI Portfolio":
    run_app(quantum_app, entry_function="main")
elif app_choice == "Nifty50 Stock Analysis":
    run_app(nifty_app, entry_function="main")
elif app_choice == "Pure Math Technical Analytics":
    # Explicitly routes to the standalone function isolated inside math_app.py
    run_app(math_app, entry_function="run_pure_math_dashboard_ui")
