import streamlit as st
import pandas as pd
import datetime
import hashlib
import os
import re
import sqlite3
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
# BASE DE DATOS SQLite
# -----------------------
DB_FILE = "prode.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY, clave TEXT NOT NULL, nombre TEXT,
            nacimiento TEXT, localidad TEXT, celular TEXT, mail TEXT,
            puntos INTEGER DEFAULT 0, goles INTEGER DEFAULT 0,
            consumo INTEGER DEFAULT 0, es_admin INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS pendientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, clave TEXT,
            nombre TEXT, nacimiento TEXT, localidad TEXT, celular TEXT, mail TEXT, comprobante TEXT
        );
        CREATE TABLE IF NOT EXISTS fases (
            nombre TEXT PRIMARY KEY, habilitada INTEGER DEFAULT 0, orden INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fase TEXT, idx INTEGER,
            local TEXT, visita TEXT, fecha TEXT, hora TEXT, UNIQUE(fase, idx)
        );
        CREATE TABLE IF NOT EXISTS resultados (
            fase TEXT, partido_idx INTEGER,
            goles_local INTEGER DEFAULT 0, goles_visita INTEGER DEFAULT 0,
            PRIMARY KEY (fase, partido_idx)
        );
        CREATE TABLE IF NOT EXISTS prodes (
            username TEXT, fase TEXT, partido_idx INTEGER,
            goles_local INTEGER DEFAULT 0, goles_visita INTEGER DEFAULT 0,
            confirmado INTEGER DEFAULT 0, PRIMARY KEY (username, fase, partido_idx)
        );
        CREATE TABLE IF NOT EXISTS config (clave TEXT PRIMARY KEY, valor TEXT);
        CREATE TABLE IF NOT EXISTS consumo_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,
            puntos INTEGER, descripcion TEXT, fecha TEXT
        );
        """)
        for i, f in enumerate(["Grupos","Dieciseisavos","Octavos","Cuartos","Semifinal","Final"]):
            conn.execute("INSERT OR IGNORE INTO fases (nombre, habilitada, orden) VALUES (?, ?, ?)",
                         (f, 1 if f == "Grupos" else 0, i))
        admin_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
        conn.execute("INSERT OR IGNORE INTO usuarios (username, clave, nombre, es_admin) VALUES (?, ?, ?, ?)",
                     ("admin", hash_clave(admin_pass), "Admin", 1))
        conn.execute("INSERT OR IGNORE INTO usuarios (username, clave, nombre, es_admin) VALUES (?, ?, ?, ?)",
                     ("prueba", hash_clave("1234"), "Prueba", 0))

def hash_clave(clave: str) -> str:
    return hashlib.sha256(clave.encode()).hexdigest()

def db_get_config(clave, default=None):
    with get_db() as conn:
        row = conn.execute("SELECT valor FROM config WHERE clave=?", (clave,)).fetchone()
        return row["valor"] if row else default

def db_set_config(clave, valor):
    with get_db() as conn:
        conn.execute("INSERT INTO config (clave, valor) VALUES (?, ?) ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor", (clave, valor))

def db_registro_abierto():
    return db_get_config("registro_abierto", "1") == "1"

def db_get_consumo_log(username=None):
    with get_db() as conn:
        if username:
            rows = conn.execute("SELECT * FROM consumo_log WHERE username=? ORDER BY id DESC", (username,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM consumo_log ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]

def db_get_usuario(username):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM usuarios WHERE username=?", (username,)).fetchone()
        return dict(row) if row else None

def db_get_fases():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM fases ORDER BY orden").fetchall()
        return {r["nombre"]: bool(r["habilitada"]) for r in rows}

def db_toggle_fase(nombre, valor):
    with get_db() as conn:
        conn.execute("UPDATE fases SET habilitada=? WHERE nombre=?", (1 if valor else 0, nombre))

def db_get_partidos(fase):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM partidos WHERE fase=? ORDER BY idx", (fase,)).fetchall()
        return [dict(r) for r in rows]

def db_guardar_partido(fase, idx, local, visita, fecha="", hora=""):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO partidos (fase, idx, local, visita, fecha, hora) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(fase, idx) DO UPDATE SET local=excluded.local, visita=excluded.visita,
            fecha=excluded.fecha, hora=excluded.hora
        """, (fase, idx, local, visita, fecha, hora))

def db_get_resultado(fase, idx):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM resultados WHERE fase=? AND partido_idx=?", (fase, idx)).fetchone()
        return (row["goles_local"], row["goles_visita"]) if row else (0, 0)

def db_guardar_resultado(fase, idx, gl, gv):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO resultados (fase, partido_idx, goles_local, goles_visita) VALUES (?, ?, ?, ?)
            ON CONFLICT(fase, partido_idx) DO UPDATE SET goles_local=excluded.goles_local, goles_visita=excluded.goles_visita
        """, (fase, idx, gl, gv))

def db_get_prode(username, fase):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM prodes WHERE username=? AND fase=?", (username, fase)).fetchall()
        if not rows:
            return {"pred": {}, "confirmado": False}
        confirmado = bool(rows[0]["confirmado"])
        pred = {r["partido_idx"]: (r["goles_local"], r["goles_visita"]) for r in rows}
        return {"pred": pred, "confirmado": confirmado}

def db_guardar_pred(username, fase, idx, gl, gv):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO prodes (username, fase, partido_idx, goles_local, goles_visita, confirmado)
            VALUES (?, ?, ?, ?, ?, 0)
            ON CONFLICT(username, fase, partido_idx) DO UPDATE SET
            goles_local=excluded.goles_local, goles_visita=excluded.goles_visita
        """, (username, fase, idx, gl, gv))

def db_confirmar_prode(username, fase):
    with get_db() as conn:
        conn.execute("UPDATE prodes SET confirmado=1 WHERE username=? AND fase=?", (username, fase))
        conn.execute("""
            INSERT OR IGNORE INTO prodes (username, fase, partido_idx, goles_local, goles_visita, confirmado)
            VALUES (?, ?, -1, 0, 0, 1)
        """, (username, fase))

def db_fase_confirmada(username, fase):
    with get_db() as conn:
        row = conn.execute(
            "SELECT confirmado FROM prodes WHERE username=? AND fase=? AND confirmado=1 LIMIT 1",
            (username, fase)).fetchone()
        return bool(row)

def db_get_pendientes():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM pendientes ORDER BY id").fetchall()
        return [dict(r) for r in rows]

def db_agregar_pendiente(data):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO pendientes (username, clave, nombre, nacimiento, localidad, celular, mail, comprobante)
            VALUES (:username, :clave, :nombre, :nacimiento, :localidad, :celular, :mail, :comprobante)
        """, data)

def db_aprobar_pendiente(pid):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM pendientes WHERE id=?", (pid,)).fetchone()
        if not row:
            return
        conn.execute("""
            INSERT OR IGNORE INTO usuarios (username, clave, nombre, nacimiento, localidad, celular, mail)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row["username"], row["clave"], row["nombre"], row["nacimiento"],
              row["localidad"], row["celular"], row["mail"]))
        conn.execute("DELETE FROM pendientes WHERE id=?", (pid,))

def db_rechazar_pendiente(pid):
    with get_db() as conn:
        conn.execute("DELETE FROM pendientes WHERE id=?", (pid,))

def db_get_todos_usuarios():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM usuarios WHERE es_admin=0").fetchall()
        return [dict(r) for r in rows]

def db_reset_clave(username, nueva_clave):
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET clave=? WHERE username=?", (hash_clave(nueva_clave), username))

def db_borrar_usuario(username):
    with get_db() as conn:
        conn.execute("DELETE FROM usuarios WHERE username=?", (username,))
        conn.execute("DELETE FROM prodes WHERE username=?", (username,))

def db_resetear_todos_puntajes():
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET puntos=0, goles=0, consumo=0 WHERE es_admin=0")
        conn.execute("DELETE FROM prodes")
        conn.execute("DELETE FROM resultados")
        conn.execute("DELETE FROM consumo_log")

def db_sumar_consumo(username, puntos, descripcion=""):
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET consumo=consumo+? WHERE username=?", (puntos, username))
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        conn.execute("INSERT INTO consumo_log (username, puntos, descripcion, fecha) VALUES (?, ?, ?, ?)",
                     (username, puntos, descripcion, fecha))

def db_eliminar_consumo_log(log_id):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM consumo_log WHERE id=?", (log_id,)).fetchone()
        if row:
            conn.execute("UPDATE usuarios SET consumo=MAX(0, consumo-?) WHERE username=?", (row["puntos"], row["username"]))
            conn.execute("DELETE FROM consumo_log WHERE id=?", (log_id,))

def db_get_resultado_completo(fase):
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM resultados WHERE fase=?", (fase,)).fetchall()
        return {r["partido_idx"]: (r["goles_local"], r["goles_visita"]) for r in rows}

def db_calcular_puntos():
    for u in db_get_todos_usuarios():
        username = u["username"]
        puntos = goles = 0
        for fase in db_get_fases():
            if not db_fase_confirmada(username, fase):
                continue
            prode = db_get_prode(username, fase)
            resultados = db_get_resultado_completo(fase)
            mult = {"Grupos":1,"Dieciseisavos":2,"Octavos":3,"Cuartos":4,"Semifinal":5,"Final":6}.get(fase, 1)
            for idx, (rl, rv) in resultados.items():
                if idx not in prode["pred"]:
                    continue
                gl, gv = prode["pred"][idx]
                if (gl > gv and rl > rv) or (gl < gv and rl < rv) or (gl == gv and rl == rv):
                    puntos += 1 * mult
                if gl == rl and gv == rv:
                    goles += 3 * mult
        with get_db() as conn:
            conn.execute("UPDATE usuarios SET puntos=?, goles=? WHERE username=?", (puntos, goles, username))

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
init_db()

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

    if "reg_error" in st.session_state:
        st.error(st.session_state.pop("reg_error"))

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
        col1, col2 = st.columns(2)
        volver = col1.form_submit_button("Volver")
        enviar = col2.form_submit_button("Enviar", type="primary")

    if "reg_error" in st.session_state:
        st.error(st.session_state.pop("reg_error"))

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
            comprobante_dir = "comprobantes"
            os.makedirs(comprobante_dir, exist_ok=True)
            ext = os.path.splitext(comprobante.name)[-1]
            ruta = os.path.join(comprobante_dir, f"{u_strip}{ext}")
            with open(ruta, "wb") as f:
                f.write(comprobante.getbuffer())
            db_agregar_pendiente({
                "username": u_strip, "clave": hash_clave(clave), "comprobante": ruta,
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
            # Vista solo lectura — igual que siempre
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
            # ── Vista editable: 3 columnas, number_input nativo en el centro ──
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

    # ── Render partidos ──────────────────────────────────────────────
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
            gi = max(0, min(st.session_state.grupo_wizard, len(grupos_con_partidos) - 1))
            letra = grupos_con_partidos[gi]
            total = len(grupos_con_partidos)

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
                nav2.markdown("<div style='text-align:center; color:#00e870; font-size:0.85rem; padding-top:8px;'>✅ Último grupo — confirmá abajo</div>", unsafe_allow_html=True)
    else:
        for p in partidos:
            render_partido(p)

    # ── Confirmación / borrador ──────────────────────────────────────
    if not confirmado:
        st.divider()
        with st.form("form_confirmar"):
            clave_confirm = st.text_input("Ingresá tu contraseña para confirmar", type="password")
            col_f1, col_f2 = st.columns(2)
            confirmar_btn = col_f1.form_submit_button("🔒 Confirmar prode", type="primary")
            borrador_btn = col_f2.form_submit_button("💾 Guardar borrador")

        if confirmar_btn:
            if hash_clave(clave_confirm) == u["clave"]:
                for idx, (gl, gv) in cambios.items():
                    db_guardar_pred(username, fase, idx, gl, gv)
                db_confirmar_prode(username, fase)
                st.session_state["wizard_grupos_completo"] = True
                st.success("¡Pronósticos confirmados! Ya no se pueden modificar.")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

        if borrador_btn:
            for idx, (gl, gv) in cambios.items():
                db_guardar_pred(username, fase, idx, gl, gv)
            st.success("Borrador guardado.")
    else:
        st.success("✅ Pronósticos confirmados para esta fase.")

    # ── Puntos y ranking ────────────────────────────────────────────
    if not grupos_completados:
        st.divider()
        st.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,))
        return

    st.divider()
    u_fresh = db_get_usuario(username)
    total_pts = u_fresh["puntos"] + u_fresh["goles"] + u_fresh["consumo"]
    todos = db_get_todos_usuarios()
    ranking = sorted(todos, key=lambda x: x["puntos"] + x["goles"] + x["consumo"], reverse=True)
    posicion = next((i + 1 for i, x in enumerate(ranking) if x["username"] == username), "—")

    st.subheader("Mis puntos")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Resultados", u_fresh["puntos"])
    col_b.metric("Goles", u_fresh["goles"])
    col_c.metric("Consumo", u_fresh["consumo"])
    col_d.metric("Total", total_pts)
    st.info(f"🏆 Posición actual: **{posicion}° de {len(ranking)}**")

    st.divider()
    col1, col2 = st.columns(2)
    col1.button("Ver Ranking", on_click=cambiar_pantalla, args=(6,))
    col2.button("Cerrar sesión", on_click=cambiar_pantalla, args=(0,))


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

        rows = []
        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        for i, u in enumerate(ranking):
            pos = i + 1
            total = u["puntos"] + u["goles"] + u["consumo"]
            rows.append({"Pos": medallas.get(pos, str(pos)), "Nombre": u.get("nombre") or u["username"],
                         "Resultados": u["puntos"], "Goles": u["goles"], "Consumo": u["consumo"],
                         "Total": total, "_username": u["username"], "_pos": pos})

        df = pd.DataFrame(rows)
        top_n = st.slider("Mostrar top", 5, max(10, len(df)), min(10, len(df)))

        filas_html = ""
        for r in rows[:top_n]:
            es_yo = r["_username"] == username_actual
            bg = "rgba(0,200,80,0.08)" if es_yo else "transparent"
            border_left = "3px solid #00c850" if es_yo else "3px solid transparent"
            filas_html += f"""
            <tr style="background:{bg}; border-left:{border_left};">
                <td style="padding:10px 12px; color:#ffffff; font-weight:700; font-size:1.1rem;">{r['Pos']}</td>
                <td style="padding:10px 12px; color:#ffffff; font-weight:600;">{r['Nombre']}</td>
                <td style="padding:10px 12px; color:#a0a0b8; text-align:center;">{r['Resultados']}</td>
                <td style="padding:10px 12px; color:#a0a0b8; text-align:center;">{r['Goles']}</td>
                <td style="padding:10px 12px; color:#a0a0b8; text-align:center;">{r['Consumo']}</td>
                <td style="padding:10px 12px; color:#00e870; font-weight:700; font-size:1.1rem; text-align:center;">{r['Total']}</td>
            </tr>"""

        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; background:#0f0f1a;
                      border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);">
            <thead><tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid rgba(255,255,255,0.1);">
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Pos</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:left;">Nombre</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Res.</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Goles</th>
                <th style="padding:10px 12px; color:#606075; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Cons.</th>
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
    tabs = st.tabs(["📋 Resumen", "👥 Pendientes", "🔀 Fases", "⚽ Partidos", "📊 Result.", "💰 Consumo", "🔑 Claves", "🗑️ Borrar", "⚠️ Reset"])

    with tabs[0]:
        st.subheader("Resumen general")
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
            db_calcular_puntos(); st.success("Puntajes recalculados correctamente.")

    with tabs[1]:
        st.subheader("Solicitudes pendientes")
        pendientes = db_get_pendientes()
        if not pendientes:
            st.info("No hay solicitudes pendientes.")
        for pend in pendientes:
            with st.expander(f"👤 {pend['username']} — {pend.get('nombre', '')}"):
                st.write(f"**Mail:** {pend.get('mail', '—')}")
                st.write(f"**Celular:** {pend.get('celular', '—')}")
                st.write(f"**Localidad:** {pend.get('localidad', '—')}")
                st.write(f"**Nacimiento:** {pend.get('nacimiento', '—')}")
                st.write(f"**Desde:** {pend.get('desde', '—')}")
                comp = pend.get("comprobante", "")
                if comp and os.path.exists(comp):
                    ext = os.path.splitext(comp)[-1].lower()
                    if ext in (".png", ".jpg", ".jpeg", ".webp"):
                        st.image(comp, caption="Comprobante")
                    else:
                        with open(comp, "rb") as f:
                            st.download_button("Descargar comprobante", f, file_name=os.path.basename(comp), key=f"dl_{pend['id']}")
                c1, c2 = st.columns(2)
                if c1.button("✅ Aprobar", key=f"ap_{pend['id']}"):
                    db_aprobar_pendiente(pend["id"]); st.success(f"{pend['username']} aprobado."); st.rerun()
                if c2.button("❌ Rechazar", key=f"re_{pend['id']}"):
                    db_rechazar_pendiente(pend["id"]); st.warning(f"{pend['username']} rechazado."); st.rerun()

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
            grupo_sel = st.selectbox("Grupo", [f"Grupo {l}" for l in "ABCDEFGHIJKL"])
            letra = grupo_sel[-1]
            inicio = "ABCDEFGHIJKL".index(letra) * 6
            partidos_existentes = db_get_partidos("Grupos")
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
                st.success(f"Grupo {letra} guardado.")
            if guardar_todos:
                st.session_state["confirmar_guardar_todos"] = True
            if st.session_state.get("confirmar_guardar_todos"):
                st.warning("⚠️ Esto sobreescribirá los partidos de todos los grupos. ¿Confirmar?")
                col_c1, col_c2 = st.columns(2)
                if col_c1.button("✅ Sí, guardar todos", key="si_guardar_todos"):
                    for gr, partidos_gr in GRUPOS_DEFAULT.items():
                        ini_gr = "ABCDEFGHIJKL".index(gr) * 6
                        for j, (loc, vis) in enumerate(partidos_gr):
                            db_guardar_partido("Grupos", ini_gr + j, loc, vis)
                    st.session_state.pop("confirmar_guardar_todos", None)
                    st.success("Todos los grupos guardados."); st.rerun()
                if col_c2.button("❌ Cancelar", key="no_guardar_todos"):
                    st.session_state.pop("confirmar_guardar_todos", None); st.rerun()

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
                        st.session_state["res_ok"] = f"✅ {p['local']} {rl} — {rv} {p['visita']}"
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

    with tabs[5]:
        st.subheader("Sumar consumo")
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
                    st.success(f"Se sumaron {pts} puntos de consumo a {opts[sel]}.")
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
                st.success(f"Registro #{int(id_eliminar)} eliminado y puntos descontados."); st.rerun()

    with tabs[6]:
        st.subheader("Resetear contraseña de usuario")
        busq_clave = st.text_input("Buscar usuario", key="busq_clave")
        if busq_clave:
            todos_f = db_get_todos_usuarios()
            opts_f = {u["username"]: u.get("nombre") or u["username"] for u in todos_f
                      if busq_clave.lower() in u["username"].lower() or busq_clave.lower() in (u.get("nombre") or "").lower()}
            if opts_f:
                with st.form("form_reset_clave"):
                    sel = st.selectbox("Usuario", list(opts_f.keys()), format_func=lambda x: f"{opts_f[x]} ({x})")
                    nueva = st.text_input("Nueva contraseña", type="password")
                    confirmar = st.text_input("Confirmar nueva contraseña", type="password")
                    resetear = st.form_submit_button("🔑 Resetear contraseña", type="primary")
                if resetear:
                    if len(nueva) < 4:
                        st.error("La contraseña debe tener al menos 4 caracteres.")
                    elif nueva != confirmar:
                        st.error("Las contraseñas no coinciden.")
                    else:
                        db_reset_clave(sel, nueva)
                        st.success(f"✅ Contraseña de **{opts_f[sel]}** reseteada.")
            else:
                st.warning("No se encontró ningún usuario.")

    with tabs[7]:
        st.subheader("🗑️ Borrar usuario")
        st.warning("Esta acción es irreversible. Se borrarán el usuario y todos sus pronósticos.")
        busq_borrar = st.text_input("Buscar usuario", key="busq_borrar")
        if busq_borrar:
            todos_b = db_get_todos_usuarios()
            opts_b = {u["username"]: u.get("nombre") or u["username"] for u in todos_b
                      if busq_borrar.lower() in u["username"].lower() or busq_borrar.lower() in (u.get("nombre") or "").lower()}
            if opts_b:
                with st.form("form_borrar_usuario"):
                    sel_b = st.selectbox("Usuario a borrar", list(opts_b.keys()), format_func=lambda x: f"{opts_b[x]} ({x})")
                    clave_admin_b = st.text_input("Tu contraseña de admin para confirmar", type="password")
                    borrar = st.form_submit_button("🗑️ Borrar usuario", type="primary")
                if borrar:
                    admin = db_get_usuario(st.session_state.usuario)
                    if admin["clave"] != hash_clave(clave_admin_b):
                        st.error("Contraseña incorrecta.")
                    else:
                        db_borrar_usuario(sel_b)
                        st.success(f"Usuario **{opts_b[sel_b]}** borrado correctamente.")
            else:
                st.warning("No se encontró ningún usuario.")

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
    st.subheader("💰 Puntos de consumo")
    st.markdown("Además de los pronósticos, el admin puede sumar puntos por consumo en el local o comercio participante. Estos puntos se suman al total y cuentan para el ranking.")
    st.divider()
    st.subheader("📊 Ranking")
    st.markdown("El ranking se actualiza automáticamente cada vez que el admin carga resultados reales. El total es la suma de: **puntos por resultados + puntos por goles + puntos por consumo**.")
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


# -----------------------
# ROUTER
# -----------------------
PANTALLAS = {
    0: pantalla_login, 1: pantalla_registro_datos, 2: pantalla_registro_cuenta,
    4: pantalla_en_revision, 5: pantalla_usuario, 6: pantalla_ranking,
    9: pantalla_admin, 10: pantalla_acerca,
}

inject_css()
pantalla_fn = PANTALLAS.get(st.session_state.step)
if pantalla_fn:
    pantalla_fn()
else:
    st.error("Pantalla no encontrada.")
    cambiar_pantalla(0)
