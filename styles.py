import streamlit as st

def inject_css():
    st.markdown("""
    <style>

    /* ===== TEMA GENERAL AZUL ===== */
    .stApp {
        background: linear-gradient(180deg, #0f2a44 0%, #163a5c 60%, #1b4b75 100%);
    }

    /* ===== ESPACIO SUPERIOR ===== */
    header {
        visibility: hidden;
        height: 0 !important;
    }

    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 1rem !important;
    }

    /* ===== INPUTS ===== */
    div[data-baseweb="input"] {
        background-color: #1e4f7a !important;
        border: 1px solid #4d8fcb !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    div[data-baseweb="input"] input {
        background: transparent !important;
        color: #ffffff !important;
        caret-color: #ffffff !important;
    }

    /* PLACEHOLDER */
    div[data-baseweb="input"] input::placeholder {
        color: #dbeafe !important;
        opacity: 1 !important;
    }

    /* OJO */
    div[data-baseweb="input"] > div:last-child {
        background-color: #1e4f7a !important;
    }

    div[data-baseweb="input"] button {
        background-color: #1e4f7a !important;
        border: none !important;
        padding: 6px !important;
    }

    div[data-baseweb="input"] button:hover {
        background-color: #25639a !important;
    }

    div[data-baseweb="input"] button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    div[data-baseweb="input"] button svg path {
        fill: #ffffff !important;
    }

    /* ===== TEXTOS LOGIN ===== */
    .login-title {
        color: #22c55e;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
    }

    .login-subtitle {
        text-align: center;
        color: #ffffff !important;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 20px;
    }

    .login-footer {
        text-align: center;
        color: #cbd5f5 !important;
        font-size: 13px;
        margin-top: 10px;
    }

    /* LABELS */
    label {
        color: #e2ecff !important;
    }

    /* BOTONES */
    .stButton > button {
        background: linear-gradient(180deg, #2f7ef7 0%, #1f68d9 100%);
        color: #ffffff !important;
        border: 1px solid #6fb1ff !important;
        border-radius: 10px !important;
    }

    .stButton > button:hover {
        border-color: #9ed0ff !important;
    }

    </style>
    """, unsafe_allow_html=True)
