"""
app.py — Punto de entrada principal de la aplicación.
"""
import streamlit as st

st.set_page_config(
    page_title="Prode Il Baigo - Mundial 2026",
    layout="wide",
    page_icon="⚽"
)

from styles import inject_css
from db import init_db
from screens_auth import (
    pantalla_login, pantalla_registro_datos,
    pantalla_registro_cuenta, pantalla_en_revision, pantalla_acerca,
)
from screens_usuario import pantalla_usuario
from screens_stats import pantalla_ranking, pantalla_estadisticas
from screens_admin import pantalla_admin


# ─── Inicialización ───────────────────────────────────────────────────────────

if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

if "step" not in st.session_state:
    st.session_state.step = 0
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "registro_temp" not in st.session_state:
    st.session_state.registro_temp = {}


# ─── CSS ──────────────────────────────────────────────────────────────────────

inject_css()


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
}

pantalla_fn = PANTALLAS.get(st.session_state.step)
if pantalla_fn:
    pantalla_fn()
else:
    st.error("Pantalla no encontrada.")
    st.session_state.step = 0
    st.rerun()
