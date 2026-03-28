
# --- V10 SPA NAV ---
def _v10_nav():
    import streamlit as st
    if "_v10_step" not in st.session_state:
        st.session_state["_v10_step"]=0
    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if st.button("◀ Paso"):
            st.session_state["_v10_step"]=max(0,st.session_state["_v10_step"]-1)
            st.rerun()
    with c3:
        if st.button("Paso ▶"):
            st.session_state["_v10_step"]=st.session_state["_v10_step"]+1
            st.rerun()
    return st.session_state["_v10_step"]
# --- END V10 ---


# --- V9 FORM MODE ---
def _v9_form_block(key):
    import streamlit as st
    return st.form(key, clear_on_submit=False)
# --- END V9 ---


# --- V7 PERF HELPERS ---
import math
def _v7_paginate(items, page_key, page_size=4):
    import streamlit as st
    total = len(items)
    pages = max(1, math.ceil(total / page_size))
    p = st.session_state.get(page_key, 0)
    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if st.button("◀", key=page_key+"_prev") and p>0:
            st.session_state[page_key]=p-1
            st.rerun()
    with c3:
        if st.button("▶", key=page_key+"_next") and p<pages-1:
            st.session_state[page_key]=p+1
            st.rerun()
    start = p*page_size
    return items[start:start+page_size]

def _v7_buffer():
    import streamlit as st
    if "_v7_buffer" not in st.session_state:
        st.session_state["_v7_buffer"] = {}
    return st.session_state["_v7_buffer"]


def _get_pred_buffer(username, fase):
    buf = _v7_buffer()
    key = f"pred::{username}::{fase}"
    if key not in buf:
        buf[key] = {}
    return buf[key]


def _get_special_buffer(username):
    buf = _v7_buffer()
    key = f"esp::{username}"
    if key not in buf:
        buf[key] = {}
    return buf[key]


def _merge_predicciones(base_pred, pred_buffer):
    merged = dict(base_pred or {})
    merged.update(pred_buffer or {})
    return merged


def _flush_pred_buffer(username, fase):
    pred_buffer = _get_pred_buffer(username, fase)
    if not pred_buffer:
        return 0
    payload = [(idx, gl, gv) for idx, (gl, gv) in sorted(pred_buffer.items())]
    db_guardar_preds_lote(username, fase, payload)
    pred_buffer.clear()
    return len(payload)
# --- END V7 ---

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

from constants import FASES, CATEGORIAS_ESPECIALES, BANDERAS, GRUPOS_DEFAULT, bandera
from db import (
    db_get_usuario, db_get_fases, db_get_partidos, db_get_prode,
    db_get_resultado_completo, db_guardar_pred, db_confirmar_prode,
    db_fase_confirmada, db_get_especial, db_guardar_especial,
    db_confirmar_especial, db_get_resultado_especial,
    db_get_equipos_grupos, get_db, hash_clave,
    db_set_config, db_get_config, db_calcular_puntos,
    db_get_prodes_fase_todos, db_touch_usuario,
    db_get_cantidad_usuarios_en_linea, db_logout_usuario, db_get_feed,
    db_get_ranking_snapshot, db_get_fases_confirmadas_usuario,
    db_get_especiales_usuario, db_get_resumen_fases_usuario,
    db_get_resultados_especiales, db_guardar_preds_lote, db_get_lista_especiales
)


def cambiar_pantalla(step):
    st.session_state.step = step


def cerrar_sesion():
    """Limpia todo el session_state y vuelve al login."""
    db_logout_usuario(st.session_state.get("usuario"))
    claves_a_limpiar = [k for k in list(st.session_state.keys())
                        if k not in ("db_initialized",)]
    for k in claves_a_limpiar:
        del st.session_state[k]
    st.session_state.step = 0
    st.session_state.usuario = None
    st.session_state.registro_temp = {}


def normalizar(s: str) -> str:
    """Quita acentos y pasa a minúsculas para búsqueda flexible."""
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii').lower()


def nombre_equipo_display(nombre: str) -> str:
    b = bandera(nombre)
    return f"{b} {nombre}" if b else str(nombre)


def _get_resumen_usuario(username, u):
    ranking_snapshot = db_get_ranking_snapshot()
    user_rank = ranking_snapshot["by_username"].get(username, {})
    puntos_usuario = user_rank.get("puntos", u.get("puntos", 0))
    goles_usuario = user_rank.get("goles", u.get("goles", 0))
    consumo_usuario = user_rank.get("consumo", u.get("consumo", 0))
    pts_esp_user = user_rank.get("especiales", 0)
    total_pts = user_rank.get("total", puntos_usuario + goles_usuario + consumo_usuario + pts_esp_user)
    posicion = user_rank.get("pos", "—")
    total_ranking = len(ranking_snapshot["rows"])
    emoji_pos = {1: "🥇", 2: "🥈", 3: "🥉"}.get(posicion, "🏅") if isinstance(posicion, int) else "🏅"
    return {
        "puntos": puntos_usuario,
        "goles": goles_usuario,
        "consumo": consumo_usuario,
        "especiales": pts_esp_user,
        "total": total_pts,
        "posicion": posicion,
        "total_ranking": total_ranking,
        "emoji_pos": emoji_pos,
    }


def _get_pendientes_fases(fases_habilitadas, fases_resumen):
    pendientes_info = []
    pendientes_info_html = []
    for f_check in fases_habilitadas:
        data = fases_resumen.get(f_check, {})
        if data.get("confirmado"):
            continue
        total = int(data.get("partidos_total", 0) or 0)
        cargados = int(data.get("cargados", 0) or 0)
        sin_cargar = max(0, total - cargados)
        if sin_cargar > 0:
            pendientes_info.append(f"{f_check} ({sin_cargar})")
            pendientes_info_html.append(f"<b>{f_check}</b>: {sin_cargar} partido{'s' if sin_cargar > 1 else ''}")
    return pendientes_info, pendientes_info_html


def _get_partidos_por_grupo(partidos):
    grupos = {chr(ord('A') + i): [] for i in range(12)}
    existentes = {}

    for p in partidos:
        idx = int(p.get("idx", -1) or -1)
        if 0 <= idx < 72:
            letra = chr(ord('A') + (idx // 6))
            partido = dict(p)
            partido["idx"] = idx
            grupos.setdefault(letra, []).append(partido)
            existentes[idx] = partido

    # Completa cualquier hueco de la fase de grupos con el fixture por defecto.
    # Esto evita que un partido faltante en DB desaparezca del pronóstico del usuario.
    for letra, defaults in GRUPOS_DEFAULT.items():
        inicio = (ord(letra) - ord('A')) * 6
        for j, (local, visita) in enumerate(defaults):
            idx_global = inicio + j
            if idx_global not in existentes and local and visita:
                grupos.setdefault(letra, []).append({
                    "idx": idx_global,
                    "fase": "Grupos",
                    "local": local,
                    "visita": visita,
                    "fecha": "",
                    "hora": "",
                })

    for letra in grupos:
        grupos[letra] = sorted(grupos[letra], key=lambda p: int(p.get("idx", -1) or -1))

    grupos_con_partidos = [letra for letra, items in grupos.items() if items]
    return grupos, grupos_con_partidos


def _render_scroll_top():
    st.components.v1.html("""
    <script>
    (function() {
        var w = window.parent || window;
        function resetScroll() {
            try { w.scrollTo(0, 0); } catch (e) {}
            try {
                if (w.document && w.document.documentElement) w.document.documentElement.scrollTop = 0;
                if (w.document && w.document.body) w.document.body.scrollTop = 0;
            } catch (e) {}
        }
        resetScroll();
        requestAnimationFrame(resetScroll);
    })();
    </script>
    """, height=0)


def _render_header(nombre_display, usuarios_en_linea):
    inicial = (str(nombre_display or "?").strip()[:1] or "?").upper()
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between;
                padding:0.4rem 0 1rem 0; border-bottom:1px solid var(--border); margin-bottom:1rem;">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:40px; height:40px; border-radius:50%;
                        background:linear-gradient(135deg,#00c860,#009944);
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.1rem; font-weight:800; color:#fff; flex-shrink:0;">
                {inicial}
            </div>
            <div>
                <div style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; letter-spacing:2px; color:var(--text); line-height:1.1;">{nombre_display}</div>
                <div style="font-size:0.65rem; color:var(--text3); text-transform:uppercase; letter-spacing:1.5px;">Mundial 2026</div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:0.65rem; color:var(--text3); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Prode Il Baigo</div>
            <div style="display:inline-flex;align-items:center;gap:6px;background:var(--blue-dim);border:1px solid var(--blue-border);
                        color:var(--blue);padding:3px 10px;border-radius:999px;font-size:0.72rem;font-weight:700;">
                <span>🟢</span><span>{usuarios_en_linea} en línea</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def pantalla_usuario():
    username = st.session_state.usuario
    db_touch_usuario(username)
    usuarios_en_linea = db_get_cantidad_usuarios_en_linea()
    u = db_get_usuario(username)
    nombre_display = u.get('nombre', username)

    _render_scroll_top()
    _render_header(nombre_display, usuarios_en_linea)

    fases = db_get_fases()

    # ── Estado de grupos: siempre desde DB, sin confiar en session_state ────────
    grupos_completados = db_fase_confirmada(username, "Grupos")
    st.session_state["wizard_grupos_completo"] = grupos_completados

    if grupos_completados:
        fases_habilitadas = [f for f in FASES if fases.get(f, False)]
        fases_confirmadas_all = db_get_fases_confirmadas_usuario(username)
        fases_confirmadas = {f: fases_confirmadas_all.get(f, False) for f in fases_habilitadas}

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
        sub = st.session_state.get("sub_pantalla", "inicio")
        resumen_usuario = None
        pendientes_info = []
        pendientes_info_html = []

        if sub in ("inicio", "puntos"):
            resumen_usuario = _get_resumen_usuario(username, u)
            fases_resumen = db_get_resumen_fases_usuario(username)
            pendientes_info, pendientes_info_html = _get_pendientes_fases(fases_habilitadas, fases_resumen)

        # ── Menú de inicio ──
        if sub == "inicio":
            # Card de posición grande
            st.markdown(f"""
            <div style="background:var(--gold-dim);border:1.5px solid var(--gold-border);
                        border-radius:16px;padding:20px 24px;margin-bottom:1.2rem;
                        display:flex;align-items:center;gap:16px;">
                <span style="font-size:2.5rem;">{resumen_usuario["emoji_pos"]}</span>
                <div>
                    <div style="font-size:0.68rem;color:var(--text3);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:2px;">Tu posición</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2rem;color:var(--gold);letter-spacing:2px;line-height:1;">{resumen_usuario["posicion"]}° de {resumen_usuario["total_ranking"]}</div>
                    <div style="font-size:0.82rem;color:var(--text2);margin-top:2px;">{resumen_usuario["total"]} puntos totales</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Aviso pendientes
            if pendientes_info:
                st.markdown(
                    '<div style="background:var(--gold-dim);border:1px solid var(--gold-border);'
                    'border-radius:10px;padding:10px 14px;margin-bottom:1rem;font-size:0.85rem;color:var(--gold);">'
                    '⚠️ Pronósticos pendientes: ' + " · ".join(pendientes_info_html) + '</div>',
                    unsafe_allow_html=True
                )

            # Menú principal — grilla 2x3
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⚽  Mis pronósticos", use_container_width=True, key="menu_prode"):
                    st.session_state["sub_pantalla"] = "pronosticos"; st.rerun()
                if st.button("🏆  Ranking", use_container_width=True, key="menu_ranking"):
                    cambiar_pantalla(6); st.rerun()
            with c2:
                if st.button("📊  Mis puntos", use_container_width=True, key="menu_puntos"):
                    st.session_state["sub_pantalla"] = "puntos"; st.rerun()
                if st.button("🏅  Destacados", use_container_width=True, key="menu_dest"):
                    cambiar_pantalla(12); st.rerun()

            st.markdown("""
            <div style="
            font-family:Bebas Neue,sans-serif;
            font-size:1.3rem;
            letter-spacing:2px;
            margin:18px 0 8px 0;
            color:var(--blue);
            ">
            ⚡ Actividad en vivo
            </div>
            """, unsafe_allow_html=True)

            feed = db_get_feed(limit=5)
            if feed:
                for ev in feed:
                    st.markdown(f"""
                    <div style="
                    background:var(--bg3);
                    border:1px solid var(--border);
                    border-radius:10px;
                    padding:8px 12px;
                    margin-bottom:6px;
                    font-size:0.85rem;
                    ">
                    {ev["texto"]}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Sin actividad reciente")

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
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--blue);">{resumen_usuario["puntos"]}</div>
                </div>
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Marcadores exactos</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--green);">{resumen_usuario["goles"]}</div>
                </div>
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Puntos de consumo</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--orange);">{resumen_usuario["consumo"]}</div>
                </div>
                <div style="background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;">
                    <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Pronósticos especiales</div>
                    <div style="font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:var(--gold);">{resumen_usuario["especiales"]}</div>
                </div>
            </div>
            <div style="background:var(--green-dim);border:1.5px solid var(--green-glow);border-radius:12px;padding:16px;text-align:center;margin-bottom:1rem;">
                <div style="font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Total</div>
                <div style="font-family:Bebas Neue,sans-serif;font-size:3rem;color:var(--green);letter-spacing:2px;">{resumen_usuario["total"]}</div>
                <div style="font-size:0.8rem;color:var(--text3);">Posición {resumen_usuario["posicion"]} de {resumen_usuario["total_ranking"]}</div>
            </div>
            """, unsafe_allow_html=True)
            return


        # ── Sub-pantalla ver pronósticos de otros ──
        if sub == "otros":
            if st.button("← Volver", key="back_otros"):
                st.session_state["sub_pantalla"] = "inicio"; st.rerun()
            st.markdown("#### 👀 Pronósticos de todos")

            fases_cerradas = [f for f in fases_habilitadas if fases_confirmadas.get(f)]
            if not fases_cerradas:
                st.info("Todavía no confirmaste ninguna fase. Los pronósticos de otros se muestran después de confirmar la tuya.")
                return

            fase_ver = st.selectbox("Fase", fases_cerradas, key="otros_fase_sel")
            partidos_ver = db_get_partidos(fase_ver)
            resultados_ver = db_get_resultado_completo(fase_ver)
            todos_prodes = db_get_prodes_fase_todos(fase_ver)

            if not todos_prodes:
                st.info("Nadie confirmó pronósticos para esta fase todavía.")
                return

            partidos_ver_pagina = _v7_paginate(partidos_ver, f"otros_page_{fase_ver}", page_size=4)
            for p in partidos_ver_pagina:
                idx_p = p["idx"]
                nom_l = nombre_equipo_display(p['local'])
                nom_v = nombre_equipo_display(p['visita'])
                res_real = resultados_ver.get(idx_p)
                res_str = f"{res_real[0]}–{res_real[1]}" if res_real else "pendiente"

                header = (
                    '<div style="background:var(--bg3);border:1px solid var(--border);' +
                    'border-radius:12px;padding:10px 14px;margin:8px 0;">' +
                    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">' +
                    f'<span style="font-weight:700;font-size:0.85rem;color:var(--text);">{nom_l} vs {nom_v}</span>' +
                    f'<span style="font-size:0.72rem;color:var(--text3);">Real: <b>{res_str}</b></span>' +
                    '</div>'
                )
                filas = ""
                for uname, udata in sorted(todos_prodes.items()):
                    gl_u, gv_u = udata["pred"].get(idx_p, ("?", "?"))
                    es_yo = uname == username
                    if res_real and gl_u != "?":
                        rl, rv = res_real
                        exacto = gl_u == rl and gv_u == rv
                        ok = (gl_u > gv_u and rl > rv) or (gl_u < gv_u and rl < rv) or (gl_u == gv_u and rl == rv)
                        icono = "🎯" if exacto else ("✅" if ok else "❌")
                    else:
                        icono = ""
                    yo = ' <span style="background:var(--green-dim);color:var(--green);font-size:0.6rem;padding:1px 5px;border-radius:8px;">vos</span>' if es_yo else ""
                    filas += (
                        '<div style="display:flex;justify-content:space-between;padding:4px 0;' +
                        'border-top:1px solid var(--border);font-size:0.82rem;">' +
                        f'<span style="color:var(--text2);">{udata["nombre"]}{yo}</span>' +
                        f'<span style="color:var(--text);font-family:JetBrains Mono,monospace;">{gl_u}–{gv_u} {icono}</span>' +
                        '</div>'
                    )
                st.markdown(header + filas + "</div>", unsafe_allow_html=True)
            return

        # ── Sub-pantalla pronósticos — continúa abajo con el código existente ──
        if st.button("← Volver al inicio", key="back_prode"):
            st.session_state["sub_pantalla"] = "inicio"; st.rerun()
        st.markdown(f"""<div style="margin:0.5rem 0 1rem 0;">
            <div style="font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:2px;color:var(--text);">⚽ Mis pronósticos</div>
        </div>""", unsafe_allow_html=True)

        # Partidos pendientes
        if pendientes_info_html:
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

    # ── Validaciones ────────────────────────────────────────────────────────────
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

    # ── 3) Pronósticos ────────────────────────────────────────────────────────────
    estado_badge = ('<span style="background:var(--green-dim);color:var(--green);font-size:0.65rem;font-weight:700;'
                    'letter-spacing:1px;text-transform:uppercase;padding:2px 9px;border-radius:20px;'
                    'border:1px solid var(--green-glow);margin-left:8px;">Confirmado ✓</span>') if confirmado else ""

    titulo_fase = fase if grupos_completados else "Grupos"
    st.markdown(f"""<div style="margin:0.8rem 0 0.5rem 0;">
        <span style="font-family:Bebas Neue,sans-serif; font-size:1.4rem; letter-spacing:2px; color:var(--text);">
            Pronósticos — {titulo_fase}</span>{estado_badge}
    </div>""", unsafe_allow_html=True)

    resultados_fase = db_get_resultado_completo(fase) if confirmado else {}
    pred_buffer = _get_pred_buffer(username, fase)
    pred_ui = _merge_predicciones(pred, pred_buffer)

    def _persistir_cambios():
        _flush_pred_buffer(username, fase)

    def render_partido(p):
        idx = p["idx"]
        gl_prev, gv_prev = pred_ui.get(idx, pred.get(idx, (0, 0)))
        res_real    = resultados_fase.get(idx)
        iconos      = ""
        color_card  = "var(--surface)"
        border_card = "var(--border2)"
        res_str     = ""

        if res_real:
            rl, rv = res_real
            acierto_res    = (gl_prev > gv_prev and rl > rv) or (gl_prev < gv_prev and rl < rv) or (gl_prev == gv_prev and rl == rv)
            acierto_exacto = gl_prev == rl and gv_prev == rv
            iconos  = ("✅" if acierto_res else "❌") + (" 🎯" if acierto_exacto else "")
            res_str = f"{rl} — {rv}"
            if acierto_exacto:
                color_card = "var(--green-dim)"; border_card = "var(--green-glow)"
            elif acierto_res:
                color_card = "var(--blue-dim)"; border_card = "var(--blue-border)"
            else:
                color_card = "var(--red-dim)"; border_card = "var(--red-border)"

        nom_local  = nombre_equipo_display(p['local'])
        nom_visita = nombre_equipo_display(p['visita'])

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
                    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:4px 10px;
                                font-family:Bebas Neue,sans-serif;font-size:1.5rem;color:var(--green);
                                min-width:36px;text-align:center;flex-shrink:0;">{gl_prev}</div>
                    <div style="color:var(--text3);font-size:0.8rem;flex-shrink:0;">:</div>
                    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:4px 10px;
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
            if gl != pred.get(idx, (0, 0))[0] or gv != pred.get(idx, (0, 0))[1]:
                pred_buffer[idx] = (gl, gv)
            else:
                pred_buffer.pop(idx, None)

    # ── Fase Grupos con wizard ────────────────────────────────────────────────
    if fase == "Grupos":
        partidos_por_grupo, grupos_con_partidos = _get_partidos_por_grupo(partidos)

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

            partidos_grupo = partidos_por_grupo.get(letra_sel, [])
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

                partidos_grupo = partidos_por_grupo.get(letra, [])
                for p in partidos_grupo:
                    render_partido(p)

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                nav1, nav2, nav3 = st.columns([1, 2, 1])
                if gi > 0:
                    if nav1.button("← Anterior", key="grupo_prev", use_container_width=True):
                        with st.spinner("Guardando..."):
                            _persistir_cambios()
                        st.session_state.grupo_wizard = gi - 1; db_set_config(f'wizard_pos_{username}', str(gi - 1)); st.rerun()

                if gi < total - 1:
                    if nav3.button("Siguiente →", key="grupo_next", type="primary", use_container_width=True):
                        with st.spinner("Guardando..."):
                            _persistir_cambios()
                        st.session_state.grupo_wizard = gi + 1; db_set_config(f'wizard_pos_{username}', str(gi + 1)); st.rerun()
                else:
                    if nav3.button("Siguiente → Especiales ⭐", key="grupo_to_especiales", type="primary", use_container_width=True):
                        with st.spinner("Guardando..."):
                            _persistir_cambios()
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
                            _persistir_cambios()
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
        partidos_pagina = _v7_paginate(partidos, f"fase_page_{fase}", page_size=4) if not confirmado else partidos
        for p in partidos_pagina:
            render_partido(p)

        if not confirmado:
            st.divider()
            with st.form(f"form_confirmar_{fase}"):
                confirmar_btn = st.form_submit_button("✅ Confirmar prode", type="primary", use_container_width=True)

            if confirmar_btn:
                with st.spinner("Confirmando pronósticos..."):
                    _flush_pred_buffer(username, fase)
                    db_confirmar_prode(username, fase)
                    db_calcular_puntos()
                st.success("✅ Pronósticos confirmados para esta fase.")

    if "msg_grupos" in st.session_state:
        st.success(st.session_state.pop("msg_grupos"))

    # Si todavía está en el wizard de grupos, salir
    if not grupos_completados:
        return

    # ── 4) Resumen de especiales ──────────────────────────────────────────────
    esp_data = db_get_especiales_usuario(username)
    resultados_especiales = db_get_resultados_especiales()
    for _cat in CATEGORIAS_ESPECIALES:
        if _cat not in esp_data:
            esp_data[_cat] = None

    if any(v for v in esp_data.values()):
        st.subheader("⭐ Mis pronósticos especiales")
        for cat, info in CATEGORIAS_ESPECIALES.items():
            esp  = esp_data[cat]
            elec = esp["eleccion"] if esp else None
            resultado_real = resultados_especiales.get(cat)

            if not elec:
                bg_c = "var(--surface)"; border_c = "var(--surface)"
                derecha = '<span style="color:var(--text3); font-size:0.8rem;">Sin completar</span>'
            elif resultado_real:
                acierto  = elec == resultado_real
                icono    = "🎯" if acierto else "❌"
                bg_c     = "var(--green-dim)" if acierto else "var(--red-dim)"
                border_c = "var(--green-glow)" if acierto else "var(--red-border)"
                derecha  = (f'<b style="color:var(--text)">{elec}</b>'
                            f'<span style="margin:0 8px; color:var(--text3);">→</span>'
                            f'<span style="color:var(--text2); font-size:0.8rem;">Real: </span>'
                            f'<b style="color:var(--text)">{resultado_real}</b>'
                            f'<span style="margin-left:6px; font-size:1rem;">{icono}</span>')
            else:
                bg_c = "var(--surface)"; border_c = "var(--border)"
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
    especiales_usuario = db_get_especiales_usuario(username)
    esp_buffer = _get_special_buffer(username)
    resultados_especiales = db_get_resultados_especiales()

    for cat, info in CATEGORIAS_ESPECIALES.items():
        esp_w = especiales_usuario.get(cat)
        elec_w = esp_buffer.get(cat, esp_w["eleccion"] if esp_w else None)
        res_real_w = resultados_especiales.get(cat)

        col_tw, col_pw = st.columns([4, 1])
        col_tw.markdown(f"**{info['label']}**")
        col_pw.markdown(f"<div style='text-align:right; color:var(--gold); font-family:Bebas Neue,sans-serif; font-size:1.1rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)

        if res_real_w:
            acierto_w = elec_w == res_real_w
            st.markdown(f"<div style='color:var(--text2); font-size:0.9rem; margin-bottom:8px;'>Resultado oficial: <b style='color:var(--text)'>{res_real_w}</b> {'🎯' if acierto_w else '❌'} — Tu pronóstico: <b style='color:var(--text)'>{elec_w or '—'}</b></div>", unsafe_allow_html=True)
            selecciones_esp[cat] = elec_w
        elif esp_w and esp_w["confirmado"]:
            st.markdown(f"<div style='color:var(--green); font-size:0.9rem; margin-bottom:8px;'>✅ Confirmado: <b>{elec_w}</b></div>", unsafe_allow_html=True)
            selecciones_esp[cat] = elec_w
        else:
            if cat == "campeon":
                ops_w = ["— Elegí un equipo —"] + [nombre_equipo_display(e) for e in eq_wiz]
                d2n_w = {nombre_equipo_display(e): e for e in eq_wiz}
                if elec_w:
                    disp_elec = nombre_equipo_display(elec_w)
                    idx_w = ops_w.index(disp_elec) if disp_elec in ops_w else 0
                else:
                    idx_w = 0
                sel_w = st.selectbox("Seleccioná el equipo", ops_w, index=idx_w, key=f"esp_sel_{cat}")
                selecciones_esp[cat] = d2n_w.get(sel_w, None) if sel_w != "— Elegí un equipo —" else None
                if selecciones_esp[cat]:
                    esp_buffer[cat] = selecciones_esp[cat]
            else:
                lista_w = db_get_lista_especiales("arqueros") if cat == "arquero" else db_get_lista_especiales("jugadores")
                label_w = "arquero" if cat == "arquero" else "jugador"

                sel_key = f"esp_elegido_{cat}"
                cambiar_key = f"esp_cambiar_{cat}"
                input_key = f"esp_busq_{cat}"
                applied_key = f"esp_busq_aplicada_{cat}"
                reset_key = f"esp_busq_reset_{cat}"

                if st.session_state.pop(reset_key, False):
                    st.session_state[input_key] = ""
                    st.session_state[applied_key] = ""

                sel_actual = st.session_state.get(sel_key, elec_w)
                if sel_actual:
                    st.markdown(f"<div style='color:var(--green); font-size:0.88rem; margin:4px 0 8px 0;'>✅ Elegido: <b>{sel_actual}</b></div>", unsafe_allow_html=True)
                selecciones_esp[cat] = sel_actual

                if st.session_state.get(cambiar_key, not bool(sel_actual)):
                    col_busq, col_btn = st.columns([5, 1])
                    with col_busq:
                        st.text_input(
                            f"Buscar {label_w}",
                            key=input_key,
                            placeholder="Escribí el nombre (con o sin acento)...",
                        )
                    with col_btn:
                        st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                        if st.button("🔎", key=f"esp_lupa_{cat}", use_container_width=True):
                            st.session_state[applied_key] = (st.session_state.get(input_key, "") or "").strip()
                            st.rerun()

                    busqueda_aplicada = (st.session_state.get(applied_key, "") or "").strip()
                    if busqueda_aplicada:
                        filtrados_w = [j for j in lista_w if normalizar(busqueda_aplicada) in normalizar(j)][:8]
                        if not filtrados_w:
                            st.caption(f"No se encontró ningún {label_w}.")
                        else:
                            for jug in filtrados_w:
                                if st.button(jug, key=f"jug_{cat}_{jug}", use_container_width=True):
                                    st.session_state[sel_key] = jug
                                    st.session_state[cambiar_key] = False
                                    st.session_state[reset_key] = True
                                    selecciones_esp[cat] = jug
                                    esp_buffer[cat] = jug
                                    st.rerun()
                    else:
                        st.caption(f"Escribí el nombre y tocá la lupa para buscar {label_w}.")
                else:
                    if st.button(f"✏️ Cambiar {label_w}", key=f"esp_cambiar_btn_{cat}"):
                        st.session_state[cambiar_key] = True
                        st.session_state[reset_key] = True
                        st.rerun()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.divider()
    if "msg_esp" in st.session_state:
        st.success(st.session_state.pop("msg_esp"))

    # ── Confirmación final ──
    confirmar_esp = st.button("✅ Confirmar grupos + especiales", type="primary", use_container_width=True)

    if confirmar_esp:
        esp_confirmados = especiales_usuario
        sin_elegir = [
            info["label"]
            for cat, info in CATEGORIAS_ESPECIALES.items()
            if selecciones_esp.get(cat) is None and not ((esp_confirmados.get(cat) or {}).get("confirmado"))
        ]
        if sin_elegir:
            st.error(f"⚠️ Falta elegir: {', '.join(sin_elegir)}")
        else:
            with st.spinner("Confirmando pronósticos..."):
                _flush_pred_buffer(username, fase)
                db_confirmar_prode(username, fase)
                for cat, elec in selecciones_esp.items():
                    esp_cat = esp_confirmados.get(cat) or {}
                    if elec and not esp_cat.get("confirmado"):
                        db_guardar_especial(username, cat, elec)
                        db_confirmar_especial(username, cat)
                _get_special_buffer(username).clear()
                db_calcular_puntos()
            st.session_state["wizard_grupos_completo"] = True
            st.session_state["msg_grupos"] = "✅ ¡Todo confirmado! Grupos y especiales guardados."
            db_set_config(f"wizard_pos_{username}", "0")
            st.rerun()

    esp_buffer = _get_special_buffer(username)
    resultados_especiales = db_get_resultados_especiales()

    for cat, info in CATEGORIAS_ESPECIALES.items():
        esp_w = especiales_usuario.get(cat)
        elec_w = esp_buffer.get(cat, esp_w["eleccion"] if esp_w else None)
        res_real_w = resultados_especiales.get(cat)

        col_tw, col_pw = st.columns([4, 1])
        col_tw.markdown(f"**{info['label']}**")
        col_pw.markdown(f"<div style='text-align:right; color:var(--gold); font-family:Bebas Neue,sans-serif; font-size:1.1rem;'>+{info['puntos']} pts</div>", unsafe_allow_html=True)

        if res_real_w:
            acierto_w = elec_w == res_real_w
            st.markdown(f"<div style='color:var(--text2); font-size:0.9rem; margin-bottom:8px;'>Resultado oficial: <b style='color:var(--text)'>{res_real_w}</b> {'🎯' if acierto_w else '❌'} — Tu pronóstico: <b style='color:var(--text)'>{elec_w or '—'}</b></div>", unsafe_allow_html=True)
            selecciones_esp[cat] = elec_w
        elif esp_w and esp_w["confirmado"]:
            st.markdown(f"<div style='color:var(--green); font-size:0.9rem; margin-bottom:8px;'>✅ Confirmado: <b>{elec_w}</b></div>", unsafe_allow_html=True)
            selecciones_esp[cat] = elec_w
        else:
            if cat == "campeon":
                ops_w = ["— Elegí un equipo —"] + [nombre_equipo_display(e) for e in eq_wiz]
                d2n_w = {nombre_equipo_display(e): e for e in eq_wiz}
                if elec_w:
                    disp_elec = nombre_equipo_display(elec_w)
                    idx_w = ops_w.index(disp_elec) if disp_elec in ops_w else 0
                else:
                    idx_w = 0
                sel_w = st.selectbox("Seleccioná el equipo", ops_w, index=idx_w, key=f"esp_sel_{cat}")
                selecciones_esp[cat] = d2n_w.get(sel_w, None) if sel_w != "— Elegí un equipo —" else None
                if selecciones_esp[cat]:
                    esp_buffer[cat] = selecciones_esp[cat]
            else:
                lista_w = db_get_lista_especiales("arqueros") if cat == "arquero" else db_get_lista_especiales("jugadores")
                label_w = "arquero" if cat == "arquero" else "jugador"

                sel_key = f"esp_elegido_{cat}"
                cambiar_key = f"esp_cambiar_{cat}"
                input_key = f"esp_busq_{cat}"
                applied_key = f"esp_busq_aplicada_{cat}"
                reset_key = f"esp_busq_reset_{cat}"

                if st.session_state.pop(reset_key, False):
                    st.session_state[input_key] = ""
                    st.session_state[applied_key] = ""

                sel_actual = st.session_state.get(sel_key, elec_w)
                if sel_actual:
                    st.markdown(f"<div style='color:var(--green); font-size:0.88rem; margin:4px 0 8px 0;'>✅ Elegido: <b>{sel_actual}</b></div>", unsafe_allow_html=True)
                selecciones_esp[cat] = sel_actual

                if st.session_state.get(cambiar_key, not bool(sel_actual)):
                    col_busq, col_btn = st.columns([5, 1])
                    with col_busq:
                        st.text_input(
                            f"Buscar {label_w}",
                            key=input_key,
                            placeholder="Escribí el nombre (con o sin acento)...",
                        )
                    with col_btn:
                        st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                        if st.button("🔎", key=f"esp_lupa_{cat}", use_container_width=True):
                            st.session_state[applied_key] = (st.session_state.get(input_key, "") or "").strip()
                            st.rerun()

                    busqueda_aplicada = (st.session_state.get(applied_key, "") or "").strip()
                    if busqueda_aplicada:
                        filtrados_w = [j for j in lista_w if normalizar(busqueda_aplicada) in normalizar(j)][:8]
                        if not filtrados_w:
                            st.caption(f"No se encontró ningún {label_w}.")
                        else:
                            for jug in filtrados_w:
                                if st.button(jug, key=f"jug_{cat}_{jug}", use_container_width=True):
                                    st.session_state[sel_key] = jug
                                    st.session_state[cambiar_key] = False
                                    st.session_state[reset_key] = True
                                    selecciones_esp[cat] = jug
                                    esp_buffer[cat] = jug
                                    st.rerun()
                    else:
                        st.caption(f"Escribí el nombre y tocá la lupa para buscar {label_w}.")
                else:
                    if st.button(f"✏️ Cambiar {label_w}", key=f"esp_cambiar_btn_{cat}"):
                        st.session_state[cambiar_key] = True
                        st.session_state[reset_key] = True
                        st.rerun()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.divider()
    if "msg_esp" in st.session_state:
        st.success(st.session_state.pop("msg_esp"))

    # ── Confirmación final ──
    confirmar_esp = st.button("✅ Confirmar grupos + especiales", type="primary", use_container_width=True)

    if confirmar_esp:
        esp_confirmados = especiales_usuario
        sin_elegir = [
            info["label"]
            for cat, info in CATEGORIAS_ESPECIALES.items()
            if selecciones_esp.get(cat) is None and not ((esp_confirmados.get(cat) or {}).get("confirmado"))
        ]
        if sin_elegir:
            st.error(f"⚠️ Falta elegir: {', '.join(sin_elegir)}")
        else:
            with st.spinner("Confirmando pronósticos..."):
                _flush_pred_buffer(username, fase)
                db_confirmar_prode(username, fase)
                for cat, elec in selecciones_esp.items():
                    esp_cat = esp_confirmados.get(cat) or {}
                    if elec and not esp_cat.get("confirmado"):
                        db_guardar_especial(username, cat, elec)
                        db_confirmar_especial(username, cat)
                _get_special_buffer(username).clear()
                db_calcular_puntos()
            st.session_state["wizard_grupos_completo"] = True
            st.session_state["msg_grupos"] = "✅ ¡Todo confirmado! Grupos y especiales guardados."
            db_set_config(f"wizard_pos_{username}", "0")
            st.rerun()

    esp_buffer = _get_special_buffer(username)
    for cat, elec in selecciones_esp.items():

        esp_actual = especiales_usuario.get(cat)
        confirmado_actual = bool(esp_actual and esp_actual["confirmado"])
        if elec and not confirmado_actual:
            esp_buffer[cat] = elec
        elif not elec and cat in esp_buffer and not confirmado_actual:
            esp_buffer.pop(cat, None)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    nav1_e, _, _ = st.columns([1, 2, 1])
    if nav1_e.button("← Grupo L", key="esp_back", use_container_width=True):
        st.session_state.grupo_wizard = total - 1; st.rerun()