import re
import textwrap

import streamlit as st

st.set_page_config(
    page_title="Prode Il Baigo",
    layout="wide",
    page_icon="⚽",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<link rel="icon" href="static/favicon.png">
<link rel="apple-touch-icon" href="static/favicon.png">
<meta name="apple-mobile-web-app-title" content="Prode Il Baigo">
<meta name="application-name" content="Prode Il Baigo">
<meta name="theme-color" content="#07111f">
<meta name="color-scheme" content="dark">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
""",
    unsafe_allow_html=True,
)

_original_markdown = st.markdown
_HTML_TAG_RE = re.compile(r"<\s*(div|span|table|img|input|br|p|section|article|header|footer|small|strong|em|ul|ol|li|h[1-6])\b", re.IGNORECASE)

def _safe_markdown(body, *args, **kwargs):
    if isinstance(body, str) and _HTML_TAG_RE.search(body):
        body = textwrap.dedent(body).strip()
        kwargs.setdefault("unsafe_allow_html", True)
    return _original_markdown(body, *args, **kwargs)

st.markdown = _safe_markdown

from styles import inject_css
from db import init_db
from screens_auth import (
    pantalla_login, pantalla_registro_datos,
    pantalla_registro_cuenta, pantalla_en_revision, pantalla_acerca,
)
from screens_usuario import pantalla_usuario
from screens_stats import pantalla_ranking, pantalla_estadisticas, pantalla_estadisticas_torneo
from screens_admin import pantalla_admin

if "db_initialized" not in st.session_state:
    try:
        init_db()
        st.session_state["db_initialized"] = True
    except Exception:
        st.markdown(
            """
            <div class="review-shell" style="max-width:560px;margin:3rem auto 0 auto;">
                <div class="review-shell__icon">⚠️</div>
                <div class="hero-title" style="font-size:2.2rem;">Error de conexión</div>
                <div class="hero-subtitle" style="max-width:420px;">
                    No se pudo conectar a la base de datos. Recargá la página.
                    Si sigue fallando, contactá al administrador.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🔄 Reintentar", use_container_width=True):
            st.rerun()
        st.stop()

if "step" not in st.session_state:
    st.session_state.step = 0
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "registro_temp" not in st.session_state:
    st.session_state.registro_temp = {}

inject_css()

PANTALLAS = {
    0: pantalla_login,
    1: pantalla_registro_datos,
    2: pantalla_registro_cuenta,
    4: pantalla_en_revision,
    5: pantalla_usuario,
    6: pantalla_ranking,
    9: pantalla_admin,
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
