"""
screens_usuario.py — Pantalla principal del usuario: pronósticos, puntos, especiales.

Orden de la pantalla (cuando grupos ya fue completado):
  1. Header con nombre
  2. Puntos + posición en el ranking
  3. Selector de fases
  4. Pronósticos de la fase activa
  5. Resumen de especiales
  6. Botones de navegación
"""
import streamlit as st
import unicodedata

from constants import FASES, CATEGORIAS_ESPECIALES, BANDERAS, JUGADORES_MUNDIALISTAS, ARQUEROS_MUNDIALISTAS, bandera
from db import (
    db_get_usuario, db_get_fases, db_get_partidos, db_get_prode,
    db_get_resultado_completo, db_guardar_pred, db_confirmar_prode,
    db_fase_confirmada, db_get_especial, db_guardar_especial,
    db_confirmar_especial, db_get_resultado_especial,
    db_get_todos_usuarios, db_get_puntos_especiales_usuarios,
    db_get_equipos_grupos, get_db, hash_clave,
    db_set_config, db_get_config, db_calcular_puntos
)


def cambiar_pantalla(step):
    st.session_state.step = step


def cerrar_sesion():
    """Limpia todo el session_state y vuelve al login."""
    claves_a_limpiar = [k for k in st.session_state.keys()
                        if k not in ("db_initialized",)]
    for k in claves_a_limpiar:
        del st.session_state[k]
    st.session_state.step = 0
    st.session_state.usuario = None


def normalizar(s: str) -> str:
    """Quita acentos y pasa a minúsculas para búsqueda flexible."""
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii').lower()


def pantalla_usuario():
    username = st.session_state.usuario
    u = db_get_usuario(username)
    nombre_display = u.get('nombre', username)

    # Scroll al tope: itera todos los elementos scrolleables del parent
    st.components.v1.html("""
    <script>
    (function() {
        function scrollAll() {
            var doc = window.parent.document;
            // Scrollear el documento raíz
            doc.documentElement.scrollTop = 0;
            doc.body.scrollTop = 0;
            // Scrollear todos los divs que tienen scroll
            var els = doc.querySelectorAll('*');
            for (var i = 0; i < els.length; i++) {
                if (els[i].scrollTop > 0) els[i].scrollTop = 0;
            }
        }
        scrollAll();
        setTimeout(scrollAll, 50);
        setTimeout(scrollAll, 200);
    })();
    </script>
    """, height=0)

    # ── 0) Header ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between;
                padding:0.4rem 0 1rem 0; border-bottom:1px solid var(--border); margin-bottom:1rem;">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:40px; height:40px; border-radius:50%;
                        background:linear-gradient(135deg,#00c860,#009944);
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.1rem; font-weight:800; color:#fff; flex-shrink:0;">
                {nombre_display[0].upper()}
            </div>
            <div>
                <div style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; letter-spacing:2px; color:var(--text); line-height:1.1;">{nombre_display}</div>
                <div style="font-size:0.65rem; color:var(--text3); text-transform:uppercase; letter-spacing:1.5px;">Mundial 2026</div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:0.65rem; color:var(--text3); text-transform:uppercase; letter-spacing:1px;">Prode Il Baigo</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fases = db_get_fases()

    # ── Estado de grupos: siempre desde DB, sin confiar en session_state ────────
    grupos_completados = db_fase_confirmada(username, "Grupos")
    st.session_state["wizard_grupos_completo"] = grupos_completados

    if grupos_completados:
        fases_habilitadas = [f for f in FASES if fases.get(f, False)]
        fases_confirmadas = {f: db_fase_confirmada(username, f) for f in fases_habilitadas}

        if not fases_habilitadas:
            st.warning("No hay fases habilitadas aún.")
            st.button("🚪 Cerrar sesión", key="logout_92", on_click=cerrar_sesion, use_container_width=True)
            return

        labels = []
        for f in fases_habilitadas:
            check = "✅ " if fases_confirmadas.get(f) else ""
            labels.append(f"{check}{f}")

        fase_idx = st.session_state.get("fase_sel_idx", 0)
        if fase_idx >= len(fases_habilitadas):
            fase_idx = 0
        fase = fases_habilitadas[fase_idx]
    else:
        fase = "Grupos"
        fases_habilitadas = []
        labels = []
        fase_idx = 0

    # ── 1) Panel principal con sub-pantallas ─────────────────────────────────
    if grupos_completados:
        u_fresh      = db_get_usuario(username)
        _pts_esp_all = db_get_puntos_especiales_usuarios()
        pts_esp_user = _pts_esp_all.get(username, 0)
        total_pts    = u_fresh["puntos"] + u_fresh["goles"] + u_fresh["consumo"] + pts_esp_user
        _todos_rank  = db_get_todos_usuarios()
        ranking      = sorted(_todos_rank, key=lambda x: x["puntos"] + x["goles"] + x["consumo"] + _pts_esp_all.get(x["username"], 0), reverse=True)
        posicion     = next((i + 1 for i, x in enumerate(ranking) if x["username"] == username), "—")
        emoji_pos    = {1:"🥇",2:"🥈",3:"🥉"}.get(posicion, "🏅") if isinstance(posicion, int) else "🏅"

        # Sub-pantalla activa
        sub = st.session_state.get("sub_pantalla", "inicio")

        # ── Menú de inicio ──
        if sub == "inicio":
            # Card de posición grande
            st.markdown(f"""
            <div style="background:var(--gold-dim);border:1.5px solid var(--gold-border);
                        border-radius:16px;padding:20px 24px;margin-bottom:1.2rem;
                        display:flex;align-items:center;gap:16px;">
                <span style="font-size:2.5rem;">{emoji_pos}</span>
                <div>
                    <div style="font-size:0.68rem;color:var(--text3);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:2px;">Tu posición</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2rem;color:var(--gold);letter-spacing:2px;line-height:1;">{posicion}° de {len(ranking)}</div>
                    <div style="font-size:0.82rem;color:var(--text2);margin-top:2px;">{total_pts} puntos totales</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Aviso pendientes
            pendientes_info = []
            for f_check in fases_habilitadas:
                if not fases_confirmadas.get(f_check):
                    pts_f  = db_get_partidos(f_check)
                    pred_f = db_get_prode(username, f_check)["pred"]
                    sin_cargar = len([p for p in pts_f if p["idx"] not in pred_f])
                    if sin_cargar > 0:
                        pendientes_info.append(f"{f_check} ({sin_cargar})")
            if pendientes_info:
                st.markdown(
                    '<div style="background:var(--gold-dim);border:1px solid var(--gold-border);'
                    'border-radius:10px;padding:10px 14px;margin-bottom:1rem;font-size:0.85rem;color:var(--gold);">'
                    '⚠️ Pronósticos pendientes: ' + " · ".join(pendientes_info) + '</div>',
                    unsafe_allow_html=True
                )

            # Menú principal — 2 columnas
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⚽  Mis pronósticos", use_container_width=True, key="menu_prode"):
                    st.session_state["sub_pantalla"] = "pronosticos"
                    st.rerun()
                if st.button("🏆  Ranking", use_container_width=True, key="menu_ranking"):
                    cambiar_pantalla(6)
            with c2:
                if st.button("📊  Mis puntos", use_container_width=True, key="menu_puntos"):
                    st.session_state["sub_pantalla"] = "puntos"
                    st.rerun()
                if st.button("🏅  Destacados", use_container_width=True, key="menu_dest"):
                    cambiar_pantalla(12)

            st.divider()
            if st.session_state.get("confirmar_logout_main"):
                st.warning("¿Seguro que querés cerrar sesión?")
                c1b, c2b = st.columns(2)
                if c1b.button("Sí, cerrar", key="main_cerrar_ok", type="primary", use_container_width=True):
                    cerrar_sesion(); st.rerun()
                if c2b.button("Cancelar", key="main_cerrar_cancel", use_container_width=True):
                    st.session_state["confirmar_logout_main"] = False; st.rerun()
            else:
                if st.button("🚪 Cerrar sesión", key="logout_402", use_container_width=True):
                    st.session_state["confirmar_logout_main"] = True; st.rerun()
            return

        # ── Sub-pantalla puntos ──
        if sub == "puntos":
            if st.button("← Volver", key="back_puntos"):
                st.session_state["sub_pantalla"] = "inicio"; st.rerun()
            st.markdown(f"""
            <div style="margin:0.5rem 0 1rem 0;">
                <div style="font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:2px;color:var(--text);">📊 Mis puntos</div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:1rem;">
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Resultados acertados</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--blue);">{u_fresh["puntos"]}</div>
                </div>
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Marcadores exactos</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--green);">{u_fresh["goles"]}</div>
                </div>
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Puntos de consumo</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--orange);">{u_fresh["consumo"]}</div>
                </div>
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Pronósticos especiales</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--gold);">{pts_esp_user}</div>
                </div>
            </div>
            <div style="background:var(--green-dim);border:1.5px solid var(--green-glow);border-radius:12px;padding:16px;text-align:center;margin-bottom:1rem;">
                <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Total</div>
                <div style="font-family:Bebas Neue,sans-serif;font-size:3rem;color:var(--green);letter-spacing:2px;">{total_pts}</div>
                <div style="font-size:0.8rem;color:var(--text3);">Posición {posicion} de {len(ranking)}</div>
            </div>
            """, unsafe_allow_html=True)
            return

        # ── Sub-pantalla pronósticos — continúa abajo con el código existente ──
        if st.button("← Volver al inicio", key="back_prode"):
            st.session_state["sub_pantalla"] = "inicio"; st.rerun()
        st.markdown(f"""<div style="margin:0.5rem 0 1rem 0;">
            <div style="font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:2px;color:var(--text);">⚽ Mis pronósticos</div>
        </div>""", unsafe_allow_html=True)

        # Partidos pendientes
        pendientes_info = []
        for f_check in fases_habilitadas:
            if not fases_confirmadas.get(f_check):
                pts_f  = db_get_partidos(f_check)
                pred_f = db_get_prode(username, f_check)["pred"]
                sin_cargar = len([p for p in pts_f if p["idx"] not in pred_f])
                if sin_cargar > 0:
                    pendientes_info.append(f"<b>{f_check}</b>: {sin_cargar} partido{'s' if sin_cargar > 1 else ''}")
        if pendientes_info:
            st.markdown(
                '<div style="background:var(--gold-dim);border:1px solid var(--gold-border);'
                'border-radius:10px;padding:10px 14px;margin-bottom:0.5rem;font-size:0.85rem;color:var(--gold);">'
                '⚠️ Pendientes de cargar: ' + " &nbsp;·&nbsp; ".join(pendientes_info) + '</div>',
                unsafe_allow_html=True
            )

        # ── 2) Selector de fases ──────────────────────────────────────────────
        st.divider()
        if len(fases_habilitadas) <= 3:
            cols_fases = st.columns(len(fases_habilitadas))
            for i, (col, f, lbl) in enumerate(zip(cols_fases, fases_habilitadas, labels)):
                es_activa = (i == fase_idx)
                if col.button(lbl, key=f"fase_btn_{f}", use_container_width=True,
                              type="primary" if es_activa else "secondary"):
                    st.session_state["fase_sel_idx"] = i
                    st.rerun()
        else:
            sel_fase = st.selectbox("Fase", labels, index=fase_idx, key="fase_sel_box", label_visibility="collapsed")
            nuevo_idx = labels.index(sel_fase)
            if nuevo_idx != fase_idx:
                st.session_state["fase_sel_idx"] = nuevo_idx
                st.rerun()

        st.divider()

    # ── Validaciones ──────────────────────────────────────────────────────────
    if not fases.get(fase, False):
        st.markdown("""<div style="background:rgba(255,180,0,0.08); border:1.5px solid rgba(255,180,0,0.25);
                    border-radius:12px; padding:14px 18px; margin:1rem 0;">
            <div style="color:var(--gold); font-weight:700; margin-bottom:4px;">⏳ Fase no habilitada</div>
            <div style="color:var(--text2); font-size:0.88rem;">Esta fase todavía no fue abierta por el admin.</div>
        </div>""", unsafe_allow_html=True)
        if not grupos_completados:
            st.button("🚪 Cerrar sesión", key="logout_157", on_click=cerrar_sesion, use_container_width=True)
        return

    partidos = db_get_partidos(fase)
    if not partidos:
        st.markdown("""<div style="background:var(--blue-dim); border:1.5px solid var(--blue-border);
                    border-radius:12px; padding:14px 18px; margin:1rem 0;">
            <div style="color:var(--blue); font-weight:700; margin-bottom:4px;">📋 Sin partidos cargados</div>
            <div style="color:var(--text2); font-size:0.88rem;">El admin aún no cargó los partidos de esta fase.</div>
        </div>""", unsafe_allow_html=True)
        if not grupos_completados:
            st.button("🚪 Cerrar sesión", key="logout_168", on_click=cerrar_sesion, use_container_width=True)
        return

    prode      = db_get_prode(username, fase)
    confirmado = prode["confirmado"]
    pred       = prode["pred"]

    # ── 3) Pronósticos ────────────────────────────────────────────────────────
    estado_badge = ('<span style="background:var(--green-dim);color:var(--green);font-size:0.65rem;font-weight:700;'
                    'letter-spacing:1px;text-transform:uppercase;padding:2px 9px;border-radius:20px;'
                    'border:1px solid var(--green-glow);margin-left:8px;">Confirmado ✓</span>') if confirmado else ""

    titulo_fase = fase if grupos_completados else "Grupos"
    st.markdown(f"""<div style="margin:0.8rem 0 0.5rem 0;">
        <span style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; letter-spacing:2px; color:var(--text);">
            Pronósticos — {titulo_fase}</span>{estado_badge}
    </div>""", unsafe_allow_html=True)

    resultados_fase = db_get_resultado_completo(fase)
    cambios = {}

    def render_partido(p):
        idx = p["idx"]
        gl_prev, gv_prev = pred.get(idx, (0, 0))
        res_real    = resultados_fase.get(idx)
        iconos      = ""
        color_card  = "rgba(255,255,255,0.03)"
        border_card = "rgba(255,255,255,0.08)"
        res_str     = ""

        if res_real:
            rl, rv = res_real
            acierto_res    = (gl_prev > gv_prev and rl > rv) or (gl_prev < gv_prev and rl < rv) or (gl_prev == gv_prev and rl == rv)
            acierto_exacto = gl_prev == rl and gv_prev == rv
            iconos  = ("✅" if acierto_res else "❌") + (" 🎯" if acierto_exacto else "")
            res_str = f"{rl} — {rv}"
            if acierto_exacto:
                color_card = "rgba(0,200,80,0.07)";  border_card = "rgba(0,200,80,0.3)"
            elif acierto_res:
                color_card = "rgba(0,150,255,0.06)"; border_card = "rgba(0,150,255,0.25)"
            else:
                color_card = "rgba(255,60,60,0.05)"; border_card = "rgba(255,60,60,0.2)"

        nom_local  = f"{bandera(p['local'])} {p['local']}"
        nom_visita = f"{bandera(p['visita'])} {p['visita']}"

        if confirmado:
            real_row = f"""<div style="text-align:center;font-size:0.7rem;color:var(--text3);margin-top:4px;">
                Real: <span style="color:var(--text2);font-weight:600;">{res_str}</span>
                <span style="margin-left:6px;">{iconos}</span></div>""" if res_str else (f'<div style="text-align:center;font-size:0.9rem;margin-top:2px;">{iconos}</div>' if iconos else "")
            st.markdown(f"""
            <div style="background:{color_card};border:1px solid {border_card};
                        border-radius:12px;padding:10px 14px;margin:5px 0;">
                <div style="display:flex;align-items:center;gap:6px;">
                    <div style="flex:1;text-align:right;font-weight:700;font-size:0.88rem;
                                color:var(--text);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{nom_local}</div>
                    <div style="background:var(--bg);border-radius:8px;padding:4px 10px;
                                font-family:Bebas Neue,sans-serif;font-size:1.5rem;color:var(--green);
                                min-width:36px;text-align:center;flex-shrink:0;">{gl_prev}</div>
                    <div style="color:var(--text3);font-size:0.8rem;flex-shrink:0;">:</div>
                    <div style="background:var(--bg);border-radius:8px;padding:4px 10px;
                                font-family:Bebas Neue,sans-serif;font-size:1.5rem;color:var(--green);
                                min-width:36px;text-align:center;flex-shrink:0;">{gv_prev}</div>
                    <div style="flex:1;text-align:left;font-weight:700;font-size:0.88rem;
                                color:var(--text);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{nom_visita}</div>
                </div>
                {real_row}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:var(--bg3);border:1.5px solid var(--border2);border-radius:12px;padding:10px 12px;margin:5px 0;">', unsafe_allow_html=True)
            col_local, col_gl, col_sep, col_gv, col_visita = st.columns([3, 1, 0.3, 1, 3])
            col_local.markdown(f"<div style='text-align:right;font-weight:700;font-size:0.88rem;padding-top:10px;color:var(--text);line-height:1.2;'>{nom_local}</div>", unsafe_allow_html=True)
            gl = col_gl.number_input("L", min_value=0, max_value=10, value=int(gl_prev), key=f"gl_{fase}_{idx}", label_visibility="collapsed")
            col_sep.markdown("<div style='text-align:center;padding-top:10px;color:var(--text3);font-size:0.8rem;'>:</div>", unsafe_allow_html=True)
            gv = col_gv.number_input("V", min_value=0, max_value=10, value=int(gv_prev), key=f"gv_{fase}_{idx}", label_visibility="collapsed")
            col_visita.markdown(f"<div style='text-align:left;font-weight:700;font-size:0.88rem;padding-top:10px;color:var(--text);line-height:1.2;'>{nom_visita}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if "partidos_ok" not in st.session_state:
                st.session_state["partidos_ok"] = {}
            ok_key = f"ok_{fase}_{idx}"
            actual = st.session_state["partidos_ok"].get(ok_key, False)
            checked = st.checkbox("✔ Confirmo el pronóstico de este partido", value=actual, key=f"chk_{fase}_{idx}")
            if checked != actual:
                st.session_state["partidos_ok"][ok_key] = checked
            cambios[idx] = (gl, gv)

    # ── Fase Grupos con wizard ────────────────────────────────────────────────
    if fase == "Grupos":
        grupos = [chr(ord('A') + i) for i in range(12)]
        grupos_con_partidos = [l for l in grupos if any(
            True for p in partidos if "ABCDEFGHIJKL".index(l) * 6 <= p["idx"] < "ABCDEFGHIJKL".index(l) * 6 + 6)]

        if confirmado:
            st.session_state["wizard_grupos_completo"] = True

        if st.session_state.get("wizard_grupos_completo", False):
            n_grupos = len(grupos_con_partidos)
            gi_conf = st.session_state.get("gi_conf", 0)
            if gi_conf >= n_grupos:
                gi_conf = 0

            letra_sel = grupos_con_partidos[gi_conf]
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; margin:0.5rem 0 0.8rem 0;'>
                <div style='height:1px; flex:1; background:var(--surface2);'></div>
                <div style='font-family:Bebas Neue,sans-serif; font-size:1.3rem; color:var(--green); letter-spacing:3px;'>GRUPO {letra_sel}</div>
                <div style='height:1px; flex:1; background:var(--surface2);'></div>
            </div>
            """, unsafe_allow_html=True)

            inicio    = "ABCDEFGHIJKL".index(letra_sel) * 6
            partidos_grupo = [p for p in partidos if inicio <= p["idx"] < inicio + 6]
            for p in partidos_grupo:
                render_partido(p)

            dest_conf = st.select_slider(
                "Grupo",
                options=list(range(n_grupos)),
                value=gi_conf,
                format_func=lambda x: f"Grupo {grupos_con_partidos[x]}",
                key=f"slider_conf_{gi_conf}",
                label_visibility="collapsed",
            )
            if dest_conf != gi_conf:
                st.session_state["gi_conf"] = dest_conf
                st.rerun()
        else:
            if "grupo_wizard" not in st.session_state:
                # Recuperar último grupo visitado de la DB
                ultimo = db_get_config(f"wizard_pos_{username}", "0")
                st.session_state.grupo_wizard = int(ultimo) if ultimo and ultimo.isdigit() else 0
            gi_raw = st.session_state.grupo_wizard
            gi     = gi_raw if gi_raw == 12 else max(0, min(gi_raw, len(grupos_con_partidos) - 1))
            total  = len(grupos_con_partidos)

            if gi == 12:
                _render_paso_especiales(username, u, fase, total, partidos, pred)
            else:
                letra = grupos_con_partidos[min(gi, len(grupos_con_partidos) - 1)]
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:10px; margin:0.5rem 0 0.8rem 0;'>
                    <div style='height:1px; flex:1; background:var(--surface2);'></div>
                    <div style='font-family:Bebas Neue,sans-serif; font-size:1.3rem; color:var(--green); letter-spacing:3px;'>GRUPO {letra}</div>
                    <div style='height:1px; flex:1; background:var(--surface2);'></div>
                </div>
                <div style='text-align:center; color:var(--text3); font-size:0.75rem; margin-bottom:0.8rem; letter-spacing:1px;'>{gi+1} DE {total}</div>
                """, unsafe_allow_html=True)

                inicio = "ABCDEFGHIJKL".index(letra) * 6
                partidos_grupo = [p for p in partidos if inicio <= p["idx"] < inicio + 6]
                for p in partidos_grupo:
                    render_partido(p)

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                nav1, nav2, nav3 = st.columns([1, 2, 1])
                if gi > 0:
                    if nav1.button("← Anterior", key="grupo_prev", use_container_width=True):
                        with st.spinner("Guardando..."):
                            for idx, (gl, gv) in cambios.items():
                                db_guardar_pred(username, fase, idx, gl, gv)
                        st.session_state.grupo_wizard = gi - 1; db_set_config(f'wizard_pos_{username}', str(gi - 1)); st.rerun()

                if gi < total - 1:
                    if nav3.button("Siguiente →", key="grupo_next", type="primary", use_container_width=True):
                        with st.spinner("Guardando..."):
                            for idx, (gl, gv) in cambios.items():
                                db_guardar_pred(username, fase, idx, gl, gv)
                        st.session_state.grupo_wizard = gi + 1; db_set_config(f'wizard_pos_{username}', str(gi + 1)); st.rerun()
                else:
                    if nav3.button("Siguiente → Especiales ⭐", key="grupo_to_especiales", type="primary", use_container_width=True):
                        with st.spinner("Guardando..."):
                            for idx, (gl, gv) in cambios.items():
                                db_guardar_pred(username, fase, idx, gl, gv)
                        st.session_state.grupo_wizard = 12; db_set_config(f'wizard_pos_{username}', '12'); st.rerun()

                # ── Slider de navegación ──
                pasos = grupos_con_partidos + ["⭐"]
                n = len(pasos)
                dest_slider = st.select_slider(
                    "Ir a",
                    options=list(range(n)),
                    value=gi,
                    format_func=lambda x: (pasos[x] if pasos[x] == "⭐" else f"Grupo {pasos[x]}"),
                    key=f"slider_wizard_{gi}",
                    label_visibility="collapsed",
                )
                if dest_slider != gi:
                    with st.spinner("Guardando..."):
                        for idx2, (gl2, gv2) in cambios.items():
                            db_guardar_pred(username, fase, idx2, gl2, gv2)
                    st.session_state.grupo_wizard = dest_slider
                    db_set_config(f'wizard_pos_{username}', str(dest_slider)); st.rerun()

            st.divider()
            if st.session_state.get("confirmar_logout_wiz"):
                st.warning("¿Seguro que querés cerrar sesión? Los pronósticos no confirmados pueden perderse.")
                c1, c2 = st.columns(2)
                if c1.button("Sí, cerrar", key="wiz_cerrar_ok", type="primary", use_container_width=True):
                    cerrar_sesion(); st.rerun()
                if c2.button("Cancelar", key="wiz_cerrar_cancel", use_container_width=True):
                    st.session_state["confirmar_logout_wiz"] = False; st.rerun()
            else:
                if st.button("🚪 Cerrar sesión", key="wiz_cerrar", use_container_width=True):
                    st.session_state["confirmar_logout_wiz"] = True; st.rerun()

    # ── Fases eliminatorias ───────────────────────────────────────────────────
    else:
        for p in partidos:
            render_partido(p)

        if not confirmado:
            st.divider()
            # Verificar checkboxes
            if "partidos_ok" not in st.session_state:
                st.session_state["partidos_ok"] = {}
            partidos_ok = st.session_state["partidos_ok"]
            total_partidos = [p["idx"] for p in partidos]
            sin_confirmar = [idx for idx in total_partidos if not partidos_ok.get(f"ok_{fase}_{idx}", False)]

            if sin_confirmar:
                st.warning(f"⚠️ Confirmá todos los partidos antes de continuar ({len(sin_confirmar)} pendiente{'s' if len(sin_confirmar) > 1 else ''}).")

            with st.form("form_confirmar"):
                clave_confirm = st.text_input("Ingresá tu contraseña para confirmar", type="password")
                confirmar_btn = st.form_submit_button("🔒 Confirmar prode", type="primary", use_container_width=True, disabled=bool(sin_confirmar))
            if confirmar_btn:
                if hash_clave(clave_confirm) != u["clave"]:
                    st.error("Contraseña incorrecta")
                else:
                    with st.spinner("Confirmando..."):
                        # Primero guardar todos los pronósticos
                        for idx_c, (gl_c, gv_c) in cambios.items():
                            db_guardar_pred(username, fase, idx_c, gl_c, gv_c)
                        db_confirmar_prode(username, fase)
                        db_calcular_puntos()
                    st.session_state["wizard_grupos_completo"] = True
                    st.success("¡Pronósticos confirmados!")
                    st.rerun()
        else:
            st.success("✅ Pronósticos confirmados para esta fase.")

    if "msg_grupos" in st.session_state:
        st.success(st.session_state.pop("msg_grupos"))

    # Si todavía está en el wizard de grupos, salir
    if not grupos_completados:
        return

    # ── 4) Resumen de especiales ──────────────────────────────────────────────
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM especiales WHERE username=%s", (username,))
        _rows = cur.fetchall()
    esp_data = {r["categoria"]: dict(r) for r in _rows}
    for _cat in CATEGORIAS_ESPECIALES:
        if _cat not in esp_data:
            esp_data[_cat] = None

    if any(v for v in esp_data.values()):
        st.subheader("⭐ Mis pronósticos especiales")
        for cat, info in CATEGORIAS_ESPECIALES.items():
            esp  = esp_data[cat]
            elec = esp["eleccion"] if esp else None
            resultado_real = db_get_resultado_especial(cat)

            if not elec:
                bg_c = "rgba(255,255,255,0.02)"; border_c = "rgba(255,255,255,0.05)"
                derecha = '<span style="color:var(--text3); font-size:0.8rem;">Sin completar</span>'
            elif resultado_real:
                acierto  = elec == resultado_real
                icono    = "🎯" if acierto else "❌"
                bg_c     = "rgba(0,200,80,0.06)" if acierto else "rgba(255,60,60,0.05)"
                border_c = "rgba(0,200,80,0.25)" if acierto else "rgba(255,60,60,0.2)"
                derecha  = (f'<b style="color:var(--text)">{elec}</b>'
                            f'<span style="margin:0 8px; color:#404058;">→</span>'
                            f'<span style="color:var(--text2); font-size:0.8rem;">Real: </span>'
                            f'<b style="color:var(--text)">{resultado_real}</b>'
                            f'<span style="margin-left:6px; font-size:1rem;">{icono}</span>')
            else:
                bg_c = "rgba(255,255,255,0.03)"; border_c = "rgba(255,255,255,0.07)"
                derecha = f'<b style="color:var(--text)">{elec}</b>'

            st.markdown(f"""<div style="background:{bg_c}; border:1px solid {border_c};
                border-radius:10px; padding:10px 16px; margin:4px 0;
                display:flex; justify-content:space-between; align-items:center;">
                <span style="color:var(--text2); font-size:0.85rem;">{info['label']}</span>
                <span>{derecha}</span>
            </div>""", unsafe_allow_html=True)

    # ── 5) Botones de navegación ──────────────────────────────────────────────
    st.divider()
    if st.button("← Volver al inicio", key="logout_402", use_container_width=True):
        st.session_state["sub_pantalla"] = "inicio"; st.rerun()


# ─── Paso 13: Especiales dentro del wizard de grupos ─────────────────────────

def _render_paso_especiales(username, u, fase, total, partidos, pred):
    st.markdown("""
    <div style='display:flex; align-items:center; gap:10px; margin:0.5rem 0 0.8rem 0;'>
        <div style='height:1px; flex:1; background:var(--surface2);'></div>
        <div style='font-family:Bebas Neue,sans-serif; font-size:1.3rem; color:var(--gold); letter-spacing:3px;'>⭐ ESPECIALES</div>
        <div style='height:1px; flex:1; background:var(--surface2);'></div>
    </div>
    <div style='text-align:center; color:var(--text3); font-size:0.75rem; margin-bottom:0.8rem; letter-spacing:1px;'>PASO 13 DE 13</div>
    """, unsafe_allow_html=True)

    eq_wiz = db_get_equipos_grupos() or sorted(BANDERAS.keys())
    selecciones_esp = {}

    for cat, info in CATEGORIAS_ESPECIALES.items():
        esp_w      = db_get_especial(username, cat)
        elec_w     = esp_w["eleccion"] if esp_w else None
        res_real_w = db_get_resultado_especial(cat)

        col_tw, col_pw = st.columns([4, 1])
        col_tw.markdown(f"**{info['label']}**")
        col_pw.markdown(f"<div style='text-align:right; color:var(--gold); font-family:Bebas Neue,sans-serif; font-size:1.1rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)

        if res_real_w:
            acierto_w = elec_w == res_real_w
            st.markdown(f"<div style='color:var(--text2); font-size:0.9rem; margin-bottom:8px;'>Resultado oficial: <b style='color:#fff'>{res_real_w}</b> {'🎯' if acierto_w else '❌'} — Tu pronóstico: <b style='color:#fff'>{elec_w or '—'}</b></div>", unsafe_allow_html=True)
            selecciones_esp[cat] = elec_w
        elif esp_w and esp_w["confirmado"]:
            st.markdown(f"<div style='color:var(--green); font-size:0.9rem; margin-bottom:8px;'>✅ Confirmado: <b>{elec_w}</b></div>", unsafe_allow_html=True)
            selecciones_esp[cat] = elec_w
        else:
            if cat == "campeon":
                ops_w = ["— Elegí un equipo —"] + [f"{bandera(e)} {e}" for e in eq_wiz]
                d2n_w = {f"{bandera(e)} {e}": e for e in eq_wiz}
                if elec_w:
                    disp_elec = f"{bandera(elec_w)} {elec_w}"
                    idx_w = ops_w.index(disp_elec) if disp_elec in ops_w else 0
                else:
                    idx_w = 0
                sel_w = st.selectbox("Seleccioná el equipo", ops_w, index=idx_w, key=f"esp_sel_{cat}")
                selecciones_esp[cat] = d2n_w.get(sel_w, None) if sel_w != "— Elegí un equipo —" else None
            else:
                lista_w = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
                label_w = "arquero" if cat == "arquero" else "jugador"

                # Mostrar selección actual — solo del session_state, nunca pre-cargado
                sel_actual = st.session_state.get(f"esp_elegido_{cat}")
                if sel_actual:
                    st.markdown(f"<div style='color:var(--green); font-size:0.88rem; margin:4px 0;'>✅ Elegido: <b>{sel_actual}</b></div>", unsafe_allow_html=True)
                selecciones_esp[cat] = sel_actual

                # Buscador — solo muestra si no hay selección o si el usuario quiere cambiar
                if st.session_state.get(f"esp_cambiar_{cat}", not bool(sel_actual)):
                    busq_w = st.text_input(f"Buscar {label_w}", value="", key=f"esp_busq_{cat}", placeholder="Escribí el nombre (con o sin acento)...")
                    if busq_w:
                        filtrados_w = [j for j in lista_w if normalizar(busq_w) in normalizar(j)][:8]
                        if not filtrados_w:
                            st.caption("No se encontró ningún jugador.")
                        else:
                            for jug in filtrados_w:
                                if st.button(jug, key=f"jug_{cat}_{jug}", use_container_width=True):
                                    st.session_state[f"esp_elegido_{cat}"] = jug
                                    st.session_state[f"esp_cambiar_{cat}"] = False
                                    selecciones_esp[cat] = jug
                                    st.rerun()
                else:
                    if st.button(f"✏️ Cambiar {label_w}", key=f"esp_cambiar_btn_{cat}"):
                        st.session_state[f"esp_cambiar_{cat}"] = True
                        st.rerun()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.divider()
    if "msg_esp" in st.session_state:
        st.success(st.session_state.pop("msg_esp"))

    with st.form("form_confirmar_especiales"):
        clave_esp_final = st.text_input("🔒 Tu contraseña para confirmar grupos + especiales", type="password", key="pw_esp_final")
        confirmar_esp   = st.form_submit_button("🔒 Confirmar todo", type="primary", use_container_width=True)

    if confirmar_esp:
        if hash_clave(clave_esp_final) != u["clave"]:
            st.error("Contraseña incorrecta.")
        else:
            # Verificar que todos los partidos tengan checkbox marcado
            partidos_ok = st.session_state.get("partidos_ok", {})
            partidos_sin_ok = [idx for idx in pred if not partidos_ok.get(f"ok_{fase}_{idx}", False) and idx >= 0]
            if partidos_sin_ok:
                st.error(f"⚠️ Faltan confirmar {len(partidos_sin_ok)} partido(s). Volvé a los grupos y marcá todos los pronósticos.")
            else:
                esp_confirmados = {cat: db_get_especial(username, cat) for cat in CATEGORIAS_ESPECIALES}
                sin_elegir = [info["label"] for cat, info in CATEGORIAS_ESPECIALES.items()
                              if selecciones_esp.get(cat) is None and not (esp_confirmados[cat] and esp_confirmados[cat]["confirmado"])]
                if sin_elegir:
                    st.error(f"⚠️ Falta elegir: {', '.join(sin_elegir)}")
                else:
                    with st.spinner("Confirmando pronósticos..."):
                        db_confirmar_prode(username, fase)
                        for cat, elec in selecciones_esp.items():
                            if elec and not (esp_confirmados[cat] and esp_confirmados[cat]["confirmado"]):
                                db_guardar_especial(username, cat, elec)
                                db_confirmar_especial(username, cat)
                        db_calcular_puntos()
                    st.session_state["wizard_grupos_completo"] = True
                    st.session_state["msg_grupos"] = "✅ ¡Todo confirmado! Grupos y especiales guardados."
                    db_set_config(f"wizard_pos_{username}", "0")
                    st.rerun()

    for cat, elec in selecciones_esp.items():
        esp_actual = db_get_especial(username, cat)
        if elec and not (esp_actual and esp_actual["confirmado"]):
            db_guardar_especial(username, cat, elec)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    nav1_e, _, _ = st.columns([1, 2, 1])
    if nav1_e.button("← Grupo L", key="esp_back", use_container_width=True):
        st.session_state.grupo_wizard = total - 1; st.rerun()