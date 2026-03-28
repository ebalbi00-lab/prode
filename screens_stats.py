"""
screens_stats.py — Pantallas de ranking, destacados y estadísticas.
"""
import streamlit as st
from constants import bandera

try:
    from streamlit_autorefresh import st_autorefresh
except Exception:
    st_autorefresh = None

from db import (
    db_get_estadisticas_usuarios, db_get_estadisticas_partidos,
    db_get_partidos, db_get_ranking_snapshot, db_get_tipo_usuario,
)


def cambiar_pantalla(step):
    st.session_state.step = step


def _destino_panel():
    usuario = st.session_state.get("usuario")
    return 9 if db_get_tipo_usuario(usuario) in ("admin", "consumo") else 5


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
        ("top_resultados", "✅ Más resultados", "resultados acertados", "#3b82f6", "rgba(59,130,246,0.12)", "rgba(59,130,246,0.28)"),
        ("top_exactos",    "🎯 Más exactos",    "scores exactos",       "#2563eb", "rgba(37,99,235,0.11)", "rgba(37,99,235,0.24)"),
        ("top_grupos",     "⚽ Rey de grupos",   "pts en Grupos",        "#14b8a6", "rgba(20,184,166,0.11)", "rgba(20,184,166,0.24)"),
        ("top_finales",    "🏆 Rey de finales",  "pts en Finales",       "#0ea5e9", "rgba(14,165,233,0.11)", "rgba(14,165,233,0.24)"),
    ]
    col_a, col_b = st.columns(2)
    cols = [col_a, col_b, col_a, col_b]
    iconos_pos = ["🥇", "🥈", "🥉"]

    for i, (key, titulo, unidad, color, bg_color, border_color) in enumerate(categorias):
        datos = stats.get(key, [])
        with cols[i]:
            if not datos:
                contenido = '<div style="color:var(--text3); font-size:0.82rem; padding:4px 0 8px 0;">Sin datos aún.</div>'
            else:
                top3 = datos[:3]
                filas = ""
                for j, d in enumerate(top3):
                    icono = iconos_pos[j] if j < 3 else str(j + 1)
                    sep = "border-top:1px solid var(--border);" if j > 0 else ""
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
                contenido = filas
            st.markdown(f"""
            <div style="background:{bg_color}; border:1.5px solid {border_color};
                        border-radius:14px; padding:14px 16px; margin-bottom:12px;">
                <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:1.5px; color:{color}; margin-bottom:10px;">{titulo}</div>
                {contenido}
            </div>
            """, unsafe_allow_html=True)


def pantalla_ranking():
    if st_autorefresh:
        st_autorefresh(interval=60 * 1000, key="ranking_refresh")

    st.markdown("""
    <div style="text-align:center; padding:1rem 0 1rem 0;">
        <div style="font-size:0.72rem; font-weight:800; text-transform:uppercase; letter-spacing:2px;
                    color:var(--blue); margin-bottom:0.45rem;">Il Baigo · Mundial 2026</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:2.8rem; font-weight:800; letter-spacing:-1px;
                    color:var(--text); line-height:1.05;">Ranking general</div>
    </div>
    """, unsafe_allow_html=True)

    username_actual = st.session_state.get("usuario", "")
    ranking_snapshot = db_get_ranking_snapshot()
    ranking = ranking_snapshot["rows"]

    if not ranking:
        st.info("Todavía no hay usuarios para mostrar.")
    else:
        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        rows = []
        for u in ranking:
            pos = u["pos"]
            rows.append({
                "Pos": medallas.get(pos, str(pos)),
                "Nombre": u["nombre"],
                "R": u["puntos"],
                "G": u["goles"],
                "C": u["consumo"],
                "E": u["especiales"],
                "Total": u["total"],
                "_username": u["username"],
                "_pos": pos,
            })

        POR_PAGINA = 20
        total_pages = max(1, (len(rows) + POR_PAGINA - 1) // POR_PAGINA)
        page = st.session_state.get("ranking_page", 0)
        if page >= total_pages:
            page = 0
        st.session_state["ranking_page"] = page

        inicio_page = page * POR_PAGINA
        filas_html = ""
        for r in rows[inicio_page:inicio_page + POR_PAGINA]:
            es_yo = r["_username"] == username_actual
            pos = r["_pos"]

            if pos == 1:
                pos_color = "#2563eb"; bg = "rgba(37,99,235,0.08)"; bl = "3px solid rgba(37,99,235,0.24)"
            elif pos == 2:
                pos_color = "#4f86f7"; bg = "rgba(79,134,247,0.07)"; bl = "3px solid rgba(79,134,247,0.20)"
            elif pos == 3:
                pos_color = "#14b8a6"; bg = "rgba(20,184,166,0.07)"; bl = "3px solid rgba(20,184,166,0.22)"
            elif es_yo:
                pos_color = "#00e87a"; bg = "rgba(0,232,122,0.07)"; bl = "3px solid rgba(0,200,96,0.5)"
            else:
                pos_color = "#525268"; bg = "transparent"; bl = "3px solid transparent"

            you_badge = (
                '<span style="background:var(--green-dim);color:var(--green);font-size:0.6rem;font-weight:700;'
                'letter-spacing:1px;text-transform:uppercase;padding:1px 6px;border-radius:10px;margin-left:6px;'
                'border:1px solid var(--green-glow);">vos</span>'
            ) if es_yo else ""

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

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        col_pg1, col_pg2, col_pg3 = st.columns([1, 3, 1])
        with col_pg1:
            if page > 0 and st.button("← Anterior", key="rank_prev"):
                st.session_state["ranking_page"] = page - 1
                st.rerun()
        with col_pg2:
            st.markdown(
                f"<div style='text-align:center; color:var(--text3); font-size:0.78rem; padding-top:8px;'>{page+1} / {total_pages} &nbsp;·&nbsp; {len(rows)} jugadores</div>",
                unsafe_allow_html=True,
            )
        with col_pg3:
            if st.button("Siguiente →", key="rank_next", disabled=(page >= total_pages - 1)):
                st.session_state["ranking_page"] = page + 1
                st.rerun()

        if username_actual and username_actual != "admin":
            pos_actual = next((r["_pos"] for r in rows if r["_username"] == username_actual), None)
            if pos_actual:
                fila = next(r for r in rows if r["_username"] == username_actual)
                st.divider()
                bg_pos = "var(--green-dim)" if pos_actual <= 3 else "var(--surface)"
                border_pos = "var(--green-glow)" if pos_actual <= 3 else "var(--border2)"
                emoji_pos = {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos_actual, "📍")
                st.markdown(f"""
                <div style="background:{bg_pos}; border:1.5px solid {border_pos};
                            border-radius:10px; padding:12px 16px; display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.6rem;">{emoji_pos}</span>
                    <div>
                        <div style="color:var(--text3); font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Tu posición</div>
                        <div style="color:var(--text); font-weight:700; font-size:1rem;">
                            {fila['Nombre']} &nbsp;·&nbsp;
                            <span style="color:var(--green);">{pos_actual}° lugar</span> &nbsp;·&nbsp;
                            <span style="color:var(--gold);">{fila['Total']} pts</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    st.divider()
    destino = _destino_panel()
    st.button("← Volver", on_click=cambiar_pantalla, args=(destino,), use_container_width=True)


def pantalla_estadisticas():
    render_destacados_usuarios()
    st.divider()
    destino = _destino_panel()
    st.button("← Volver", on_click=cambiar_pantalla, args=(destino,), use_container_width=True)


def pantalla_estadisticas_torneo():
    st.markdown("""<div style="font-family:Bebas Neue,sans-serif;font-size:1.8rem;
        letter-spacing:3px;color:var(--text);margin-bottom:1rem;">📊 Estadísticas del torneo</div>""",
        unsafe_allow_html=True)

    stats_partidos = db_get_estadisticas_partidos()
    if not stats_partidos:
        st.info("Todavía no hay resultados cargados.")
    else:
        por_fase = {}
        for r in stats_partidos:
            f = r["fase"]
            if f not in por_fase:
                por_fase[f] = []
            por_fase[f].append(r)

        for fase, partidos_stats in por_fase.items():
            partidos_info = db_get_partidos(fase)
            info_map = {p["idx"]: p for p in partidos_info}

            st.markdown(f"""<div style="font-family:Bebas Neue,sans-serif;font-size:1.1rem;
                letter-spacing:2px;color:var(--text2);margin:1rem 0 0.5rem 0;
                text-transform:uppercase;">{fase}</div>""", unsafe_allow_html=True)

            for r in partidos_stats:
                p_info = info_map.get(r["partido_idx"], {})
                local = p_info.get("local", "?")
                visita = p_info.get("visita", "?")
                total = r["total_prodes"] or 0
                exactos = r["exactos"] or 0
                result = r["resultados"] or 0
                rl, rv = r["rl"], r["rv"]
                pct_res = int(result / total * 100) if total > 0 else 0
                pct_ex = int(exactos / total * 100) if total > 0 else 0

                st.markdown(
                    f'<div style="background:var(--bg3);border:1px solid var(--border);'
                    f'border-radius:10px;padding:10px 14px;margin:5px 0;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
                    f'<span style="font-weight:700;font-size:0.85rem;color:var(--text);">{bandera(local)} {local} {rl}–{rv} {bandera(visita)} {visita}</span>'
                    f'<span style="font-size:0.72rem;color:var(--text3);">{total} pronósticos</span>'
                    f'</div>'
                    f'<div style="display:flex;gap:12px;font-size:0.78rem;">'
                    f'<span style="color:var(--blue);">✅ Resultado: {result} ({pct_res}%)</span>'
                    f'<span style="color:var(--green);">🎯 Exacto: {exactos} ({pct_ex}%)</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

    st.divider()
    destino = _destino_panel()
    st.button("← Volver", on_click=cambiar_pantalla, args=(destino,), use_container_width=True, key="back_stats_torneo")
