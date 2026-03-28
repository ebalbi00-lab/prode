import streamlit as st

def inject_css():
    st.markdown("""
    <style>

    /* ===== INPUT BASE (MISMO FONDO PARA TODO) ===== */

    div[data-baseweb="input"] {
        background-color: #e6f0ff !important;
        border-radius: 8px !important;
        border: 1px solid #cfe0ff !important;
        overflow: hidden !important;
    }

    /* INPUT TEXTO */
    div[data-baseweb="input"] input {
        background-color: transparent !important;
        color: #1e293b !important;
    }

    /* CONTENEDOR DERECHO (OJO) */
    div[data-baseweb="input"] > div:last-child {
        background-color: #e6f0ff !important;
    }

    /* BOTÓN DEL OJO (MISMO COLOR QUE INPUT) */
    div[data-baseweb="input"] button {
        background-color: #e6f0ff !important;
        border: none !important;
        box-shadow: none !important;
        padding: 6px !important;
    }

    /* HOVER SUAVE (MISMO ESTILO) */
    div[data-baseweb="input"] button:hover {
        background-color: #d6e6ff !important;
    }

    /* ICONO DEL OJO */
    div[data-baseweb="input"] button svg {
        color: #2f7ef7 !important;
        fill: #2f7ef7 !important;
    }

    div[data-baseweb="input"] button svg path {
        fill: #2f7ef7 !important;
    }

    /* ===== TITULO ===== */

    .login-title {
        color: #16a34a;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
    }

    .login-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)
