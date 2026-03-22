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

from constants import FASES, CATEGORIAS_ESPECIALES, BANDERAS, ARQUEROS_MUNDIALISTAS, JUGADORES_MUNDIALISTAS, GRUPOS_DEFAULT, bandera
from db import (
    db_get_usuario, db_get_todos_usuarios, db_get_pendientes,
    db_get_fases, db_toggle_fase, db_get_partidos, db_guardar_partido,
    db_get_resultado_completo, db_guardar_resultado, db_limpiar_resultados_fase,
    db_limpiar_resultados_especiales,
    db_calcular_puntos, db_calcular_puntos_especiales,
    db_get_consumo_log, db_sumar_consumo, db_eliminar_consumo_log,
    db_aprobar_pendiente, db_rechazar_pendiente,
    db_reset_clave, db_borrar_usuario, db_resetear_todos_puntajes,
    db_registro_abierto, db_set_config,
    db_get_especial, db_get_resultado_especial, db_guardar_resultado_especial,
    db_get_todos_especiales, db_fusionar_variantes_especial,
    db_get_equipos_grupos, hash_clave, get_db,
)
from screens_stats import render_destacados_usuarios


def cambiar_pantalla(step):
    st.session_state.step = step


def pantalla_admin():
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; padding:0.3rem 0 1.2rem 0;
                border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:1rem;">
        <div style="width:42px; height:42px; border-radius:10px;
                    background:var(--gold-dim); border:1.5px solid var(--gold-border);
                    display:flex; align-items:center; justify-content:center; font-size:1.3rem;">⚙️</div>
        <div>
            <div style="font-family:Bebas Neue,sans-serif; font-size:1.7rem; letter-spacing:2px; color:var(--text); line-height:1.1;">Panel Admin</div>
            <div style="font-size:0.7rem; color:var(--text3); text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Prode Il Baigo · Mundial 2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📋 Resumen", "👥 Pendientes", "🔀 Fases", "⚽ Partidos", "📊 Result.", "💰 Consumo", "⭐ Especiales", "👤 Usuarios", "🏅 Destacados", "⚠️ Reset", "📥 Exportar"])

    with tabs[0]:
        _tab_resumen()
    with tabs[1]:
        _tab_pendientes()
    with tabs[2]:
        _tab_fases()
    with tabs[3]:
        _tab_partidos()
    with tabs[4]:
        _tab_resultados()
    with tabs[5]:
        _tab_consumo()
    with tabs[6]:
        _tab_especiales()
    with tabs[7]:
        _tab_usuarios()
    with tabs[8]:
        st.subheader("🏅 Destacados — Estadísticas por usuario")
        render_destacados_usuarios()
    with tabs[9]:
        _tab_reset()
    with tabs[10]:
        _tab_exportar()

    st.divider()
    col1, col2 = st.columns(2)
    col1.button("🏆 Ver Ranking",   on_click=cambiar_pantalla, args=(6,),  use_container_width=True)
    col2.button("🚪 Cerrar sesión", on_click=cambiar_pantalla, args=(0,), use_container_width=True)


# ─── Tabs ─────────────────────────────────────────────────────────────────────

def _tab_resumen():
    st.subheader("Resumen general")
    if "msg_resumen" in st.session_state:
        st.success(st.session_state.pop("msg_resumen"))

    todos     = db_get_todos_usuarios()
    pendientes = db_get_pendientes()
    fases     = db_get_fases()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Usuarios activos",       len(todos))
    col2.metric("Solicitudes pendientes", len(pendientes))
    col3.metric("Fases habilitadas",      sum(1 for v in fases.values() if v))
    col4.metric("Total consumo acumulado", sum(u["consumo"] for u in todos))

    st.divider()
    st.subheader("Inscripciones")
    registro_abierto = db_registro_abierto()
    nuevo_estado = st.toggle("Registro abierto", value=registro_abierto, key="toggle_registro")
    if nuevo_estado != registro_abierto:
        db_set_config("registro_abierto", "1" if nuevo_estado else "0"); st.rerun()

    st.divider()
    st.subheader("Confirmaciones por fase")
    with get_db() as _conn:
        _cur = _conn.cursor()
        _cur.execute("SELECT fase, COUNT(DISTINCT username) as cnt FROM prodes WHERE confirmado=1 AND partido_idx=-1 GROUP BY fase")
        _conf_map = {r["fase"]: r["cnt"] for r in _cur.fetchall()}
    for fase in FASES:
        if not fases.get(fase):
            continue
        st.write(f"**{fase}:** {_conf_map.get(fase, 0)} / {len(todos)} confirmados")

    st.divider()
    if st.button("🔄 Recalcular puntajes"):
        with st.spinner("Recalculando..."):
            db_calcular_puntos()
        st.session_state["msg_resumen"] = "✅ Puntajes recalculados correctamente."
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
            st.write(f"**Comprobante:** {pend.get('comprobante', '—')}")
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
        grupos_con_datos  = set()
        for p in partidos_cargados:
            letra_g = "ABCDEFGHIJKL"[p["idx"] // 6]
            grupos_con_datos.add(letra_g)

        opciones_grupos = [f"{'✅' if l in grupos_con_datos else '○'} Grupo {l}" for l in "ABCDEFGHIJKL"]
        grupo_sel_raw   = st.selectbox("Grupo", opciones_grupos)
        letra           = grupo_sel_raw[-1]
        inicio          = "ABCDEFGHIJKL".index(letra) * 6
        existentes_map  = {p["idx"]: p for p in partidos_cargados}
        defaults        = GRUPOS_DEFAULT.get(letra, [("", "")] * 6)

        with st.form(f"form_grupo_{letra}"):
            nuevos = []
            for j in range(6):
                idx_global = inicio + j
                prev = existentes_map.get(idx_global, {})
                c1, c2 = st.columns(2)
                l = c1.text_input("Local",     value=prev.get("local",  defaults[j][0]), key=f"gl_{letra}_{j}")
                v = c2.text_input("Visitante", value=prev.get("visita", defaults[j][1]), key=f"gv_{letra}_{j}")
                nuevos.append((idx_global, l, v))
            col_b1, col_b2 = st.columns(2)
            guardar      = col_b1.form_submit_button(f"Guardar Grupo {letra}", type="primary")
            guardar_todos = col_b2.form_submit_button("Guardar todos los grupos")

        if guardar:
            with st.spinner(f"Guardando Grupo {letra}..."):
                for idx_global, l, v in nuevos:
                    if l and v: db_guardar_partido("Grupos", idx_global, l, v)
                st.cache_data.clear()
            st.session_state["msg_grupos"] = f"✅ Grupo {letra} guardado."
            st.rerun()

        if guardar_todos:
            with st.spinner("Guardando todos los grupos..."):
                for gr, partidos_gr in GRUPOS_DEFAULT.items():
                    ini_gr = "ABCDEFGHIJKL".index(gr) * 6
                    for j, (loc, vis) in enumerate(partidos_gr):
                        db_guardar_partido("Grupos", ini_gr + j, loc, vis)
                st.cache_data.clear()
            st.session_state["msg_grupos"] = "✅ Todos los grupos guardados con los equipos por defecto."
            st.rerun()

    else:
        cant = {"Dieciseisavos": 16, "Octavos": 8, "Cuartos": 4, "Semifinal": 2, "Final": 1}[fase_sel]
        partidos_existentes = db_get_partidos(fase_sel)
        existentes_map      = {p["idx"]: p for p in partidos_existentes}
        equipos_grupos      = db_get_equipos_grupos()

        if not equipos_grupos:
            st.warning("⚠️ Primero cargá los partidos de la fase de Grupos.")
        else:
            NINGUNO   = "— Seleccionar —"
            opciones  = [NINGUNO] + [f"{bandera(e)} {e}" for e in equipos_grupos]
            disp_a_n  = {f"{bandera(e)} {e}": e for e in equipos_grupos}

            with st.form(f"form_{fase_sel}"):
                nuevos = []
                for i in range(cant):
                    prev          = existentes_map.get(i, {})
                    prev_local    = prev.get("local",  "")
                    prev_visita   = prev.get("visita", "")
                    disp_local    = f"{bandera(prev_local)} {prev_local}"   if prev_local  else NINGUNO
                    disp_visita   = f"{bandera(prev_visita)} {prev_visita}" if prev_visita else NINGUNO
                    idx_local     = opciones.index(disp_local)  if disp_local  in opciones else 0
                    idx_visita    = opciones.index(disp_visita) if disp_visita in opciones else 0

                    st.markdown(f"<div style='color:var(--text3); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-top:0.8rem; margin-bottom:0.2rem;'>Partido {i+1}</div>", unsafe_allow_html=True)
                    c1, c2     = st.columns(2)
                    sel_local  = c1.selectbox("Local",     opciones, index=idx_local,  key=f"{fase_sel}_l_{i}")
                    sel_visita = c2.selectbox("Visitante", opciones, index=idx_visita, key=f"{fase_sel}_v_{i}")
                    nuevos.append((i, disp_a_n.get(sel_local, ""), disp_a_n.get(sel_visita, "")))

                guardar = st.form_submit_button("Guardar partidos", type="primary")

            if guardar:
                guardados = sum(1 for i, l, v in nuevos if l and v and db_guardar_partido(fase_sel, i, l, v) is None)
                # db_guardar_partido retorna None siempre, contamos los que tienen l y v
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
        border    = "rgba(0,200,80,0.3)" if tiene_res else "rgba(255,255,255,0.08)"
        bg        = "rgba(0,200,80,0.05)" if tiene_res else "rgba(255,255,255,0.02)"

        st.markdown(f'<div style="background:{bg}; border:1px solid {border}; border-radius:12px; padding:10px 14px; margin:6px 0;">', unsafe_allow_html=True)
        activar = st.checkbox("Cargar resultado", value=tiene_res, key=f"chk_{fase_sel}_{idx}")
        if activar:
            c_local, c_rl, c_sep, c_rv, c_visita, c_btn = st.columns([3, 1, 0.4, 1, 3, 1.5])
            c_local.markdown(f"<div style='text-align:right; font-weight:700; font-size:0.9rem; padding-top:9px; color:var(--text);'>{bandera(p['local'])} {p['local']}</div>", unsafe_allow_html=True)
            rl = c_rl.number_input("rl", 0, 15, int(rl_prev), key=f"rl_{fase_sel}_{idx}", label_visibility="collapsed")
            c_sep.markdown("<div style='text-align:center; padding-top:9px; color:#404058;'>—</div>", unsafe_allow_html=True)
            rv = c_rv.number_input("rv", 0, 15, int(rv_prev), key=f"rv_{fase_sel}_{idx}", label_visibility="collapsed")
            c_visita.markdown(f"<div style='text-align:left; font-weight:700; font-size:0.9rem; padding-top:9px; color:var(--text);'>{bandera(p['visita'])} {p['visita']}</div>", unsafe_allow_html=True)
            if c_btn.button("💾", key=f"save_{fase_sel}_{idx}", help="Guardar resultado"):
                with st.spinner("Guardando..."):
                    db_guardar_resultado(fase_sel, idx, rl, rv)
                    db_calcular_puntos()
                st.session_state["res_ok"] = f"✅ Guardado: {p['local']} {rl} — {rv} {p['visita']}"
                st.rerun()
            if tiene_res:
                st.caption(f"✅ Guardado: {p['local']} {rl_prev} — {rv_prev} {p['visita']}")
        else:
            st.markdown(f"""<div style="display:flex; align-items:center; gap:8px; padding:2px 0 4px 0;">
                <div style="color:var(--text); font-weight:700; font-size:0.9rem; flex:1; text-align:right;">{bandera(p['local'])} {p['local']}</div>
                <div style="color:#404058; font-size:0.8rem;">vs</div>
                <div style="color:var(--text); font-weight:700; font-size:0.9rem; flex:1;">{bandera(p['visita'])} {p['visita']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

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


def _tab_especiales():
    st.subheader("⭐ Pronósticos especiales — Resultados")
    if "msg_esp_adm" in st.session_state:
        st.success(st.session_state.pop("msg_esp_adm"))

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



    with st.form("form_admin_esp_todos"):
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
                lista_adm = ARQUEROS_MUNDIALISTAS if cat == "arquero" else JUGADORES_MUNDIALISTAS
                label_adm = "arquero" if cat == "arquero" else "jugador"
                busq_adm = st.text_input(f"Buscar {label_adm}", value="", key=f"adm_busq_{cat}", placeholder="Escribí el nombre (con o sin acento)...")
                filtrados_adm = [j for j in lista_adm if _norm(busq_adm) in _norm(j)] if busq_adm else lista_adm
                opciones_adm = ["— Seleccioná —"] + filtrados_adm
                if resultado_actual and resultado_actual in filtrados_adm:
                    idx_adm = filtrados_adm.index(resultado_actual) + 1
                else:
                    idx_adm = 0
                sel_adm = st.selectbox(f"Nuevo {label_adm} real", opciones_adm, index=idx_adm, key=f"adm_sel_{cat}")
                selecciones_adm[cat] = sel_adm if sel_adm != "— Seleccioná —" else None
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.divider()
        pw_esp_adm     = st.text_input("🔒 Tu contraseña de admin", type="password", key="pw_guardar_esp")
        guardar_todos_esp = st.form_submit_button("💾 Guardar todos y aplicar puntos", type="primary")

    if guardar_todos_esp:
        admin_esp = db_get_usuario(st.session_state.usuario)
        if admin_esp["clave"] != hash_clave(pw_esp_adm):
            st.session_state["msg_esp_adm"] = "❌ Contraseña incorrecta."
        else:
            guardados = 0
            with st.spinner("Guardando..."):
                for cat, ganador in selecciones_adm.items():
                    if ganador:
                        db_guardar_resultado_especial(cat, ganador); guardados += 1
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
    st.subheader("⚠️ Resetear todos los puntajes")
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
    st.dataframe(df_filtrado[["Usuario","Nombre","Nacimiento","Localidad","Celular","Mail"]], use_container_width=True, hide_index=True)
    st.divider()

    cols_registro = ["Usuario", "Nombre", "Nacimiento", "Localidad", "Celular", "Mail"]
    csv_completo  = df_exp[cols_registro].to_csv(index=False, sep=";").encode("utf-8-sig")
    csv_filtrado  = df_filtrado[cols_registro].to_csv(index=False, sep=";").encode("utf-8-sig")
    col_d1, col_d2 = st.columns(2)
    col_d1.download_button("⬇️ Descargar todos (CSV)",     csv_completo, "usuarios_prode_completo.csv", "text/csv", use_container_width=True)
    col_d2.download_button("⬇️ Descargar filtrados (CSV)", csv_filtrado, "usuarios_prode_filtrado.csv", "text/csv", use_container_width=True)
    st.caption("El CSV incluye: usuario, nombre, nacimiento, localidad, celular y mail.")