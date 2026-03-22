import streamlit as st
import pandas as pd
import datetime
import hashlib
import os
import re
import psycopg2
import psycopg2.extras
import psycopg2.pool
from contextlib import contextmanager

st.set_page_config(page_title="Prode Il Baigo - Mundial 2026", layout="wide", page_icon="⚽")


# -----------------------
# ESTILOS GLOBALES
# -----------------------
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        background: #0a0a0f;
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(0,200,80,0.07) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(0,120,255,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 60% 80%, rgba(200,50,50,0.05) 0%, transparent 50%);
        color: #e8e8f0;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; max-width: 900px !important; }

    h1 {
        font-family: 'Bebas Neue', sans-serif !important; font-size: 3.2rem !important;
        letter-spacing: 3px !important;
        background: linear-gradient(135deg, #00c850, #00ff88) !important;
        -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
        background-clip: text !important; margin-bottom: 0.2rem !important; line-height: 1.1 !important;
    }
    h2 { font-family: 'Bebas Neue', sans-serif !important; font-size: 1.8rem !important; letter-spacing: 2px !important; color: #e8e8f0 !important; }
    h3 { font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; color: #a0a0b8 !important; font-size: 0.85rem !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; }

    .stTextInput > div > div > input, .stPasswordInput > div > div > input {
        background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important; color: #ffffff !important; padding: 0.6rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important; transition: all 0.2s ease !important;
        -webkit-text-fill-color: #ffffff !important; caret-color: #00c850 !important;
    }
    .stTextInput > div > div > input:focus, .stPasswordInput > div > div > input:focus {
        border-color: #00c850 !important; background: #1a1a2e !important;
        box-shadow: 0 0 0 3px rgba(0,200,80,0.15) !important; -webkit-text-fill-color: #ffffff !important;
    }
    .stTextInput > div > div > input::placeholder, .stPasswordInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.3) !important; -webkit-text-fill-color: rgba(255,255,255,0.3) !important;
    }
    .stTextInput label, .stPasswordInput label, .stSelectbox label, .stNumberInput label,
    .stFileUploader label, .stRadio label, .stDateInput label {
        color: #a0a0b8 !important; font-size: 0.82rem !important; font-weight: 500 !important;
        text-transform: uppercase !important; letter-spacing: 1px !important;
    }
    .stSelectbox > div > div { background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 10px !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    .stSelectbox > div > div > div { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    .stNumberInput > div > div > input {
        background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
        caret-color: #00c850 !important; text-align: center !important;
        font-size: 1.4rem !important; font-weight: 700 !important;
        font-family: 'Bebas Neue', sans-serif !important;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #00c850 !important;
        box-shadow: 0 0 0 3px rgba(0,200,80,0.15) !important;
    }
    .stButton > button {
        background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important; color: #e8e8f0 !important; font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important; font-size: 0.9rem !important; padding: 0.55rem 1.4rem !important;
        transition: all 0.2s ease !important; letter-spacing: 0.5px !important;
    }
    .stButton > button:hover { background: rgba(255,255,255,0.1) !important; border-color: rgba(255,255,255,0.25) !important; transform: translateY(-1px) !important; box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important; }
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #00c850, #00a040) !important; border: none !important; color: #fff !important; font-weight: 700 !important; box-shadow: 0 4px 15px rgba(0,200,80,0.3) !important; }
    .stButton > button[kind="primary"]:hover { background: linear-gradient(135deg, #00e060, #00c850) !important; box-shadow: 0 6px 25px rgba(0,200,80,0.45) !important; transform: translateY(-2px) !important; }

    .stFormSubmitButton > button { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; color: #e8e8f0 !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; transition: all 0.2s ease !important; }
    .stFormSubmitButton > button:hover { background: rgba(255,255,255,0.1) !important; transform: translateY(-1px) !important; }
    .stFormSubmitButton > button[kind="primary"] { background: linear-gradient(135deg, #00c850, #00a040) !important; border: none !important; color: #fff !important; font-weight: 700 !important; box-shadow: 0 4px 15px rgba(0,200,80,0.3) !important; }
    .stFormSubmitButton > button[kind="primary"]:hover { background: linear-gradient(135deg, #00e060, #00c850) !important; box-shadow: 0 6px 25px rgba(0,200,80,0.45) !important; transform: translateY(-2px) !important; }

    .stSuccess { background: rgba(0,200,80,0.1) !important; border: 1px solid rgba(0,200,80,0.3) !important; border-radius: 10px !important; color: #00e870 !important; }
    .stError { background: rgba(255,60,60,0.1) !important; border: 1px solid rgba(255,60,60,0.3) !important; border-radius: 10px !important; color: #ff6b6b !important; }
    .stWarning { background: rgba(255,180,0,0.1) !important; border: 1px solid rgba(255,180,0,0.3) !important; border-radius: 10px !important; color: #ffcc44 !important; }
    .stInfo { background: rgba(0,120,255,0.08) !important; border: 1px solid rgba(0,120,255,0.25) !important; border-radius: 10px !important; color: #66aaff !important; }

    [data-testid="stMetric"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 14px !important; padding: 1rem 1.2rem !important; transition: all 0.2s ease !important; }
    [data-testid="stMetric"]:hover { border-color: rgba(0,200,80,0.3) !important; background: rgba(0,200,80,0.04) !important; }
    [data-testid="stMetricLabel"] { color: #a0a0b8 !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
    [data-testid="stMetricValue"] { color: #00e870 !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 2.2rem !important; letter-spacing: 1px !important; }

    [data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.08) !important; }
    .dvn-scroller { background: #0f0f1a !important; }

    .stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03) !important; border-radius: 12px !important; padding: 4px !important; gap: 4px !important; border: 1px solid rgba(255,255,255,0.06) !important; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 8px !important; color: #a0a0b8 !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.8rem !important; padding: 0.4rem 0.8rem !important; transition: all 0.2s ease !important; }
    .stTabs [aria-selected="true"] { background: rgba(0,200,80,0.15) !important; color: #00e870 !important; border: 1px solid rgba(0,200,80,0.25) !important; }

    .stRadio [data-testid="stMarkdownContainer"] p { color: #e8e8f0 !important; font-weight: 500 !important; }
    .stRadio > div { background: rgba(255,255,255,0.03) !important; border-radius: 12px !important; padding: 0.5rem 1rem !important; border: 1px solid rgba(255,255,255,0.07) !important; }
    .stCheckbox, [data-testid="stToggle"] { color: #e8e8f0 !important; }

    .streamlit-expanderHeader { background: rgba(255,255,255,0.03) !important; border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.08) !important; color: #e8e8f0 !important; font-weight: 600 !important; }
    .streamlit-expanderContent { background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.06) !important; border-top: none !important; border-radius: 0 0 10px 10px !important; }

    hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.5rem 0 !important; }
    .stSlider [data-baseweb="slider"] { padding: 0.5rem 0 !important; }
    .stCaption, caption { color: #606075 !important; font-size: 0.78rem !important; }
    .stMarkdown p { color: #c8c8d8 !important; line-height: 1.7 !important; }
    .stMarkdown strong { color: #e8e8f0 !important; }

    [data-testid="stFileUploader"] { background: rgba(255,255,255,0.03) !important; border: 1.5px dashed rgba(255,255,255,0.15) !important; border-radius: 12px !important; transition: all 0.2s !important; }
    [data-testid="stFileUploader"]:hover { border-color: rgba(0,200,80,0.4) !important; background: rgba(0,200,80,0.03) !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3a3a4a; }

    [data-testid="stForm"] { background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 16px !important; padding: 1.5rem !important; }

    @media (max-width: 768px) {
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; padding-top: 1rem !important; }
        h1 { font-size: 2.2rem !important; letter-spacing: 2px !important; }
        h2 { font-size: 1.4rem !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.7rem !important; padding: 0.3rem 0.4rem !important; }
        .stTabs [data-baseweb="tab-list"] { flex-wrap: wrap !important; gap: 2px !important; }
        .stTextInput > div > div > input, .stPasswordInput > div > div > input { font-size: 16px !important; padding: 0.75rem 1rem !important; }
        .stButton > button, .stFormSubmitButton > button { padding: 0.75rem 1rem !important; font-size: 0.95rem !important; width: 100% !important; }
        [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
        .stRadio > div > div { flex-wrap: wrap !important; gap: 4px !important; }
        .stNumberInput > div > div > input { font-size: 1.6rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------
# BASE DE DATOS PostgreSQL
# -----------------------

def get_db_url():
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        return os.environ.get("DATABASE_URL", "")

@st.cache_resource
def get_connection_pool():
    url = get_db_url()
    if not url:
        st.error("⚠️ No se encontró DATABASE_URL. Configurá los secrets en Streamlit Cloud o la variable de entorno local.")
        st.stop()
    return psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=url,
        cursor_factory=psycopg2.extras.RealDictCursor
    )

@contextmanager
def get_db():
    pool = get_connection_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)

@st.cache_resource
def init_tablas():
    """Crea las tablas e inserta datos fijos. Se cachea — corre una sola vez."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            clave TEXT NOT NULL,
            nombre TEXT,
            nacimiento TEXT,
            localidad TEXT,
            celular TEXT,
            mail TEXT,
            puntos INTEGER DEFAULT 0,
            goles INTEGER DEFAULT 0,
            consumo INTEGER DEFAULT 0,
            es_admin INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS pendientes (
            id SERIAL PRIMARY KEY,
            username TEXT,
            clave TEXT,
            nombre TEXT,
            nacimiento TEXT,
            localidad TEXT,
            celular TEXT,
            mail TEXT,
            comprobante TEXT
        );
        CREATE TABLE IF NOT EXISTS fases (
            nombre TEXT PRIMARY KEY,
            habilitada INTEGER DEFAULT 0,
            orden INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS partidos (
            id SERIAL PRIMARY KEY,
            fase TEXT,
            idx INTEGER,
            local TEXT,
            visita TEXT,
            fecha TEXT,
            hora TEXT,
            UNIQUE(fase, idx)
        );
        CREATE TABLE IF NOT EXISTS resultados (
            fase TEXT,
            partido_idx INTEGER,
            goles_local INTEGER DEFAULT 0,
            goles_visita INTEGER DEFAULT 0,
            PRIMARY KEY (fase, partido_idx)
        );
        CREATE TABLE IF NOT EXISTS prodes (
            username TEXT,
            fase TEXT,
            partido_idx INTEGER,
            goles_local INTEGER DEFAULT 0,
            goles_visita INTEGER DEFAULT 0,
            confirmado INTEGER DEFAULT 0,
            PRIMARY KEY (username, fase, partido_idx)
        );
        CREATE TABLE IF NOT EXISTS config (
            clave TEXT PRIMARY KEY,
            valor TEXT
        );
        CREATE TABLE IF NOT EXISTS consumo_log (
            id SERIAL PRIMARY KEY,
            username TEXT,
            puntos INTEGER,
            descripcion TEXT,
            fecha TEXT
        );
        CREATE TABLE IF NOT EXISTS especiales (
            username TEXT,
            categoria TEXT,
            eleccion TEXT,
            confirmado INTEGER DEFAULT 0,
            PRIMARY KEY (username, categoria)
        );
        CREATE TABLE IF NOT EXISTS especiales_resultados (
            categoria TEXT PRIMARY KEY,
            resultado TEXT
        );

        """)
        for i, f in enumerate(["Grupos","Dieciseisavos","Octavos","Cuartos","Semifinal","Final"]):
            cur.execute(
                "INSERT INTO fases (nombre, habilitada, orden) VALUES (%s, %s, %s) ON CONFLICT (nombre) DO NOTHING",
                (f, 1 if f == "Grupos" else 0, i)
            )

def init_db():
    """Crea tablas (cacheado) y garantiza que admin y prueba siempre existan."""
    init_tablas()
    admin_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
    try:
        admin_pass = st.secrets["ADMIN_PASSWORD"]
    except Exception:
        pass
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (username, clave, nombre, es_admin) VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING",
            ("admin", hash_clave(admin_pass), "Admin", 1)
        )
        cur.execute(
            "INSERT INTO usuarios (username, clave, nombre, es_admin) VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING",
            ("prueba", hash_clave("1234"), "Prueba", 0)
        )

def hash_clave(clave: str) -> str:
    return hashlib.sha256(clave.encode()).hexdigest()

def db_get_config(clave, default=None):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT valor FROM config WHERE clave=%s", (clave,))
        row = cur.fetchone()
        return row["valor"] if row else default

def db_set_config(clave, valor):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO config (clave, valor) VALUES (%s, %s) ON CONFLICT (clave) DO UPDATE SET valor=EXCLUDED.valor",
            (clave, valor)
        )

def db_registro_abierto():
    return db_get_config("registro_abierto", "1") == "1"

def db_get_consumo_log(username=None):
    with get_db() as conn:
        cur = conn.cursor()
        if username:
            cur.execute("SELECT * FROM consumo_log WHERE username=%s ORDER BY id DESC", (username,))
        else:
            cur.execute("SELECT * FROM consumo_log ORDER BY id DESC")
        return [dict(r) for r in cur.fetchall()]

def db_get_usuario(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
        row = cur.fetchone()
        return dict(row) if row else None

@st.cache_data(ttl=30)
def db_get_fases():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM fases ORDER BY orden")
        return {r["nombre"]: bool(r["habilitada"]) for r in cur.fetchall()}

def db_toggle_fase(nombre, valor):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE fases SET habilitada=%s WHERE nombre=%s", (1 if valor else 0, nombre))
    st.cache_data.clear()

@st.cache_data(ttl=60)
def db_get_partidos(fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM partidos WHERE fase=%s ORDER BY idx", (fase,))
        return [dict(r) for r in cur.fetchall()]

def db_guardar_partido(fase, idx, local, visita, fecha="", hora=""):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO partidos (fase, idx, local, visita, fecha, hora) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (fase, idx) DO UPDATE SET
            local=EXCLUDED.local, visita=EXCLUDED.visita,
            fecha=EXCLUDED.fecha, hora=EXCLUDED.hora
        """, (fase, idx, local, visita, fecha, hora))
    st.cache_data.clear()

def db_get_resultado(fase, idx):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resultados WHERE fase=%s AND partido_idx=%s", (fase, idx))
        row = cur.fetchone()
        return (row["goles_local"], row["goles_visita"]) if row else (0, 0)

def db_guardar_resultado(fase, idx, gl, gv):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO resultados (fase, partido_idx, goles_local, goles_visita) VALUES (%s, %s, %s, %s)
            ON CONFLICT (fase, partido_idx) DO UPDATE SET
            goles_local=EXCLUDED.goles_local, goles_visita=EXCLUDED.goles_visita
        """, (fase, idx, gl, gv))
    st.cache_data.clear()

def db_get_prode(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM prodes WHERE username=%s AND fase=%s", (username, fase))
        rows = cur.fetchall()
        if not rows:
            return {"pred": {}, "confirmado": False}
        confirmado = bool(rows[0]["confirmado"])
        pred = {r["partido_idx"]: (r["goles_local"], r["goles_visita"]) for r in rows}
        return {"pred": pred, "confirmado": confirmado}

def db_guardar_pred(username, fase, idx, gl, gv):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO prodes (username, fase, partido_idx, goles_local, goles_visita, confirmado)
            VALUES (%s, %s, %s, %s, %s, 0)
            ON CONFLICT (username, fase, partido_idx) DO UPDATE SET
            goles_local=EXCLUDED.goles_local, goles_visita=EXCLUDED.goles_visita
        """, (username, fase, idx, gl, gv))

def db_confirmar_prode(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE prodes SET confirmado=1 WHERE username=%s AND fase=%s", (username, fase))
        cur.execute("""
            INSERT INTO prodes (username, fase, partido_idx, goles_local, goles_visita, confirmado)
            VALUES (%s, %s, -1, 0, 0, 1)
            ON CONFLICT (username, fase, partido_idx) DO NOTHING
        """, (username, fase))

def db_fase_confirmada(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT confirmado FROM prodes WHERE username=%s AND fase=%s AND confirmado=1 LIMIT 1",
            (username, fase)
        )
        return bool(cur.fetchone())

def db_get_pendientes():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pendientes ORDER BY id")
        return [dict(r) for r in cur.fetchall()]

def db_agregar_pendiente(data):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pendientes (username, clave, nombre, nacimiento, localidad, celular, mail, comprobante)
            VALUES (%(username)s, %(clave)s, %(nombre)s, %(nacimiento)s, %(localidad)s, %(celular)s, %(mail)s, %(comprobante)s)
        """, data)

def db_aprobar_pendiente(pid):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pendientes WHERE id=%s", (pid,))
        row = cur.fetchone()
        if not row:
            return
        cur.execute("""
            INSERT INTO usuarios (username, clave, nombre, nacimiento, localidad, celular, mail)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, (row["username"], row["clave"], row["nombre"], row["nacimiento"],
              row["localidad"], row["celular"], row["mail"]))
        cur.execute("DELETE FROM pendientes WHERE id=%s", (pid,))

def db_rechazar_pendiente(pid):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM pendientes WHERE id=%s", (pid,))

@st.cache_data(ttl=15)
def db_get_todos_usuarios():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE es_admin=0")
        return [dict(r) for r in cur.fetchall()]

def db_reset_clave(username, nueva_clave):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET clave=%s WHERE username=%s", (hash_clave(nueva_clave), username))

def db_borrar_usuario(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE username=%s", (username,))
        cur.execute("DELETE FROM prodes WHERE username=%s", (username,))

def db_resetear_todos_puntajes():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET puntos=0, goles=0, consumo=0 WHERE es_admin=0")
        cur.execute("DELETE FROM prodes")
        cur.execute("DELETE FROM resultados")
        cur.execute("DELETE FROM consumo_log")

def db_sumar_consumo(username, puntos, descripcion=""):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET consumo=consumo+%s WHERE username=%s", (puntos, username))
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cur.execute(
            "INSERT INTO consumo_log (username, puntos, descripcion, fecha) VALUES (%s, %s, %s, %s)",
            (username, puntos, descripcion, fecha)
        )

def db_eliminar_consumo_log(log_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM consumo_log WHERE id=%s", (log_id,))
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE usuarios SET consumo=GREATEST(0, consumo-%s) WHERE username=%s",
                (row["puntos"], row["username"])
            )
            cur.execute("DELETE FROM consumo_log WHERE id=%s", (log_id,))

@st.cache_data(ttl=15)
def db_get_resultado_completo(fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resultados WHERE fase=%s", (fase,))
        return {r["partido_idx"]: (r["goles_local"], r["goles_visita"]) for r in cur.fetchall()}

def db_calcular_puntos():
    # Una sola query SQL — evita cientos de roundtrips a Supabase
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            WITH mult AS (
                SELECT unnest(ARRAY['Grupos','Dieciseisavos','Octavos','Cuartos','Semifinal','Final']) AS fase,
                       unnest(ARRAY[1,2,3,4,5,6]) AS m
            ),
            calc AS (
                SELECT
                    p.username,
                    SUM(CASE
                        WHEN (p.goles_local > p.goles_visita AND r.goles_local > r.goles_visita)
                          OR (p.goles_local < p.goles_visita AND r.goles_local < r.goles_visita)
                          OR (p.goles_local = p.goles_visita AND r.goles_local = r.goles_visita)
                        THEN x.m ELSE 0
                    END) AS puntos,
                    SUM(CASE
                        WHEN p.goles_local = r.goles_local AND p.goles_visita = r.goles_visita
                        THEN x.m * 3 ELSE 0
                    END) AS goles
                FROM prodes p
                JOIN resultados r ON r.fase = p.fase AND r.partido_idx = p.partido_idx
                JOIN mult x ON x.fase = p.fase
                WHERE p.confirmado = 1 AND p.partido_idx >= 0
                GROUP BY p.username
            )
            UPDATE usuarios u
            SET puntos = COALESCE(c.puntos, 0),
                goles  = COALESCE(c.goles, 0)
            FROM (
                SELECT u2.username,
                       COALESCE(c2.puntos, 0) AS puntos,
                       COALESCE(c2.goles, 0)  AS goles
                FROM usuarios u2
                LEFT JOIN calc c2 ON c2.username = u2.username
                WHERE u2.es_admin = 0
            ) c
            WHERE u.username = c.username
        """)
    st.cache_data.clear()


# -----------------------
# LISTAS DE JUGADORES
# -----------------------
JUGADORES_MUNDIALISTAS = sorted([
    "Lionel Messi", "Ángel Di María", "Lautaro Martínez", "Julián Álvarez",
    "Rodrigo De Paul", "Alexis Mac Allister", "Cristian Romero", "Nicolás Otamendi",
    "Neymar Jr", "Vinicius Jr", "Rodrygo", "Raphinha", "Bruno Guimarães",
    "Kylian Mbappé", "Antoine Griezmann", "Ousmane Dembélé", "Aurélien Tchouaméni",
    "Erling Haaland", "Martin Ødegaard", "Alexander Isak",
    "Harry Kane", "Jude Bellingham", "Phil Foden", "Bukayo Saka", "Marcus Rashford",
    "Cristiano Ronaldo", "Bruno Fernandes", "Bernardo Silva", "Rúben Dias",
    "Pedri", "Lamine Yamal", "Álvaro Morata", "Rodri", "Gavi",
    "Leroy Sané", "Florian Wirtz", "Jamal Musiala", "Kai Havertz", "Thomas Müller",
    "Romelu Lukaku", "Kevin De Bruyne", "Dodi Lukebakio",
    "Ciro Immobile", "Federico Chiesa", "Nicolo Barella",
    "Memphis Depay", "Xavi Simons", "Cody Gakpo",
    "Luka Modric", "Ivan Perisic", "Mateo Kovacic",
    "Granit Xhaka", "Xherdan Shaqiri", "Breel Embolo",
    "Robert Lewandowski", "Piotr Zielinski",
    "Mohamed Salah", "Mostafa Mohamed",
    "Sadio Mané", "Ismaïla Sarr",
    "Riyad Mahrez", "Islam Slimani",
    "Hakim Ziyech", "Youssef En-Nesyri", "Achraf Hakimi",
    "Victor Osimhen", "Kelechi Iheanacho",
    "André Ayew", "Jordan Ayew",
    "Sébastien Haller", "Franck Kessié",
    "Hiroki Sakai", "Takumi Minamino", "Daichi Kamada",
    "Son Heung-min", "Hwang Hee-chan",
    "Mathew Leckie", "Martin Boyle",
    "Christian Pulisic", "Weston McKennie", "Tyler Adams", "Tim Weah",
    "Alphonso Davies", "Jonathan David", "Cyle Larin",
    "Hirving Lozano", "Raúl Jiménez", "Henry Martín",
    "Luis Díaz", "James Rodríguez", "Falcao",
    "Enner Valencia", "Moisés Caicedo",
    "Darwin Núñez", "Federico Valverde", "Luis Suárez",
    "Miguel Almirón", "Ángel Romero",
    "Gianluca Lapadula", "André Carrillo",
    "Jhon Durán", "Rafael Santos Borré",
    "Dusan Vlahovic", "Sergej Milinkovic-Savic",
    "Khvicha Kvaratskhelia", "Georges Mikautadze",
    "Giorgi Mamardashvili",
    "Cengiz Ünder", "Hakan Çalhanoğlu", "Arda Güler",
    "Victor Boniface", "Ademola Lookman",
    "Xavi Simons", "Memphis Depay",
    "Emre Can", "İlkay Gündoğan",
    "Marco Asensio", "Dani Olmo",
    "Ansu Fati", "Ferran Torres",
])

ARQUEROS_MUNDIALISTAS = sorted([
    "Emiliano Martínez", "Franco Armani",
    "Alisson Becker", "Ederson", "Weverton",
    "Hugo Lloris", "Mike Maignan", "Alphonse Areola",
    "Thibaut Courtois", "Koen Casteels", "Simon Mignolet",
    "Manuel Neuer", "Marc-André ter Stegen", "Kevin Trapp",
    "David de Gea", "Unai Simón", "Robert Sánchez",
    "Gianluigi Donnarumma", "Alex Meret",
    "Jordan Pickford", "Nick Pope", "Aaron Ramsdale",
    "Rui Patrício", "Diogo Costa",
    "Yassine Bounou", "Munir",
    "Édouard Mendy", "Seny Dieng",
    "Bono", "Yahia Fofana",
    "Mathew Ryan", "Andrew Redmayne",
    "Matt Turner", "Ethan Horvath",
    "Maxime Crépeau", "Milan Borjan",
    "Guillermo Ochoa", "Alfredo Talavera",
    "Keylor Navas", "Patrick Sequeira",
    "Ángel Mena", "Alexander Domínguez",
    "Sergio Rochet", "Sebastián Sosa",
    "Antony Silva", "Diego Melgarejo",
    "Pedro Gallese", "Carlos Cáceda",
    "Benji Siegrist", "Yann Sommer",
    "Lukáš Hrádecký", "Saša Kalajdžić",
    "Dominik Livaković", "Ivica Ivušić",
    "Jan Oblak", "Vanja Milinković-Savić",
    "Giorgi Mamardashvili",
    "Altay Bayındır", "Uğurcan Çakır",
    "Hiroki Sakai",
])

def selectbox_busqueda(label, opciones, key, valor_actual=None):
    """Selectbox con búsqueda: el usuario filtra escribiendo."""
    busqueda = st.text_input(
        f"Buscar {label.lower()}",
        value="",
        key=f"busq_{key}",
        placeholder="Escribí para filtrar..."
    )
    filtrados = [o for o in opciones if busqueda.lower() in o.lower()] if busqueda else opciones
    if not filtrados:
        st.warning("No se encontró ningún jugador con ese nombre.")
        return valor_actual
    idx = filtrados.index(valor_actual) if valor_actual in filtrados else 0
    return st.selectbox(label, filtrados, index=idx, key=f"sel_{key}")


# -----------------------
# ESPECIALES DB
# -----------------------
CATEGORIAS_ESPECIALES = {
    "campeon":    {"label": "🏆 Campeón del Mundial",     "puntos": 20},
    "goleador":   {"label": "⚽ Goleador del Mundial",    "puntos": 10},
    "arquero":    {"label": "🧤 Mejor Arquero",           "puntos": 8},
    "jugador":    {"label": "⭐ Mejor Jugador (MVP)",     "puntos": 8},
}

def db_get_especial(username, categoria):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM especiales WHERE username=%s AND categoria=%s", (username, categoria))
        row = cur.fetchone()
        return dict(row) if row else None

def db_guardar_especial(username, categoria, eleccion):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO especiales (username, categoria, eleccion, confirmado)
            VALUES (%s, %s, %s, 0)
            ON CONFLICT (username, categoria) DO UPDATE SET eleccion=EXCLUDED.eleccion
        """, (username, categoria, eleccion))
    st.cache_data.clear()

def db_confirmar_especial(username, categoria):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE especiales SET confirmado=1 WHERE username=%s AND categoria=%s", (username, categoria))
    st.cache_data.clear()

def db_get_resultado_especial(categoria):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT resultado FROM especiales_resultados WHERE categoria=%s", (categoria,))
        row = cur.fetchone()
        return row["resultado"] if row else None

def db_guardar_resultado_especial(categoria, resultado):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO especiales_resultados (categoria, resultado) VALUES (%s, %s)
            ON CONFLICT (categoria) DO UPDATE SET resultado=EXCLUDED.resultado
        """, (categoria, resultado))
    st.cache_data.clear()

def db_calcular_puntos_especiales():
    with get_db() as conn:
        cur = conn.cursor()
        for cat, info in CATEGORIAS_ESPECIALES.items():
            resultado = db_get_resultado_especial(cat)
            if not resultado:
                continue
            cur.execute("""
                UPDATE usuarios SET puntos = puntos + %s
                WHERE username IN (
                    SELECT username FROM especiales
                    WHERE categoria=%s AND eleccion=%s AND confirmado=1
                )
            """, (info["puntos"], cat, resultado))
    st.cache_data.clear()

@st.cache_data(ttl=30)
def db_fusionar_variantes_especial(cat, variantes, nombre_oficial):
    """Reemplaza todas las variantes por el nombre oficial en la tabla especiales."""
    if not variantes:
        return
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE especiales SET eleccion=%s WHERE categoria=%s AND eleccion = ANY(%s)",
            (nombre_oficial, cat, variantes)
        )
    st.cache_data.clear()

def db_sumar_puntos_especial_a_usuarios(usernames, puntos):
    """Suma puntos directamente a una lista de usernames."""
    if not usernames:
        return
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET puntos = puntos + %s WHERE username = ANY(%s)",
            (puntos, usernames)
        )
    st.cache_data.clear()

def db_get_todos_especiales():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM especiales ORDER BY username, categoria")
        return [dict(r) for r in cur.fetchall()]

def db_limpiar_resultados_fase(fase):
    """Borra todos los resultados reales de una fase y recalcula puntos."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM resultados WHERE fase=%s", (fase,))
    st.cache_data.clear()

def db_limpiar_resultados_especiales():
    """Borra todos los resultados especiales."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM especiales_resultados")
    st.cache_data.clear()

def db_limpiar_prode_fase(username, fase):
    """Borra todos los pronósticos no confirmados del usuario para una fase."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM prodes WHERE username=%s AND fase=%s AND confirmado=0",
            (username, fase)
        )
    st.cache_data.clear()

def db_limpiar_especiales(username):
    """Borra todos los especiales no confirmados del usuario."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM especiales WHERE username=%s AND confirmado=0",
            (username,)
        )
    st.cache_data.clear()

def db_get_puntos_especiales_usuarios():
    """Devuelve dict {username: puntos_especiales} calculado en tiempo real."""
    result = {}
    for cat, info in CATEGORIAS_ESPECIALES.items():
        resultado_real = db_get_resultado_especial(cat)
        if not resultado_real:
            continue
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT username FROM especiales WHERE categoria=%s AND eleccion=%s AND confirmado=1",
                (cat, resultado_real)
            )
            for row in cur.fetchall():
                u = row["username"]
                result[u] = result.get(u, 0) + info["puntos"]
    return result

@st.cache_data(ttl=60)
def db_get_estadisticas_especiales():
    """Estadísticas de pronósticos especiales: distribución de elecciones."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT categoria, eleccion, COUNT(*) as votos
            FROM especiales WHERE confirmado=1
            GROUP BY categoria, eleccion
            ORDER BY categoria, votos DESC
        """)
        rows = cur.fetchall()
    result = {}
    for r in rows:
        cat = r["categoria"]
        if cat not in result:
            result[cat] = []
        result[cat].append({"eleccion": r["eleccion"], "votos": r["votos"]})
    return result

@st.cache_data(ttl=60)
def db_get_estadisticas_partidos():
    """Para cada partido con resultado, calcula aciertos exactos, resultado y errores."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                r.fase, r.partido_idx,
                r.goles_local as rl, r.goles_visita as rv,
                COUNT(p.username) as total_prodes,
                SUM(CASE WHEN p.goles_local = r.goles_local AND p.goles_visita = r.goles_visita THEN 1 ELSE 0 END) as exactos,
                SUM(CASE WHEN
                    (p.goles_local > p.goles_visita AND r.goles_local > r.goles_visita) OR
                    (p.goles_local < p.goles_visita AND r.goles_local < r.goles_visita) OR
                    (p.goles_local = p.goles_visita AND r.goles_local = r.goles_visita)
                THEN 1 ELSE 0 END) as resultados
            FROM resultados r
            LEFT JOIN prodes p ON p.fase = r.fase AND p.partido_idx = r.partido_idx AND p.confirmado = 1 AND p.partido_idx >= 0
            GROUP BY r.fase, r.partido_idx, r.goles_local, r.goles_visita
        """)
        return [dict(r) for r in cur.fetchall()]

@st.cache_data(ttl=60)
def db_get_estadisticas_generales():
    """Totales generales del torneo."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as total FROM usuarios WHERE es_admin=0")
        total_usuarios = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(DISTINCT username) as total FROM prodes WHERE confirmado=1 AND partido_idx=-1")
        confirmaron = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) as total FROM resultados")
        partidos_jugados = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) as total FROM prodes WHERE confirmado=1 AND partido_idx>=0 AND goles_local=goles_visita AND goles_local=0 AND goles_visita=0")
    return {
        "total_usuarios": total_usuarios,
        "confirmaron": confirmaron,
        "partidos_jugados": partidos_jugados,
    }

def fase_cerrada(fase):
    partidos = db_get_partidos(fase)
    if not partidos:
        return False
    ahora = datetime.datetime.now()
    for p in partidos:
        if not p.get("fecha") or not p.get("hora"):
            return False
        try:
            inicio = datetime.datetime.strptime(f"{p['fecha']} {p['hora']}", "%Y-%m-%d %H:%M")
            if ahora < inicio:
                return False
        except Exception:
            return False
    return True

def partido_cerrado(partido):
    if not partido.get("fecha") or not partido.get("hora"):
        return False
    try:
        inicio = datetime.datetime.strptime(f"{partido['fecha']} {partido['hora']}", "%Y-%m-%d %H:%M")
        return datetime.datetime.now() >= inicio
    except Exception:
        return False

def db_get_equipos_grupos():
    partidos = db_get_partidos("Grupos")
    equipos = sorted(set(
        e for p in partidos for e in [p["local"], p["visita"]]
        if e and not re.match(r'^rep\d*$', e.lower())
    ))
    return equipos


# -----------------------
# INIT
# -----------------------
init_db()  # cached via @st.cache_resource — solo corre una vez

if "step" not in st.session_state:
    st.session_state.step = 0
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "registro_temp" not in st.session_state:
    st.session_state.registro_temp = {}

FASES = ["Grupos", "Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final"]

# -----------------------
# BANDERAS
# -----------------------
BANDERAS = {
    "Argentina": "🇦🇷", "Brasil": "🇧🇷", "Uruguay": "🇺🇾", "Colombia": "🇨🇴",
    "Ecuador": "🇪🇨", "Paraguay": "🇵🇾", "Chile": "🇨🇱", "Venezuela": "🇻🇪",
    "Peru": "🇵🇪", "Bolivia": "🇧🇴",
    "EEUU": "🇺🇸", "Canada": "🇨🇦", "Mexico": "🇲🇽", "Haiti": "🇭🇹",
    "Jamaica": "🇯🇲", "Panama": "🇵🇦", "Costa Rica": "🇨🇷", "Honduras": "🇭🇳",
    "El Salvador": "🇸🇻", "Curazao": "🇨🇼", "Trinidad y Tobago": "🇹🇹",
    "Francia": "🇫🇷", "Alemania": "🇩🇪", "España": "🇪🇸", "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Portugal": "🇵🇹", "Paises Bajos": "🇳🇱", "Belgica": "🇧🇪", "Italia": "🇮🇹",
    "Croacia": "🇭🇷", "Suiza": "🇨🇭", "Austria": "🇦🇹", "Dinamarca": "🇩🇰",
    "Suecia": "🇸🇪", "Noruega": "🇳🇴", "Polonia": "🇵🇱", "Ucrania": "🇺🇦",
    "Turquia": "🇹🇷", "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Gales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Irlanda": "🇮🇪",
    "Grecia": "🇬🇷", "Hungria": "🇭🇺", "Serbia": "🇷🇸", "Eslovenia": "🇸🇮",
    "Rumania": "🇷🇴", "Eslovaquia": "🇸🇰", "Albania": "🇦🇱", "Georgia": "🇬🇪",
    "Republica Checa": "🇨🇿",
    "Marruecos": "🇲🇦", "Senegal": "🇸🇳", "Ghana": "🇬🇭", "Nigeria": "🇳🇬",
    "Costa de Marfil": "🇨🇮", "Egipto": "🇪🇬", "Tunez": "🇹🇳", "Argelia": "🇩🇿",
    "Cabo Verde": "🇨🇻", "Sudafrica": "🇿🇦", "Camerun": "🇨🇲", "Mali": "🇲🇱",
    "Guinea": "🇬🇳", "Tanzania": "🇹🇿", "Congo": "🇨🇬",
    "Japon": "🇯🇵", "Corea del Sur": "🇰🇷", "Australia": "🇦🇺", "Iran": "🇮🇷",
    "Arabia Saudita": "🇸🇦", "Catar": "🇶🇦", "Uzbekistan": "🇺🇿", "Jordania": "🇯🇴",
    "Irak": "🇮🇶", "Emiratos": "🇦🇪", "Nueva Zelanda": "🇳🇿", "Fiji": "🇫🇯",
    "Indonesia": "🇮🇩", "China": "🇨🇳", "India": "🇮🇳",
}

def bandera(nombre):
    return BANDERAS.get(nombre, "🏳️")


# -----------------------
# FUNCIONES
# -----------------------
def cambiar_pantalla(step):
    st.session_state.step = step

def login(usuario, clave):
    u = db_get_usuario(usuario)
    if not u:
        st.session_state.login_error = "Usuario no existe"
        st.rerun()
    elif u["clave"] != hash_clave(clave):
        st.session_state.login_error = "Clave incorrecta"
        st.rerun()
    else:
        st.session_state.usuario = usuario
        st.session_state.step = 9 if u["es_admin"] else 5
        st.rerun()

def avanzar_datos_personales(nombre, nacimiento, localidad, celular, mail, desde=""):
    mail_valido = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", mail.strip())
    if not (nombre.strip() and localidad.strip() and celular.strip() and mail.strip()):
        st.session_state.reg_error = "Completá todos los campos"
    elif not mail_valido:
        st.session_state.reg_error = "El mail no tiene formato válido"
    else:
        st.session_state.registro_temp = {
            "nombre": nombre.strip(), "nacimiento": str(nacimiento),
            "localidad": localidad.strip(), "celular": celular.strip(),
            "mail": mail.strip(), "desde": desde
        }
        st.session_state.step = 2


# -----------------------
# PANTALLAS
# -----------------------

def pantalla_login():
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem 0;">
        <div style="font-size:4rem; margin-bottom:0.5rem;">⚽</div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:3.5rem; letter-spacing:4px;
                    background:linear-gradient(135deg,#00c850,#00ff88);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; line-height:1.1;">PRODE IL BAIGO</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:1rem; color:#606075;
                    letter-spacing:3px; text-transform:uppercase; margin-top:0.3rem;">Mundial 2026</div>
    </div>
    """, unsafe_allow_html=True)

    if "login_error" in st.session_state:
        st.error(st.session_state.pop("login_error"))

    with st.form("form_login"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Clave", type="password")
        col1, col2 = st.columns(2)
        ingresar = col1.form_submit_button("Ingresar", type="primary", use_container_width=True)
        registrarse = col2.form_submit_button("Registrarse", use_container_width=True)

    if ingresar:
        login(usuario, clave)
    if registrarse:
        cambiar_pantalla(1)
        st.rerun()

    st.divider()
    st.button("ℹ️ Acerca del prode", on_click=cambiar_pantalla, args=(10,), use_container_width=True)


def pantalla_registro_datos():
    st.title("Registro — Datos personales")
    if not db_registro_abierto():
        st.error("⛔ El registro está cerrado. No se aceptan nuevas inscripciones.")
        st.button("Volver", on_click=cambiar_pantalla, args=(0,))
        return

    meses_es = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    with st.form("form_registro_datos"):
        nombre = st.text_input("Nombre y apellido")
        st.markdown("**Fecha de nacimiento**")
        año_sel = st.selectbox("Año de nacimiento", options=list(range(1930, datetime.date.today().year + 1))[::-1])
        mes_sel = st.selectbox("Mes de nacimiento", options=list(range(1, 13)), format_func=lambda x: meses_es[x - 1])
        dia_sel = st.selectbox("Día de nacimiento", options=list(range(1, 32)))
        localidad = st.text_input("Localidad")
        celular = st.text_input("Celular")
        mail = st.text_input("Mail")
        desde = st.text_input("¿Desde dónde te estás inscribiendo? Nombrá comercio, institución o redes")
        if "reg_error" in st.session_state:
            st.error(st.session_state.pop("reg_error"))
        col1, col2 = st.columns(2)
        volver = col1.form_submit_button("Volver")
        continuar = col2.form_submit_button("Continuar", type="primary")

    if volver:
        cambiar_pantalla(0); st.rerun()
    if continuar:
        try:
            nacimiento = datetime.date(año_sel, mes_sel, dia_sel)
        except ValueError:
            st.session_state.reg_error = "Fecha inválida. Revisá el día seleccionado."
            st.rerun()
        avanzar_datos_personales(nombre, nacimiento, localidad, celular, mail, desde)
        st.rerun()


def pantalla_registro_cuenta():
    st.title("Registro — Cuenta y pago")
    with st.form("form_registro_cuenta"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Clave (mínimo 4 caracteres)", type="password")
        confirmar = st.text_input("Confirmar clave", type="password")
        st.markdown("**Alias:** prode.mundial.2026")
        st.markdown("**CVU:** 0000003100000000000000")
        comprobante = st.file_uploader("Comprobante de pago")
        if "reg_error" in st.session_state:
            st.error(st.session_state.pop("reg_error"))
        col1, col2 = st.columns(2)
        volver = col1.form_submit_button("Volver")
        enviar = col2.form_submit_button("Enviar", type="primary")

    if volver:
        cambiar_pantalla(1); st.rerun()
    if enviar:
        u_strip = usuario.strip().lower()
        if not u_strip:
            st.session_state.reg_error = "Ingresá un nombre de usuario"
        elif not re.match(r'^[a-zA-Z0-9._-]+$', u_strip):
            st.session_state.reg_error = "El usuario solo puede tener letras, números, puntos, guiones o guiones bajos"
        elif len(u_strip) < 3:
            st.session_state.reg_error = "El usuario debe tener al menos 3 caracteres"
        elif db_get_usuario(u_strip):
            st.session_state.reg_error = "Usuario ya existe"
        elif len(clave) < 4:
            st.session_state.reg_error = "La clave debe tener al menos 4 caracteres"
        elif clave != confirmar:
            st.session_state.reg_error = "Las claves no coinciden"
        elif not comprobante:
            st.session_state.reg_error = "Subí el comprobante de pago"
        else:
            # En Streamlit Cloud no hay filesystem persistente.
            # Guardamos el nombre original del archivo como referencia.
            comprobante_nombre = comprobante.name
            db_agregar_pendiente({
                "username": u_strip, "clave": hash_clave(clave), "comprobante": comprobante_nombre,
                **st.session_state.registro_temp
            })
            st.session_state.step = 4
            st.rerun()


def pantalla_en_revision():
    st.markdown("""
    <div style="text-align:center; padding:3rem 1rem;">
        <div style="font-size:4rem; margin-bottom:1rem;">⏳</div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:2.5rem; letter-spacing:3px; color:#ffcc44;">
            INSCRIPCIÓN EN REVISIÓN</div>
        <div style="color:#a0a0b8; margin-top:1rem; font-size:1rem; line-height:1.7;">
            Tu solicitud está siendo revisada por el administrador.<br>Te avisamos cuando sea aprobada.</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Volver al inicio", on_click=cambiar_pantalla, args=(0,))


def pantalla_usuario():
    username = st.session_state.usuario
    u = db_get_usuario(username)
    st.title(f"Panel — {u.get('nombre', username)}")


    fases = db_get_fases()
    grupos_completados = st.session_state.get("wizard_grupos_completo", False) or db_fase_confirmada(username, "Grupos")

    if grupos_completados:
        fase = st.radio("Fase", options=FASES, horizontal=True)
    else:
        fase = "Grupos"

    if not fases.get(fase, False):
        st.warning("Esta fase no está habilitada aún.")
        if not grupos_completados:
            st.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,))
        return

    partidos = db_get_partidos(fase)
    if not partidos:
        st.info("El admin aún no cargó los partidos de esta fase.")
        if not grupos_completados:
            st.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,))
        return

    prode = db_get_prode(username, fase)
    confirmado = prode["confirmado"]
    pred = prode["pred"]

    if grupos_completados:
        st.subheader(f"Pronósticos — {fase}")
    else:
        st.subheader("Pronósticos — Grupos")

    resultados_fase = db_get_resultado_completo(fase)
    cambios = {}

    def render_partido(p):
        idx = p["idx"]
        gl_prev, gv_prev = pred.get(idx, (0, 0))
        res_real = resultados_fase.get(idx)
        res_str = ""
        iconos = ""
        color_card = "rgba(255,255,255,0.03)"
        border_card = "rgba(255,255,255,0.08)"

        if res_real:
            rl, rv = res_real
            acierto_res = (gl_prev > gv_prev and rl > rv) or (gl_prev < gv_prev and rl < rv) or (gl_prev == gv_prev and rl == rv)
            acierto_exacto = gl_prev == rl and gv_prev == rv
            iconos = ("✅" if acierto_res else "❌") + (" 🎯" if acierto_exacto else "")
            res_str = f"{rl} — {rv}"
            if acierto_exacto:
                color_card = "rgba(0,200,80,0.07)"; border_card = "rgba(0,200,80,0.3)"
            elif acierto_res:
                color_card = "rgba(0,150,255,0.06)"; border_card = "rgba(0,150,255,0.25)"
            else:
                color_card = "rgba(255,60,60,0.05)"; border_card = "rgba(255,60,60,0.2)"

        nom_local  = f"{bandera(p['local'])} {p['local']}"
        nom_visita = f"{bandera(p['visita'])} {p['visita']}"

        if confirmado:
            st.markdown(f"""
            <div style="background:{color_card}; border:1px solid {border_card};
                        border-radius:12px; padding:12px 16px; margin:6px 0;
                        display:flex; align-items:center; justify-content:space-between; gap:6px;">
                <div style="color:#ffffff; font-weight:700; font-size:0.95rem; flex:1; text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{nom_local}</div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:1.6rem; color:#00e870; min-width:20px; text-align:center; flex-shrink:0;">{gl_prev}</div>
                <div style="color:#404058; font-size:0.9rem; flex-shrink:0;">—</div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:1.6rem; color:#00e870; min-width:20px; text-align:center; flex-shrink:0;">{gv_prev}</div>
                <div style="color:#ffffff; font-weight:700; font-size:0.95rem; flex:1; text-align:left; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{nom_visita}</div>
                {f'<div style="font-size:1rem; flex-shrink:0;">{iconos}</div>' if iconos else ""}
            </div>
            {f'<div style="text-align:center; font-size:0.72rem; color:#606075; margin:-2px 0 4px 0;">Real: <span style="color:#a0a0b8;">{res_str}</span></div>' if res_str else ""}
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
                        border-radius:12px; padding:12px 16px; margin:6px 0;">
            """, unsafe_allow_html=True)

            col_local, col_gl, col_gv, col_visita = st.columns([3, 1, 1, 3])

            col_local.markdown(
                f"<div style='text-align:right; font-weight:700; font-size:0.95rem; "
                f"padding-top:10px; color:#fff; line-height:1.4;'>{nom_local}</div>",
                unsafe_allow_html=True)

            gl = col_gl.number_input(
                "Local", min_value=0, max_value=10, value=int(gl_prev),
                key=f"gl_{fase}_{idx}", label_visibility="collapsed")

            gv = col_gv.number_input(
                "Visita", min_value=0, max_value=10, value=int(gv_prev),
                key=f"gv_{fase}_{idx}", label_visibility="collapsed")

            col_visita.markdown(
                f"<div style='text-align:left; font-weight:700; font-size:0.95rem; "
                f"padding-top:10px; color:#fff; line-height:1.4;'>{nom_visita}</div>",
                unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            cambios[idx] = (gl, gv)

    if fase == "Grupos":
        grupos = [chr(ord('A') + i) for i in range(12)]
        grupos_con_partidos = [l for l in grupos if any(
            True for p in partidos if "ABCDEFGHIJKL".index(l)*6 <= p["idx"] < "ABCDEFGHIJKL".index(l)*6+6)]

        if confirmado:
            st.session_state["wizard_grupos_completo"] = True

        if st.session_state.get("wizard_grupos_completo", False):
            grupo_sel = st.selectbox("Elegí el grupo", [f"Grupo {l}" for l in grupos_con_partidos])
            letra_sel = grupo_sel[-1]
            inicio = "ABCDEFGHIJKL".index(letra_sel) * 6
            partidos_grupo = [p for p in partidos if inicio <= p["idx"] < inicio + 6]
            st.markdown(f"<div style='font-family:Bebas Neue,sans-serif; font-size:1.1rem; color:#606075; letter-spacing:3px; margin-top:0.5rem; text-transform:uppercase;'>GRUPO {letra_sel}</div>", unsafe_allow_html=True)
            for p in partidos_grupo:
                render_partido(p)
        else:
            if "grupo_wizard" not in st.session_state:
                st.session_state.grupo_wizard = 0
            gi_raw = st.session_state.grupo_wizard
            gi = gi_raw if gi_raw == 12 else max(0, min(gi_raw, len(grupos_con_partidos) - 1))
            letra = grupos_con_partidos[min(gi, len(grupos_con_partidos)-1)]
            total = len(grupos_con_partidos)

            if gi == 12:
                # ── Paso 13: especiales + confirmación final ──
                st.markdown("""
                <div style='display:flex; align-items:center; gap:10px; margin:0.5rem 0 0.8rem 0;'>
                    <div style='height:1px; flex:1; background:rgba(255,255,255,0.07);'></div>
                    <div style='font-family:Bebas Neue,sans-serif; font-size:1.3rem; color:#ffd700; letter-spacing:3px;'>⭐ ESPECIALES</div>
                    <div style='height:1px; flex:1; background:rgba(255,255,255,0.07);'></div>
                </div>
                <div style='text-align:center; color:#606075; font-size:0.75rem; margin-bottom:0.8rem; letter-spacing:1px;'>PASO 13 DE 13</div>
                """, unsafe_allow_html=True)

                eq_wiz = db_get_equipos_grupos() or sorted(BANDERAS.keys())
                selecciones_esp = {}

                for cat, info in CATEGORIAS_ESPECIALES.items():
                    esp_w = db_get_especial(username, cat)
                    elec_w = esp_w["eleccion"] if esp_w else None
                    res_real_w = db_get_resultado_especial(cat)

                    col_tw, col_pw = st.columns([4,1])
                    col_tw.markdown(f"**{info['label']}**")
                    col_pw.markdown(f"<div style='text-align:right; color:#ffd700; font-family:Bebas Neue,sans-serif; font-size:1.1rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)

                    if res_real_w:
                        acierto_w = elec_w == res_real_w
                        st.markdown(f"<div style='color:#a0a0b8; font-size:0.9rem; margin-bottom:8px;'>Resultado oficial: <b style='color:#fff'>{res_real_w}</b> {'🎯' if acierto_w else '❌'} — Tu pronóstico: <b style='color:#fff'>{elec_w or '—'}</b></div>", unsafe_allow_html=True)
                        selecciones_esp[cat] = elec_w
                    elif esp_w and esp_w["confirmado"]:
                        st.markdown(f"<div style='color:#00e870; font-size:0.9rem; margin-bottom:8px;'>✅ Confirmado: <b>{elec_w}</b></div>", unsafe_allow_html=True)
                        selecciones_esp[cat] = elec_w
                    else:
                        if cat == "campeon":
                            ops_w = [f"{bandera(e)} {e}" for e in eq_wiz]
                            d2n_w = {f"{bandera(e)} {e}": e for e in eq_wiz}
                            idx_w = next((i for i,e in enumerate(eq_wiz) if e==elec_w), 0)
                            sel_w = st.selectbox("Seleccioná el equipo", ops_w, index=idx_w, key=f"esp_sel_{cat}")
                            selecciones_esp[cat] = d2n_w.get(sel_w, sel_w)
                        else:
                            lista_w = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
                            label_w = "arquero" if cat == "arquero" else "jugador"
                            # Buscador: filtra la lista al escribir
                            busq_w = st.text_input(f"Buscar {label_w}", value="", key=f"esp_busq_{cat}", placeholder="Escribí para filtrar...")
                            st.caption(f"Si no encontrás al {label_w}, elegí **— Otro (escribir abajo) —** al final de la lista y escribí el nombre.")
                            filtrados_w = [j for j in lista_w if busq_w.lower() in j.lower()] if busq_w else lista_w
                            opciones_w = filtrados_w + ["— Otro (escribir abajo) —"]
                            # Determinar índice actual
                            if elec_w in filtrados_w:
                                idx_w = filtrados_w.index(elec_w)
                            elif elec_w and elec_w not in lista_w:
                                idx_w = len(opciones_w) - 1  # "Otro"
                            else:
                                idx_w = 0
                            sel_w = st.selectbox(f"Seleccioná el {label_w}", opciones_w, index=min(idx_w, len(opciones_w)-1), key=f"esp_sel_{cat}")
                            if sel_w == "— Otro (escribir abajo) —":
                                otro_val = elec_w if (elec_w and elec_w not in lista_w) else ""
                                otro_w = st.text_input(f"Nombre del {label_w}", value=otro_val, key=f"esp_otro_{cat}", placeholder=f"Escribí el nombre completo")
                                selecciones_esp[cat] = otro_w.strip() if otro_w.strip() else None
                            else:
                                selecciones_esp[cat] = sel_w

                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

                # ── Confirmación final aquí, solo en paso 13 ──
                st.divider()
                if "msg_esp" in st.session_state:
                    st.success(st.session_state.pop("msg_esp"))

                with st.form("form_confirmar_especiales"):
                    clave_esp_final = st.text_input("🔒 Tu contraseña para confirmar grupos + especiales", type="password", key="pw_esp_final")
                    col_ef1, col_ef2, col_ef3 = st.columns(3)
                    borrador_esp = col_ef1.form_submit_button("💾 Guardar borrador")
                    limpiar_esp = col_ef2.form_submit_button("🗑️ Limpiar especiales")
                    confirmar_esp = col_ef3.form_submit_button("🔒 Confirmar todo", type="primary")

                if borrador_esp:
                    for idx2, (gl2, gv2) in cambios.items():
                        db_guardar_pred(username, fase, idx2, gl2, gv2)
                    for cat, elec in selecciones_esp.items():
                        if elec and not (db_get_especial(username, cat) and db_get_especial(username, cat)["confirmado"]):
                            db_guardar_especial(username, cat, elec)
                    st.session_state["msg_esp"] = "💾 Borrador guardado."
                    st.rerun()

                if limpiar_esp:
                    db_limpiar_especiales(username)
                    st.session_state["msg_esp"] = "🗑️ Especiales eliminados. Podés volver a elegir."
                    st.rerun()

                if confirmar_esp:
                    if hash_clave(clave_esp_final) != u["clave"]:
                        st.error("Contraseña incorrecta.")
                    else:
                        faltan = [info["label"] for cat, info in CATEGORIAS_ESPECIALES.items()
                                  if not selecciones_esp.get(cat) and not (db_get_especial(username, cat) and db_get_especial(username, cat)["confirmado"])]
                        if faltan:
                            st.error(f"Falta completar: {', '.join(faltan)}")
                        else:
                            for idx2, (gl2, gv2) in cambios.items():
                                db_guardar_pred(username, fase, idx2, gl2, gv2)
                            db_confirmar_prode(username, fase)
                            for cat, elec in selecciones_esp.items():
                                if elec and not (db_get_especial(username, cat) and db_get_especial(username, cat)["confirmado"]):
                                    db_guardar_especial(username, cat, elec)
                                    db_confirmar_especial(username, cat)
                            st.session_state["wizard_grupos_completo"] = True
                            st.session_state["msg_grupos"] = "✅ ¡Todo confirmado! Grupos y especiales guardados."
                            st.rerun()

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                nav1_e, _, _ = st.columns([1,2,1])
                if nav1_e.button("← Grupo L", key="esp_back", use_container_width=True):
                    st.session_state.grupo_wizard = total - 1; st.rerun()

            else:
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:10px; margin:0.5rem 0 0.8rem 0;'>
                    <div style='height:1px; flex:1; background:rgba(255,255,255,0.07);'></div>
                    <div style='font-family:Bebas Neue,sans-serif; font-size:1.3rem; color:#00e870; letter-spacing:3px;'>GRUPO {letra}</div>
                    <div style='height:1px; flex:1; background:rgba(255,255,255,0.07);'></div>
                </div>
                <div style='text-align:center; color:#606075; font-size:0.75rem; margin-bottom:0.8rem; letter-spacing:1px;'>{gi+1} DE {total}</div>
                """, unsafe_allow_html=True)

                inicio = "ABCDEFGHIJKL".index(letra) * 6
                partidos_grupo = [p for p in partidos if inicio <= p["idx"] < inicio + 6]
                for p in partidos_grupo:
                    render_partido(p)

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                nav1, nav2, nav3 = st.columns([1, 2, 1])
                if nav1.button("← Anterior", key="grupo_prev", use_container_width=True, disabled=(gi == 0)):
                    st.session_state.grupo_wizard = gi - 1; st.rerun()
                if gi < total - 1:
                    if nav3.button("Siguiente →", key="grupo_next", type="primary", use_container_width=True):
                        st.session_state.grupo_wizard = gi + 1; st.rerun()
                else:
                    if nav3.button("Siguiente → Especiales ⭐", key="grupo_to_especiales", type="primary", use_container_width=True):
                        st.session_state.grupo_wizard = 12; st.rerun()

    else:
        for p in partidos:
            render_partido(p)

    # Confirmación para fases que NO son grupos (octavos, cuartos, etc.)
    if fase != "Grupos" and not confirmado:
        st.divider()
        with st.form("form_confirmar"):
            clave_confirm = st.text_input("Ingresá tu contraseña para confirmar", type="password")
            col_f1, col_f2, col_f3 = st.columns(3)
            confirmar_btn = col_f1.form_submit_button("🔒 Confirmar prode", type="primary")
            borrador_btn  = col_f2.form_submit_button("💾 Guardar borrador")
            limpiar_btn   = col_f3.form_submit_button("🗑️ Limpiar fase")

        if confirmar_btn:
            if hash_clave(clave_confirm) != u["clave"]:
                st.error("Contraseña incorrecta")
            else:
                for idx, (gl, gv) in cambios.items():
                    db_guardar_pred(username, fase, idx, gl, gv)
                db_confirmar_prode(username, fase)
                st.session_state["wizard_grupos_completo"] = True
                st.success("¡Pronósticos confirmados!")
                st.rerun()

        if borrador_btn:
            for idx, (gl, gv) in cambios.items():
                db_guardar_pred(username, fase, idx, gl, gv)
            st.success("Borrador guardado.")

        if limpiar_btn:
            db_limpiar_prode_fase(username, fase)
            st.session_state["msg_fase_limpiada"] = f"🗑️ Pronósticos de {fase} eliminados. Podés empezar de nuevo."
            st.rerun()

    if "msg_fase_limpiada" in st.session_state:
        st.success(st.session_state.pop("msg_fase_limpiada"))

    elif fase != "Grupos" and confirmado:
        st.success("✅ Pronósticos confirmados para esta fase.")

    # Para grupos wizard en pasos 0-11: guardar borrador sin confirmar
    if fase == "Grupos" and not confirmado and gi != 12:
        st.divider()
        col_bor1, col_bor2 = st.columns(2)
        with col_bor1.form("form_borrador_grupos"):
            borrador_btn_g = st.form_submit_button("💾 Guardar borrador", use_container_width=True)
        if borrador_btn_g:
            for idx, (gl, gv) in cambios.items():
                db_guardar_pred(username, fase, idx, gl, gv)
            st.session_state["msg_grupos"] = f"💾 Borrador del Grupo {letra} guardado."
            st.rerun()
        # Limpiar fase solo si hay algo guardado
        prode_actual = db_get_prode(username, "Grupos")
        if prode_actual["pred"]:
            with col_bor2.form("form_limpiar_grupos"):
                limpiar_btn_g = st.form_submit_button("🗑️ Limpiar todo lo guardado", use_container_width=True)
            if limpiar_btn_g:
                db_limpiar_prode_fase(username, "Grupos")
                st.session_state["msg_grupos"] = "🗑️ Pronósticos de Grupos eliminados. Podés empezar de nuevo."
                st.rerun()

    if "msg_grupos" in st.session_state:
        st.success(st.session_state.pop("msg_grupos"))

    if not grupos_completados:
        st.divider()
        st.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,))
        return


    st.divider()
    u_fresh = db_get_usuario(username)
    pts_esp_user = db_get_puntos_especiales_usuarios().get(username, 0)
    total_pts = u_fresh["puntos"] + u_fresh["goles"] + u_fresh["consumo"] + pts_esp_user
    todos = db_get_todos_usuarios()
    pts_esp_rank = db_get_puntos_especiales_usuarios()
    ranking = sorted(todos, key=lambda x: x["puntos"] + x["goles"] + x["consumo"] + pts_esp_rank.get(x["username"], 0), reverse=True)
    posicion = next((i + 1 for i, x in enumerate(ranking) if x["username"] == username), "—")

    st.subheader("Mis puntos")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    col_a.metric("Resultados", u_fresh["puntos"])
    col_b.metric("Goles", u_fresh["goles"])
    col_c.metric("Consumo", u_fresh["consumo"])
    col_d.metric("⭐ Especiales", pts_esp_user)
    col_e.metric("Total", total_pts)
    st.info(f"🏆 Posición actual: **{posicion}° de {len(ranking)}**")

    # ── Resumen de especiales para usuario que ya confirmó ──
    esp_data = {cat: db_get_especial(username, cat) for cat in CATEGORIAS_ESPECIALES}
    any_esp = any(v for v in esp_data.values())
    if any_esp:
        st.subheader("⭐ Mis pronósticos especiales")
        for cat, info in CATEGORIAS_ESPECIALES.items():
            esp = esp_data[cat]
            elec = esp["eleccion"] if esp else None
            confirmado_esp = esp and esp["confirmado"]
            resultado_real = db_get_resultado_especial(cat)

            if not elec:
                bg_c = "rgba(255,255,255,0.02)"
                border_c = "rgba(255,255,255,0.05)"
                derecha = '<span style="color:#606075; font-size:0.8rem;">Sin completar</span>'
            elif resultado_real:
                acierto = elec == resultado_real
                icono = "🎯" if acierto else "❌"
                bg_c = "rgba(0,200,80,0.06)" if acierto else "rgba(255,60,60,0.05)"
                border_c = "rgba(0,200,80,0.25)" if acierto else "rgba(255,60,60,0.2)"
                derecha = (
                    f'<b style="color:#fff">{elec}</b>'
                    f'<span style="margin:0 8px; color:#404058;">→</span>'
                    f'<span style="color:#a0a0b8; font-size:0.8rem;">Real: </span>'
                    f'<b style="color:#fff">{resultado_real}</b>'
                    f'<span style="margin-left:6px; font-size:1rem;">{icono}</span>'
                )
            else:
                bg_c = "rgba(255,255,255,0.03)"
                border_c = "rgba(255,255,255,0.07)"
                derecha = f'<b style="color:#fff">{elec}</b>'

            st.markdown(f"""<div style="background:{bg_c}; border:1px solid {border_c};
                border-radius:10px; padding:10px 16px; margin:4px 0;
                display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#a0a0b8; font-size:0.85rem;">{info['label']}</span>
                <span>{derecha}</span>
            </div>""", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.button("Ver Ranking", on_click=cambiar_pantalla, args=(6,), use_container_width=True)
    col2.button("📊 Estadísticas", on_click=cambiar_pantalla, args=(12,), use_container_width=True)
    col3.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,), use_container_width=True)


def pantalla_ranking():
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem 0;">
        <div style="font-family:'Bebas Neue',sans-serif; font-size:3rem; letter-spacing:4px;
                    background:linear-gradient(135deg,#ffd700,#ffaa00);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">🏆 RANKING</div>
    </div>
    """, unsafe_allow_html=True)
    username_actual = st.session_state.get("usuario", "")

    todos = db_get_todos_usuarios()
    if not todos:
        st.info("Todavía no hay usuarios para mostrar.")
    else:
        ranking = sorted(todos, key=lambda x: x["puntos"] + x["goles"] + x["consumo"], reverse=True)
        if len(ranking) >= 3:
            nombres = [u.get("nombre") or u["username"] for u in ranking[:3]]
            totales = [u["puntos"] + u["goles"] + u["consumo"] for u in ranking[:3]]
            c2, c1, c3 = st.columns(3)
            c1.metric("🥇 " + nombres[0], f"{totales[0]} pts")
            c2.metric("🥈 " + nombres[1], f"{totales[1]} pts")
            c3.metric("🥉 " + nombres[2], f"{totales[2]} pts")
            st.divider()

        pts_esp = db_get_puntos_especiales_usuarios()
        rows = []
        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        for i, u in enumerate(ranking):
            pos = i + 1
            esp = pts_esp.get(u["username"], 0)
            total = u["puntos"] + u["goles"] + u["consumo"] + esp
            rows.append({"Pos": medallas.get(pos, str(pos)), "Nombre": u.get("nombre") or u["username"],
                         "Resultados": u["puntos"], "Goles": u["goles"], "Consumo": u["consumo"],
                         "Especiales": esp, "Total": total, "_username": u["username"], "_pos": pos})

        df = pd.DataFrame(rows)
        top_n = st.slider("Mostrar top", 5, max(10, len(df)), min(10, len(df)))

        hay_especiales = any(r["Especiales"] > 0 for r in rows)

        filas_html = ""
        for r in rows[:top_n]:
            es_yo = r["_username"] == username_actual
            bg = "rgba(0,200,80,0.08)" if es_yo else "transparent"
            border_left = "3px solid #00c850" if es_yo else "3px solid transparent"
            col_esp = f'<td style="padding:10px 12px; color:#ffd700; text-align:center;">{r["Especiales"]}</td>' if hay_especiales else ""
            filas_html += f"""
            <tr style="background:{bg}; border-left:{border_left};">
                <td style="padding:10px 12px; color:#ffffff; font-weight:700; font-size:1.1rem;">{r['Pos']}</td>
                <td style="padding:10px 12px; color:#ffffff; font-weight:600;">{r['Nombre']}</td>
                <td style="padding:10px 12px; color:#a0a0b8; text-align:center;">{r['Resultados']}</td>
                <td style="padding:10px 12px; color:#a0a0b8; text-align:center;">{r['Goles']}</td>
                <td style="padding:10px 12px; color:#a0a0b8; text-align:center;">{r['Consumo']}</td>
                {col_esp}
                <td style="padding:10px 12px; color:#00e870; font-weight:700; font-size:1.1rem; text-align:center;">{r['Total']}</td>
            </tr>"""

        th_esp = '<th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">⭐ Esp.</th>' if hay_especiales else ""
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; background:#0f0f1a;
                      border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);">
            <thead><tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Pos</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Nombre</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Res.</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Goles</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Cons.</th>
                {th_esp}
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Total</th>
            </tr></thead>
            <tbody>{filas_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

        if username_actual and username_actual != "admin":
            pos_actual = next((r["_pos"] for r in rows if r["_username"] == username_actual), None)
            if pos_actual and pos_actual > top_n:
                fila = next(r for r in rows if r["_username"] == username_actual)
                st.divider()
                st.info(f"Tu posición: **{pos_actual}°** — {fila['Nombre']} | Total: **{fila['Total']} pts**")

    st.divider()
    destino = 9 if st.session_state.get("usuario") == "admin" else 5
    st.button("Volver", on_click=cambiar_pantalla, args=(destino,))


def pantalla_admin():
    st.title("⚙️ Panel Admin")
    tabs = st.tabs(["📋 Resumen", "👥 Pendientes", "🔀 Fases", "⚽ Partidos", "📊 Result.", "💰 Consumo", "⭐ Especiales", "👤 Usuarios", "⚠️ Reset", "📥 Exportar"])

    with tabs[0]:
        st.subheader("Resumen general")
        if "msg_resumen" in st.session_state:
            st.success(st.session_state.pop("msg_resumen"))
        todos = db_get_todos_usuarios()
        pendientes = db_get_pendientes()
        fases = db_get_fases()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Usuarios activos", len(todos))
        col2.metric("Solicitudes pendientes", len(pendientes))
        col3.metric("Fases habilitadas", sum(1 for v in fases.values() if v))
        col4.metric("Total consumo acumulado", sum(u["consumo"] for u in todos))
        st.divider()
        st.subheader("Inscripciones")
        registro_abierto = db_registro_abierto()
        nuevo_estado = st.toggle("Registro abierto", value=registro_abierto, key="toggle_registro")
        if nuevo_estado != registro_abierto:
            db_set_config("registro_abierto", "1" if nuevo_estado else "0"); st.rerun()
        st.divider()
        st.subheader("Confirmaciones por fase")
        for fase in FASES:
            if not fases.get(fase):
                continue
            confirmados = sum(1 for u in todos if db_fase_confirmada(u["username"], fase))
            st.write(f"**{fase}:** {confirmados} / {len(todos)} confirmados")
        st.divider()
        if st.button("🔄 Recalcular puntajes"):
            db_calcular_puntos()
            st.session_state["msg_resumen"] = "✅ Puntajes recalculados correctamente."
            st.rerun()

    with tabs[1]:
        st.subheader("Solicitudes pendientes")
        if "msg_pendientes" in st.session_state:
            st.success(st.session_state.pop("msg_pendientes"))
        pendientes = db_get_pendientes()
        if not pendientes:
            st.info("No hay solicitudes pendientes.")
        for pend in pendientes:
            with st.expander(f"👤 {pend['username']} — {pend.get('nombre', '')}"):
                st.write(f"**Mail:** {pend.get('mail', '—')}")
                st.write(f"**Celular:** {pend.get('celular', '—')}")
                st.write(f"**Localidad:** {pend.get('localidad', '—')}")
                st.write(f"**Nacimiento:** {pend.get('nacimiento', '—')}")
                st.write(f"**Comprobante:** {pend.get('comprobante', '—')}")
                c1, c2 = st.columns(2)
                if c1.button("✅ Aprobar", key=f"ap_{pend['id']}"):
                    db_aprobar_pendiente(pend["id"])
                    st.cache_data.clear()
                    st.session_state["msg_pendientes"] = f"✅ {pend['username']} aprobado."
                    st.rerun()
                if c2.button("❌ Rechazar", key=f"re_{pend['id']}"):
                    db_rechazar_pendiente(pend["id"])
                    st.session_state["msg_pendientes"] = f"⚠️ {pend['username']} rechazado."
                    st.rerun()

    with tabs[2]:
        st.subheader("Habilitar / Deshabilitar fases")
        fases = db_get_fases()
        cols = st.columns(len(FASES))
        for idx, f in enumerate(FASES):
            estado = fases.get(f, False)
            nuevo = cols[idx].toggle(f, value=estado, key=f"toggle_{f}")
            if nuevo != estado:
                db_toggle_fase(f, nuevo); st.rerun()

    with tabs[3]:
        st.subheader("Cargar partidos")
        if "msg_grupos" in st.session_state:
            st.success(st.session_state.pop("msg_grupos"))
        fase_sel = st.selectbox("Fase", FASES, key="fase_partidos")

        GRUPOS_DEFAULT = {
            "A": [("Mexico","Sudafrica"),("Corea del Sur","rep1"),("rep1","Sudafrica"),("Mexico","Corea del Sur"),("rep1","Mexico"),("Sudafrica","Corea del Sur")],
            "B": [("Canada","rep2"),("Catar","Suiza"),("Suiza","rep2"),("Canada","Catar"),("Suiza","Canada"),("rep2","Catar")],
            "C": [("Brasil","Marruecos"),("Haiti","Escocia"),("Escocia","Marruecos"),("Brasil","Haiti"),("Escocia","Brasil"),("Marruecos","Haiti")],
            "D": [("EEUU","Paraguay"),("Australia","rep3"),("rep3","Paraguay"),("EEUU","Australia"),("rep3","EEUU"),("Paraguay","Australia")],
            "E": [("Alemania","Curazao"),("Costa de Marfil","Ecuador"),("Alemania","Costa de Marfil"),("Ecuador","Curazao"),("Ecuador","Alemania"),("Curazao","Costa de Marfil")],
            "F": [("Paises Bajos","Japon"),("rep4","Tunez"),("Tunez","Japon"),("Paises Bajos","rep4"),("Japon","rep4"),("Tunez","Paises Bajos")],
            "G": [("Belgica","Egipto"),("Iran","Nueva Zelanda"),("Belgica","Iran"),("Nueva Zelanda","Egipto"),("Egipto","Iran"),("Nueva Zelanda","Belgica")],
            "H": [("España","Cabo Verde"),("Arabia Saudita","Uruguay"),("España","Arabia Saudita"),("Uruguay","Cabo Verde"),("Cabo Verde","Arabia Saudita"),("Uruguay","España")],
            "I": [("Francia","Senegal"),("rep5","Noruega"),("Francia","rep5"),("Noruega","Senegal"),("Noruega","Francia"),("Senegal","rep5")],
            "J": [("Austria","Jordania"),("Argentina","Argelia"),("Argentina","Austria"),("Jordania","Argelia"),("Argelia","Austria"),("Jordania","Argentina")],
            "K": [("Portugal","rep6"),("Uzbekistan","Colombia"),("Portugal","Uzbekistan"),("Colombia","rep6"),("Colombia","Portugal"),("rep6","Uzbekistan")],
            "L": [("Inglaterra","Croacia"),("Ghana","Panama"),("Inglaterra","Ghana"),("Panama","Croacia"),("Panama","Inglaterra"),("Croacia","Ghana")],
        }

        if fase_sel == "Grupos":
            partidos_cargados = db_get_partidos("Grupos")
            grupos_con_datos = set()
            for p in partidos_cargados:
                letra_g = "ABCDEFGHIJKL"[p["idx"] // 6]
                grupos_con_datos.add(letra_g)
            opciones_grupos = [f"{'✅' if l in grupos_con_datos else '○'} Grupo {l}" for l in "ABCDEFGHIJKL"]
            grupo_sel_raw = st.selectbox("Grupo", opciones_grupos)
            grupo_sel = grupo_sel_raw[-7:]  # "Grupo X"
            letra = grupo_sel[-1]
            inicio = "ABCDEFGHIJKL".index(letra) * 6
            partidos_existentes = partidos_cargados
            existentes_map = {p["idx"]: p for p in partidos_existentes}
            defaults = GRUPOS_DEFAULT.get(letra, [("", "")] * 6)
            with st.form(f"form_grupo_{letra}"):
                nuevos = []
                for j in range(6):
                    idx_global = inicio + j
                    prev = existentes_map.get(idx_global, {})
                    c1, c2 = st.columns(2)
                    l = c1.text_input("Local", value=prev.get("local", defaults[j][0]), key=f"gl_{letra}_{j}")
                    v = c2.text_input("Visitante", value=prev.get("visita", defaults[j][1]), key=f"gv_{letra}_{j}")
                    nuevos.append((idx_global, l, v))
                col_b1, col_b2 = st.columns(2)
                guardar = col_b1.form_submit_button(f"Guardar Grupo {letra}", type="primary")
                guardar_todos = col_b2.form_submit_button("Guardar todos los grupos")
            if guardar:
                for idx_global, l, v in nuevos:
                    if l and v: db_guardar_partido("Grupos", idx_global, l, v)
                st.cache_data.clear()
                st.session_state["msg_grupos"] = f"✅ Grupo {letra} guardado."
                st.rerun()
            if guardar_todos:
                for gr, partidos_gr in GRUPOS_DEFAULT.items():
                    ini_gr = "ABCDEFGHIJKL".index(gr) * 6
                    for j, (loc, vis) in enumerate(partidos_gr):
                        db_guardar_partido("Grupos", ini_gr + j, loc, vis)
                st.cache_data.clear()
                st.session_state["msg_grupos"] = "✅ Todos los grupos guardados con los equipos por defecto."
                st.rerun()
        else:
            cant = {"Dieciseisavos": 16, "Octavos": 8, "Cuartos": 4, "Semifinal": 2, "Final": 1}[fase_sel]
            partidos_existentes = db_get_partidos(fase_sel)
            existentes_map = {p["idx"]: p for p in partidos_existentes}
            equipos_grupos = db_get_equipos_grupos()

            if not equipos_grupos:
                st.warning("⚠️ Primero cargá los partidos de la fase de Grupos para poder seleccionar equipos acá.")
            else:
                NINGUNO = "— Seleccionar —"
                opciones = [NINGUNO] + [f"{bandera(e)} {e}" for e in equipos_grupos]
                display_a_nombre = {f"{bandera(e)} {e}": e for e in equipos_grupos}

                with st.form(f"form_{fase_sel}"):
                    nuevos = []
                    for i in range(cant):
                        prev = existentes_map.get(i, {})
                        prev_local  = prev.get("local", "")
                        prev_visita = prev.get("visita", "")
                        disp_local  = f"{bandera(prev_local)} {prev_local}"   if prev_local  else NINGUNO
                        disp_visita = f"{bandera(prev_visita)} {prev_visita}" if prev_visita else NINGUNO
                        idx_local  = opciones.index(disp_local)  if disp_local  in opciones else 0
                        idx_visita = opciones.index(disp_visita) if disp_visita in opciones else 0

                        st.markdown(
                            f"<div style='color:#606075; font-size:0.75rem; text-transform:uppercase; "
                            f"letter-spacing:1px; margin-top:0.8rem; margin-bottom:0.2rem;'>Partido {i+1}</div>",
                            unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        sel_local  = c1.selectbox("Local",     opciones, index=idx_local,  key=f"{fase_sel}_l_{i}")
                        sel_visita = c2.selectbox("Visitante", opciones, index=idx_visita, key=f"{fase_sel}_v_{i}")
                        nombre_local  = display_a_nombre.get(sel_local,  "")
                        nombre_visita = display_a_nombre.get(sel_visita, "")
                        nuevos.append((i, nombre_local, nombre_visita))

                    guardar = st.form_submit_button("Guardar partidos", type="primary")

                if guardar:
                    guardados = 0
                    for i, l, v in nuevos:
                        if l and v:
                            db_guardar_partido(fase_sel, i, l, v)
                            guardados += 1
                    if guardados:
                        st.success(f"✅ {guardados} partido(s) guardado(s).")
                    else:
                        st.warning("No se guardó ningún partido. Seleccioná al menos un par de equipos.")

    with tabs[4]:
        st.subheader("Cargar resultados reales")
        if "res_ok" in st.session_state:
            st.success(st.session_state.pop("res_ok"))
        fase_sel = st.selectbox("Fase", FASES, key="fase_resultados")
        partidos = db_get_partidos(fase_sel)
        if not partidos:
            st.info("No hay partidos cargados para esta fase.")
        else:
            resultados_actuales = db_get_resultado_completo(fase_sel)
            if fase_sel == "Grupos":
                grupo_sel_r = st.selectbox("Grupo", [f"Grupo {l}" for l in "ABCDEFGHIJKL"], key="grupo_res")
                letra_r = grupo_sel_r[-1]
                inicio_r = "ABCDEFGHIJKL".index(letra_r) * 6
                partidos_grupo_r = [p for p in partidos if inicio_r <= p["idx"] < inicio_r + 6]
            else:
                partidos_grupo_r = partidos

            for p in partidos_grupo_r:
                idx = p["idx"]
                tiene_res = idx in resultados_actuales
                rl_prev, rv_prev = resultados_actuales.get(idx, (0, 0))
                border = "rgba(0,200,80,0.3)" if tiene_res else "rgba(255,255,255,0.08)"
                bg = "rgba(0,200,80,0.05)" if tiene_res else "rgba(255,255,255,0.02)"
                st.markdown(f'<div style="background:{bg}; border:1px solid {border}; border-radius:12px; padding:10px 14px; margin:6px 0;">', unsafe_allow_html=True)
                activar = st.checkbox("Cargar resultado", value=tiene_res, key=f"chk_{fase_sel}_{idx}")
                if activar:
                    c_local, c_rl, c_sep, c_rv, c_visita, c_btn = st.columns([3, 1, 0.4, 1, 3, 1.5])
                    c_local.markdown(f"<div style='text-align:right; font-weight:700; font-size:0.9rem; padding-top:9px; color:#fff;'>{bandera(p['local'])} {p['local']}</div>", unsafe_allow_html=True)
                    rl = c_rl.number_input("rl", 0, 15, int(rl_prev), key=f"rl_{fase_sel}_{idx}", label_visibility="collapsed")
                    c_sep.markdown("<div style='text-align:center; padding-top:9px; color:#404058;'>—</div>", unsafe_allow_html=True)
                    rv = c_rv.number_input("rv", 0, 15, int(rv_prev), key=f"rv_{fase_sel}_{idx}", label_visibility="collapsed")
                    c_visita.markdown(f"<div style='text-align:left; font-weight:700; font-size:0.9rem; padding-top:9px; color:#fff;'>{bandera(p['visita'])} {p['visita']}</div>", unsafe_allow_html=True)
                    if c_btn.button("💾", key=f"save_{fase_sel}_{idx}", help="Guardar resultado"):
                        db_guardar_resultado(fase_sel, idx, rl, rv)
                        db_calcular_puntos()
                        st.session_state["res_ok"] = f"✅ Guardado: {p['local']} {rl} — {rv} {p['visita']}"
                        st.rerun()
                    if tiene_res:
                        st.caption(f"✅ Guardado: {p['local']} {rl_prev} — {rv_prev} {p['visita']}")
                else:
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:8px; padding:2px 0 4px 0;">
                        <div style="color:#fff; font-weight:700; font-size:0.9rem; flex:1; text-align:right;">{bandera(p['local'])} {p['local']}</div>
                        <div style="color:#404058; font-size:0.8rem;">vs</div>
                        <div style="color:#fff; font-weight:700; font-size:0.9rem; flex:1;">{bandera(p['visita'])} {p['visita']}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Botón limpiar resultados de la fase (o grupo seleccionado)
            st.divider()
            cant_resultados = len(resultados_actuales)
            if cant_resultados > 0:
                if fase_sel == "Grupos":
                    cant_grupo = sum(1 for idx in resultados_actuales if inicio_r <= idx < inicio_r + 6)
                    label_limpiar = f"Grupo {letra_r} ({cant_grupo} resultado(s))"
                    confirmar_limpiar = f"resultados del {label_limpiar}"
                else:
                    label_limpiar = f"{fase_sel} ({cant_resultados} resultado(s))"
                    confirmar_limpiar = f"resultados de {fase_sel}"

                with st.form(f"form_limpiar_res_{fase_sel}"):
                    st.warning(f"⚠️ Esto borrará los {confirmar_limpiar} y recalculará los puntajes.")
                    pw_limpiar = st.text_input("Tu contraseña de admin para confirmar", type="password", key=f"pw_limpiar_{fase_sel}")
                    limpiar_res_btn = st.form_submit_button(f"🗑️ Limpiar {label_limpiar}", type="primary")

                if limpiar_res_btn:
                    admin_lr = db_get_usuario(st.session_state.usuario)
                    if admin_lr["clave"] != hash_clave(pw_limpiar):
                        st.session_state["res_ok"] = "❌ Contraseña incorrecta."
                    else:
                        if fase_sel == "Grupos":
                            # Solo borrar los del grupo seleccionado
                            with get_db() as conn:
                                cur = conn.cursor()
                                cur.execute(
                                    "DELETE FROM resultados WHERE fase=%s AND partido_idx >= %s AND partido_idx < %s",
                                    ("Grupos", inicio_r, inicio_r + 6)
                                )
                            st.cache_data.clear()
                        else:
                            db_limpiar_resultados_fase(fase_sel)
                        db_calcular_puntos()
                        st.session_state["res_ok"] = f"🗑️ Resultados de {label_limpiar} eliminados y puntajes recalculados."
                    st.rerun()

    with tabs[5]:
        st.subheader("Sumar consumo")
        if "msg_consumo" in st.session_state:
            st.success(st.session_state.pop("msg_consumo"))
        busq_consumo = st.text_input("Buscar usuario", key="busq_consumo")
        if busq_consumo:
            todos = db_get_todos_usuarios()
            opts = {u["username"]: u.get("nombre") or u["username"] for u in todos
                    if busq_consumo.lower() in u["username"].lower() or busq_consumo.lower() in (u.get("nombre") or "").lower()}
            if opts:
                with st.form("form_consumo"):
                    sel = st.selectbox("Usuario", list(opts.keys()), format_func=lambda x: f"{opts[x]} ({x})")
                    pts = st.number_input("Puntos a sumar", 0, 500, 0)
                    desc = st.text_input("Descripción (opcional)", placeholder="Ej: consumo viernes 20/6")
                    sumar = st.form_submit_button("Sumar consumo", type="primary")
                if sumar:
                    db_sumar_consumo(sel, pts, desc); db_calcular_puntos()
                    st.session_state["msg_consumo"] = f"✅ Se sumaron {pts} puntos de consumo a {opts[sel]}."
                    st.rerun()
            else:
                st.warning("No se encontró ningún usuario.")

        st.divider()
        st.subheader("Historial de consumo")
        col_f1, col_f2, col_f3 = st.columns(3)
        filtro_usuario = col_f1.text_input("Filtrar por usuario", key="hist_usuario")
        filtro_desde = col_f2.date_input("Desde", value=None, key="hist_desde")
        filtro_hasta = col_f3.date_input("Hasta", value=None, key="hist_hasta")
        log = db_get_consumo_log()
        if log:
            df_log = pd.DataFrame(log)[["id", "fecha", "username", "puntos", "descripcion"]]
            df_log.columns = ["ID", "Fecha", "Usuario", "Puntos", "Descripción"]
            df_log["Fecha"] = pd.to_datetime(df_log["Fecha"])
            if filtro_usuario:
                df_log = df_log[df_log["Usuario"].str.contains(filtro_usuario, case=False, na=False)]
            if filtro_desde:
                df_log = df_log[df_log["Fecha"].dt.date >= filtro_desde]
            if filtro_hasta:
                df_log = df_log[df_log["Fecha"].dt.date <= filtro_hasta]
            df_log["Fecha"] = df_log["Fecha"].dt.strftime("%d/%m/%Y %H:%M")
            PAGINA_SIZE = 20
            total = len(df_log)
            if total == 0:
                st.info("No hay registros con esos filtros.")
            else:
                total_paginas = max(1, (total - 1) // PAGINA_SIZE + 1)
                pagina = st.number_input("Página", min_value=1, max_value=total_paginas, value=1, step=1)
                inicio = (pagina - 1) * PAGINA_SIZE
                fin = inicio + PAGINA_SIZE
                st.caption(f"Mostrando {min(fin, total)} de {total} registros — Página {pagina}/{total_paginas}")
                slice_df = df_log.iloc[inicio:fin]
                filas_log = ""
                for _, row in slice_df.iterrows():
                    filas_log += f"""<tr>
                        <td style="padding:9px 12px; color:#606075; font-size:0.85rem;">{row['ID']}</td>
                        <td style="padding:9px 12px; color:#a0a0b8;">{row['Fecha']}</td>
                        <td style="padding:9px 12px; color:#ffffff; font-weight:600;">{row['Usuario']}</td>
                        <td style="padding:9px 12px; color:#00e870; font-weight:700; text-align:center;">{row['Puntos']}</td>
                        <td style="padding:9px 12px; color:#c8c8d8;">{row.get('Descripción', '')}</td>
                    </tr>"""
                st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);">
                    <thead><tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
                        <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">ID</th>
                        <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Fecha</th>
                        <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Usuario</th>
                        <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Pts</th>
                        <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Descripción</th>
                    </tr></thead><tbody>{filas_log}</tbody></table>""", unsafe_allow_html=True)
                st.markdown(f"**Total puntos en filtro: {df_log['Puntos'].sum()}**")
        else:
            st.info("Todavía no hay registros de consumo.")

        st.divider()
        st.subheader("Eliminar registro de consumo")
        st.caption("Esto resta los puntos al usuario y elimina el registro.")
        with st.form("form_eliminar_consumo"):
            id_eliminar = st.number_input("ID del registro a eliminar", min_value=1, step=1, key="id_eliminar_consumo")
            clave_admin_el = st.text_input("Tu contraseña de admin para confirmar", type="password")
            eliminar_btn = st.form_submit_button("🗑️ Eliminar registro", type="primary")
        if eliminar_btn:
            admin = db_get_usuario(st.session_state.usuario)
            if admin["clave"] != hash_clave(clave_admin_el):
                st.error("Contraseña incorrecta.")
            else:
                db_eliminar_consumo_log(int(id_eliminar)); db_calcular_puntos()
                st.session_state["msg_consumo"] = f"✅ Registro #{int(id_eliminar)} eliminado y puntos descontados."
                st.rerun()

    with tabs[6]:
        st.subheader("⭐ Pronósticos especiales — Resultados")
        st.caption("Cargá el ganador real de cada categoría. Los buscadores filtran la lista — el selectbox es lo que se guarda.")

        if "msg_esp_adm" in st.session_state:
            st.success(st.session_state.pop("msg_esp_adm"))

        equipos_adm = db_get_equipos_grupos() or sorted(BANDERAS.keys())

        filtros_adm = {}  # sin buscadores externos

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── Panel de fusión de variantes ──
        todos_esp_adm = db_get_todos_especiales()
        df_esp_adm = pd.DataFrame(todos_esp_adm) if todos_esp_adm else pd.DataFrame()

        # Recolectar variantes escritas como "Otro" por categoría
        variantes_por_cat = {}
        for cat in CATEGORIAS_ESPECIALES:
            if cat == "campeon":
                continue
            lista_oficial = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
            if not df_esp_adm.empty and cat in df_esp_adm["categoria"].values:
                sub = df_esp_adm[df_esp_adm["categoria"] == cat]
                # Solo los que NO están en la lista oficial (fueron escritos a mano)
                otros = sub[~sub["eleccion"].isin(lista_oficial)]["eleccion"].unique().tolist()
                if otros:
                    variantes_por_cat[cat] = otros

        with st.expander("🔀 Unificar variantes escritas a mano"):
            st.caption("Mostrá las variantes que los usuarios escribieron a mano y unificalas en un nombre canónico.")
            for cat in [c for c in CATEGORIAS_ESPECIALES if c != "campeon"]:
                info = CATEGORIAS_ESPECIALES[cat]
                variantes = variantes_por_cat.get(cat, [])
                if variantes:
                    st.markdown(f"**{info['label']}** — {len(variantes)} variante(s) detectada(s):")
                    sels_fusion = st.multiselect(
                        "Seleccioná las variantes a unificar",
                        variantes,
                        key=f"fusion_sel_{cat}",
                        format_func=lambda x: f"{x} ({sum(1 for r in todos_esp_adm if r['categoria']==cat and r['eleccion']==x)} votos)"
                    )
                    nombre_fusion = st.text_input(
                        "Nombre oficial que reemplaza a todas las variantes",
                        key=f"fusion_nombre_{cat}",
                        placeholder="Ej: Erling Haaland"
                    )
                    if st.button("🔀 Fusionar", key=f"btn_fusion_{cat}"):
                        if sels_fusion and nombre_fusion.strip():
                            db_fusionar_variantes_especial(cat, sels_fusion, nombre_fusion.strip())
                            st.session_state["msg_esp_adm"] = f"✅ {len(sels_fusion)} variante(s) de {info['label']} unificadas como **{nombre_fusion.strip()}**"
                            st.rerun()
                        else:
                            st.warning("Seleccioná al menos una variante y escribí el nombre oficial.")
                else:
                    st.markdown(f"**{info['label']}** — sin variantes manuales.")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # Form con los selectboxes — solo se guarda al presionar el botón
        with st.form("form_admin_esp_todos"):
            selecciones_adm = {}

            for cat, info in CATEGORIAS_ESPECIALES.items():
                resultado_actual = db_get_resultado_especial(cat)

                col_tit, col_pts = st.columns([4,1])
                col_tit.markdown(f"**{info['label']}**")
                col_pts.markdown(f"<div style='text-align:right; color:#ffd700; font-family:Bebas Neue,sans-serif; font-size:1.1rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)

                # Solo mostrar "guardado" si realmente existe en DB
                if resultado_actual:
                    st.markdown(f"<div style='color:#00e870; font-size:0.82rem; margin-bottom:2px;'>Guardado actualmente: <b>{resultado_actual}</b></div>", unsafe_allow_html=True)

                if cat == "campeon":
                    ops_adm = [f"{bandera(e)} {e}" for e in equipos_adm]
                    d2n_adm = {f"{bandera(e)} {e}": e for e in equipos_adm}
                    # Si no hay resultado guardado, índice 0 (primer equipo, no pre-seleccionado como guardado)
                    idx_adm = next((i for i,e in enumerate(equipos_adm) if e == resultado_actual), 0)
                    sel_adm = st.selectbox("Nuevo campeón real", ops_adm, index=idx_adm, key=f"adm_sel_{cat}")
                    selecciones_adm[cat] = d2n_adm.get(sel_adm, sel_adm)
                else:
                    lista_adm = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
                    label_adm = "arquero" if cat == "arquero" else "jugador"
                    busq = filtros_adm.get(cat, "")
                    db_extra = []
                    if not df_esp_adm.empty and cat in df_esp_adm["categoria"].values:
                        sub_adm = df_esp_adm[df_esp_adm["categoria"] == cat]
                        db_extra = [e for e in sub_adm["eleccion"].unique() if e not in lista_adm]
                    lista_con_extra = lista_adm + db_extra
                    filtrados_adm = [j for j in lista_con_extra if busq.lower() in j.lower()] if busq else lista_con_extra
                    opciones_adm = ["— Seleccioná —"] + filtrados_adm + ["— Otro —"]
                    # Si hay resultado guardado, pre-seleccionarlo; si no, dejar en "Seleccioná"
                    if resultado_actual and resultado_actual in filtrados_adm:
                        idx_adm = filtrados_adm.index(resultado_actual) + 1  # +1 por el "Seleccioná"
                    elif resultado_actual and resultado_actual not in lista_adm:
                        idx_adm = len(opciones_adm) - 1  # "Otro"
                    else:
                        idx_adm = 0  # "Seleccioná"
                    sel_adm = st.selectbox(f"Nuevo {label_adm} real", opciones_adm, index=idx_adm, key=f"adm_sel_{cat}")
                    if sel_adm == "— Otro —":
                        otro_adm = st.text_input(f"Nombre del {label_adm}", value=resultado_actual if resultado_actual and resultado_actual not in lista_adm else "", key=f"adm_otro_{cat}")
                        selecciones_adm[cat] = otro_adm.strip() if otro_adm.strip() else None
                    elif sel_adm == "— Seleccioná —":
                        selecciones_adm[cat] = None
                    else:
                        selecciones_adm[cat] = sel_adm

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            st.divider()
            pw_esp_adm = st.text_input("🔒 Tu contraseña de admin para confirmar", type="password", key="pw_guardar_esp")
            guardar_todos_esp = st.form_submit_button("💾 Guardar todos y aplicar puntos", type="primary")

        if guardar_todos_esp:
            admin_esp = db_get_usuario(st.session_state.usuario)
            if admin_esp["clave"] != hash_clave(pw_esp_adm):
                st.session_state["msg_esp_adm"] = "❌ Contraseña incorrecta."
            else:
                guardados = 0
                for cat, ganador in selecciones_adm.items():
                    if ganador:
                        db_guardar_resultado_especial(cat, ganador)
                        guardados += 1
                if guardados:
                    db_calcular_puntos_especiales()
                    st.session_state["msg_esp_adm"] = f"✅ {guardados} resultado(s) guardado(s) y puntos aplicados."
                else:
                    st.session_state["msg_esp_adm"] = "⚠️ No seleccionaste ningún ganador."
            st.rerun()

        # ── Limpiar resultados especiales ──
        st.divider()
        resultados_esp_actuales = {cat: db_get_resultado_especial(cat) for cat in CATEGORIAS_ESPECIALES}
        if any(v for v in resultados_esp_actuales.values()):
            with st.form("form_limpiar_especiales"):
                st.warning("⚠️ Esto borrará TODOS los resultados especiales cargados y recalculará los puntajes.")
                pw_limp_esp = st.text_input("Tu contraseña de admin para confirmar", type="password", key="pw_limpiar_esp")
                limpiar_esp_btn = st.form_submit_button("🗑️ Limpiar resultados especiales", type="primary")
            if limpiar_esp_btn:
                admin_le = db_get_usuario(st.session_state.usuario)
                if admin_le["clave"] != hash_clave(pw_limp_esp):
                    st.session_state["msg_esp_adm"] = "❌ Contraseña incorrecta."
                else:
                    db_limpiar_resultados_especiales()
                    db_calcular_puntos()
                    st.session_state["msg_esp_adm"] = "🗑️ Resultados especiales eliminados y puntajes recalculados."
                st.rerun()

    with tabs[7]:
        st.subheader("👤 Gestión de usuarios")

        if "msg_usuarios" in st.session_state:
            st.success(st.session_state.pop("msg_usuarios"))
        if "err_usuarios" in st.session_state:
            st.error(st.session_state.pop("err_usuarios"))

        accion = st.radio("Acción", ["➕ Crear", "✏️ Editar", "🔑 Contraseña", "🗑️ Borrar"],
                          horizontal=True, key="accion_usuarios")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        meses_es_adm = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

        # ── CREAR ──
        if accion == "➕ Crear":
            with st.form("form_crear_usuario"):
                st.markdown("**Cuenta**")
                nu_user  = st.text_input("Username", placeholder="mínimo 3 caracteres, sin espacios")
                nu_pass  = st.text_input("Contraseña", type="password", placeholder="mínimo 4 caracteres")
                nu_pass2 = st.text_input("Confirmar contraseña", type="password")
                st.markdown("**Datos personales**")
                nu_nombre = st.text_input("Nombre y apellido")
                nu_mail   = st.text_input("Mail")
                nu_cel    = st.text_input("Celular")
                nu_loc    = st.text_input("Localidad")
                st.markdown("**Fecha de nacimiento**")
                col_y, col_m, col_d = st.columns(3)
                nu_anio = col_y.selectbox("Año", list(range(1930, datetime.date.today().year+1))[::-1], key="nu_anio")
                nu_mes  = col_m.selectbox("Mes", list(range(1,13)), format_func=lambda x: meses_es_adm[x-1], key="nu_mes")
                nu_dia  = col_d.selectbox("Día", list(range(1,32)), key="nu_dia")
                nu_admin = st.checkbox("Es administrador")
                crear_btn = st.form_submit_button("➕ Crear usuario", type="primary")

            if crear_btn:
                u_strip = nu_user.strip().lower()
                try:
                    nu_nac = str(datetime.date(nu_anio, nu_mes, nu_dia))
                except ValueError:
                    nu_nac = ""
                if not u_strip or len(u_strip) < 3:
                    st.session_state["err_usuarios"] = "El username debe tener al menos 3 caracteres."
                elif not re.match(r'^[a-zA-Z0-9._-]+$', u_strip):
                    st.session_state["err_usuarios"] = "Username solo puede tener letras, números, puntos, guiones."
                elif db_get_usuario(u_strip):
                    st.session_state["err_usuarios"] = f"El username '{u_strip}' ya existe."
                elif len(nu_pass) < 4:
                    st.session_state["err_usuarios"] = "La contraseña debe tener al menos 4 caracteres."
                elif nu_pass != nu_pass2:
                    st.session_state["err_usuarios"] = "Las contraseñas no coinciden."
                elif not nu_nombre.strip():
                    st.session_state["err_usuarios"] = "El nombre es obligatorio."
                elif not nu_nac:
                    st.session_state["err_usuarios"] = "Fecha de nacimiento inválida."
                else:
                    with get_db() as conn:
                        cur = conn.cursor()
                        cur.execute("""
                            INSERT INTO usuarios (username, clave, nombre, mail, celular, localidad, nacimiento, es_admin)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (u_strip, hash_clave(nu_pass), nu_nombre.strip(),
                              nu_mail.strip(), nu_cel.strip(), nu_loc.strip(), nu_nac, 1 if nu_admin else 0))
                    st.cache_data.clear()
                    st.session_state["msg_usuarios"] = f"✅ Usuario **{u_strip}** creado."
                    st.rerun()

        # ── EDITAR ──
        elif accion == "✏️ Editar":
            busq_ed = st.text_input("Buscar usuario", key="busq_editar", placeholder="Nombre o username...")
            todos_ed = db_get_todos_usuarios()
            if busq_ed:
                todos_ed = [u for u in todos_ed if busq_ed.lower() in u["username"].lower() or busq_ed.lower() in (u.get("nombre") or "").lower()]
            if not todos_ed:
                st.info("Escribí para buscar un usuario.")
            elif busq_ed:
                opts_ed = {u["username"]: f"{u.get('nombre') or u['username']} (@{u['username']})" for u in todos_ed}
                sel_ed = st.selectbox("Seleccioná", list(opts_ed.keys()), format_func=lambda x: opts_ed[x], key="sel_editar")
                u_ed = db_get_usuario(sel_ed)
                if u_ed:
                    # Parsear nacimiento existente
                    nac_str = u_ed.get("nacimiento") or ""
                    try:
                        nac_date = datetime.date.fromisoformat(nac_str)
                        nac_anio, nac_mes, nac_dia = nac_date.year, nac_date.month, nac_date.day
                    except Exception:
                        nac_anio, nac_mes, nac_dia = 1990, 1, 1
                    with st.form("form_editar_usuario"):
                        ed_nombre = st.text_input("Nombre y apellido", value=u_ed.get("nombre") or "")
                        ed_mail   = st.text_input("Mail",     value=u_ed.get("mail")     or "")
                        ed_cel    = st.text_input("Celular",  value=u_ed.get("celular")  or "")
                        ed_loc    = st.text_input("Localidad",value=u_ed.get("localidad")or "")
                        st.markdown("**Fecha de nacimiento**")
                        col_y2, col_m2, col_d2 = st.columns(3)
                        ed_anio = col_y2.selectbox("Año", list(range(1930, datetime.date.today().year+1))[::-1],
                                                   index=list(range(1930, datetime.date.today().year+1))[::-1].index(nac_anio) if nac_anio in range(1930, datetime.date.today().year+1) else 0,
                                                   key="ed_anio")
                        ed_mes  = col_m2.selectbox("Mes", list(range(1,13)), index=nac_mes-1,
                                                   format_func=lambda x: meses_es_adm[x-1], key="ed_mes")
                        ed_dia  = col_d2.selectbox("Día", list(range(1,32)), index=nac_dia-1, key="ed_dia")
                        guardar_ed = st.form_submit_button("💾 Guardar cambios", type="primary")
                    if guardar_ed:
                        try:
                            ed_nac = str(datetime.date(ed_anio, ed_mes, ed_dia))
                        except ValueError:
                            ed_nac = nac_str
                        if not ed_nombre.strip():
                            st.session_state["err_usuarios"] = "El nombre no puede estar vacío."
                        else:
                            with get_db() as conn:
                                cur = conn.cursor()
                                cur.execute("""
                                    UPDATE usuarios SET nombre=%s, mail=%s, celular=%s, localidad=%s, nacimiento=%s
                                    WHERE username=%s
                                """, (ed_nombre.strip(), ed_mail.strip(), ed_cel.strip(), ed_loc.strip(), ed_nac, sel_ed))
                            st.cache_data.clear()
                            st.session_state["msg_usuarios"] = f"✅ Datos de **{sel_ed}** actualizados."
                            st.rerun()

        # ── CAMBIAR CONTRASEÑA ──
        elif accion == "🔑 Contraseña":
            busq_pw = st.text_input("Buscar usuario", key="busq_clave", placeholder="Nombre o username...")
            todos_pw = db_get_todos_usuarios()
            if busq_pw:
                todos_pw = [u for u in todos_pw if busq_pw.lower() in u["username"].lower() or busq_pw.lower() in (u.get("nombre") or "").lower()]
            if not todos_pw:
                st.info("Escribí para buscar un usuario.")
            elif busq_pw:
                opts_pw = {u["username"]: f"{u.get('nombre') or u['username']} (@{u['username']})" for u in todos_pw}
                sel_pw = st.selectbox("Seleccioná", list(opts_pw.keys()), format_func=lambda x: opts_pw[x], key="sel_clave")
                with st.form("form_reset_clave"):
                    nueva_pw  = st.text_input("Nueva contraseña", type="password")
                    nueva_pw2 = st.text_input("Confirmar nueva contraseña", type="password")
                    resetear_pw = st.form_submit_button("🔑 Cambiar contraseña", type="primary")
                if resetear_pw:
                    if len(nueva_pw) < 4:
                        st.session_state["err_usuarios"] = "Mínimo 4 caracteres."
                    elif nueva_pw != nueva_pw2:
                        st.session_state["err_usuarios"] = "Las contraseñas no coinciden."
                    else:
                        db_reset_clave(sel_pw, nueva_pw)
                        st.session_state["msg_usuarios"] = f"✅ Contraseña de **{sel_pw}** actualizada."
                        st.rerun()

        # ── BORRAR ──
        elif accion == "🗑️ Borrar":
            st.warning("⚠️ Irreversible — se borran el usuario y todos sus pronósticos.")
            busq_del = st.text_input("Buscar usuario", key="busq_borrar", placeholder="Nombre o username...")
            todos_del = db_get_todos_usuarios()
            if busq_del:
                todos_del = [u for u in todos_del if busq_del.lower() in u["username"].lower() or busq_del.lower() in (u.get("nombre") or "").lower()]
            if not todos_del:
                st.info("Escribí para buscar un usuario.")
            elif busq_del:
                opts_del = {u["username"]: f"{u.get('nombre') or u['username']} (@{u['username']})" for u in todos_del}
                sel_del = st.selectbox("Seleccioná el usuario a borrar", list(opts_del.keys()), format_func=lambda x: opts_del[x], key="sel_borrar")
                with st.form("form_borrar_usuario"):
                    clave_adm_del = st.text_input("Tu contraseña de admin", type="password")
                    borrar_btn = st.form_submit_button("🗑️ Borrar usuario", type="primary")
                if borrar_btn:
                    admin_u = db_get_usuario(st.session_state.usuario)
                    if admin_u["clave"] != hash_clave(clave_adm_del):
                        st.session_state["err_usuarios"] = "Contraseña incorrecta."
                    else:
                        db_borrar_usuario(sel_del)
                        st.cache_data.clear()
                        st.session_state["msg_usuarios"] = f"✅ Usuario **{sel_del}** borrado."
                    st.rerun()

    with tabs[8]:
        st.subheader("⚠️ Resetear todos los puntajes")
        st.error("Esta acción borrará TODOS los pronósticos, resultados y puntajes de todos los usuarios. No se puede deshacer.")
        with st.form("form_reset_general"):
            clave_admin_r = st.text_input("Tu contraseña de admin para confirmar", type="password")
            confirmar_r = st.text_input("Escribí CONFIRMAR para continuar")
            resetear_todo = st.form_submit_button("⚠️ Resetear todo", type="primary")
        if resetear_todo:
            admin = db_get_usuario(st.session_state.usuario)
            if admin["clave"] != hash_clave(clave_admin_r):
                st.error("Contraseña incorrecta.")
            elif confirmar_r != "CONFIRMAR":
                st.error('Tenés que escribir exactamente CONFIRMAR para continuar.')
            else:
                db_resetear_todos_puntajes()
                st.success("✅ Todos los puntajes, pronósticos y resultados fueron reseteados.")

    with tabs[9]:
        st.subheader("📥 Base de datos de usuarios")
        st.caption("Todos los usuarios aprobados con sus datos personales.")

        todos_exp = db_get_todos_usuarios()
        if not todos_exp:
            st.info("No hay usuarios registrados todavía.")
        else:
            # Construir dataframe con todos los campos útiles
            rows_exp = []
            for u in todos_exp:
                rows_exp.append({
                    "Usuario": u.get("username", ""),
                    "Nombre": u.get("nombre", ""),
                    "Nacimiento": u.get("nacimiento", ""),
                    "Localidad": u.get("localidad", ""),
                    "Celular": u.get("celular", ""),
                    "Mail": u.get("mail", ""),
                    "Puntos": u.get("puntos", 0),
                    "Goles": u.get("goles", 0),
                    "Consumo": u.get("consumo", 0),
                    "Total": u.get("puntos", 0) + u.get("goles", 0) + u.get("consumo", 0),
                })
            df_exp = pd.DataFrame(rows_exp)

            # Métricas rápidas
            col_e1, col_e2, col_e3 = st.columns(3)
            col_e1.metric("Total usuarios", len(df_exp))
            col_e2.metric("Con mail", df_exp["Mail"].apply(lambda x: bool(x)).sum())
            col_e3.metric("Con celular", df_exp["Celular"].apply(lambda x: bool(x)).sum())
            st.divider()

            # Filtros
            col_f1, col_f2 = st.columns(2)
            filtro_nombre = col_f1.text_input("Buscar por nombre o usuario", key="exp_filtro_nombre")
            filtro_localidad = col_f2.text_input("Filtrar por localidad", key="exp_filtro_loc")

            df_filtrado = df_exp.copy()
            if filtro_nombre:
                mask = (
                    df_filtrado["Nombre"].str.contains(filtro_nombre, case=False, na=False) |
                    df_filtrado["Usuario"].str.contains(filtro_nombre, case=False, na=False)
                )
                df_filtrado = df_filtrado[mask]
            if filtro_localidad:
                df_filtrado = df_filtrado[df_filtrado["Localidad"].str.contains(filtro_localidad, case=False, na=False)]

            st.caption(f"Mostrando {len(df_filtrado)} de {len(df_exp)} usuarios")
            st.dataframe(df_filtrado[["Usuario","Nombre","Nacimiento","Localidad","Celular","Mail"]], use_container_width=True, hide_index=True)

            st.divider()
            # Botón de descarga CSV
            # Solo datos de registro, sin puntos. Sep punto y coma para Excel en español
            cols_registro = ["Usuario", "Nombre", "Nacimiento", "Localidad", "Celular", "Mail"]
            csv_completo = df_exp[cols_registro].to_csv(index=False, sep=";").encode("utf-8-sig")
            csv_filtrado = df_filtrado[cols_registro].to_csv(index=False, sep=";").encode("utf-8-sig")

            col_d1, col_d2 = st.columns(2)
            col_d1.download_button(
                label="⬇️ Descargar todos (CSV)",
                data=csv_completo,
                file_name="usuarios_prode_completo.csv",
                mime="text/csv",
                use_container_width=True,
            )
            col_d2.download_button(
                label="⬇️ Descargar filtrados (CSV)",
                data=csv_filtrado,
                file_name="usuarios_prode_filtrado.csv",
                mime="text/csv",
                use_container_width=True,
            )
            st.caption("El CSV incluye: usuario, nombre, nacimiento, localidad, celular y mail. Abre directo en Excel.")

    st.divider()
    col1, col2 = st.columns(2)
    col1.button("Ver Ranking", on_click=cambiar_pantalla, args=(6,))
    col2.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,))


def pantalla_acerca():
    st.title("ℹ️ Acerca del Prode Il Baigo - Mundial 2026")
    st.subheader("⚽ ¿Cómo funciona?")
    st.markdown("""
Pronosticás el resultado de cada partido antes de que empiece.
Una vez que el partido arranca, tu pronóstico queda bloqueado y no podés modificarlo.
Podés guardar un borrador y después confirmarlo con tu contraseña cuando estés seguro.
""")
    st.divider()
    st.subheader("🏆 Sistema de puntos")
    st.markdown("Los puntos **aumentan por fase**. Cuanto más avanzada la etapa, más valen los aciertos.")
    fases_pts = ["Grupos","Dieciseisavos","Octavos","Cuartos","Semifinal","Final"]
    res_pts = [1, 2, 3, 4, 5, 6]
    exacto_pts = [3, 6, 9, 12, 15, 18]
    filas_pts = ""
    for i, fase in enumerate(fases_pts):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        filas_pts += f'<tr style="background:{bg};"><td style="padding:10px 14px; color:#ffffff; font-weight:600;">{fase}</td><td style="padding:10px 14px; color:#66ccff; font-weight:700; text-align:center;">{res_pts[i]}</td><td style="padding:10px 14px; color:#00e870; font-weight:700; text-align:center;">{exacto_pts[i]}</td></tr>'
    st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); margin-bottom:1rem;">
        <thead><tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
            <th style="padding:10px 14px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Fase</th>
            <th style="padding:10px 14px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">✅ Resultado</th>
            <th style="padding:10px 14px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">🎯 Exacto</th>
        </tr></thead><tbody>{filas_pts}</tbody></table>""", unsafe_allow_html=True)
    st.caption("**Resultado** = acertás quién gana o si es empate.")
    st.caption("**Exacto** = acertás el marcador exacto (ambos goles). Solo suma si acertás local Y visitante.")
    st.caption("Ejemplo Grupos: pronóstico 2-1, real 2-1 → 1 pt + 3 pts = **4 puntos**")
    st.caption("Ejemplo Final: pronóstico 2-1, real 2-1 → 6 pts + 18 pts = **24 puntos**")
    st.caption("Ejemplo Octavos: pronóstico 1-0, real 3-0 → 3 pts + 0 pts = **3 puntos**")
    st.divider()
    st.subheader("⭐ Pronósticos especiales")
    st.markdown("Al completar los grupos, podés elegir el **campeón**, **goleador**, **mejor arquero** y **mejor jugador** del torneo. Confirmás junto con los grupos y no se pueden modificar después.")
    fases_esp = [("🏆 Campeón del Mundial", 20), ("⚽ Goleador del Mundial", 10), ("🧤 Mejor Arquero", 8), ("⭐ Mejor Jugador (MVP)", 8)]
    filas_esp_acerca = ""
    for i, (lbl, pts) in enumerate(fases_esp):
        bg_e = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        filas_esp_acerca += f'<tr style="background:{bg_e};"><td style="padding:10px 14px; color:#ffffff; font-weight:600;">{lbl}</td><td style="padding:10px 14px; color:#ffd700; font-weight:700; text-align:center;">+{pts} pts</td></tr>'
    st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); margin-bottom:0.5rem;">
        <thead><tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
            <th style="padding:10px 14px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Categoría</th>
            <th style="padding:10px 14px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Puntos si acertás</th>
        </tr></thead><tbody>{filas_esp_acerca}</tbody></table>""", unsafe_allow_html=True)
    st.caption("Para goleador, arquero y MVP podés buscar por nombre. Si no lo encontrás en la lista, usá la opción **Otro** y escribilo a mano.")
    st.divider()
    st.subheader("💰 Puntos de consumo")
    st.markdown("Además de los pronósticos, el admin puede sumar puntos por consumo en el local o presencia en los partidos. Estos puntos se suman al total y cuentan para el ranking.")
    st.divider()
    st.subheader("📊 Ranking")
    st.markdown("El ranking se actualiza automáticamente cada vez que el admin carga resultados reales. El total es la suma de: **puntos por resultados + puntos por goles + puntos por consumo + especiales**.")
    st.divider()
    st.subheader("📋 Fases del torneo")
    for fase, desc in {
        "Grupos": "72 partidos — 12 grupos de 4 equipos cada uno",
        "Dieciseisavos": "16 partidos — eliminación directa",
        "Octavos": "8 partidos — eliminación directa",
        "Cuartos": "4 partidos — eliminación directa",
        "Semifinal": "2 partidos — eliminación directa",
        "Final": "1 partido — la gran final",
    }.items():
        st.markdown(f"**{fase}:** {desc}")
    st.divider()
    st.subheader("❓ Preguntas frecuentes")
    with st.expander("¿Puedo modificar mi pronóstico después de confirmarlo?"):
        st.write("No. Una vez que confirmás con tu contraseña, el pronóstico queda bloqueado definitivamente.")
    with st.expander("¿Qué pasa si no cargo pronósticos para una fase?"):
        st.write("No sumás puntos para esa fase. Te recomendamos cargar y confirmar antes de que empiece el primer partido.")
    with st.expander("¿Hasta cuándo puedo cargar mi pronóstico?"):
        st.write("El admin controla manualmente cuándo se cierra cada fase. Mientras la fase esté habilitada podés cargar y modificar tus pronósticos.")
    with st.expander("¿Cómo se registra el consumo?"):
        st.write("El admin lo carga manualmente desde el panel. Si creés que falta registrar tu consumo, contactá al organizador.")
    with st.expander("¿Olvidé mi contraseña, qué hago?"):
        st.write("Contactá al administrador por fuera de la app para que te resetee la contraseña.")
    st.divider()
    st.button("Volver", on_click=cambiar_pantalla, args=(0,))



def pantalla_especiales():
    username = st.session_state.usuario
    u = db_get_usuario(username)

    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 0.5rem 0;">
        <div style="font-family:'Bebas Neue',sans-serif; font-size:2.8rem; letter-spacing:4px;
                    background:linear-gradient(135deg,#ffd700,#ffaa00);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">⭐ PRONÓSTICOS ESPECIALES</div>
        <div style="color:#606075; font-size:0.85rem; letter-spacing:2px; text-transform:uppercase; margin-top:0.3rem;">
            Elegí antes del inicio del torneo — puntos extra garantizados
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Puntos por categoría
    equipos = db_get_equipos_grupos()
    # Si no hay equipos cargados todavía usamos lista completa
    if not equipos:
        equipos = sorted([k for k in BANDERAS.keys()])

    jugadores_populares = JUGADORES_MUNDIALISTAS
    arqueros_populares = ARQUEROS_MUNDIALISTAS

    st.divider()

    for cat, info in CATEGORIAS_ESPECIALES.items():
        esp = db_get_especial(username, cat)
        confirmado = esp and esp["confirmado"] == 1
        eleccion_actual = esp["eleccion"] if esp else None
        resultado_real = db_get_resultado_especial(cat)

        # Card por categoría
        color_card = "rgba(255,200,0,0.05)" if confirmado else "rgba(255,255,255,0.02)"
        border_card = "rgba(255,200,0,0.3)" if confirmado else "rgba(255,255,255,0.08)"

        st.markdown(f"""
        <div style="background:{color_card}; border:1px solid {border_card};
                    border-radius:14px; padding:16px 20px; margin:10px 0;">
        """, unsafe_allow_html=True)

        col_titulo, col_pts = st.columns([4, 1])
        col_titulo.markdown(f"### {info['label']}")
        col_pts.markdown(f"<div style='text-align:right; padding-top:8px; color:#ffd700; font-family:Bebas Neue,sans-serif; font-size:1.4rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)

        if resultado_real:
            acierto = eleccion_actual == resultado_real
            icono = "🎯" if acierto else "❌"
            st.markdown(f"**Resultado oficial:** {resultado_real} {icono}")
            if eleccion_actual:
                st.markdown(f"**Tu pronóstico:** {eleccion_actual}")

        elif confirmado:
            st.success(f"✅ Confirmado: **{eleccion_actual}**")

        else:
            # Formulario editable
            with st.form(f"form_esp_{cat}"):
                if cat == "campeon":
                    opciones = [f"{bandera(e)} {e}" for e in equipos]
                    disp_a_nombre = {f"{bandera(e)} {e}": e for e in equipos}
                    idx_actual = next((i for i, e in enumerate(equipos) if e == eleccion_actual), 0)
                    sel = st.selectbox("Seleccioná el equipo", opciones, index=idx_actual, key=f"sel_{cat}")
                    eleccion_nueva = disp_a_nombre.get(sel, sel)

                elif cat == "goleador":
                    eleccion_nueva = selectbox_busqueda("Jugador", jugadores_populares, f"esp_{cat}", eleccion_actual)

                elif cat == "arquero":
                    eleccion_nueva = selectbox_busqueda("Arquero", arqueros_populares, f"esp_{cat}", eleccion_actual)

                else:  # jugador MVP
                    eleccion_nueva = selectbox_busqueda("Jugador", jugadores_populares, f"esp_{cat}", eleccion_actual)

                clave_confirm = st.text_input("Contraseña para confirmar (dejá vacío para solo guardar)", type="password", key=f"pw_{cat}")
                col_b1, col_b2 = st.columns(2)
                guardar_btn = col_b1.form_submit_button("💾 Guardar borrador")
                confirmar_btn = col_b2.form_submit_button("🔒 Confirmar", type="primary")

            if guardar_btn and eleccion_nueva:
                db_guardar_especial(username, cat, eleccion_nueva)
                st.success("Borrador guardado.")
                st.rerun()

            if confirmar_btn:
                if not eleccion_nueva:
                    st.error("Seleccioná una opción primero.")
                elif hash_clave(clave_confirm) != u["clave"]:
                    st.error("Contraseña incorrecta.")
                else:
                    db_guardar_especial(username, cat, eleccion_nueva)
                    db_confirmar_especial(username, cat)
                    st.success(f"✅ Confirmado: {eleccion_nueva}")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    col1.button("← Volver", on_click=cambiar_pantalla, args=(5,))
    col2.button("Ver Ranking", on_click=cambiar_pantalla, args=(6,))


def pantalla_estadisticas():
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 0.5rem 0;">
        <div style="font-family:'Bebas Neue',sans-serif; font-size:2.8rem; letter-spacing:4px;
                    background:linear-gradient(135deg,#00c850,#00ff88);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">📊 ESTADÍSTICAS</div>
        <div style="color:#606075; font-size:0.85rem; letter-spacing:2px; text-transform:uppercase;">Mundial 2026 — Il Baigo</div>
    </div>
    """, unsafe_allow_html=True)

    gen = db_get_estadisticas_generales()
    col1, col2, col3 = st.columns(3)
    col1.metric("Participantes", gen["total_usuarios"])
    col2.metric("Confirmaron grupos", gen["confirmaron"])
    col3.metric("Partidos jugados", gen["partidos_jugados"])

    # ── Pronósticos especiales ──
    esp_stats = db_get_estadisticas_especiales()
    if esp_stats:
        st.divider()
        st.subheader("⭐ Pronósticos especiales — ¿qué eligió la gente?")
        for cat, info in CATEGORIAS_ESPECIALES.items():
            datos = esp_stats.get(cat, [])
            if not datos:
                continue
            total_votos = sum(d["votos"] for d in datos)
            resultado_real = db_get_resultado_especial(cat)
            st.markdown(f"**{info['label']}**")
            filas = ""
            for i, d in enumerate(datos[:10]):
                pct = round(d["votos"] / total_votos * 100) if total_votos else 0
                es_ganador = resultado_real and d["eleccion"] == resultado_real
                bg_row = "rgba(0,200,80,0.07)" if es_ganador else ("rgba(255,255,255,0.03)" if i % 2 == 0 else "transparent")
                check = "✅ " if es_ganador else ""
                bar_width = max(4, pct)
                filas += f"""<tr style="background:{bg_row};">
                    <td style="padding:8px 12px; color:#fff; font-weight:{'700' if es_ganador else '400'}; width:40%;">{check}{d['eleccion']}</td>
                    <td style="padding:8px 12px; width:45%;">
                        <div style="background:rgba(255,255,255,0.08); border-radius:4px; height:8px; overflow:hidden;">
                            <div style="background:{'#00c850' if es_ganador else '#378ADD'}; width:{bar_width}%; height:100%; border-radius:4px;"></div>
                        </div>
                    </td>
                    <td style="padding:8px 12px; color:#a0a0b8; text-align:right; font-size:0.85rem;">{pct}% ({d['votos']})</td>
                </tr>"""
            st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:10px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); margin-bottom:1rem;">
                <thead><tr style="background:rgba(255,255,255,0.05);">
                    <th style="padding:8px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Elección</th>
                    <th style="padding:8px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;"></th>
                    <th style="padding:8px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; text-align:right;">%</th>
                </tr></thead><tbody>{filas}</tbody></table>""", unsafe_allow_html=True)

    # ── Partidos ──
    part_stats = db_get_estadisticas_partidos()
    if part_stats:
        st.divider()
        st.subheader("⚽ Partidos — aciertos de la gente")

        # Top partidos con más exactos
        con_prodes = [p for p in part_stats if p["total_prodes"] and p["total_prodes"] > 0]
        if con_prodes:
            # Calcular % exacto y % resultado
            for p in con_prodes:
                p["pct_exacto"] = round(p["exactos"] / p["total_prodes"] * 100) if p["total_prodes"] else 0
                p["pct_res"]    = round(p["resultados"] / p["total_prodes"] * 100) if p["total_prodes"] else 0

            # Cargar nombres de partidos
            partidos_db = {}
            for fase in FASES:
                for pd_ in db_get_partidos(fase):
                    partidos_db[(fase, pd_["idx"])] = pd_

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("**🎯 Los más adivinados (exacto)**")
                top_exactos = sorted(con_prodes, key=lambda x: x["pct_exacto"], reverse=True)[:5]
                filas_e = ""
                for p in top_exactos:
                    pd_ = partidos_db.get((p["fase"], p["partido_idx"]), {})
                    nombre = f"{pd_.get('local','?')} vs {pd_.get('visita','?')}" if pd_ else f"{p['fase']} #{p['partido_idx']}"
                    resultado = f"{p['rl']}—{p['rv']}"
                    filas_e += f"""<tr>
                        <td style="padding:7px 10px; color:#fff; font-size:0.82rem;">{nombre}</td>
                        <td style="padding:7px 10px; color:#606075; font-size:0.8rem; text-align:center;">{resultado}</td>
                        <td style="padding:7px 10px; color:#00e870; font-weight:700; text-align:right;">{p['pct_exacto']}%</td>
                    </tr>"""
                st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:10px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);">
                    <thead><tr style="background:rgba(255,255,255,0.05);">
                        <th style="padding:7px 10px; color:#606075; font-size:0.7rem; text-transform:uppercase; text-align:left;">Partido</th>
                        <th style="padding:7px 10px; color:#606075; font-size:0.7rem; text-transform:uppercase; text-align:center;">Res.</th>
                        <th style="padding:7px 10px; color:#606075; font-size:0.7rem; text-transform:uppercase; text-align:right;">Exacto</th>
                    </tr></thead><tbody>{filas_e}</tbody></table>""", unsafe_allow_html=True)

            with col_t2:
                st.markdown("**❌ Los que nadie adivinó**")
                top_dificiles = sorted(con_prodes, key=lambda x: x["pct_res"])[:5]
                filas_d = ""
                for p in top_dificiles:
                    pd_ = partidos_db.get((p["fase"], p["partido_idx"]), {})
                    nombre = f"{pd_.get('local','?')} vs {pd_.get('visita','?')}" if pd_ else f"{p['fase']} #{p['partido_idx']}"
                    resultado = f"{p['rl']}—{p['rv']}"
                    filas_d += f"""<tr>
                        <td style="padding:7px 10px; color:#fff; font-size:0.82rem;">{nombre}</td>
                        <td style="padding:7px 10px; color:#606075; font-size:0.8rem; text-align:center;">{resultado}</td>
                        <td style="padding:7px 10px; color:#ff6b6b; font-weight:700; text-align:right;">{p['pct_res']}%</td>
                    </tr>"""
                st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:10px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);">
                    <thead><tr style="background:rgba(255,255,255,0.05);">
                        <th style="padding:7px 10px; color:#606075; font-size:0.7rem; text-transform:uppercase; text-align:left;">Partido</th>
                        <th style="padding:7px 10px; color:#606075; font-size:0.7rem; text-transform:uppercase; text-align:center;">Res.</th>
                        <th style="padding:7px 10px; color:#606075; font-size:0.7rem; text-transform:uppercase; text-align:right;">Acertaron</th>
                    </tr></thead><tbody>{filas_d}</tbody></table>""", unsafe_allow_html=True)

            # Resumen por fase
            st.divider()
            st.markdown("**📋 Rendimiento por fase**")
            fases_stats = {}
            for p in con_prodes:
                fase = p["fase"]
                if fase not in fases_stats:
                    fases_stats[fase] = {"exactos": 0, "resultados": 0, "total": 0, "partidos": 0}
                fases_stats[fase]["exactos"]    += p["exactos"]
                fases_stats[fase]["resultados"] += p["resultados"]
                fases_stats[fase]["total"]      += p["total_prodes"]
                fases_stats[fase]["partidos"]   += 1

            filas_f = ""
            for fase in FASES:
                if fase not in fases_stats:
                    continue
                fs = fases_stats[fase]
                pct_res = round(fs["resultados"] / fs["total"] * 100) if fs["total"] else 0
                pct_ex  = round(fs["exactos"]    / fs["total"] * 100) if fs["total"] else 0
                filas_f += f"""<tr>
                    <td style="padding:9px 12px; color:#fff; font-weight:600;">{fase}</td>
                    <td style="padding:9px 12px; color:#a0a0b8; text-align:center;">{fs['partidos']}</td>
                    <td style="padding:9px 12px; color:#66aaff; text-align:center;">{pct_res}%</td>
                    <td style="padding:9px 12px; color:#00e870; text-align:center;">{pct_ex}%</td>
                </tr>"""
            st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:#0f0f1a; border-radius:10px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);">
                <thead><tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
                    <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; text-align:left;">Fase</th>
                    <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; text-align:center;">Partidos</th>
                    <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; text-align:center;">% Resultado</th>
                    <th style="padding:9px 12px; color:#606075; font-size:0.72rem; text-transform:uppercase; text-align:center;">% Exacto</th>
                </tr></thead><tbody>{filas_f}</tbody></table>""", unsafe_allow_html=True)

    if not esp_stats and not part_stats:
        st.info("Las estadísticas se van completando a medida que se juegan los partidos y el admin carga los resultados.")

    st.divider()
    destino = 9 if st.session_state.get("usuario") == "admin" else 5
    st.button("← Volver", on_click=cambiar_pantalla, args=(destino,))


# -----------------------
# ROUTER
# -----------------------
PANTALLAS = {
    0: pantalla_login, 1: pantalla_registro_datos, 2: pantalla_registro_cuenta,
    4: pantalla_en_revision, 5: pantalla_usuario, 6: pantalla_ranking,
    9: pantalla_admin, 10: pantalla_acerca, 11: pantalla_especiales, 12: pantalla_estadisticas,
}

inject_css()
pantalla_fn = PANTALLAS.get(st.session_state.step)
if pantalla_fn:
    pantalla_fn()
else:
    st.error("Pantalla no encontrada.")
    cambiar_pantalla(0)
