# screens_stats.py FINAL (UI FIXED)

from collections import Counter
import streamlit as st
from constants import bandera

try:
    from streamlit_autorefresh import st_autorefresh
except Exception:
    st_autorefresh = None

from db import (
    db_get_estadisticas_usuarios,
    db_get_estadisticas_partidos,
    db_get_partidos,
    db_get_ranking_snapshot,
    db_get_tipo_usuario,
    db_get_todos_especiales,
)

def cambiar_pantalla(step):
    st.session_state.step = step

def _destino_panel():
    usuario = st.session_state.get("usuario")
    return 9 if db_get_tipo_usuario(usuario) in ("admin", "consumo") else 5

# ─────────────────────────────
# TOP ESPECIALES
# ─────────────────────────────

def _top_especiales(counter_obj):
    total = sum(counter_obj.values())
    top = counter_obj.most_common(3)
    usados = sum(v for _, v in top)
    otros = total - usados

    resultado = []
    for i, (nombre, votos) in enumerate(top, 1):
        pct = (votos / total * 100) if total else 0
        resultado.append((i, nombre, votos, pct))

    if otros > 0:
        pct = (otros / total * 100) if total else 0
        resultado.append(("otros", "Otros", otros, pct))

    return resultado

def _render_top_especiales(titulo, data, color, bg, border):
    st.markdown(f'''
    <div style="background:{bg}; border:1.5px solid {border};
                border-radius:14px; padding:14px 16px; margin-bottom:12px;">
        <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:1.5px; color:{color}; margin-bottom:10px;">{titulo}</div>
    ''', unsafe_allow_html=True)

    if not data:
        st.markdown('<div style="color:var(--text3);">Sin datos aún.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    ranking = _top_especiales(data)

    for i, nombre, votos, pct in ranking:
        pos = "Otros" if i == "otros" else f"{i}°"
        sep = "" if i == 1 else "border-top:1px solid var(--border);"

        st.markdown(f'''
        <div style="display:flex; justify-content:space-between; padding:7px 0; {sep}">
            <div style="display:flex; gap:8px;">
                <span style="color:var(--text3); font-weight:800;">{pos}</span>
                <span style="font-weight:600;">{nombre}</span>
            </div>
            <span style="color:{color}; font-weight:800;">
                {votos} votos · {pct:.0f}%
            </span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────
# DESTACADOS
# ─────────────────────────────

def render_destacados_usuarios():
    stats = db_get_estadisticas_usuarios()

    categorias = [
        ("top_resultados", "Más resultados", "#3b82f6"),
        ("top_exactos", "Más exactos", "#2563eb"),
        ("top_grupos", "Rey de grupos", "#14b8a6"),
        ("top_finales", "Rey de finales", "#0ea5e9"),
    ]

    iconos = ["🥇", "🥈", "🥉"]

    for key, titulo, color in categorias:
        st.markdown(f"### {titulo}")
        datos = stats.get(key, [])[:3]

        for i, d in enumerate(datos):
            nombre = d.get("nombre") or d.get("username")
            valor = d.get("valor", 0)

            st.markdown(f"{iconos[i]} {nombre} — {valor} pts")

# ─────────────────────────────
# RANKING
# ─────────────────────────────

def pantalla_ranking():
    st.markdown("# 🏆 Ranking")
    ranking = db_get_ranking_snapshot()["rows"]
    medallas = {1:"🥇",2:"🥈",3:"🥉"}

    for u in ranking:
        pos = medallas.get(u["pos"], f"{u['pos']}°")
        st.write(f"{pos} - {u['nombre']} ({u['total']} pts)")

# ─────────────────────────────
# ESTADÍSTICAS
# ─────────────────────────────

def pantalla_estadisticas():
    render_destacados_usuarios()

    especiales = db_get_todos_especiales() or []

    campeon = Counter()
    goleador = Counter()
    arquero = Counter()
    jugador = Counter()

    for e in especiales:
        if e["categoria"] == "campeon":
            campeon[e["eleccion"]] += 1
        elif e["categoria"] == "goleador":
            goleador[e["eleccion"]] += 1
        elif e["categoria"] == "arquero":
            arquero[e["eleccion"]] += 1
        elif e["categoria"] == "jugador":
            jugador[e["eleccion"]] += 1

    st.markdown("## 📊 Elecciones de la gente")

    _render_top_especiales("🏆 Campeón", campeon, "#f5c76b", "rgba(245,199,107,0.12)", "rgba(245,199,107,0.28)")
    _render_top_especiales("⚽ Goleador", goleador, "#34d399", "rgba(52,211,153,0.12)", "rgba(52,211,153,0.28)")
    _render_top_especiales("🧤 Arquero", arquero, "#6ee7ff", "rgba(110,231,255,0.12)", "rgba(110,231,255,0.28)")
    _render_top_especiales("⭐ MVP", jugador, "#fb923c", "rgba(251,146,60,0.12)", "rgba(251,146,60,0.28)")

# ─────────────────────────────
# TORNEO
# ─────────────────────────────

def pantalla_estadisticas_torneo():
    st.markdown("# 📊 Estadísticas torneo")
    stats = db_get_estadisticas_partidos()

    if not stats:
        st.info("Sin datos")
        return

    for r in stats:
        st.write(f"{bandera(r['local'])} {r['local']} {r['rl']}-{r['rv']} {bandera(r['visita'])} {r['visita']}")
