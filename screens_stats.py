"""
screens_stats.py — Pantallas de ranking, destacados y estadísticas.
"""
import streamlit as st

from db import (
    db_get_todos_usuarios, db_get_puntos_especiales_usuarios,
    db_get_estadisticas_usuarios,
)


def cambiar_pantalla(step):
    st.session_state.step = step


def render_destacados_usuarios():
    st.markdown("""
    <div style="margin-bottom:1rem;">
        <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:2px;
                    color:var(--text3); margin-bottom:0.4rem;">Estadísticas</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:1.8rem; letter-spacing:3px; color:var(--text);">
            🏅 DESTACADOS</div>
    </div>
    """, unsafe_allow_html=True)

    stats = db_get_estadisticas_usuarios()
    categorias = [
        ("top_resultados", "✅ Más resultados", "resultados acertados", "#5599ff", "rgba(85,153,255,0.12)", "rgba(85,153,255,0.3)"),
        ("top_exactos",    "🎯 Más exactos",    "scores exactos",       "#ffc840", "rgba(255,200,64,0.12)", "rgba(255,200,64,0.3)"),
        ("top_grupos",     "⚽ Rey de grupos",   "pts en Grupos",        "#00e87a", "rgba(0,232,122,0.12)", "rgba(0,232,122,0.3)"),
        ("top_finales",    "🏆 Rey de finales",  "pts en Finales",       "#ff8844", "rgba(255,136,68,0.12)", "rgba(255,136,68,0.3)"),
    ]
    col_a, col_b = st.columns(2)
    cols = [col_a, col_b, col_a, col_b]
    iconos_pos = ["🥇", "🥈", "🥉"]

    for i, (key, titulo, unidad, color, bg_color, border_color) in enumerate(categorias):
        datos = stats.get(key, [])
        with cols[i]:
            st.markdown(f"""
            <div style="background:{bg_color}; border:1.5px solid {border_color};
                        border-radius:14px; padding:14px 16px; margin-bottom:12px;">
                <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:1.5px; color:{color}; margin-bottom:10px;">{titulo}</div>
            """, unsafe_allow_html=True)

            if not datos:
                st.markdown(f'<div style="color:var(--text3); font-size:0.82rem; padding:4px 0 8px 0;">Sin datos aún.</div>', unsafe_allow_html=True)
            else:
                top3  = datos[:3]
                filas = ""
                for j, d in enumerate(top3):
                    icono = iconos_pos[j] if j < 3 else str(j + 1)
                    sep   = "border-top:1px solid rgba(255,255,255,0.06);" if j > 0 else ""
                    filas += f"""
                    <div style="display:flex; align-items:center; justify-content:space-between;
                                padding:7px 0; {sep}">
                        <div style="display:flex; align-items:center; gap:8px; min-width:0;">
                            <span style="font-size:1.0rem; flex-shrink:0;">{icono}</span>
                            <span style="color:var(--text); font-weight:600; font-size:0.88rem;
                                         white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:130px;">{d['nombre']}</span>
                        </div>
                        <span style="color:{color}; font-weight:800; font-size:0.95rem;
                                      font-family:JetBrains Mono,monospace; flex-shrink:0; margin-left:8px;">{d['valor']}</span>
                    </div>"""
                st.markdown(filas, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def pantalla_ranking():
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 1rem 0;">
        <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:2.5px;
                    color:var(--text3); margin-bottom:0.3rem;">Il Baigo — Mundial 2026</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:3.2rem; letter-spacing:4px;
                    background:linear-gradient(135deg,#ffc840 0%,#ffdd80 50%,#ffa820 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; line-height:1.05;">🏆 RANKING</div>
        <div style="display:inline-block; background:var(--gold-dim); border:1px solid var(--gold-border);
                    border-radius:20px; padding:3px 18px; font-family:Bebas Neue,sans-serif;
                    font-size:1rem; color:var(--gold); letter-spacing:3px; margin-top:0.2rem;">TOP 15</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        from streamlit_autorefresh import st_autorefresh
        count = st_autorefresh(interval=60 * 1000, key="ranking_autorefresh")
        if count > 0:
            st.cache_data.clear()
    except ImportError:
        pass

    username_actual = st.session_state.get("usuario", "")
    todos = db_get_todos_usuarios()

    if not todos:
        st.info("Todavía no hay usuarios para mostrar.")
    else:
        _pts_esp_r = db_get_puntos_especiales_usuarios()
        ranking    = sorted(todos, key=lambda x: x["puntos"] + x["goles"] + x["consumo"] + _pts_esp_r.get(x["username"], 0), reverse=True)
        medallas   = {1: "🥇", 2: "🥈", 3: "🥉"}
        rows = []
        for i, u in enumerate(ranking):
            pos  = i + 1
            esp  = _pts_esp_r.get(u["username"], 0)
            total = u["puntos"] + u["goles"] + u["consumo"] + esp
            rows.append({"Pos": medallas.get(pos, str(pos)), "Nombre": u.get("nombre") or u["username"],
                         "R": u["puntos"], "G": u["goles"], "C": u["consumo"],
                         "E": esp, "Total": total, "_username": u["username"], "_pos": pos})

        top_n = min(15, len(rows))
        filas_html = ""
        for r in rows[:top_n]:
            es_yo = r["_username"] == username_actual
            pos   = r["_pos"]
            if pos == 1:
                pos_color = "#ffc840"; bg = "rgba(255,200,64,0.07)"; bl = "3px solid rgba(255,200,64,0.5)"
            elif pos == 2:
                pos_color = "#c0c8d8"; bg = "rgba(192,200,216,0.05)"; bl = "3px solid rgba(192,200,216,0.3)"
            elif pos == 3:
                pos_color = "#cd8040"; bg = "rgba(205,128,64,0.06)"; bl = "3px solid rgba(205,128,64,0.35)"
            elif es_yo:
                pos_color = "#00e87a"; bg = "rgba(0,232,122,0.07)"; bl = "3px solid rgba(0,200,96,0.5)"
            else:
                pos_color = "#525268"; bg = "transparent"; bl = "3px solid transparent"

            you_badge = ('<span style="background:var(--green-dim);color:var(--green);font-size:0.6rem;font-weight:700;'
                         'letter-spacing:1px;text-transform:uppercase;padding:1px 6px;border-radius:10px;margin-left:6px;'
                         'border:1px solid var(--green-glow);">vos</span>') if es_yo else ""
            filas_html += (
                f'<tr style="background:{bg};border-left:{bl};transition:background 0.15s;">'
                f'<td style="padding:10px 10px;font-weight:800;font-size:1.05rem;color:{pos_color};min-width:42px;text-align:center;">{r["Pos"]}</td>'
                f'<td style="padding:10px 8px;color:var(--text);font-weight:600;font-size:0.92rem;max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{r["Nombre"]}{you_badge}</td>'
                f'<td style="padding:10px 8px;color:var(--text2);text-align:center;font-family:JetBrains Mono,monospace;font-size:0.88rem;">{r["R"]}</td>'
                f'<td style="padding:10px 8px;color:var(--text2);text-align:center;font-family:JetBrains Mono,monospace;font-size:0.88rem;">{r["G"]}</td>'
                f'<td style="padding:10px 8px;color:var(--text2);text-align:center;font-family:JetBrains Mono,monospace;font-size:0.88rem;">{r["C"]}</td>'
                f'<td style="padding:10px 8px;color:var(--gold);text-align:center;font-family:JetBrains Mono,monospace;font-size:0.9rem;font-weight:700;">{r["E"]}</td>'
                f'<td style="padding:10px 10px;color:var(--green);font-weight:800;text-align:center;font-family:JetBrains Mono,monospace;font-size:1rem;">{r["Total"]}</td>'
                f'</tr>'
            )

        st.markdown(
            '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:14px;border:1.5px solid var(--border);overflow:hidden;">'
            '<table style="width:100%;min-width:320px;border-collapse:collapse;background:var(--table-bg);">'
            '<thead><tr style="background:var(--table-head);border-bottom:1px solid var(--border);">'
            '<th style="padding:10px 10px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;min-width:42px;">#</th>'
            '<th style="padding:10px 8px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:left;">Jugador</th>'
            '<th style="padding:10px 8px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;" title="Resultados">R</th>'
            '<th style="padding:10px 8px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;" title="Goles exactos">G</th>'
            '<th style="padding:10px 8px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;" title="Consumo">C</th>'
            '<th style="padding:10px 8px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;">ESP</th>'
            '<th style="padding:10px 10px;color:var(--green);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;">Total</th>'
            '</tr></thead>'
            f'<tbody>{filas_html}</tbody>'
            '</table></div>',
            unsafe_allow_html=True,
        )

        if username_actual and username_actual != "admin":
            pos_actual = next((r["_pos"] for r in rows if r["_username"] == username_actual), None)
            if pos_actual and pos_actual > top_n:
                fila = next(r for r in rows if r["_username"] == username_actual)
                st.divider()
                st.markdown(f"""
                <div style="background:var(--green-dim); border:1.5px solid var(--green-glow);
                            border-radius:10px; padding:12px 16px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.4rem;">📍</span>
                    <div>
                        <div style="color:var(--text2); font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Tu posición</div>
                        <div style="color:var(--text); font-weight:700; font-size:1rem;">{fila['Nombre']} — <span style="color:var(--green);">{pos_actual}° lugar</span> · <span style="color:var(--gold);">{fila['Total']} pts</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    st.divider()
    destino = 9 if st.session_state.get("usuario") == "admin" else 5
    st.button("← Volver", on_click=cambiar_pantalla, args=(destino,), use_container_width=True)


def pantalla_estadisticas():
    render_destacados_usuarios()
    st.divider()
    destino = 9 if st.session_state.get("usuario") == "admin" else 5
    st.button("← Volver", on_click=cambiar_pantalla, args=(destino,), use_container_width=True)