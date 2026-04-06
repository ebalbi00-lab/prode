"""
screens_admin.py — Panel de administración completo.
"""
import datetime
import re
import unicodedata
import pandas as pd
import streamlit as st

def _norm(s: str) -> str:
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii').lower()

from constants import (
    FASES,
    CATEGORIAS_ESPECIALES,
    BANDERAS,
    GRUPOS_DEFAULT,
    bandera,
    JUGADORES_MUNDIALISTAS,
    ARQUEROS_MUNDIALISTAS,
)
from db import (
    db_get_usuario, db_get_todos_usuarios, db_get_pendientes,
    db_get_fases, db_toggle_fase, db_get_partidos, db_guardar_partido,
    db_get_resultado_completo, db_guardar_resultado, db_limpiar_resultados_fase,
    db_limpiar_resultados_especiales,
    db_calcular_puntos, db_calcular_puntos_especiales,
    db_get_consumo_log, db_sumar_consumo, db_eliminar_consumo_log,
    db_aprobar_pendiente, db_rechazar_pendiente,
    db_reset_clave, db_borrar_usuario, db_resetear_todos_puntajes,
    db_registro_abierto, db_set_config, db_get_pago_config, db_set_pago_config,
    db_get_especial, db_get_resultado_especial, db_guardar_resultado_especial,
    db_get_todos_especiales, db_fusionar_variantes_especial,
    db_get_equipos_grupos, db_renombrar_equipo_global, hash_clave, get_db,
    db_touch_usuario, db_get_cantidad_usuarios_en_linea, db_logout_usuario, db_get_feed,
    db_get_lista_especiales, db_set_lista_especiales_desde_texto, db_reset_lista_especiales,
)
from screens_stats import render_destacados_usuarios, pantalla_estadisticas_torneo, _render_tab_estadisticas_completa


def cambiar_pantalla(step):
    st.session_state.step = step


def cerrar_sesion_admin():
    db_logout_usuario(st.session_state.get("usuario"))
    claves_a_limpiar = [k for k in list(st.session_state.keys()) if k not in ("db_initialized",)]
    for k in claves_a_limpiar:
        del st.session_state[k]
    st.session_state.step = 0
    st.session_state.usuario = None
    st.session_state.registro_temp = {}


def _fmt_equipo(nombre: str) -> str:
    nombre = str(nombre or "").strip()
    if not nombre:
        return "—"
    icono = bandera(nombre)
    if icono == "🏳️" and _norm(nombre).startswith("rep") and nombre[3:].isdigit():
        icono = "🔹"
    return f"{icono} {nombre}"




def _get_panel_context():
    username = st.session_state.get("usuario")
    u = db_get_usuario(username) or {}
    nivel = int(u.get("es_admin", 0) or 0)
    es_admin_total = nivel == 1
    es_panel_consumo = nivel == 2
    return {
        "username": username,
        "user": u,
        "nivel": nivel,
        "es_admin_total": es_admin_total,
        "es_panel_consumo": es_panel_consumo,
        "titulo": "Panel Admin" if es_admin_total else "Panel Consumo",
        "subtitulo": "Prode Il Baigo · Mundial 2026",
        "icono": "⚙️" if es_admin_total else "🍻",
    }


def _render_panel_feed(limit=6):
    st.markdown("""
    <div style="font-family:Bebas Neue,sans-serif;font-size:1.3rem;letter-spacing:2px;margin:0.4rem 0 0.7rem 0;color:var(--blue);">
    ⚡ Actividad en vivo
    </div>
    """, unsafe_allow_html=True)
    feed = db_get_feed(limit=limit)
    if not feed:
        st.caption("Sin actividad reciente")
        return
    for ev in feed:
        st.markdown(f"""
        <div style="background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:8px 12px;margin-bottom:6px;font-size:0.85rem;">
        {ev['texto']}
        </div>
        """, unsafe_allow_html=True)

def pantalla_admin():
    ctx = _get_panel_context()
    if ctx["nivel"] not in (1, 2):
        st.error("No tenés permisos para entrar a este panel.")
        st.button("← Volver", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
        return

    db_touch_usuario(ctx["username"])
    usuarios_en_linea = db_get_cantidad_usuarios_en_linea()
    _pend_count = len(db_get_pendientes()) if ctx["es_admin_total"] else 0

    header_left, header_right = st.columns([0.72, 0.28])
    with header_left:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:0.4rem 0 1rem 0;">
            <div style="width:40px;height:40px;border-radius:10px;background:var(--gold-dim);border:1.5px solid var(--gold-border);display:flex;align-items:center;justify-content:center;font-size:1.2rem;">{ctx['icono']}</div>
            <div>
                <div style="font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:2px;color:var(--text);line-height:1.05;">{ctx['titulo']}</div>
                <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1.5px;">{ctx['subtitulo']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with header_right:
        badges = [
            f'<span style="display:inline-flex;align-items:center;background:var(--blue-dim);color:var(--blue);font-size:0.72rem;font-weight:700;padding:5px 12px;border-radius:999px;border:1px solid var(--blue-border);">🟢 {usuarios_en_linea} en línea</span>'
        ]
        if ctx["es_admin_total"] and _pend_count > 0:
            badges.append(
                f'<span style="display:inline-flex;align-items:center;background:var(--red);color:#fff;font-size:0.72rem;font-weight:700;padding:5px 12px;border-radius:999px;">⚠️ {_pend_count} pendiente{"s" if _pend_count > 1 else ""}</span>'
            )
        st.markdown(
            '<div style="display:flex;justify-content:flex-end;align-items:center;gap:8px;flex-wrap:wrap;padding:0.55rem 0 1rem 0;">' + ''.join(badges) + '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('<div style="height:1px;background:var(--border);margin:0 0 1rem 0;"></div>', unsafe_allow_html=True)

    sec = st.session_state.get("admin_sec", "inicio")
    if ctx["es_admin_total"]:
        secciones = [
            ("resumen",    "📋", "Resumen",      "Estado general y confirmaciones"),
            ("pagos",      "💳", "Pagos",        "Editar datos de pago del registro"),
            ("usuarios",   "👤", "Usuarios",     "Gestionar usuarios"),
            ("pendientes", "👥", "Pendientes",   "Aprobar o rechazar solicitudes"),
            ("fases",      "🔀", "Fases",        "Habilitar fases del torneo"),
            ("partidos",   "⚽", "Partidos",     "Cargar equipos de cada partido"),
            ("resultados", "📊", "Resultados",   "Ingresar marcadores reales"),
            ("consumo",    "💰", "Consumo",      "Sumar puntos de consumo"),
            ("destacados", "📊", "Estadísticas", "Destacados y especiales más elegidos"),
            ("especiales", "⭐", "Especiales",   "Resultados especiales"),
            ("exportar",   "📥", "Exportar",     "Descargar base de datos"),
            ("reset",      "⚠️", "Reset",        "Resetear fases o todo"),
        ]
    else:
        secciones = [
            ("resumen", "📋", "Resumen", "Usuarios en línea y actividad"),
            ("consumo", "💰", "Consumo", "Sumar y ajustar puntos de consumo"),
            ("destacados", "📊", "Estadísticas", "Destacados y especiales más elegidos"),
        ]

    allowed_keys = {k for k, *_ in secciones}
    if sec not in allowed_keys and sec != "inicio":
        sec = "inicio"
        st.session_state["admin_sec"] = "inicio"

    if sec == "inicio":
        for i, (key, icono, titulo, desc) in enumerate(secciones):
            badge = f' <span style="background:var(--red);color:#fff;font-size:0.65rem;padding:1px 7px;border-radius:10px;font-family:Outfit,sans-serif;">{_pend_count}</span>' if key == "pendientes" and _pend_count > 0 else ""
            col_card, col_btn = st.columns([4, 1])
            with col_card:
                st.markdown(f"""<div style="background:var(--bg3);border:1px solid var(--border);
                    border-radius:12px;padding:14px 16px;margin-bottom:2px;">
                    <div style="font-size:1.1rem;margin-bottom:3px;">{icono}</div>
                    <div style="font-weight:700;color:var(--text);font-size:0.9rem;">{titulo}{badge}</div>
                    <div style="color:var(--text3);font-size:0.72rem;margin-top:1px;">{desc}</div>
                </div>""", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if st.button("Abrir", key=f"menu_{key}", use_container_width=True):
                    st.session_state["admin_sec"] = key
                    st.rerun()

        st.divider()
        _render_panel_feed(limit=6)
        st.divider()
        c1, c2 = st.columns(2)
        c1.button("🏆 Ranking", on_click=cambiar_pantalla, args=(6,), use_container_width=True, key="admin_rank")
        c2.button("🚪 Cerrar sesión", on_click=cerrar_sesion_admin, use_container_width=True, key="admin_logout")
        return

    if st.button("← Volver al menú", key="admin_back"):
        st.session_state["admin_sec"] = "inicio"
        st.rerun()

    if sec == "resumen":
        _tab_resumen(panel_consumo=ctx["es_panel_consumo"])
    elif sec == "pendientes" and ctx["es_admin_total"]:
        _tab_pendientes()
    elif sec == "fases" and ctx["es_admin_total"]:
        _tab_fases()
    elif sec == "partidos" and ctx["es_admin_total"]:
        _tab_partidos()
    elif sec == "resultados" and ctx["es_admin_total"]:
        _tab_resultados()
    elif sec == "consumo":
        _tab_consumo()
    elif sec == "pagos" and ctx["es_admin_total"]:
        _tab_pagos()
    elif sec == "especiales" and ctx["es_admin_total"]:
        _tab_especiales()
    elif sec == "usuarios" and ctx["es_admin_total"]:
        _tab_usuarios()
    elif sec == "destacados":
        _render_tab_estadisticas_completa()
    elif sec == "reset" and ctx["es_admin_total"]:
        _tab_reset()
    elif sec == "exportar" and ctx["es_admin_total"]:
        _tab_exportar()


# ─── Tabs ─────────────────────────────────────────────────────────────────────

def _tab_resumen(panel_consumo=False):
    if "msg_resumen" in st.session_state:
        st.success(st.session_state.pop("msg_resumen"))

    todos      = db_get_todos_usuarios()
    pendientes = db_get_pendientes()
    fases      = db_get_fases()
    fases_hab  = sum(1 for v in fases.values() if v)
    total_cons = sum(u["consumo"] for u in todos)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Usuarios", len(todos))
    col2.metric("⏳ Pendientes", len(pendientes))
    col3.metric("🔀 Fases activas", fases_hab)
    col4.metric("🍺 Consumo total", total_cons)

    if panel_consumo:
        st.divider()
        st.button("🏆 Ver ranking", on_click=cambiar_pantalla, args=(6,), use_container_width=True, key="consumo_rank")
        return

    st.divider()

    with get_db() as _conn:
        _cur = _conn.cursor()
        _cur.execute("SELECT fase, COUNT(DISTINCT username) as cnt FROM prodes WHERE confirmado=1 AND partido_idx=-1 GROUP BY fase")
        _conf_map = {r["fase"]: r["cnt"] for r in _cur.fetchall()}

    total_u = len(todos) or 1
    fases_activas = [f for f in FASES if fases.get(f)]
    if fases_activas:
        st.markdown("**Confirmaciones por fase**")
        for fase in fases_activas:
            cnt = _conf_map.get(fase, 0)
            pct = cnt / total_u
            st.write(f"{fase}  —  {cnt} / {len(todos)}")
            st.progress(pct)

    st.divider()
    registro_abierto = db_registro_abierto()
    nuevo_estado = st.toggle("📋 Registro abierto", value=registro_abierto, key="toggle_registro")
    if nuevo_estado != registro_abierto:
        db_set_config("registro_abierto", "1" if nuevo_estado else "0")
        st.rerun()


def _tab_pendientes():
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
            comp = pend.get('comprobante', '')
            if comp and comp.startswith('data:'):
                if 'pdf' in comp[:30]:
                    username = pend["username"]
                    st.markdown('<a href="' + comp + '" download="comprobante_' + username + '.pdf" style="display:inline-block;margin-top:6px;padding:0.55rem 1.2rem;background:#E50914;color:#ffffff;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;">⬇️ Descargar comprobante PDF</a>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<img src="{comp}" style="max-width:100%; max-height:300px; border-radius:8px; margin-top:6px;" />', unsafe_allow_html=True)
            elif comp:
                st.write(f"**Comprobante:** {comp}")
            c1, c2 = st.columns(2)
            if c1.button("✅ Aprobar", key=f"ap_{pend['id']}"):
                with st.spinner("Aprobando..."):
                    db_aprobar_pendiente(pend["id"]); st.cache_data.clear()
                st.session_state["msg_pendientes"] = f"✅ {pend['username']} aprobado."
                st.rerun()
            if c2.button("❌ Rechazar", key=f"re_{pend['id']}"):
                db_rechazar_pendiente(pend["id"])
                st.session_state["msg_pendientes"] = f"⚠️ {pend['username']} rechazado."
                st.rerun()


def _tab_fases():
    st.subheader("Habilitar / Deshabilitar fases")
    fases = db_get_fases()
    cols  = st.columns(len(FASES))
    for idx, f in enumerate(FASES):
        estado = fases.get(f, False)
        nuevo  = cols[idx].toggle(f, value=estado, key=f"toggle_{f}")
        if nuevo != estado:
            db_toggle_fase(f, nuevo); st.rerun()


def _tab_partidos():
    st.subheader("Cargar partidos")
    if "msg_grupos" in st.session_state:
        st.success(st.session_state.pop("msg_grupos"))

    fase_sel = st.selectbox("Fase", FASES, key="fase_partidos")

    if fase_sel == "Grupos":
        partidos_cargados = db_get_partidos("Grupos")
        grupos_con_datos = set()
        for p in partidos_cargados:
            letra_g = "ABCDEFGHIJKL"[p["idx"] // 6]
            grupos_con_datos.add(letra_g)

        opciones_grupos = [f"{'✅' if l in grupos_con_datos else '○'} Grupo {l}" for l in "ABCDEFGHIJKL"]
        grupo_sel_raw = st.selectbox("Grupo", opciones_grupos)
        letra = grupo_sel_raw[-1]
        inicio = "ABCDEFGHIJKL".index(letra) * 6
        existentes_map = {p["idx"]: p for p in partidos_cargados}
        defaults = GRUPOS_DEFAULT.get(letra, [("", "")] * 6)

        equipos_existentes = db_get_equipos_grupos()
        equipos_base = sorted(
            set([
                *equipos_existentes,
                *[eq for partido in defaults for eq in partido if eq],
                *["Republica Checa", "Bosnia y Herzegovina", "Turquia", "Suecia", "Irak", "RD Congo"],
            ]),
            key=lambda x: str(x).lower()
        )

        st.markdown("### Editar nombres de equipos")
        st.caption("Esto reemplaza el nombre en partidos y selecciones especiales donde ya exista.")
        c_ren1, c_ren2 = st.columns([1.2, 1.2])
        equipo_actual = c_ren1.selectbox(
            "Equipo actual",
            options=equipos_base,
            format_func=_fmt_equipo,
            key=f"ren_equipo_{letra}",
        )
        nuevo_nombre = c_ren2.text_input(
            "Nuevo nombre",
            value=equipo_actual,
            key=f"ren_equipo_nuevo_{letra}",
        )
        if st.button("Guardar nuevo nombre", key=f"ren_equipo_btn_{letra}", use_container_width=True):
            nombre_limpio = (nuevo_nombre or "").strip()
            if not equipo_actual:
                st.error("Seleccioná un equipo.")
            elif not nombre_limpio:
                st.error("Escribí el nuevo nombre.")
            elif nombre_limpio == equipo_actual:
                st.warning("El nombre nuevo es igual al actual.")
            else:
                db_renombrar_equipo_global(equipo_actual, nombre_limpio)

                # No tocar valores de widgets ya instanciados en este mismo render.
                # Se limpian las keys y el rerun reconstruye todo con el nombre nuevo.
                for k in [f"ren_equipo_{letra}", f"ren_equipo_nuevo_{letra}"]:
                    if k in st.session_state:
                        del st.session_state[k]

                st.session_state["msg_grupos"] = f"✅ {equipo_actual} ahora es {nombre_limpio}."
                st.rerun()

        st.divider()

        with st.form(f"form_grupo_{letra}"):
            nuevos = []
            for j in range(6):
                idx_global = inicio + j
                prev = existentes_map.get(idx_global, {})
                local_actual = prev.get("local", defaults[j][0])
                visita_actual = prev.get("visita", defaults[j][1])

                opciones_local = equipos_base[:]
                if local_actual and local_actual not in opciones_local:
                    opciones_local.append(local_actual)
                opciones_local = sorted(set(opciones_local), key=lambda x: str(x).lower())

                opciones_visita = equipos_base[:]
                if visita_actual and visita_actual not in opciones_visita:
                    opciones_visita.append(visita_actual)
                opciones_visita = sorted(set(opciones_visita), key=lambda x: str(x).lower())

                c1, c2 = st.columns(2)
                l = c1.selectbox(
                    "Local",
                    options=opciones_local,
                    index=opciones_local.index(local_actual) if local_actual in opciones_local else 0,
                    format_func=_fmt_equipo,
                    key=f"gl_{letra}_{j}",
                )
                v = c2.selectbox(
                    "Visitante",
                    options=opciones_visita,
                    index=opciones_visita.index(visita_actual) if visita_actual in opciones_visita else 0,
                    format_func=_fmt_equipo,
                    key=f"gv_{letra}_{j}",
                )
                nuevos.append((idx_global, l, v))

            col_b1, col_b2 = st.columns(2)
            guardar = col_b1.form_submit_button(f"Guardar Grupo {letra}", type="primary")
            guardar_todos = col_b2.form_submit_button("Guardar todos los grupos")

        if guardar:
            errores = [f"Partido {((idx_global - inicio) + 1)}: mismo equipo de local y visitante" for idx_global, l, v in nuevos if l and v and l == v]
            if errores:
                st.error("⚠️ " + " · ".join(errores))
            else:
                with st.spinner(f"Guardando Grupo {letra}..."):
                    for idx_global, l, v in nuevos:
                        if l and v:
                            db_guardar_partido("Grupos", idx_global, l, v)
                st.session_state["msg_grupos"] = f"✅ Grupo {letra} guardado."
                st.rerun()

        if guardar_todos:
            with st.spinner("Guardando todos los grupos..."):
                for gr, partidos_gr in GRUPOS_DEFAULT.items():
                    ini_gr = "ABCDEFGHIJKL".index(gr) * 6
                    for j, (loc, vis) in enumerate(partidos_gr):
                        db_guardar_partido("Grupos", ini_gr + j, loc, vis)
            st.session_state["msg_grupos"] = "✅ Todos los grupos guardados con los equipos por defecto."
            st.rerun()

    else:
        cant = {"Dieciseisavos": 16, "Octavos": 8, "Cuartos": 4, "Semifinal": 2, "Final": 1}[fase_sel]
        partidos_existentes = db_get_partidos(fase_sel)
        existentes_map = {p["idx"]: p for p in partidos_existentes}
        equipos_grupos = db_get_equipos_grupos()

        if not equipos_grupos:
            st.warning("⚠️ Primero cargá los partidos de la fase de Grupos.")
        else:
            NINGUNO = "— Seleccionar —"
            opciones = [NINGUNO] + equipos_grupos

            with st.form(f"form_{fase_sel}"):
                nuevos = []
                for i in range(cant):
                    prev = existentes_map.get(i, {})
                    prev_local = prev.get("local", "")
                    prev_visita = prev.get("visita", "")
                    idx_local = opciones.index(prev_local) if prev_local in opciones else 0
                    idx_visita = opciones.index(prev_visita) if prev_visita in opciones else 0

                    st.markdown(f"<div style='color:var(--text3); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-top:0.8rem; margin-bottom:0.2rem;'>Partido {i+1}</div>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    sel_local = c1.selectbox("Local", opciones, index=idx_local, format_func=lambda x: x if x == NINGUNO else _fmt_equipo(x), key=f"{fase_sel}_l_{i}")
                    sel_visita = c2.selectbox("Visitante", opciones, index=idx_visita, format_func=lambda x: x if x == NINGUNO else _fmt_equipo(x), key=f"{fase_sel}_v_{i}")
                    nuevos.append((i, "" if sel_local == NINGUNO else sel_local, "" if sel_visita == NINGUNO else sel_visita))

                guardar = st.form_submit_button("Guardar partidos", type="primary")

            if guardar:
                errores = [f"Partido {i+1}: mismo equipo de local y visitante" for i, l, v in nuevos if l and v and l == v]
                if errores:
                    st.error("⚠️ " + " · ".join(errores))
                else:
                    guardados = sum(1 for _, l, v in nuevos if l and v)
                    for i, l, v in nuevos:
                        if l and v:
                            db_guardar_partido(fase_sel, i, l, v)
                    st.success(f"✅ {guardados} partido(s) guardado(s).") if guardados else st.warning("No se guardó ningún partido.")


def _tab_resultados():
    st.subheader("Cargar resultados reales")
    if "res_ok" in st.session_state:
        st.success(st.session_state.pop("res_ok"))

    fase_sel = st.selectbox("Fase", FASES, key="fase_resultados")
    partidos = db_get_partidos(fase_sel)
    if not partidos:
        st.info("No hay partidos cargados para esta fase.")
        return

    resultados_actuales = db_get_resultado_completo(fase_sel)

    if fase_sel == "Grupos":
        grupo_sel_r = st.selectbox("Grupo", [f"Grupo {l}" for l in "ABCDEFGHIJKL"], key="grupo_res")
        letra_r     = grupo_sel_r[-1]
        inicio_r    = "ABCDEFGHIJKL".index(letra_r) * 6
        partidos_vista = [p for p in partidos if inicio_r <= p["idx"] < inicio_r + 6]
    else:
        partidos_vista = partidos
        inicio_r       = 0
        letra_r        = ""

    for p in partidos_vista:
        idx       = p["idx"]
        tiene_res = idx in resultados_actuales
        rl_prev, rv_prev = resultados_actuales.get(idx, (0, 0))
        border    = "rgba(0,200,80,0.3)" if tiene_res else "var(--border2)"
        bg        = "rgba(0,200,80,0.05)" if tiene_res else "var(--surface)"

        activar = st.checkbox("Cargar resultado", value=tiene_res, key=f"chk_{fase_sel}_{idx}")
        if activar:
            c_local, c_rl, c_sep, c_rv, c_visita, c_btn = st.columns([3, 1, 0.4, 1, 3, 1.5])
            c_local.markdown(f"<div style='text-align:right; font-weight:700; font-size:0.9rem; padding-top:9px; color:var(--text);'>{bandera(p['local'])} {p['local']}</div>", unsafe_allow_html=True)
            rl = c_rl.number_input("rl", 0, 15, int(rl_prev), key=f"rl_{fase_sel}_{idx}", label_visibility="collapsed")
            c_sep.markdown("<div style='text-align:center; padding-top:9px; color:var(--text3);'>—</div>", unsafe_allow_html=True)
            rv = c_rv.number_input("rv", 0, 15, int(rv_prev), key=f"rv_{fase_sel}_{idx}", label_visibility="collapsed")
            c_visita.markdown(f"<div style='text-align:left; font-weight:700; font-size:0.9rem; padding-top:9px; color:var(--text);'>{bandera(p['visita'])} {p['visita']}</div>", unsafe_allow_html=True)
            if c_btn.button("💾", key=f"save_{fase_sel}_{idx}", help="Guardar resultado"):
                with st.spinner("Guardando y recalculando puntajes..."):
                    db_guardar_resultado(fase_sel, idx, rl, rv)
                    db_calcular_puntos()
                    db_calcular_puntos_especiales()
                    st.cache_data.clear()
                st.session_state["res_ok"] = f"✅ Guardado: {p['local']} {rl} — {rv} {p['visita']}. Puntajes y ranking actualizados."
                st.rerun()
            if tiene_res:
                st.caption(f"✅ Guardado: {p['local']} {rl_prev} — {rv_prev} {p['visita']}")
        else:
            st.markdown(f"""<div style="display:flex; align-items:center; gap:8px; padding:2px 0 4px 0;">
                <div style="color:var(--text); font-weight:700; font-size:0.9rem; flex:1; text-align:right;">{bandera(p['local'])} {p['local']}</div>
                <div style="color:var(--text3); font-size:0.8rem;">vs</div>
                <div style="color:var(--text); font-weight:700; font-size:0.9rem; flex:1;">{bandera(p['visita'])} {p['visita']}</div>
            </div>""", unsafe_allow_html=True)

    # Limpiar resultados
    st.divider()
    cant_resultados = len(resultados_actuales)
    if cant_resultados > 0:
        if fase_sel == "Grupos":
            cant_grupo = sum(1 for idx in resultados_actuales if inicio_r <= idx < inicio_r + 6)
            label_limpiar = f"Grupo {letra_r} ({cant_grupo} resultado(s))"
        else:
            label_limpiar = f"{fase_sel} ({cant_resultados} resultado(s))"

        with st.form(f"form_limpiar_res_{fase_sel}"):
            st.warning(f"⚠️ Esto borrará los resultados de {label_limpiar} y recalculará los puntajes.")
            pw_limpiar    = st.text_input("Tu contraseña de admin para confirmar", type="password", key=f"pw_limpiar_{fase_sel}")
            limpiar_btn   = st.form_submit_button(f"🗑️ Limpiar {label_limpiar}", type="primary")

        if limpiar_btn:
            admin_lr = db_get_usuario(st.session_state.usuario)
            if admin_lr["clave"] != hash_clave(pw_limpiar):
                st.session_state["res_ok"] = "❌ Contraseña incorrecta."
            else:
                if fase_sel == "Grupos":
                    with get_db() as conn:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM resultados WHERE fase=%s AND partido_idx >= %s AND partido_idx < %s",
                                    ("Grupos", inicio_r, inicio_r + 6))
                    st.cache_data.clear()
                else:
                    db_limpiar_resultados_fase(fase_sel)
                db_calcular_puntos()
                st.session_state["res_ok"] = f"🗑️ Resultados de {label_limpiar} eliminados y puntajes recalculados."
            st.rerun()


def _tab_consumo():
    st.subheader("Sumar consumo")
    if "msg_consumo" in st.session_state:
        st.success(st.session_state.pop("msg_consumo"))

    busq_consumo = st.text_input("Buscar usuario", key="busq_consumo")
    if busq_consumo:
        todos = db_get_todos_usuarios()
        opts  = {u["username"]: u.get("nombre") or u["username"] for u in todos
                 if busq_consumo.lower() in u["username"].lower() or busq_consumo.lower() in (u.get("nombre") or "").lower()}
        if opts:
            with st.form("form_consumo"):
                sel  = st.selectbox("Usuario", list(opts.keys()), format_func=lambda x: f"{opts[x]} ({x})")
                pts  = st.number_input("Puntos a sumar", 0, 500, 0)
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
    filtro_desde   = col_f2.date_input("Desde", value=None, key="hist_desde")
    filtro_hasta   = col_f3.date_input("Hasta", value=None, key="hist_hasta")
    log = db_get_consumo_log()
    if log:
        df_log = pd.DataFrame(log)[["id", "fecha", "username", "puntos", "descripcion"]]
        df_log.columns = ["ID", "Fecha", "Usuario", "Puntos", "Descripción"]
        df_log["Fecha"] = pd.to_datetime(df_log["Fecha"])
        if filtro_usuario: df_log = df_log[df_log["Usuario"].str.contains(filtro_usuario, case=False, na=False)]
        if filtro_desde:   df_log = df_log[df_log["Fecha"].dt.date >= filtro_desde]
        if filtro_hasta:   df_log = df_log[df_log["Fecha"].dt.date <= filtro_hasta]
        df_log["Fecha"] = df_log["Fecha"].dt.strftime("%d/%m/%Y %H:%M")
        PAGINA_SIZE   = 20
        total         = len(df_log)
        if total == 0:
            st.info("No hay registros con esos filtros.")
        else:
            total_paginas = max(1, (total - 1) // PAGINA_SIZE + 1)
            pagina        = st.number_input("Página", min_value=1, max_value=total_paginas, value=1, step=1)
            inicio        = (pagina - 1) * PAGINA_SIZE
            fin           = inicio + PAGINA_SIZE
            st.caption(f"Mostrando {min(fin, total)} de {total} registros — Página {pagina}/{total_paginas}")
            slice_df = df_log.iloc[inicio:fin]
            filas_log = ""
            for _, row in slice_df.iterrows():
                filas_log += f"""<tr>
                    <td style="padding:9px 12px; color:var(--text3); font-size:0.85rem;">{row['ID']}</td>
                    <td style="padding:9px 12px; color:var(--text2);">{row['Fecha']}</td>
                    <td style="padding:9px 12px; color:var(--text); font-weight:600;">{row['Usuario']}</td>
                    <td style="padding:9px 12px; color:var(--green); font-weight:700; text-align:center;">{row['Puntos']}</td>
                    <td style="padding:9px 12px; color:var(--text2);">{row.get('Descripción', '')}</td>
                </tr>"""
            st.markdown(f"""<table style="width:100%; border-collapse:collapse; background:var(--table-bg); border-radius:12px; overflow:hidden; border:1px solid var(--border);">
                <thead><tr style="background:var(--table-head); border-bottom:1px solid var(--border);">
                    <th style="padding:9px 12px; color:var(--text3); font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">ID</th>
                    <th style="padding:9px 12px; color:var(--text3); font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Fecha</th>
                    <th style="padding:9px 12px; color:var(--text3); font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Usuario</th>
                    <th style="padding:9px 12px; color:var(--text3); font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; text-align:center;">Pts</th>
                    <th style="padding:9px 12px; color:var(--text3); font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Descripción</th>
                </tr></thead><tbody>{filas_log}</tbody></table>""", unsafe_allow_html=True)
            st.markdown(f"**Total puntos en filtro: {df_log['Puntos'].sum()}**")
    else:
        st.info("Todavía no hay registros de consumo.")

    st.divider()
    st.subheader("Eliminar registro de consumo")
    with st.form("form_eliminar_consumo"):
        id_eliminar    = st.number_input("ID del registro a eliminar", min_value=1, step=1)
        clave_admin_el = st.text_input("Tu contraseña de admin para confirmar", type="password")
        eliminar_btn   = st.form_submit_button("🗑️ Eliminar registro", type="primary")
    if eliminar_btn:
        admin = db_get_usuario(st.session_state.usuario)
        if admin["clave"] != hash_clave(clave_admin_el):
            st.error("Contraseña incorrecta.")
        else:
            db_eliminar_consumo_log(int(id_eliminar)); db_calcular_puntos()
            st.session_state["msg_consumo"] = f"✅ Registro #{int(id_eliminar)} eliminado y puntos descontados."
            st.rerun()



def _tab_pagos():
    st.subheader("Datos de pago del registro")

    if "msg_pagos" in st.session_state:
        st.success(st.session_state.pop("msg_pagos"))

    pago = db_get_pago_config()

    with st.form("form_admin_pagos"):
        titular = st.text_input("Titular", value=pago.get("titular", ""))
        alias = st.text_input("Alias", value=pago.get("alias", ""))
        cvu = st.text_input("CVU", value=pago.get("cvu", ""))
        monto = st.text_input("Monto de inscripción", value=pago.get("monto", ""), placeholder="Ej: $5000")
        instrucciones = st.text_area(
            "Texto adicional",
            value=pago.get("instrucciones", ""),
            placeholder="Ej: Transferí, subí el comprobante y aguardá aprobación."
        )

        guardar = st.form_submit_button("Guardar cambios", type="primary", use_container_width=True)

    if guardar:
        if not titular.strip():
            st.error("Completá el titular.")
            return
        if not alias.strip():
            st.error("Completá el alias.")
            return
        if not cvu.strip():
            st.error("Completá el CVU.")
            return

        db_set_pago_config(titular, alias, cvu, instrucciones, monto)
        st.session_state["msg_pagos"] = "✅ Datos de pago actualizados."
        st.rerun()

    st.divider()
    # Recargar config guardada para la vista previa (no depender de los widgets del form)
    pago_preview = db_get_pago_config()
    titular_p     = pago_preview.get("titular", "")
    alias_p       = pago_preview.get("alias", "")
    cvu_p         = pago_preview.get("cvu", "")
    instruc_p     = pago_preview.get("instrucciones", "")
    monto_p       = pago_preview.get("monto", "")

    st.markdown("**Vista previa** (muestra los datos guardados actualmente)")
    if not titular_p and not alias_p and not cvu_p:
        st.info("Todavía no hay datos de pago guardados. Completá el formulario y guardá.")
    else:
        instruc_html = '<div style="margin-top:10px;color:#cfdbeb;font-size:0.82rem;line-height:1.6;">' + instruc_p + '</div>' if instruc_p else ""
        monto_html = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><span style="color:#cfdbeb;font-size:0.82rem;">Inscripción</span><span style="color:#f5c76b;font-weight:800;font-size:1rem;">' + monto_p + '</span></div>' if monto_p else ""
        preview_html = (
            '<div style="background:rgba(245,199,107,0.12);border:1.5px solid rgba(245,199,107,0.32);border-radius:10px;padding:12px 16px;margin:0.5rem 0;">'
            '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#f5c76b;margin-bottom:10px;">💰 Datos de pago</div>'
            + monto_html +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
            '<span style="color:#cfdbeb;font-size:0.82rem;">Titular</span>'
            '<span style="color:#f5f8fc;font-weight:700;font-size:0.88rem;">' + titular_p + '</span>'
            '</div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
            '<span style="color:#cfdbeb;font-size:0.82rem;">Alias</span>'
            '<span style="color:#f5f8fc;font-weight:700;font-family:monospace;font-size:0.88rem;">' + alias_p + '</span>'
            '</div>'
            '<div style="background:#10203a;border:1.5px solid rgba(143,170,214,0.28);border-radius:7px;color:#f5f8fc;font-family:monospace;font-size:0.88rem;font-weight:700;padding:8px 12px;">' + cvu_p + '</div>'
            + instruc_html +
            '</div>'
        )
        st.markdown(preview_html, unsafe_allow_html=True)



def _parse_uploaded_special_list(uploaded_file):
    if not uploaded_file:
        return ''
    data = uploaded_file.read()
    for enc in ('utf-8', 'utf-8-sig', 'latin-1'):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode('utf-8', errors='ignore')


def _render_admin_lista_especiales(tipo: str, titulo: str, ayuda: str):
    st.markdown(f"### {titulo}")
    lista_actual = db_get_lista_especiales(tipo)
    st.caption(f"{len(lista_actual)} nombres activos. {ayuda}")

    uploaded = st.file_uploader(
        f"Subir archivo para {titulo.lower()}",
        type=['txt', 'csv'],
        key=f"upload_lista_{tipo}",
        help='Acepta .txt o .csv con un nombre por línea, o separados por coma o punto y coma.',
    )
    default_text = st.session_state.get(f"raw_lista_{tipo}", '')
    if uploaded is not None:
        default_text = _parse_uploaded_special_list(uploaded)
        st.session_state[f"raw_lista_{tipo}"] = default_text

    raw_text = st.text_area(
        'Pegá la lista completa',
        value=default_text,
        key=f"raw_lista_{tipo}",
        height=180,
        placeholder='Un nombre por línea\nEjemplo:\nLionel Messi\nJulián Álvarez\nKylian Mbappé',
    )

    c1, c2 = st.columns(2)
    if c1.button('💾 Reemplazar lista completa', key=f"save_lista_{tipo}", use_container_width=True, type='primary'):
        try:
            nueva = db_set_lista_especiales_desde_texto(tipo, raw_text)
            st.session_state['msg_esp_adm'] = f"✅ Lista de {titulo.lower()} actualizada. Ahora hay {len(nueva)} nombres."
        except Exception as e:
            st.session_state['msg_esp_adm'] = f"❌ {e}"
        st.rerun()
    if c2.button('↺ Volver a la lista base', key=f"reset_lista_{tipo}", use_container_width=True):
        base = db_reset_lista_especiales(tipo)
        st.session_state[f"raw_lista_{tipo}"] = '\n'.join(base)
        st.session_state['msg_esp_adm'] = f"✅ Lista de {titulo.lower()} restablecida a la versión base."
        st.rerun()

    if lista_actual:
        preview = lista_actual[:12]
        st.markdown(
            "<div style='background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:12px 14px;margin:8px 0 14px 0;'>"
            f"<div style='font-size:0.72rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Vista previa</div>"
            f"<div style='color:var(--text2);font-size:0.85rem;line-height:1.7;'>" + ' · '.join(preview) + (' · ...' if len(lista_actual) > 12 else '') + '</div></div>',
            unsafe_allow_html=True,
        )

def _tab_especiales():
    st.subheader("⭐ Pronósticos especiales — Resultados")
    if "msg_esp_adm" in st.session_state:
        st.success(st.session_state.pop("msg_esp_adm"))

    with st.expander("🗂️ Listas de jugadores y arqueros para especiales", expanded=True):
        st.markdown("Cuando guardás una lista nueva, reemplaza completa la anterior y se refleja tanto en admin como en usuario.")
        _render_admin_lista_especiales("jugadores", "Jugadores", "Sirve para goleador y mejor jugador.")
        _render_admin_lista_especiales("arqueros", "Arqueros", "Sirve para mejor arquero.")


    equipos_adm  = db_get_equipos_grupos() or sorted(BANDERAS.keys())
    todos_esp    = db_get_todos_especiales()
    df_esp       = pd.DataFrame(todos_esp) if todos_esp else pd.DataFrame()

    # Variantes manuales
    variantes_por_cat = {}
    for cat in CATEGORIAS_ESPECIALES:
        if cat == "campeon": continue
        lista_oficial = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
        if not df_esp.empty and cat in df_esp["categoria"].values:
            sub    = df_esp[df_esp["categoria"] == cat]
            otros  = sub[~sub["eleccion"].isin(lista_oficial)]["eleccion"].unique().tolist()
            if otros: variantes_por_cat[cat] = otros



    selecciones_adm = {}
    for cat, info in CATEGORIAS_ESPECIALES.items():
        resultado_actual = db_get_resultado_especial(cat)
        col_tit, col_pts = st.columns([4, 1])
        col_tit.markdown(f"**{info['label']}**")
        col_pts.markdown(f"<div style='text-align:right; color:var(--gold); font-family:Bebas Neue,sans-serif; font-size:1.1rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)
        if resultado_actual:
            st.markdown(f"<div style='color:var(--green); font-size:0.82rem; margin-bottom:2px;'>Guardado: <b>{resultado_actual}</b></div>", unsafe_allow_html=True)

        if cat == "campeon":
            ops_adm = [f"{bandera(e)} {e}" for e in equipos_adm]
            d2n_adm = {f"{bandera(e)} {e}": e for e in equipos_adm}
            idx_adm = next((i for i, e in enumerate(equipos_adm) if e == resultado_actual), 0)
            sel_adm = st.selectbox("Nuevo campeón real", ops_adm, index=idx_adm, key=f"adm_sel_{cat}")
            selecciones_adm[cat] = d2n_adm.get(sel_adm, sel_adm)
        else:
            lista_adm = db_get_lista_especiales('arqueros') if cat == 'arquero' else db_get_lista_especiales('jugadores')
            label_adm = "arquero" if cat == "arquero" else "jugador"

            sel_key = f"adm_elegido_{cat}"
            cambiar_key = f"adm_cambiar_{cat}"
            input_key = f"adm_busq_{cat}"
            applied_key = f"adm_busq_aplicada_{cat}"
            reset_key = f"adm_busq_reset_{cat}"

            if st.session_state.pop(reset_key, False):
                st.session_state[input_key] = ""
                st.session_state[applied_key] = ""

            sel_actual = st.session_state.get(sel_key, resultado_actual)
            if sel_actual:
                st.markdown(f"<div style='color:var(--green); font-size:0.88rem; margin:4px 0 8px 0;'>✅ Elegido: <b>{sel_actual}</b></div>", unsafe_allow_html=True)
            selecciones_adm[cat] = sel_actual

            if st.session_state.get(cambiar_key, not bool(sel_actual)):
                col_busq, col_btn = st.columns([5, 1])
                with col_busq:
                    st.text_input(
                        f"Buscar {label_adm}",
                        key=input_key,
                        placeholder="Escribí el nombre (con o sin acento)...",
                    )
                with col_btn:
                    st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                    if st.button("🔎", key=f"adm_lupa_{cat}", use_container_width=True):
                        st.session_state[applied_key] = (st.session_state.get(input_key, "") or "").strip()
                        st.rerun()

                busqueda_aplicada = (st.session_state.get(applied_key, "") or "").strip()
                if busqueda_aplicada:
                    filtrados_adm = [j for j in lista_adm if _norm(busqueda_aplicada) in _norm(j)][:8]
                    if not filtrados_adm:
                        st.caption(f"No se encontró ningún {label_adm}.")
                    else:
                        for jug in filtrados_adm:
                            if st.button(jug, key=f"adm_jug_{cat}_{jug}", use_container_width=True):
                                st.session_state[sel_key] = jug
                                st.session_state[cambiar_key] = False
                                st.session_state[reset_key] = True
                                selecciones_adm[cat] = jug
                                st.rerun()
                else:
                    st.caption(f"Escribí el nombre y tocá la lupa para buscar {label_adm}.")
            else:
                if st.button(f"✏️ Cambiar {label_adm}", key=f"adm_cambiar_btn_{cat}"):
                    st.session_state[cambiar_key] = True
                    st.session_state[reset_key] = True
                    st.rerun()
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.divider()
    pw_esp_adm = st.text_input("🔒 Tu contraseña de admin", type="password", key="pw_guardar_esp")
    guardar_todos_esp = st.button("💾 Guardar todos y aplicar puntos", type="primary", use_container_width=True)

    if guardar_todos_esp:
        admin_esp = db_get_usuario(st.session_state.usuario)
        if admin_esp["clave"] != hash_clave(pw_esp_adm):
            st.session_state["msg_esp_adm"] = "❌ Contraseña incorrecta."
        else:
            guardados = 0
            with st.spinner("Guardando..."):
                for cat, ganador in selecciones_adm.items():
                    if ganador:
                        db_guardar_resultado_especial(cat, ganador)
                        guardados += 1
                if guardados:
                    db_calcular_puntos_especiales()
            st.session_state["msg_esp_adm"] = f"✅ {guardados} resultado(s) guardado(s) y puntos aplicados." if guardados else "⚠️ No seleccionaste ningún ganador."
        st.rerun()

    # Limpiar especiales
    st.divider()
    resultados_esp_actuales = {cat: db_get_resultado_especial(cat) for cat in CATEGORIAS_ESPECIALES}
    if any(v for v in resultados_esp_actuales.values()):
        with st.form("form_limpiar_especiales"):
            st.warning("⚠️ Esto borrará TODOS los resultados especiales y recalculará puntajes.")
            pw_limp_esp   = st.text_input("Tu contraseña de admin", type="password", key="pw_limpiar_esp")
            limpiar_esp   = st.form_submit_button("🗑️ Limpiar resultados especiales", type="primary")
        if limpiar_esp:
            admin_le = db_get_usuario(st.session_state.usuario)
            if admin_le["clave"] != hash_clave(pw_limp_esp):
                st.session_state["msg_esp_adm"] = "❌ Contraseña incorrecta."
            else:
                db_limpiar_resultados_especiales(); db_calcular_puntos()
                st.session_state["msg_esp_adm"] = "🗑️ Resultados especiales eliminados y puntajes recalculados."
            st.rerun()


def _tab_usuarios():
    st.subheader("👤 Gestión de usuarios")
    if "msg_usuarios" in st.session_state: st.success(st.session_state.pop("msg_usuarios"))
    if "err_usuarios" in st.session_state: st.error(st.session_state.pop("err_usuarios"))

    accion = st.radio("Acción", ["➕ Crear", "✏️ Editar", "🔑 Contraseña", "🗑️ Borrar"], horizontal=True, key="accion_usuarios")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    meses_es_adm = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    if accion == "➕ Crear":
        with st.form("form_crear_usuario"):
            nu_user  = st.text_input("Username")
            nu_pass  = st.text_input("Contraseña", type="password")
            nu_pass2 = st.text_input("Confirmar contraseña", type="password")
            nu_nombre = st.text_input("Nombre y apellido")
            nu_mail   = st.text_input("Mail")
            nu_cel    = st.text_input("Celular")
            nu_loc    = st.text_input("Localidad")
            col_y, col_m, col_d = st.columns(3)
            nu_anio = col_y.selectbox("Año", list(range(1930, datetime.date.today().year+1))[::-1], key="nu_anio")
            nu_mes  = col_m.selectbox("Mes", list(range(1,13)), format_func=lambda x: meses_es_adm[x-1], key="nu_mes")
            nu_dia  = col_d.selectbox("Día", list(range(1,32)), key="nu_dia")
            nu_admin = st.checkbox("Es administrador")
            crear_btn = st.form_submit_button("➕ Crear usuario", type="primary")
        if crear_btn:
            u_strip = nu_user.strip().lower()
            try:   nu_nac = str(datetime.date(nu_anio, nu_mes, nu_dia))
            except ValueError: nu_nac = ""
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
                with st.spinner("Creando usuario..."):
                    with get_db() as conn:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO usuarios (username, clave, nombre, mail, celular, localidad, nacimiento, es_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                    (u_strip, hash_clave(nu_pass), nu_nombre.strip(), nu_mail.strip(), nu_cel.strip(), nu_loc.strip(), nu_nac, 1 if nu_admin else 0))
                    st.cache_data.clear()
                st.session_state["msg_usuarios"] = f"✅ Usuario **{u_strip}** creado."
                st.rerun()

    elif accion == "✏️ Editar":
        busq_ed = st.text_input("Buscar usuario", key="busq_editar", placeholder="Nombre o username...")
        todos_ed = db_get_todos_usuarios()
        if busq_ed:
            todos_ed = [u for u in todos_ed if busq_ed.lower() in u["username"].lower() or busq_ed.lower() in (u.get("nombre") or "").lower()]
        if busq_ed and todos_ed:
            opts_ed = {u["username"]: f"{u.get('nombre') or u['username']} (@{u['username']})" for u in todos_ed}
            sel_ed  = st.selectbox("Seleccioná", list(opts_ed.keys()), format_func=lambda x: opts_ed[x], key="sel_editar")
            u_ed    = db_get_usuario(sel_ed)
            if u_ed:
                nac_str = u_ed.get("nacimiento") or ""
                try:    nac_date = datetime.date.fromisoformat(nac_str); nac_anio, nac_mes, nac_dia = nac_date.year, nac_date.month, nac_date.day
                except: nac_anio, nac_mes, nac_dia = 1990, 1, 1
                with st.form("form_editar_usuario"):
                    ed_nombre = st.text_input("Nombre y apellido", value=u_ed.get("nombre") or "")
                    ed_mail   = st.text_input("Mail",     value=u_ed.get("mail")     or "")
                    ed_cel    = st.text_input("Celular",  value=u_ed.get("celular")  or "")
                    ed_loc    = st.text_input("Localidad",value=u_ed.get("localidad")or "")
                    col_y2, col_m2, col_d2 = st.columns(3)
                    ed_anio = col_y2.selectbox("Año", list(range(1930, datetime.date.today().year+1))[::-1],
                                               index=list(range(1930, datetime.date.today().year+1))[::-1].index(nac_anio) if nac_anio in range(1930, datetime.date.today().year+1) else 0, key="ed_anio")
                    ed_mes  = col_m2.selectbox("Mes", list(range(1,13)), index=nac_mes-1, format_func=lambda x: meses_es_adm[x-1], key="ed_mes")
                    ed_dia  = col_d2.selectbox("Día", list(range(1,32)), index=nac_dia-1, key="ed_dia")
                    guardar_ed = st.form_submit_button("💾 Guardar cambios", type="primary")
                if guardar_ed:
                    try:    ed_nac = str(datetime.date(ed_anio, ed_mes, ed_dia))
                    except: ed_nac = nac_str
                    if not ed_nombre.strip():
                        st.session_state["err_usuarios"] = "El nombre no puede estar vacío."
                    else:
                        with get_db() as conn:
                            cur = conn.cursor()
                            cur.execute("UPDATE usuarios SET nombre=%s, mail=%s, celular=%s, localidad=%s, nacimiento=%s WHERE username=%s",
                                        (ed_nombre.strip(), ed_mail.strip(), ed_cel.strip(), ed_loc.strip(), ed_nac, sel_ed))
                        st.cache_data.clear()
                        st.session_state["msg_usuarios"] = f"✅ Datos de **{sel_ed}** actualizados."
                        st.rerun()
        elif busq_ed:
            st.info("No se encontró ningún usuario.")

    elif accion == "🔑 Contraseña":
        busq_pw  = st.text_input("Buscar usuario", key="busq_clave", placeholder="Nombre o username...")
        todos_pw = db_get_todos_usuarios()
        if busq_pw:
            todos_pw = [u for u in todos_pw if busq_pw.lower() in u["username"].lower() or busq_pw.lower() in (u.get("nombre") or "").lower()]
        if busq_pw and todos_pw:
            opts_pw = {u["username"]: f"{u.get('nombre') or u['username']} (@{u['username']})" for u in todos_pw}
            sel_pw  = st.selectbox("Seleccioná", list(opts_pw.keys()), format_func=lambda x: opts_pw[x], key="sel_clave")
            with st.form("form_reset_clave"):
                nueva_pw  = st.text_input("Nueva contraseña", type="password")
                nueva_pw2 = st.text_input("Confirmar nueva contraseña", type="password")
                resetear  = st.form_submit_button("🔑 Cambiar contraseña", type="primary")
            if resetear:
                if len(nueva_pw) < 4:    st.session_state["err_usuarios"] = "Mínimo 4 caracteres."
                elif nueva_pw != nueva_pw2: st.session_state["err_usuarios"] = "Las contraseñas no coinciden."
                else:
                    db_reset_clave(sel_pw, nueva_pw)
                    st.session_state["msg_usuarios"] = f"✅ Contraseña de **{sel_pw}** actualizada."
                    st.rerun()
        elif busq_pw:
            st.info("No se encontró ningún usuario.")

    elif accion == "🗑️ Borrar":
        st.warning("⚠️ Irreversible — se borran el usuario y todos sus pronósticos.")
        busq_del  = st.text_input("Buscar usuario", key="busq_borrar", placeholder="Nombre o username...")
        todos_del = db_get_todos_usuarios()
        if busq_del:
            todos_del = [u for u in todos_del if busq_del.lower() in u["username"].lower() or busq_del.lower() in (u.get("nombre") or "").lower()]
        if busq_del and todos_del:
            opts_del = {u["username"]: f"{u.get('nombre') or u['username']} (@{u['username']})" for u in todos_del}
            sel_del  = st.selectbox("Seleccioná el usuario a borrar", list(opts_del.keys()), format_func=lambda x: opts_del[x], key="sel_borrar")
            with st.form("form_borrar_usuario"):
                clave_adm_del = st.text_input("Tu contraseña de admin", type="password")
                borrar_btn    = st.form_submit_button("🗑️ Borrar usuario", type="primary")
            if borrar_btn:
                admin_u = db_get_usuario(st.session_state.usuario)
                if admin_u["clave"] != hash_clave(clave_adm_del):
                    st.session_state["err_usuarios"] = "Contraseña incorrecta."
                else:
                    db_borrar_usuario(sel_del); st.cache_data.clear()
                    st.session_state["msg_usuarios"] = f"✅ Usuario **{sel_del}** borrado."
                st.rerun()
        elif busq_del:
            st.info("No se encontró ningún usuario.")


def _tab_reset():
    st.subheader("⚠️ Resetear puntajes")

    # ── Reset por fase ──────────────────────────────────────────────────────
    st.markdown("**Resetear una fase específica**")
    st.caption("Borra los pronósticos y resultados de una sola fase y recalcula los puntajes.")

    fases_con_datos = []
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT fase FROM (
                SELECT fase FROM prodes WHERE partido_idx >= 0
                UNION
                SELECT fase FROM resultados
            ) sub ORDER BY fase
        """)
        fases_con_datos = [r["fase"] for r in cur.fetchall()]

    if not fases_con_datos:
        st.info("No hay fases con datos para resetear.")
    else:
        with st.form("form_reset_fase"):
            fase_reset = st.selectbox("Fase a resetear", fases_con_datos, key="fase_reset_sel")
            pw_reset_f = st.text_input("Tu contraseña de admin", type="password", key="pw_reset_fase")
            reset_fase_btn = st.form_submit_button(f"🗑️ Resetear fase", type="primary")
        if reset_fase_btn:
            admin_rf = db_get_usuario(st.session_state.usuario)
            if admin_rf["clave"] != hash_clave(pw_reset_f):
                st.error("Contraseña incorrecta.")
            else:
                with get_db() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM prodes WHERE fase=%s", (fase_reset,))
                    cur.execute("DELETE FROM resultados WHERE fase=%s", (fase_reset,))
                db_calcular_puntos()
                st.cache_data.clear()
                st.success(f"✅ Fase {fase_reset} reseteada.")
                st.rerun()

    st.divider()

    # ── Recalcular puntajes ─────────────────────────────────────────────────
    st.markdown("**Recalcular puntajes**")
    st.caption("Vuelve a calcular todos los puntos en base a los pronósticos y resultados actuales.")
    with st.form("form_recalcular"):
        pw_recalc = st.text_input("Tu contraseña de admin", type="password", key="pw_recalcular")
        recalc_btn = st.form_submit_button("🔄 Recalcular puntajes", type="primary")
    if recalc_btn:
        admin_rc = db_get_usuario(st.session_state.usuario)
        if admin_rc["clave"] != hash_clave(pw_recalc):
            st.error("Contraseña incorrecta.")
        else:
            db_calcular_puntos()
            st.cache_data.clear()
            st.success("✅ Puntajes recalculados correctamente.")
            st.rerun()

    st.divider()

    # ── Reset total ─────────────────────────────────────────────────────────
    st.markdown("**Resetear todo**")
    st.error("Esta acción borrará TODOS los pronósticos, resultados y puntajes. No se puede deshacer.")
    with st.form("form_reset_general"):
        clave_admin_r = st.text_input("Tu contraseña de admin para confirmar", type="password")
        confirmar_r   = st.text_input("Escribí CONFIRMAR para continuar")
        resetear_todo = st.form_submit_button("⚠️ Resetear todo", type="primary")
    if resetear_todo:
        admin = db_get_usuario(st.session_state.usuario)
        if admin["clave"] != hash_clave(clave_admin_r):
            st.error("Contraseña incorrecta.")
        elif confirmar_r != "CONFIRMAR":
            st.error("Tenés que escribir exactamente CONFIRMAR para continuar.")
        else:
            db_resetear_todos_puntajes()
            st.success("✅ Todos los puntajes, pronósticos y resultados fueron reseteados.")


def _tab_exportar():
    st.subheader("📥 Base de datos de usuarios")
    todos_exp = db_get_todos_usuarios()
    if not todos_exp:
        st.info("No hay usuarios registrados todavía.")
        return

    rows_exp = [{"Usuario": u.get("username",""), "Nombre": u.get("nombre",""),
                 "Nacimiento": u.get("nacimiento",""), "Localidad": u.get("localidad",""),
                 "Celular": u.get("celular",""), "Mail": u.get("mail",""),
                 "Puntos": u.get("puntos",0), "Goles": u.get("goles",0),
                 "Consumo": u.get("consumo",0),
                 "Total": u.get("puntos",0)+u.get("goles",0)+u.get("consumo",0)} for u in todos_exp]
    df_exp = pd.DataFrame(rows_exp)

    col_e1, col_e2, col_e3 = st.columns(3)
    col_e1.metric("Total usuarios", len(df_exp))
    col_e2.metric("Con mail",    df_exp["Mail"].apply(bool).sum())
    col_e3.metric("Con celular", df_exp["Celular"].apply(bool).sum())
    st.divider()

    col_f1, col_f2 = st.columns(2)
    filtro_nombre    = col_f1.text_input("Buscar por nombre o usuario", key="exp_filtro_nombre")
    filtro_localidad = col_f2.text_input("Filtrar por localidad", key="exp_filtro_loc")

    df_filtrado = df_exp.copy()
    if filtro_nombre:
        mask = (df_filtrado["Nombre"].str.contains(filtro_nombre, case=False, na=False) |
                df_filtrado["Usuario"].str.contains(filtro_nombre, case=False, na=False))
        df_filtrado = df_filtrado[mask]
    if filtro_localidad:
        df_filtrado = df_filtrado[df_filtrado["Localidad"].str.contains(filtro_localidad, case=False, na=False)]

    st.caption(f"Mostrando {len(df_filtrado)} de {len(df_exp)} usuarios")
    with st.expander(f"Ver lista ({len(df_filtrado)} usuarios)", expanded=False):
        st.dataframe(df_filtrado[["Usuario","Nombre","Nacimiento","Localidad","Celular","Mail"]], use_container_width=True, hide_index=True)
    st.divider()

    cols_registro = ["Usuario", "Nombre", "Nacimiento", "Localidad", "Celular", "Mail"]
    csv_completo  = df_exp[cols_registro].to_csv(index=False, sep=";").encode("utf-8-sig")
    csv_filtrado  = df_filtrado[cols_registro].to_csv(index=False, sep=";").encode("utf-8-sig")
    col_d1, col_d2 = st.columns(2)
    col_d1.download_button("⬇️ Descargar todos (CSV)",     csv_completo, "usuarios_prode_completo.csv", "text/csv", use_container_width=True)
    col_d2.download_button("⬇️ Descargar filtrados (CSV)", csv_filtrado, "usuarios_prode_filtrado.csv", "text/csv", use_container_width=True)
    st.caption("El CSV incluye: usuario, nombre, nacimiento, localidad, celular y mail.")