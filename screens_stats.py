# screens_stats.py FINAL

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

def _top_especiales(counter_obj):
    total = sum(counter_obj.values())
    top = counter_obj.most_common(3)
    usados = sum(v for _, v in top)
    otros = total - usados
    resultado = []
    for i,(nombre,votos) in enumerate(top,1):
        pct = (votos/total*100) if total else 0
        resultado.append((i,nombre,votos,pct))
    if otros>0:
        pct = (otros/total*100) if total else 0
        resultado.append(("otros","Otros",otros,pct))
    return resultado

def _render_top_especiales(titulo,data):
    st.markdown(f"### {titulo}")
    if not data:
        st.caption("Sin datos aún.")
        return
    ranking = _top_especiales(data)
    for i,nombre,votos,pct in ranking:
        pos = "Otros" if i=="otros" else f"{i}°"
        st.markdown(f"{pos} {nombre} — {votos} votos · {pct:.0f}%")

def render_destacados_usuarios():
    st.markdown("## 📊 Estadísticas")
    stats = db_get_estadisticas_usuarios()
    for key,titulo in [
        ("top_resultados","Más resultados"),
        ("top_exactos","Más exactos"),
        ("top_grupos","Rey de grupos"),
        ("top_finales","Rey de finales"),
    ]:
        datos = stats.get(key,[])[:3]
        st.markdown(f"### {titulo}")
        for i,d in enumerate(datos):
            nombre = d.get("nombre") or d.get("username")
            valor = d.get("valor",0)
            st.markdown(f"{i+1}° {nombre} — {valor} pts")

def pantalla_ranking():
    st.markdown("# 🏆 Ranking")
    ranking = db_get_ranking_snapshot()["rows"]
    medallas={1:"🥇",2:"🥈",3:"🥉"}
    for u in ranking:
        pos = medallas.get(u["pos"],f"{u['pos']}°")
        st.write(f"{pos} - {u['nombre']} ({u['total']} pts)")

def pantalla_estadisticas():
    render_destacados_usuarios()
    especiales = db_get_todos_especiales() or []
    campeon,goleador,arquero,jugador = Counter(),Counter(),Counter(),Counter()
    for e in especiales:
        if e["categoria"]=="campeon": campeon[e["eleccion"]]+=1
        elif e["categoria"]=="goleador": goleador[e["eleccion"]]+=1
        elif e["categoria"]=="arquero": arquero[e["eleccion"]]+=1
        elif e["categoria"]=="jugador": jugador[e["eleccion"]]+=1
    st.markdown("## 📊 Elecciones de la gente")
    _render_top_especiales("🏆 Campeón",campeon)
    _render_top_especiales("⚽ Goleador",goleador)
    _render_top_especiales("🧤 Arquero",arquero)
    _render_top_especiales("⭐ MVP",jugador)

def pantalla_estadisticas_torneo():
    st.markdown("# 📊 Estadísticas torneo")
    stats = db_get_estadisticas_partidos()
    if not stats:
        st.info("Sin datos")
        return
    for r in stats:
        st.write(f"{bandera(r['local'])} {r['local']} {r['rl']}-{r['rv']} {bandera(r['visita'])} {r['visita']}")
