"""
db.py — Conexión, pool y todas las funciones de acceso a la base de datos.
Optimizado: invalidación quirúrgica de cache en lugar de clear() global.
"""
import datetime
import hashlib
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
        db_get_config.clear(clave, None)
        db_get_config.clear(clave, "dark")
        db_get_config.clear(clave, "1")
        db_get_config.clear(clave, "0")
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


@st.cache_data(ttl=300)
def db_get_equipos_grupos():
    import re
    partidos = db_get_partidos("Grupos")
    equipos = sorted(set(
        e for p in partidos for e in [p["local"], p["visita"]]
        if e and not re.match(r'^rep\d*$', e.lower())
    ))
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
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM pendientes WHERE id=%s", (pid,))
        row = cur.fetchone()
        if not row:
            return
        cur.execute("""
            INSERT INTO usuarios (username, clave, nombre, nacimiento, localidad, celular, mail)
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (username) DO NOTHING
        """, (row["username"], row["clave"], row["nombre"], row["nacimiento"],
              row["localidad"], row["celular"], row["mail"]))
        cur.execute("DELETE FROM pendientes WHERE id=%s", (pid,))
    try:
        db_get_pendientes.clear()
        db_get_todos_usuarios.clear()
    except Exception:
        pass


def db_rechazar_pendiente(pid):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM pendientes WHERE id=%s", (pid,))
    try:
        db_get_pendientes.clear()
    except Exception:
        pass


# ─── Consumo ──────────────────────────────────────────────────────────────────

def db_sumar_consumo(username, puntos, descripcion=""):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET consumo=consumo+%s WHERE username=%s", (puntos, username))
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cur.execute(
            "INSERT INTO consumo_log (username, puntos, descripcion, fecha) VALUES (%s, %s, %s, %s)",
            (username, puntos, descripcion, fecha)
        )
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
    """Recalcula puntos de partidos. Preserva puntos de especiales ya calculados."""
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
            ),
            pts_esp AS (
                SELECT username, SUM(info_pts) AS pts_especiales
                FROM (
                    SELECT e.username,
                           CASE e.categoria
                               WHEN 'campeon'  THEN 20
                               WHEN 'goleador' THEN 10
                               WHEN 'arquero'  THEN 8
                               WHEN 'jugador'  THEN 8
                               ELSE 0
                           END AS info_pts
                    FROM especiales e
                    JOIN especiales_resultados er ON er.categoria = e.categoria AND er.resultado = e.eleccion
                    WHERE e.confirmado = 1
                ) sub GROUP BY username
            )
            UPDATE usuarios u
            SET puntos = COALESCE(c.puntos, 0) + COALESCE(pe.pts_especiales, 0),
                goles  = COALESCE(c.goles, 0)
            FROM (
                SELECT u2.username,
                       COALESCE(c2.puntos, 0) AS puntos,
                       COALESCE(c2.goles, 0)  AS goles
                FROM usuarios u2
                LEFT JOIN calc c2 ON c2.username = u2.username
                WHERE u2.es_admin = 0
            ) c
            LEFT JOIN pts_esp pe ON pe.username = c.username
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
    _invalidar_resultado_especial(categoria)


def db_calcular_puntos_especiales():
    """Suma puntos especiales. Seguro contra doble ejecución — guarda en config cuáles categorías ya fueron calculadas."""
    with get_db() as conn:
        cur = conn.cursor()
        for cat, info in CATEGORIAS_ESPECIALES.items():
            resultado = db_get_resultado_especial(cat)
            if not resultado:
                continue
            # Verificar si ya se calculó esta categoría
            cur.execute("SELECT valor FROM config WHERE clave=%s", (f"esp_calculado_{cat}",))
            row = cur.fetchone()
            if row and row["valor"] == resultado:
                continue  # Ya calculado para este resultado, saltar
            cur.execute("""
                UPDATE usuarios SET puntos = puntos + %s
                WHERE username IN (
                    SELECT username FROM especiales
                    WHERE categoria=%s AND eleccion=%s AND confirmado=1
                )
            """, (info["puntos"], cat, resultado))
            # Marcar como calculado
            cur.execute(
                "INSERT INTO config (clave, valor) VALUES (%s, %s) ON CONFLICT (clave) DO UPDATE SET valor=EXCLUDED.valor",
                (f"esp_calculado_{cat}", resultado)
            )
    try:
        db_get_todos_usuarios.clear()
        db_get_puntos_especiales_usuarios.clear()
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