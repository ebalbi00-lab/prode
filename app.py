"""
app.py — Punto de entrada principal.
El tema oscuro/claro se guarda en ?t= (query_params) — persiste entre recargas.
"""
import streamlit as st

st.set_page_config(
    page_title="Prode Il Baigo - Mundial 2026",
    layout="wide",
    page_icon="⚽"
)

from styles import inject_css, render_tema_boton
from db import init_db
from screens_auth import (
    pantalla_login, pantalla_registro_datos,
    pantalla_registro_cuenta, pantalla_en_revision, pantalla_acerca,
)
from screens_usuario import pantalla_usuario
from screens_stats import pantalla_ranking, pantalla_estadisticas, pantalla_estadisticas_torneo
from screens_admin import pantalla_admin

# ─── Inicialización ───────────────────────────────────────────────────────────

if "db_initialized" not in st.session_state:
    try:
        init_db()
        st.session_state["db_initialized"] = True
    except Exception as e:
        st.markdown("""
        <div style="text-align:center; padding:4rem 1rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">⚠️</div>
            <div style="font-family:Bebas Neue,sans-serif; font-size:2rem; letter-spacing:3px; color:#ff5566; margin-bottom:0.8rem;">
                Error de conexión</div>
            <div style="color:#8898bb; font-size:0.95rem; line-height:1.75; max-width:400px; margin:0 auto;">
                No se pudo conectar a la base de datos.<br>
                Por favor intentá recargar la página en unos segundos.<br><br>
                Si el problema persiste, contactá al administrador.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Reintentar"):
            st.rerun()
        st.stop()

if "step" not in st.session_state:
    st.session_state.step = 0
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "registro_temp" not in st.session_state:
    st.session_state.registro_temp = {}

# ─── Tema + CSS ───────────────────────────────────────────────────────────────

inject_css()          # CSS generado según tema actual en query_params
render_tema_boton()   # Botón ☀️/🌙 arriba a la derecha

# ─── Router ───────────────────────────────────────────────────────────────────

PANTALLAS = {
    0:  pantalla_login,
    1:  pantalla_registro_datos,
    2:  pantalla_registro_cuenta,
    4:  pantalla_en_revision,
    5:  pantalla_usuario,
    6:  pantalla_ranking,
    9:  pantalla_admin,
    10: pantalla_acerca,
    12: pantalla_estadisticas,
    13: pantalla_estadisticas_torneo,
}

pantalla_fn = PANTALLAS.get(st.session_state.step)
if pantalla_fn:
    pantalla_fn()
else:
    st.session_state.step = 0
    st.rerun()