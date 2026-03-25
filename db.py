"""
db.py — Conexión, pool y todas las funciones de acceso a la base de datos.
Optimizado: invalidación quirúrgica de cache en lugar de clear() global.
"""
import datetime
import hashlib
import json
import os

import psycopg2
import psycopg2.extras
import psycopg2.pool
import streamlit as st
from contextlib import contextmanager

from constants import FASES, CATEGORIAS_ESPECIALES


# ─── Conexión ────────────────────────────────────────────────────────────────

def get_db_url():
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        return os.environ.get("DATABASE_URL", "")


@st.cache_resource
def get_connection_pool():
    url = get_db_url()
    if not url:
        st.error("⚠️ No se encontró DATABASE_URL.")
        st.stop()
    return psycopg2.pool.ThreadedConnectionPool(
        minconn=2, maxconn=10, dsn=url,
        cursor_factory=psycopg2.extras.RealDictCursor,
        keepalives=1, keepalives_idle=30,
        keepalives_interval=10, keepalives_count=5,
    )


@contextmanager
def get_db():
    pool = get_connection_pool()
    conn = None
    for intento in range(3):
        try:
            conn = pool.getconn()
            # Verificar que la conexión esté viva
            conn.cursor().execute("SELECT 1")
            break
        except Exception:
            if conn:
                try:
                    pool.putconn(conn, close=True)
                except Exception:
                    pass
                conn = None
            if intento == 2:
                raise
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        if conn:
            pool.putconn(conn)


# ─── Helpers de invalidación quirúrgica ──────────────────────────────────────
# En lugar de clear() global, invalidamos solo las funciones afectadas.
# Esto evita que guardar un pronóstico tire el cache de ranking, fases, etc.

def _invalidar_prode(username, fase):
    db_get_prode.clear(username, fase)
    try:
        db_fase_confirmada.clear(username, fase)
    except Exception:
        pass

def _invalidar_resultados(fase):
    try:
        db_get_resultado_completo.clear(fase)
    except Exception:
        pass

def _invalidar_usuarios():
    try:
        db_get_todos_usuarios.clear()
        db_get_puntos_especiales_usuarios.clear()
    except Exception:
        pass

def _invalidar_especial(username, categoria):
    try:
        db_get_especial.clear(username, categoria)
    except Exception:
        pass

def _invalidar_resultado_especial(categoria):
    try:
        db_get_resultado_especial.clear(categoria)
    except Exception:
        pass


# ─── Inicialización ───────────────────────────────────────────────────────────

@st.cache_resource
def init_tablas():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY, clave TEXT NOT NULL, nombre TEXT,
            nacimiento TEXT, localidad TEXT, celular TEXT, mail TEXT,
            puntos INTEGER DEFAULT 0, goles INTEGER DEFAULT 0,
            consumo INTEGER DEFAULT 0, es_admin INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS pendientes (
            id SERIAL PRIMARY KEY, username TEXT, clave TEXT, nombre TEXT,
            nacimiento TEXT, localidad TEXT, celular TEXT, mail TEXT, comprobante TEXT
        );
        CREATE TABLE IF NOT EXISTS fases (
            nombre TEXT PRIMARY KEY, habilitada INTEGER DEFAULT 0, orden INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS partidos (
            id SERIAL PRIMARY KEY, fase TEXT, idx INTEGER,
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
            confirmado INTEGER DEFAULT 0,
            PRIMARY KEY (username, fase, partido_idx)
        );
        CREATE TABLE IF NOT EXISTS config (clave TEXT PRIMARY KEY, valor TEXT);
        CREATE TABLE IF NOT EXISTS consumo_log (
            id SERIAL PRIMARY KEY, username TEXT, puntos INTEGER,
            descripcion TEXT, fecha TEXT
        );
        CREATE TABLE IF NOT EXISTS especiales (
            username TEXT, categoria TEXT, eleccion TEXT,
            confirmado INTEGER DEFAULT 0, PRIMARY KEY (username, categoria)
        );
        CREATE TABLE IF NOT EXISTS especiales_resultados (
            categoria TEXT PRIMARY KEY, resultado TEXT
        );
        CREATE TABLE IF NOT EXISTS actividad_usuarios (
            username TEXT PRIMARY KEY,
            last_seen TIMESTAMP NOT NULL DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS actividad_feed (
            id SERIAL PRIMARY KEY,
            tipo TEXT DEFAULT 'general',
            username TEXT,
            texto TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS ranking_snapshots (
            id SERIAL PRIMARY KEY,
            posiciones_json TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """)
        for i, f in enumerate(FASES):
            cur.execute(
                "INSERT INTO fases (nombre, habilitada, orden) VALUES (%s, %s, %s) ON CONFLICT (nombre) DO NOTHING",
                (f, 1 if f == "Grupos" else 0, i)
            )


def init_db():
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


# ─── Presencia / usuarios en línea ───────────────────────────────────────────

def _invalidar_actividad():
    try:
        db_get_usuarios_en_linea.clear()
        db_get_cantidad_usuarios_en_linea.clear()
    except Exception:
        pass


def _invalidar_feed():
    try:
        db_get_feed.clear()
    except Exception:
        pass


def _invalidar_ranking_movimientos():
    try:
        db_get_ranking_movimientos.clear()
    except Exception:
        pass


def _nombre_usuario(username):
    usuario = db_get_usuario(username)
    if not usuario:
        return username
    return usuario.get("nombre") or usuario.get("username") or username


def _snapshot_ranking_actual(conn):
    cur = conn.cursor()
    cur.execute("SELECT username, puntos, goles, consumo FROM usuarios WHERE es_admin=0 ORDER BY username")
    usuarios = cur.fetchall()
    cur.execute("SELECT categoria, resultado FROM especiales_resultados")
    resultados_esp = {r["categoria"]: r["resultado"] for r in cur.fetchall() if r.get("resultado")}

    puntos_especiales = {}
    if resultados_esp:
        for cat, info in CATEGORIAS_ESPECIALES.items():
            resultado = resultados_esp.get(cat)
            if not resultado:
                continue
            cur.execute("SELECT username FROM especiales WHERE categoria=%s AND confirmado=1 AND eleccion=%s", (cat, resultado))
            for row in cur.fetchall():
                puntos_especiales[row["username"]] = puntos_especiales.get(row["username"], 0) + int(info.get("puntos", 0))

    ranking = sorted(
        usuarios,
        key=lambda u: int(u["puntos"] or 0) + int(u["goles"] or 0) + int(u["consumo"] or 0) + puntos_especiales.get(u["username"], 0),
        reverse=True,
    )
    return {u["username"]: idx + 1 for idx, u in enumerate(ranking)}


def _guardar_snapshot_ranking():
    with get_db() as conn:
        snapshot = _snapshot_ranking_actual(conn)
        cur = conn.cursor()
        cur.execute("INSERT INTO ranking_snapshots (posiciones_json) VALUES (%s)", (json.dumps(snapshot),))
    _invalidar_ranking_movimientos()


def db_feed_evento(texto, tipo="general", username=None):
    texto = (texto or "").strip()
    if not texto:
        return
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO actividad_feed (tipo, username, texto) VALUES (%s, %s, %s)", (tipo, username, texto))
    _invalidar_feed()


@st.cache_data(ttl=10)
def db_get_feed(limit=12):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, tipo, username, texto, created_at
            FROM actividad_feed
            ORDER BY created_at DESC, id DESC
            LIMIT %s
        """, (limit,))
        return [dict(r) for r in cur.fetchall()]


@st.cache_data(ttl=15)
def db_get_ranking_movimientos():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT posiciones_json FROM ranking_snapshots ORDER BY created_at DESC, id DESC LIMIT 1")
        row = cur.fetchone()
        prev = json.loads(row["posiciones_json"]) if row and row.get("posiciones_json") else {}
        actual = _snapshot_ranking_actual(conn)

    movimientos = {}
    for username, pos_actual in actual.items():
        pos_prev = prev.get(username)
        movimientos[username] = 0 if pos_prev is None else int(pos_prev) - int(pos_actual)
    return movimientos


def db_touch_usuario(username):
    username = (username or "").strip().lower()
    if not username:
        return
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO actividad_usuarios (username, last_seen)
            VALUES (%s, NOW())
            ON CONFLICT (username)
            DO UPDATE SET last_seen = EXCLUDED.last_seen
        """, (username,))
    _invalidar_actividad()


def db_logout_usuario(username):
    username = (username or "").strip().lower()
    if not username:
        return
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM actividad_usuarios WHERE username=%s", (username,))
    _invalidar_actividad()


@st.cache_data(ttl=10)
def db_get_usuarios_en_linea(minutos=2):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.username, u.nombre, u.es_admin, a.last_seen
            FROM actividad_usuarios a
            JOIN usuarios u ON u.username = a.username
            WHERE a.last_seen >= NOW() - (%s * INTERVAL '1 minute')
            ORDER BY a.last_seen DESC
        """, (minutos,))
        return [dict(r) for r in cur.fetchall()]


@st.cache_data(ttl=10)
def db_get_cantidad_usuarios_en_linea(minutos=2):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) AS total
            FROM actividad_usuarios
            WHERE last_seen >= NOW() - (%s * INTERVAL '1 minute')
        """, (minutos,))
        row = cur.fetchone()
        return int(row["total"] if row else 0)


# ─── Config ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=15)
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
    try:
        db_get_config.clear()
        db_get_pago_config.clear()
    except Exception:
        pass


@st.cache_data(ttl=300)
def db_get_pago_config():
    return {
        "titular": db_get_config("pago_titular", "Il Baigo"),
        "alias": db_get_config("pago_alias", "prode.mundial.2026"),
        "cvu": db_get_config("pago_cvu", "0000003100000000000000"),
        "instrucciones": db_get_config("pago_instrucciones", ""),
    }


def db_set_pago_config(titular, alias, cvu, instrucciones=""):
    db_set_config("pago_titular", (titular or "").strip())
    db_set_config("pago_alias", (alias or "").strip())
    db_set_config("pago_cvu", (cvu or "").strip())
    db_set_config("pago_instrucciones", (instrucciones or "").strip())
    try:
        db_get_pago_config.clear()
    except Exception:
        pass


def db_registro_abierto():
    return db_get_config("registro_abierto", "1") == "1"


# ─── Usuarios ─────────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def db_get_usuario(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
        row = cur.fetchone()
        return dict(row) if row else None


@st.cache_data(ttl=120)
def db_get_todos_usuarios():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE es_admin=0")
        return [dict(r) for r in cur.fetchall()]


def db_reset_clave(username, nueva_clave):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET clave=%s WHERE username=%s", (hash_clave(nueva_clave), username))
    try:
        db_get_usuario.clear(username)
    except Exception:
        pass


def db_borrar_usuario(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE username=%s", (username,))
        cur.execute("DELETE FROM prodes WHERE username=%s", (username,))
    try:
        db_get_usuario.clear(username)
        db_get_todos_usuarios.clear()
    except Exception:
        pass


def db_resetear_todos_puntajes():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET puntos=0, goles=0, consumo=0 WHERE es_admin=0")
        cur.execute("DELETE FROM prodes")
        cur.execute("DELETE FROM resultados")
        cur.execute("DELETE FROM consumo_log")
        cur.execute("DELETE FROM especiales")
        cur.execute("DELETE FROM especiales_resultados")
    st.cache_data.clear()  # reset total — OK acá, es acción de admin poco frecuente


# ─── Fases ────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def db_get_fases():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM fases ORDER BY orden")
        return {r["nombre"]: bool(r["habilitada"]) for r in cur.fetchall()}


def db_toggle_fase(nombre, valor):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE fases SET habilitada=%s WHERE nombre=%s", (1 if valor else 0, nombre))
    db_feed_evento(f"Se {'abrió' if valor else 'cerró'} la fase {nombre}", tipo="fase")
    try:
        db_get_fases.clear()
    except Exception:
        st.cache_data.clear()


# ─── Partidos ─────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
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
    try:
        db_get_partidos.clear(fase)
        db_get_equipos_grupos.clear()
    except Exception:
        pass




def db_renombrar_equipo_global(nombre_actual, nuevo_nombre):
    nombre_actual = (nombre_actual or "").strip()
    nuevo_nombre = (nuevo_nombre or "").strip()
    if not nombre_actual or not nuevo_nombre or nombre_actual == nuevo_nombre:
        return

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE partidos SET local=%s WHERE local=%s", (nuevo_nombre, nombre_actual))
        cur.execute("UPDATE partidos SET visita=%s WHERE visita=%s", (nuevo_nombre, nombre_actual))
        cur.execute("UPDATE especiales SET eleccion=%s WHERE eleccion=%s", (nuevo_nombre, nombre_actual))
        cur.execute("UPDATE especiales_resultados SET resultado=%s WHERE resultado=%s", (nuevo_nombre, nombre_actual))

    try:
        db_get_partidos.clear("Grupos")
    except Exception:
        pass
    try:
        db_get_equipos_grupos.clear()
    except Exception:
        pass
    try:
        db_get_todos_especiales.clear()
    except Exception:
        pass
    try:
        db_get_resultado_especial.clear("campeon")
    except Exception:
        pass
@st.cache_data(ttl=300)
def db_get_equipos_grupos():
    partidos = db_get_partidos("Grupos")
    equipos = sorted(
        set(
            str(e).strip()
            for p in partidos
            for e in [p.get("local"), p.get("visita")]
            if e and str(e).strip()
        ),
        key=lambda x: x.lower()
    )
    return equipos


# ─── Resultados ───────────────────────────────────────────────────────────────

def db_guardar_resultado(fase, idx, gl, gv):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO resultados (fase, partido_idx, goles_local, goles_visita) VALUES (%s, %s, %s, %s)
            ON CONFLICT (fase, partido_idx) DO UPDATE SET
            goles_local=EXCLUDED.goles_local, goles_visita=EXCLUDED.goles_visita
        """, (fase, idx, gl, gv))
    db_feed_evento(f"Se cargó un resultado en {fase}: partido #{idx + 1} terminó {gl}-{gv}", tipo="resultado")
    _invalidar_resultados(fase)


@st.cache_data(ttl=30)
def db_get_resultado_completo(fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resultados WHERE fase=%s", (fase,))
        return {r["partido_idx"]: (r["goles_local"], r["goles_visita"]) for r in cur.fetchall()}


def db_limpiar_resultados_fase(fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM resultados WHERE fase=%s", (fase,))
    _invalidar_resultados(fase)


def db_limpiar_resultados_especiales():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM especiales_resultados")
    try:
        db_get_estadisticas_especiales.clear()
    except Exception:
        pass
    for cat in CATEGORIAS_ESPECIALES:
        _invalidar_resultado_especial(cat)


# ─── Pronósticos ──────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def db_get_prode(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM prodes WHERE username=%s AND fase=%s", (username, fase))
        rows = cur.fetchall()
        if not rows:
            return {"pred": {}, "confirmado": False}
        confirmado = any(r["confirmado"] for r in rows)
        pred = {r["partido_idx"]: (r["goles_local"], r["goles_visita"]) for r in rows}
        return {"pred": pred, "confirmado": confirmado}


def db_guardar_pred(username, fase, idx, gl, gv):
    """Guarda un pronóstico. NO invalida cache global — solo el prode de este usuario/fase."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO prodes (username, fase, partido_idx, goles_local, goles_visita, confirmado)
            VALUES (%s, %s, %s, %s, %s, 0)
            ON CONFLICT (username, fase, partido_idx) DO UPDATE SET
            goles_local=EXCLUDED.goles_local, goles_visita=EXCLUDED.goles_visita
        """, (username, fase, idx, gl, gv))
    _invalidar_prode(username, fase)


def db_confirmar_prode(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE prodes SET confirmado=1 WHERE username=%s AND fase=%s", (username, fase))
        cur.execute("""
            INSERT INTO prodes (username, fase, partido_idx, goles_local, goles_visita, confirmado)
            VALUES (%s, %s, -1, 0, 0, 1)
            ON CONFLICT (username, fase, partido_idx) DO NOTHING
        """, (username, fase))
    db_feed_evento(f"{_nombre_usuario(username)} confirmó sus pronósticos de {fase}", tipo="prode", username=username)
    _invalidar_prode(username, fase)
    _invalidar_usuarios()


@st.cache_data(ttl=60)
def db_fase_confirmada(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT confirmado FROM prodes WHERE username=%s AND fase=%s AND confirmado=1 LIMIT 1",
            (username, fase)
        )
        return bool(cur.fetchone())


def db_limpiar_prode_fase(username, fase):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM prodes WHERE username=%s AND fase=%s AND confirmado=0",
            (username, fase)
        )
    _invalidar_prode(username, fase)


def db_resetear_prodes_fase(fase):
    """Admin: resetea todos los pronósticos confirmados de una fase para que usuarios puedan re-cargar."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM prodes WHERE fase=%s", (fase,))
    try:
        db_fase_confirmada.clear()
        db_get_todos_usuarios.clear()
    except Exception:
        pass


# ─── Pendientes ───────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
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
    try:
        db_get_pendientes.clear()
    except Exception:
        pass


def db_aprobar_pendiente(pid):
    username_aprobado = None
    nombre_aprobado = None
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pendientes WHERE id=%s", (pid,))
        row = cur.fetchone()
        if not row:
            return
        username_aprobado = row["username"]
        nombre_aprobado = row.get("nombre") or row["username"]
        cur.execute("""
            INSERT INTO usuarios (username, clave, nombre, nacimiento, localidad, celular, mail)
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (username) DO NOTHING
        """, (row["username"], row["clave"], row["nombre"], row["nacimiento"],
              row["localidad"], row["celular"], row["mail"]))
        cur.execute("DELETE FROM pendientes WHERE id=%s", (pid,))
    db_feed_evento(f"Se aprobó el ingreso de {nombre_aprobado}", tipo="usuario", username=username_aprobado)
    try:
        db_get_pendientes.clear()
        db_get_todos_usuarios.clear()
    except Exception:
        pass


def db_rechazar_pendiente(pid):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, nombre FROM pendientes WHERE id=%s", (pid,))
        row = cur.fetchone()
        cur.execute("DELETE FROM pendientes WHERE id=%s", (pid,))
    if row:
        db_feed_evento(f"Se rechazó la solicitud de {row.get('nombre') or row['username']}", tipo="usuario", username=row["username"])
    try:
        db_get_pendientes.clear()
    except Exception:
        pass


# ─── Consumo ──────────────────────────────────────────────────────────────────

def db_sumar_consumo(username, puntos, descripcion=""):
    _guardar_snapshot_ranking()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET consumo=consumo+%s WHERE username=%s", (puntos, username))
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cur.execute(
            "INSERT INTO consumo_log (username, puntos, descripcion, fecha) VALUES (%s, %s, %s, %s)",
            (username, puntos, descripcion, fecha)
        )
    db_feed_evento(f"{_nombre_usuario(username)} sumó {puntos} punto{'s' if int(puntos) != 1 else ''} de consumo", tipo="consumo", username=username)
    try:
        db_get_usuario.clear(username)
        db_get_todos_usuarios.clear()
        db_get_consumo_log.clear()
        db_get_consumo_log.clear(username)
    except Exception:
        pass


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
    try:
        db_get_todos_usuarios.clear()
        db_get_consumo_log.clear()
    except Exception:
        pass


@st.cache_data(ttl=20)
def db_get_consumo_log(username=None):
    with get_db() as conn:
        cur = conn.cursor()
        if username:
            cur.execute("SELECT * FROM consumo_log WHERE username=%s ORDER BY id DESC", (username,))
        else:
            cur.execute("SELECT * FROM consumo_log ORDER BY id DESC")
        return [dict(r) for r in cur.fetchall()]


# ─── Puntajes ─────────────────────────────────────────────────────────────────

def db_calcular_puntos():
    """Recalcula solo puntos de partidos y exactos. Los especiales se calculan aparte."""
    _guardar_snapshot_ranking()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            WITH mult (fase, m) AS (
                VALUES
                    ('Grupos',        1),
                    ('Dieciseisavos', 2),
                    ('Octavos',       3),
                    ('Cuartos',       4),
                    ('Semifinal',     5),
                    ('Final',         6)
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
    try:
        db_get_todos_usuarios.clear()
        db_get_puntos_especiales_usuarios.clear()
        db_get_estadisticas_usuarios.clear()
        db_get_estadisticas_generales.clear()
        db_get_estadisticas_partidos.clear()
    except Exception:
        pass


# ─── Especiales ───────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
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
    _invalidar_especial(username, categoria)


def db_confirmar_especial(username, categoria):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE especiales SET confirmado=1 WHERE username=%s AND categoria=%s", (username, categoria))
    db_feed_evento(f"{_nombre_usuario(username)} confirmó un pronóstico especial", tipo="especial", username=username)
    _invalidar_especial(username, categoria)


@st.cache_data(ttl=30)
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
    db_feed_evento(f"Se publicó el resultado especial de {categoria}", tipo="especial")
    _invalidar_resultado_especial(categoria)


def db_calcular_puntos_especiales():
    """
    No suma nada en usuarios.puntos.
    Solo invalida caches porque los especiales se leen dinámicamente
    desde db_get_puntos_especiales_usuarios().
    """
    _guardar_snapshot_ranking()
    try:
        db_get_todos_usuarios.clear()
        db_get_puntos_especiales_usuarios.clear()
        db_get_estadisticas_usuarios.clear()
        db_get_estadisticas_generales.clear()
    except Exception:
        pass


def db_fusionar_variantes_especial(cat, variantes, nombre_oficial):
    if not variantes:
        return
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE especiales SET eleccion=%s WHERE categoria=%s AND eleccion = ANY(%s)",
            (nombre_oficial, cat, variantes)
        )
    try:
        db_get_estadisticas_especiales.clear()
    except Exception:
        pass


def db_get_todos_especiales():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM especiales ORDER BY username, categoria")
        return [dict(r) for r in cur.fetchall()]


def db_limpiar_especiales(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM especiales WHERE username=%s AND confirmado=0", (username,))
    for cat in CATEGORIAS_ESPECIALES:
        _invalidar_especial(username, cat)


@st.cache_data(ttl=120)
def db_get_puntos_especiales_usuarios():
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


# ─── Ver pronósticos de otros usuarios ───────────────────────────────────────

@st.cache_data(ttl=60)
def db_get_prodes_fase_todos(fase):
    """Devuelve pronósticos confirmados de todos los usuarios para una fase."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, u.nombre, p.partido_idx,
                   p.goles_local, p.goles_visita
            FROM prodes p
            JOIN usuarios u ON u.username = p.username
            WHERE p.fase = %s AND p.confirmado = 1 AND p.partido_idx >= 0
            ORDER BY p.username, p.partido_idx
        """, (fase,))
        rows = cur.fetchall()
    result = {}
    for r in rows:
        uname = r["username"]
        if uname not in result:
            result[uname] = {"nombre": r["nombre"] or uname, "pred": {}}
        result[uname]["pred"][r["partido_idx"]] = (r["goles_local"], r["goles_visita"])
    return result


# ─── Estadísticas ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def db_get_estadisticas_especiales():
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
            LEFT JOIN prodes p ON p.fase = r.fase AND p.partido_idx = r.partido_idx
                AND p.confirmado = 1 AND p.partido_idx >= 0
            GROUP BY r.fase, r.partido_idx, r.goles_local, r.goles_visita
        """)
        return [dict(r) for r in cur.fetchall()]


@st.cache_data(ttl=60)
def db_get_estadisticas_generales():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as total FROM usuarios WHERE es_admin=0")
        total_usuarios = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(DISTINCT username) as total FROM prodes WHERE confirmado=1 AND partido_idx=-1")
        confirmaron = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) as total FROM resultados")
        partidos_jugados = cur.fetchone()["total"]
    return {
        "total_usuarios": total_usuarios,
        "confirmaron": confirmaron,
        "partidos_jugados": partidos_jugados,
    }


@st.cache_data(ttl=60)
def db_get_estadisticas_usuarios():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username,
                   SUM(CASE WHEN
                       (p.goles_local > p.goles_visita AND r.goles_local > r.goles_visita) OR
                       (p.goles_local < p.goles_visita AND r.goles_local < r.goles_visita) OR
                       (p.goles_local = p.goles_visita AND r.goles_local = r.goles_visita)
                   THEN 1 ELSE 0 END) AS resultados
            FROM prodes p
            JOIN resultados r ON r.fase = p.fase AND r.partido_idx = p.partido_idx
            JOIN usuarios u ON u.username = p.username AND u.es_admin = 0
            WHERE p.confirmado = 1 AND p.partido_idx >= 0
            GROUP BY p.username ORDER BY resultados DESC
        """)
        top_resultados = [dict(r) for r in cur.fetchall()]
        cur.execute("""
            SELECT p.username,
                   SUM(CASE WHEN p.goles_local = r.goles_local AND p.goles_visita = r.goles_visita
                   THEN 1 ELSE 0 END) AS exactos
            FROM prodes p
            JOIN resultados r ON r.fase = p.fase AND r.partido_idx = p.partido_idx
            JOIN usuarios u ON u.username = p.username AND u.es_admin = 0
            WHERE p.confirmado = 1 AND p.partido_idx >= 0
            GROUP BY p.username ORDER BY exactos DESC
        """)
        top_exactos = [dict(r) for r in cur.fetchall()]
        cur.execute("""
            SELECT p.username,
                   SUM(CASE WHEN
                       (p.goles_local > p.goles_visita AND r.goles_local > r.goles_visita) OR
                       (p.goles_local < p.goles_visita AND r.goles_local < r.goles_visita) OR
                       (p.goles_local = p.goles_visita AND r.goles_local = r.goles_visita)
                   THEN 1 ELSE 0 END) +
                   SUM(CASE WHEN p.goles_local = r.goles_local AND p.goles_visita = r.goles_visita
                   THEN 1 ELSE 0 END) AS puntos_grupos
            FROM prodes p
            JOIN resultados r ON r.fase = p.fase AND r.partido_idx = p.partido_idx
            JOIN usuarios u ON u.username = p.username AND u.es_admin = 0
            WHERE p.confirmado = 1 AND p.partido_idx >= 0 AND p.fase = 'Grupos'
            GROUP BY p.username ORDER BY puntos_grupos DESC
        """)
        top_grupos = [dict(r) for r in cur.fetchall()]
        cur.execute("""
            SELECT p.username,
                   SUM(CASE WHEN
                       (p.goles_local > p.goles_visita AND r.goles_local > r.goles_visita) OR
                       (p.goles_local < p.goles_visita AND r.goles_local < r.goles_visita) OR
                       (p.goles_local = p.goles_visita AND r.goles_local = r.goles_visita)
                   THEN 1 ELSE 0 END) +
                   SUM(CASE WHEN p.goles_local = r.goles_local AND p.goles_visita = r.goles_visita
                   THEN 1 ELSE 0 END) AS puntos_finales
            FROM prodes p
            JOIN resultados r ON r.fase = p.fase AND r.partido_idx = p.partido_idx
            JOIN usuarios u ON u.username = p.username AND u.es_admin = 0
            WHERE p.confirmado = 1 AND p.partido_idx >= 0
              AND p.fase IN ('Dieciseisavos','Octavos','Cuartos','Semifinal','Final')
            GROUP BY p.username ORDER BY puntos_finales DESC
        """)
        top_finales = [dict(r) for r in cur.fetchall()]

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, nombre FROM usuarios WHERE es_admin=0")
        nombres_map = {r["username"]: (r["nombre"] or r["username"]) for r in cur.fetchall()}

    def enrich(lst, key):
        return [{"nombre": nombres_map.get(r["username"], r["username"]),
                 "valor": r.get(key) or 0, "username": r["username"]}
                for r in lst if (r.get(key) or 0) > 0]

    return {
        "top_resultados": enrich(top_resultados, "resultados"),
        "top_exactos":    enrich(top_exactos,    "exactos"),
        "top_grupos":     enrich(top_grupos,      "puntos_grupos"),
        "top_finales":    enrich(top_finales,     "puntos_finales"),
    }