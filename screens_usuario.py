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

from constants import FASES, CATEGORIAS_ESPECIALES, BANDERAS, JUGADORES_MUNDIALISTAS, ARQUEROS_MUNDIALISTAS, bandera
from db import (
    db_get_usuario, db_get_fases, db_get_partidos, db_get_prode,
    db_get_resultado_completo, db_guardar_pred, db_confirmar_prode,
    db_fase_confirmada, db_get_especial, db_guardar_especial,
    db_confirmar_especial, db_get_resultado_especial,
    db_get_todos_usuarios, db_get_puntos_especiales_usuarios,
    db_get_equipos_grupos, get_db, hash_clave
)


def cambiar_pantalla(step):
    st.session_state.step = step


def pantalla_usuario():
    username = st.session_state.usuario
    u = db_get_usuario(username)
    nombre_display = u.get('nombre', username)

    # ── 0) Header ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:14px; padding:0.3rem 0 1.2rem 0;
                border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:1.2rem;">
        <div style="width:46px; height:46px; border-radius:50%;
                    background:linear-gradient(135deg,#00c860,#009944);
                    display:flex; align-items:center; justify-content:center;
                    font-size:1.3rem; font-weight:800; color:var(--text); flex-shrink:0;
                    box-shadow:0 4px 14px rgba(0,200,96,0.35);">
            {nombre_display[0].upper()}
        </div>
        <div>
            <div style="font-family:Bebas Neue,sans-serif; font-size:1.6rem; letter-spacing:2px; color:var(--text); line-height:1.1;">{nombre_display}</div>
            <div style="font-size:0.72rem; color:var(--text3); text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Panel de pronósticos</div>
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
            st.button("🚪 Cerrar sesión", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
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

    # ── 1) Puntos + posición (solo si ya completó grupos) ─────────────────────
    if grupos_completados:
        u_fresh      = db_get_usuario(username)
        _pts_esp_all = db_get_puntos_especiales_usuarios()
        pts_esp_user = _pts_esp_all.get(username, 0)
        total_pts    = u_fresh["puntos"] + u_fresh["goles"] + u_fresh["consumo"] + pts_esp_user
        _todos_rank  = db_get_todos_usuarios()
        ranking      = sorted(_todos_rank, key=lambda x: x["puntos"] + x["goles"] + x["consumo"] + _pts_esp_all.get(x["username"], 0), reverse=True)
        posicion     = next((i + 1 for i, x in enumerate(ranking) if x["username"] == username), "—")

        st.markdown(f"""<div style="background:var(--gold-dim); border:1.5px solid var(--gold-border);
                    border-radius:10px; padding:10px 16px; margin-bottom:0.8rem;
                    display:flex; align-items:center; gap:10px;">
            <span style="font-size:1.3rem;">🏆</span>
            <span style="color:var(--text2); font-size:0.9rem;">Tu posición actual:</span>
            <span style="color:var(--gold); font-family:Bebas Neue,sans-serif; font-size:1.3rem; letter-spacing:1px;">
                {posicion}° de {len(ranking)}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:2px;
                    color:var(--text3); margin-bottom:0.7rem;">Mis puntos</div>""", unsafe_allow_html=True)
        col_a, col_b, col_c, col_d, col_e = st.columns(5)
        col_a.metric("Resultados",    u_fresh["puntos"])
        col_b.metric("Goles",         u_fresh["goles"])
        col_c.metric("Consumo",       u_fresh["consumo"])
        col_d.metric("⭐ Especiales", pts_esp_user)
        col_e.metric("Total",         total_pts)

        # ── 2) Selector de fases ──────────────────────────────────────────────
        st.divider()
        cols_fases = st.columns(len(fases_habilitadas))
        for i, (col, f, lbl) in enumerate(zip(cols_fases, fases_habilitadas, labels)):
            es_activa = (i == fase_idx)
            if col.button(lbl, key=f"fase_btn_{f}", use_container_width=True,
                          type="primary" if es_activa else "secondary"):
                st.session_state["fase_sel_idx"] = i
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
            st.button("🚪 Cerrar sesión", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
        return

    partidos = db_get_partidos(fase)
    if not partidos:
        st.markdown("""<div style="background:var(--blue-dim); border:1.5px solid var(--blue-border);
                    border-radius:12px; padding:14px 18px; margin:1rem 0;">
            <div style="color:var(--blue); font-weight:700; margin-bottom:4px;">📋 Sin partidos cargados</div>
            <div style="color:var(--text2); font-size:0.88rem;">El admin aún no cargó los partidos de esta fase.</div>
        </div>""", unsafe_allow_html=True)
        if not grupos_completados:
            st.button("🚪 Cerrar sesión", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
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
            st.markdown(f"""
            <div style="background:{color_card}; border:1px solid {border_card};
                        border-radius:12px; padding:12px 16px; margin:6px 0;
                        display:flex; align-items:center; justify-content:space-between; gap:6px;">
                <div style="color:var(--text); font-weight:700; font-size:0.95rem; flex:1; text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{nom_local}</div>
                <div style="font-family:Bebas Neue,sans-serif; font-size:1.6rem; color:var(--green); min-width:20px; text-align:center; flex-shrink:0;">{gl_prev}</div>
                <div style="color:#404058; font-size:0.9rem; flex-shrink:0;">—</div>
                <div style="font-family:Bebas Neue,sans-serif; font-size:1.6rem; color:var(--green); min-width:20px; text-align:center; flex-shrink:0;">{gv_prev}</div>
                <div style="color:var(--text); font-weight:700; font-size:0.95rem; flex:1; text-align:left; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{nom_visita}</div>
                {f'<div style="font-size:1rem; flex-shrink:0;">{iconos}</div>' if iconos else ""}
            </div>
            {f'<div style="text-align:center; font-size:0.72rem; color:var(--text3); margin:-2px 0 4px 0;">Real: <span style="color:var(--text2);">{res_str}</span></div>' if res_str else ""}
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background:var(--table-row); border:1px solid var(--border);
                        border-radius:12px; padding:12px 16px; margin:6px 0;">""", unsafe_allow_html=True)
            col_local, col_gl, col_gv, col_visita = st.columns([3, 1, 1, 3])
            col_local.markdown(f"<div style='text-align:right; font-weight:700; font-size:0.95rem; padding-top:10px; color:var(--text); line-height:1.4;'>{nom_local}</div>", unsafe_allow_html=True)
            gl = col_gl.number_input("Local",  min_value=0, max_value=10, value=int(gl_prev), key=f"gl_{fase}_{idx}", label_visibility="collapsed")
            gv = col_gv.number_input("Visita", min_value=0, max_value=10, value=int(gv_prev), key=f"gv_{fase}_{idx}", label_visibility="collapsed")
            col_visita.markdown(f"<div style='text-align:left; font-weight:700; font-size:0.95rem; padding-top:10px; color:var(--text); line-height:1.4;'>{nom_visita}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            cambios[idx] = (gl, gv)
            if (gl, gv) != (int(gl_prev), int(gv_prev)):
                db_guardar_pred(username, fase, idx, gl, gv)

    # ── Fase Grupos con wizard ────────────────────────────────────────────────
    if fase == "Grupos":
        grupos = [chr(ord('A') + i) for i in range(12)]
        grupos_con_partidos = [l for l in grupos if any(
            True for p in partidos if "ABCDEFGHIJKL".index(l) * 6 <= p["idx"] < "ABCDEFGHIJKL".index(l) * 6 + 6)]

        if confirmado:
            st.session_state["wizard_grupos_completo"] = True

        if st.session_state.get("wizard_grupos_completo", False):
            grupo_sel = st.selectbox("Elegí el grupo", [f"Grupo {l}" for l in grupos_con_partidos])
            letra_sel = grupo_sel[-1]
            inicio    = "ABCDEFGHIJKL".index(letra_sel) * 6
            partidos_grupo = [p for p in partidos if inicio <= p["idx"] < inicio + 6]
            st.markdown(f"<div style='font-family:Bebas Neue,sans-serif; font-size:1.1rem; color:var(--text3); letter-spacing:3px; margin-top:0.5rem; text-transform:uppercase;'>GRUPO {letra_sel}</div>", unsafe_allow_html=True)
            for p in partidos_grupo:
                render_partido(p)
        else:
            if "grupo_wizard" not in st.session_state:
                st.session_state.grupo_wizard = 0
            gi_raw = st.session_state.grupo_wizard
            gi     = gi_raw if gi_raw == 12 else max(0, min(gi_raw, len(grupos_con_partidos) - 1))
            total  = len(grupos_con_partidos)

            if gi == 12:
                _render_paso_especiales(username, u, fase, total, partidos)
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
                if nav1.button("← Anterior", key="grupo_prev", use_container_width=True, disabled=(gi == 0)):
                    with st.spinner("Guardando..."):
                        for idx, (gl, gv) in cambios.items():
                            db_guardar_pred(username, fase, idx, gl, gv)
                    st.session_state.grupo_wizard = gi - 1; st.rerun()

                if gi < total - 1:
                    if nav3.button("Siguiente →", key="grupo_next", type="primary", use_container_width=True):
                        with st.spinner("Guardando..."):
                            for idx, (gl, gv) in cambios.items():
                                db_guardar_pred(username, fase, idx, gl, gv)
                        st.session_state.grupo_wizard = gi + 1; st.rerun()
                else:
                    if nav3.button("Siguiente → Especiales ⭐", key="grupo_to_especiales", type="primary", use_container_width=True):
                        with st.spinner("Guardando..."):
                            for idx, (gl, gv) in cambios.items():
                                db_guardar_pred(username, fase, idx, gl, gv)
                        st.session_state.grupo_wizard = 12; st.rerun()

    # ── Fases eliminatorias ───────────────────────────────────────────────────
    else:
        for p in partidos:
            render_partido(p)

        if not confirmado:
            st.divider()
            with st.form("form_confirmar"):
                clave_confirm = st.text_input("Ingresá tu contraseña para confirmar", type="password")
                confirmar_btn = st.form_submit_button("🔒 Confirmar prode", type="primary", use_container_width=True)
            if confirmar_btn:
                if hash_clave(clave_confirm) != u["clave"]:
                    st.error("Contraseña incorrecta")
                else:
                    with st.spinner("Confirmando..."):
                        db_confirmar_prode(username, fase)
                    st.session_state["wizard_grupos_completo"] = True
                    st.success("¡Pronósticos confirmados!")
                    st.rerun()
        else:
            st.success("✅ Pronósticos confirmados para esta fase.")

    if "msg_grupos" in st.session_state:
        st.success(st.session_state.pop("msg_grupos"))

    # Si todavía está en el wizard de grupos, solo mostrar cerrar sesión
    if not grupos_completados:
        st.divider()
        st.button("🚪 Cerrar sesión", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
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
    col1, col2, col3 = st.columns(3)
    col1.button("🏆 Ranking",       on_click=cambiar_pantalla, args=(6,),  use_container_width=True)
    col2.button("🏅 Destacados",    on_click=cambiar_pantalla, args=(12,), use_container_width=True)
    col3.button("🚪 Cerrar sesión", on_click=cambiar_pantalla, args=(0,),  use_container_width=True)


# ─── Paso 13: Especiales dentro del wizard de grupos ─────────────────────────

def _render_paso_especiales(username, u, fase, total, partidos):
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
                ops_w = [f"{bandera(e)} {e}" for e in eq_wiz]
                d2n_w = {f"{bandera(e)} {e}": e for e in eq_wiz}
                idx_w = next((i for i, e in enumerate(eq_wiz) if e == elec_w), 0)
                sel_w = st.selectbox("Seleccioná el equipo", ops_w, index=idx_w, key=f"esp_sel_{cat}")
                selecciones_esp[cat] = d2n_w.get(sel_w, sel_w)
            else:
                lista_w = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
                label_w = "arquero" if cat == "arquero" else "jugador"
                busq_w  = st.text_input(f"Buscar {label_w}", value="", key=f"esp_busq_{cat}", placeholder="Escribí para filtrar...")
                st.caption(f"Si no encontrás al {label_w}, elegí **— Otro (escribir abajo) —** al final de la lista.")
                filtrados_w = [j for j in lista_w if busq_w.lower() in j.lower()] if busq_w else lista_w
                opciones_w  = filtrados_w + ["— Otro (escribir abajo) —"]
                if elec_w in filtrados_w:
                    idx_w = filtrados_w.index(elec_w)
                elif elec_w and elec_w not in lista_w:
                    idx_w = len(opciones_w) - 1
                else:
                    idx_w = 0
                sel_w = st.selectbox(f"Seleccioná el {label_w}", opciones_w, index=min(idx_w, len(opciones_w) - 1), key=f"esp_sel_{cat}")
                if sel_w == "— Otro (escribir abajo) —":
                    otro_val = elec_w if (elec_w and elec_w not in lista_w) else ""
                    otro_w   = st.text_input(f"Nombre del {label_w}", value=otro_val, key=f"esp_otro_{cat}", placeholder="Escribí el nombre completo")
                    selecciones_esp[cat] = otro_w.strip() if otro_w.strip() else None
                else:
                    selecciones_esp[cat] = sel_w

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
            faltan = [info["label"] for cat, info in CATEGORIAS_ESPECIALES.items()
                      if not selecciones_esp.get(cat) and not (db_get_especial(username, cat) and db_get_especial(username, cat)["confirmado"])]
            if faltan:
                st.error(f"Falta completar: {', '.join(faltan)}")
            else:
                with st.spinner("Confirmando pronósticos..."):
                    db_confirmar_prode(username, fase)
                    for cat, elec in selecciones_esp.items():
                        if elec and not (db_get_especial(username, cat) and db_get_especial(username, cat)["confirmado"]):
                            db_guardar_especial(username, cat, elec)
                            db_confirmar_especial(username, cat)
                st.session_state["wizard_grupos_completo"] = True
                st.session_state["msg_grupos"] = "✅ ¡Todo confirmado! Grupos y especiales guardados."
                st.rerun()

    for cat, elec in selecciones_esp.items():
        if elec and not (db_get_especial(username, cat) and db_get_especial(username, cat)["confirmado"]):
            db_guardar_especial(username, cat, elec)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    nav1_e, _, _ = st.columns([1, 2, 1])
    if nav1_e.button("← Grupo L", key="esp_back", use_container_width=True):
        st.session_state.grupo_wizard = total - 1; st.rerun()