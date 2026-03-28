import streamlit as st

def inject_css():
    st.markdown("""
    <style>

    body {
        background: linear-gradient(180deg, #07111f 0%, #0A1F44 100%);
        color: #E6F0FF;
    }

    .stTextInput > div > div {
        background: linear-gradient(180deg, #07111f 0%, #0A1F44 100%) !important;
        border: 1px solid #1E6BFF33 !important;
        border-radius: 12px !important;
    }

    .stTextInput input {
        background: transparent !important;
        color: #E6F0FF !important;
    }

    /* BOTON OJO */
    button[kind="secondary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    button[kind="secondary"]:hover,
    button[kind="secondary"]:focus,
    button[kind="secondary"]:active {
        background: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }

    button[kind="secondary"] svg {
        fill: #AFC8FF !important;
    }

    /* BOTONES + - */
    button {
        background: transparent !important;
        border: none !important;
    }

    button:hover {
        background: rgba(30,107,255,0.15) !important;
    }

    /* SPINNER / STATUS */
    [data-testid="stStatusWidget"],
    [data-testid="stSpinner"] {
        background: transparent !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stStatusWidget"] > div,
    [data-testid="stSpinner"] > div {
        background: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stStatusWidget"] p {
        margin: 0 !important;
        color: #E6F0FF !important;
    }

    [data-testid="stSpinner"] svg {
        stroke: #1E6BFF !important;
    }

    </style>
    """, unsafe_allow_html=True)
