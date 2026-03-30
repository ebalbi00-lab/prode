import streamlit as st

def inject_css():
    st.markdown(f"""
    <style>
    [data-testid="stTextInput"], [data-testid="stNumberInput"], [data-testid="stSelectbox"] {{
        width: 100% !important;
        min-width: 0 !important;
    }}

    [data-testid="column"] {{
        min-width: 0 !important;
    }}

    div[data-testid="stSpinner"] {{
        background: rgba(10, 20, 36, 0.88) !important;
        border-radius: 16px !important;
        padding: 10px 14px !important;
    }}
    </style>
    """, unsafe_allow_html=True)
