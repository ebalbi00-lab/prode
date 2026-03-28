import streamlit as st

def inject_css():
    st.markdown("""
    <style>

    /* ===== TEMA GENERAL AZUL ===== */
    .stApp {
        background: linear-gradient(180deg, #0f2a44 0%, #163a5c 55%, #1b4b75 100%);
    }

    /* ===== ESPACIADO GENERAL ===== */
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
        box-shadow: none !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #7fc0ff !important;
        box-shadow: 0 0 0 1px rgba(127, 192, 255, 0.35) !important;
    }

    div[data-baseweb="input"] input {
        background: transparent !important;
        color: #ffffff !important;
        caret-color: #ffffff !important;
    }

    /* placeholder: usuario / tu_usuario / etc */
    div[data-baseweb="input"] input::placeholder {
        color: #d7e8ff !important;
        opacity: 1 !important;
    }

    /* compatibilidad extra */
    input::placeholder,
    textarea::placeholder {
        color: #d7e8ff !important;
        opacity: 1 !important;
    }

    /* wrapper derecho del ojo */
    div[data-baseweb="input"] > div:last-child {
        background-color: #1e4f7a !important;
    }

    /* botón del ojo */
    div[data-baseweb="input"] button {
        background-color: #1e4f7a !important;
        border: none !important;
        box-shadow: none !important;
        padding: 6px !important;
        min-height: 100% !important;
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
        line-height: 1.1;
    }

    .login-subtitle {
        text-align: center;
        color: #e2ecff !important;
        font-size: 14px;
        font-weight: 600;
        margin-top: 0.2rem;
        margin-bottom: 1rem;
        opacity: 1 !important;
    }

    /* labels normales */
    label, .stTextInput label, .stPasswordInput label {
        color: #eef5ff !important;
    }

    /* botones generales */
    .stButton > button {
        background: linear-gradient(180deg, #2f7ef7 0%, #1f68d9 100%);
        color: #ffffff !important;
        border: 1px solid #6fb1ff !important;
        border-radius: 10px !important;
    }

    .stButton > button:hover {
        border-color: #9ed0ff !important;
        box-shadow: 0 0 0 1px rgba(158, 208, 255, 0.28) !important;
    }

    </style>
    """, unsafe_allow_html=True)
