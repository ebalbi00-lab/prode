import streamlit as st

def inject_css():
    st.markdown("""
    <style>

    /* ===== THEME GENERAL AZUL ===== */

    .stApp {
        background: linear-gradient(180deg, #0f2a44 0%, #163a5c 100%);
    }

    /* CONTENEDOR PRINCIPAL */
    .block-container {
        padding-top: 1rem !important;  /* reduce espacio superior */
        padding-bottom: 1rem !important;
    }

    /* ELIMINAR ESPACIO EXTRA ARRIBA */
    header {
        visibility: hidden;
        height: 0px;
    }

    /* ===== INPUT PASSWORD (OJO INTEGRADO) ===== */

    div[data-baseweb="input"] {
        background-color: #1e4f7a !important;
        border-radius: 8px !important;
        border: 1px solid #2f7ef7 !important;
        overflow: hidden !important;
    }

    div[data-baseweb="input"] input {
        background-color: transparent !important;
        color: #ffffff !important;
    }

    div[data-baseweb="input"] > div:last-child {
        background-color: #1e4f7a !important;
    }

    div[data-baseweb="input"] button {
        background-color: #1e4f7a !important;
        border: none !important;
        box-shadow: none !important;
        padding: 6px !important;
    }

    div[data-baseweb="input"] button:hover {
        background-color: #2f7ef7 !important;
    }

    div[data-baseweb="input"] button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    div[data-baseweb="input"] button svg path {
        fill: #ffffff !important;
    }

    /* ===== TITULO ===== */

    .login-title {
        color: #22c55e;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
    }

    .login-subtitle {
        text-align: center;
        color: #cbd5f5;
        font-size: 14px;
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)
