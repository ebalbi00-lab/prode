"""
screens_auth.py — Pantallas de login, registro y revisión.
"""
import datetime
import re
import streamlit as st

from db import (
    db_get_usuario, db_agregar_pendiente, db_registro_abierto, hash_clave, db_get_pendientes, db_get_pago_config,
    db_touch_usuario, db_get_tipo_usuario
)
from constants import FASES
from ui_helpers import password_input_with_toggle


def cambiar_pantalla(step):
    st.session_state.step = step


def login(usuario, clave):
    intentos = st.session_state.get("login_intentos", 0)
    if intentos >= 5:
        st.session_state.login_error = "Demasiados intentos fallidos. Recargá la página."
        st.rerun()

    u = db_get_usuario(usuario.strip().lower())
    if not u or u["clave"] != hash_clave(clave):
        st.session_state["login_intentos"] = intentos + 1
        st.session_state.login_error = "Usuario o clave incorrectos"
        st.rerun()

    st.session_state["login_intentos"] = 0
    st.session_state.usuario = usuario.strip().lower()
    db_touch_usuario(st.session_state.usuario)
    st.session_state.step = 9 if db_get_tipo_usuario(st.session_state.usuario) in ("admin", "consumo") else 5
    st.rerun()


def avanzar_datos_personales(nombre, nacimiento, localidad, celular, mail, desde=""):
    mail_valido = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", mail.strip())
    if not (nombre.strip() and localidad.strip() and celular.strip() and mail.strip()):
        st.session_state.reg_error = "Completá todos los campos obligatorios"
    elif not mail_valido:
        st.session_state.reg_error = "El mail no tiene un formato válido"
    else:
        st.session_state.registro_temp = {
            "nombre": nombre.strip(),
            "nacimiento": str(nacimiento),
            "localidad": localidad.strip(),
            "celular": celular.strip(),
            "mail": mail.strip(),
            "desde": desde.strip(),
        }
        st.session_state.step = 2


def _hero(title: str, eyebrow: str, subtitle: str, icon: str = "⚽"):
    st.markdown(f"""
    <div class="hero-shell hero-shell--center">
        <div class="hero-orb">{icon}</div>
        <div class="hero-eyebrow">{eyebrow}</div>
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def _step_header(step: str, title: str, subtitle: str):
    st.markdown(f"""
    <div class="section-header-card">
        <div class="hero-eyebrow">{step}</div>
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def pantalla_login():
    _hero(
        "Prode Il Baigo",
        "Mundial 2026 · pronosticá, competí y gana grandes premios",
        "Entrá con tu cuenta o registrate para dejar tus pronósticos listos antes del arranque.",
        "⚽",
    )

    if "login_error" in st.session_state:
        st.error(st.session_state.pop("login_error"))

    st.markdown('<div class="section-title" style="font-size:1.35rem;margin-top:1.1rem;">Ingresar</div>', unsafe_allow_html=True)
    with st.form("form_login"):
        usuario = st.text_input("Usuario", placeholder="Ej: enzo, juan123, mati.prode")
        clave = password_input_with_toggle("Clave", "login_clave", placeholder="Tu contraseña")
        c1, c2 = st.columns(2)
        ingresar = c1.form_submit_button("Entrar ahora", type="primary", use_container_width=True)
        registrarse = c2.form_submit_button("Crear cuenta", use_container_width=True)

    if ingresar:
        with st.spinner("Validando acceso..."):
            login(usuario, clave)
    if registrarse:
        cambiar_pantalla(1)
        st.rerun()

    st.markdown(
        """
        <div class="glass-note" style="margin-top:1rem;">
            <div class="glass-note__title">Qué te vas a encontrar adentro</div>
            <div class="glass-note__text">Pronósticos por fase, ranking general, estadísticas del torneo y especiales para sumar puntos extra.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta1, cta2 = st.columns([1.1, 1])
    with cta1:
        st.button("ℹ️ Cómo funciona el prode", on_click=cambiar_pantalla, args=(10,), use_container_width=True)
    with cta2:
        st.markdown(
            """
            <a href="https://www.instagram.com/il_baigo" target="_blank" class="social-cta">
                <span>📷</span>
                <span>Seguinos en Instagram</span>
            </a>
            """,
            unsafe_allow_html=True,
        )


def pantalla_registro_datos():
    _step_header(
        "Paso 1 de 2",
        "Tus datos",
        "Completá la base del registro. Lo justo y necesario para validar la inscripción.",
    )

    if not db_registro_abierto():
        st.error("El registro está cerrado. No se están tomando nuevas inscripciones.")
        st.button("← Volver al inicio", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
        return

    meses_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    with st.form("form_registro_datos"):
        nombre = st.text_input("Nombre y apellido", placeholder="Como figura en tu pago")
        st.markdown('<div class="field-subtitle">Fecha de nacimiento</div>', unsafe_allow_html=True)
        c_fecha1, c_fecha2, c_fecha3 = st.columns(3)
        with c_fecha1:
            año_sel = st.selectbox("Año", options=list(range(1930, datetime.date.today().year + 1))[::-1])
        with c_fecha2:
            mes_sel = st.selectbox("Mes", options=list(range(1, 13)), format_func=lambda x: meses_es[x - 1])
        with c_fecha3:
            dia_sel = st.selectbox("Día", options=list(range(1, 32)))

        localidad = st.text_input("Localidad", placeholder="Ciudad o barrio")
        celular = st.text_input("Celular", placeholder="11 1234 5678")
        mail = st.text_input("Mail", placeholder="nombre@mail.com")
        desde = st.text_input("¿Cómo llegaste al prode?", placeholder="Local, redes, amigos, evento, etc.")

        if "reg_error" in st.session_state:
            st.error(st.session_state.pop("reg_error"))

        col1, col2 = st.columns(2)
        volver = col1.form_submit_button("← Volver", use_container_width=True)
        continuar = col2.form_submit_button("Seguir con la cuenta", type="primary", use_container_width=True)

    if volver:
        cambiar_pantalla(0)
        st.rerun()

    if continuar:
        try:
            nacimiento = datetime.date(año_sel, mes_sel, dia_sel)
        except ValueError:
            st.session_state.reg_error = "La fecha no es válida. Revisá día, mes y año."
            st.rerun()
        avanzar_datos_personales(nombre, nacimiento, localidad, celular, mail, desde)
        st.rerun()


def pantalla_registro_cuenta():
    pago = db_get_pago_config()
    titular_pago = pago.get("titular", "Il Baigo")
    alias_pago = pago.get("alias", "prode.mundial.2026")
    cvu_pago = pago.get("cvu", "0000003100000000000000")
    instrucciones_pago = pago.get("instrucciones", "")

    _step_header(
        "Paso 2 de 2",
        "Cuenta y pago",
        "Elegí tus credenciales, hacé el pago y subí el comprobante para que revisen tu ingreso.",
    )

    st.markdown(f"""
    <div class="payment-card">
        <div class="payment-card__title">💳 Datos para transferir</div>
        <div class="payment-grid">
            <div><span>Titular</span><strong>{titular_pago or '—'}</strong></div>
            <div><span>Alias</span><strong>{alias_pago or '—'}</strong></div>
        </div>
        <div class="payment-cvu-label">CVU · tocá para copiar</div>
        <input type="text" value="{cvu_pago or ''}" readonly onclick="this.select();" ontouchstart="this.select();"
            style="width:100%;background:rgba(4,17,31,0.88);border:1px solid var(--gold-border);border-radius:14px;color:var(--text);font-family:JetBrains Mono,monospace;font-size:0.95rem;font-weight:800;padding:0.9rem 1rem;box-sizing:border-box;" />
        {f'<div class="payment-help">{instrucciones_pago}</div>' if instrucciones_pago else ''}
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_registro_cuenta"):
        usuario = st.text_input("Usuario", placeholder="Sin espacios. Ej: juan123")
        clave = password_input_with_toggle("Clave", "registro_clave", placeholder="Mínimo 4 caracteres")
        confirmar = password_input_with_toggle("Confirmar clave", "registro_confirmar", placeholder="Repetí la clave")
        comprobante = st.file_uploader("Comprobante de pago")

        st.markdown(
            """
            <div class="glass-note" style="margin-top:0.45rem;">
                <div class="glass-note__title">Antes de enviar</div>
                <div class="glass-note__text">Revisá que el usuario quede bien escrito. Es el que vas a usar para entrar durante todo el torneo.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "reg_error" in st.session_state:
            st.error(st.session_state.pop("reg_error"))

        col1, col2 = st.columns(2)
        volver = col1.form_submit_button("← Volver", use_container_width=True)
        enviar = col2.form_submit_button("Enviar solicitud", type="primary", use_container_width=True)

    if volver:
        cambiar_pantalla(1)
        st.rerun()

    if enviar:
        u_strip = usuario.strip().lower()
        if not u_strip:
            st.session_state.reg_error = "Ingresá un usuario"
        elif not re.match(r'^[a-zA-Z0-9._-]+$', u_strip):
            st.session_state.reg_error = "El usuario solo puede llevar letras, números, puntos, guiones o guiones bajos"
        elif len(u_strip) < 3:
            st.session_state.reg_error = "El usuario debe tener al menos 3 caracteres"
        elif db_get_usuario(u_strip):
            st.session_state.reg_error = "Ese usuario ya existe"
        elif any(p["username"] == u_strip for p in db_get_pendientes()):
            st.session_state.reg_error = "Ya hay una solicitud pendiente con ese usuario"
        elif len(clave) < 4:
            st.session_state.reg_error = "La clave debe tener al menos 4 caracteres"
        elif clave != confirmar:
            st.session_state.reg_error = "Las claves no coinciden"
        elif not comprobante:
            st.session_state.reg_error = "Subí el comprobante de pago"
        else:
            import base64
            comprobante_b64 = base64.b64encode(comprobante.read()).decode()
            comprobante_data = f"data:{comprobante.type};base64,{comprobante_b64}"
            with st.spinner("Enviando solicitud..."):
                db_agregar_pendiente({
                    "username": u_strip,
                    "clave": hash_clave(clave),
                    "comprobante": comprobante_data,
                    **st.session_state.registro_temp,
                })
            st.session_state.step = 4
            st.rerun()


def pantalla_en_revision():
    st.markdown("""
    <div class="review-shell">
        <div class="review-shell__icon">⏳</div>
        <div class="hero-title" style="font-size:2.35rem;">Solicitud recibida</div>
        <div class="hero-subtitle" style="max-width:460px;">
            Ya quedó cargada. Ahora la revisa el administrador junto con el comprobante de pago.
            Apenas esté aprobada, vas a poder entrar con tu usuario y empezar a jugar.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("← Volver al inicio", on_click=cambiar_pantalla, args=(0,), use_container_width=True)


def pantalla_acerca():
    _step_header(
        "Guía rápida",
        "Cómo funciona el prode",
        "Todo lo importante para entender reglas, puntaje y dinámica sin perder tiempo.",
    )

    st.markdown(
        """
        <div class="glass-note glass-note--success">
            <div class="glass-note__title">⚽ Dinámica</div>
            <div class="glass-note__text">Cargás tus resultados antes del cierre de cada fase. La app guarda mientras avanzás y al final confirmás con tu clave.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title" style="font-size:1.2rem;">Sistema de puntos</div>', unsafe_allow_html=True)
    st.markdown("Cuanto más avanzada la fase, más valen los aciertos. Acertar el marcador exacto siempre paga bastante más.")

    res_pts = [1, 2, 3, 4, 5, 6]
    exacto_pts = [3, 6, 9, 12, 15, 18]
    filas_pts = ""
    for i, fase in enumerate(FASES):
        bg = "var(--surface)" if i % 2 == 0 else "transparent"
        filas_pts += (
            f'<tr style="background:{bg};">'
            f'<td style="padding:12px 14px;color:var(--text);font-weight:700;font-size:0.94rem;">{fase}</td>'
            f'<td style="padding:12px 14px;color:var(--blue);font-weight:900;text-align:center;font-family:JetBrains Mono,monospace;">{res_pts[i]}</td>'
            f'<td style="padding:12px 14px;color:var(--green);font-weight:900;text-align:center;font-family:JetBrains Mono,monospace;">{exacto_pts[i]}</td>'
            '</tr>'
        )

    st.markdown(
        f"""
        <div class="table-shell" style="margin-bottom:0.6rem;">
            <table style="width:100%;border-collapse:collapse;background:var(--table-bg);">
                <thead>
                    <tr style="background:var(--table-head);border-bottom:1px solid var(--border);">
                        <th style="padding:12px 14px;color:var(--text3);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:left;">Fase</th>
                        <th style="padding:12px 14px;color:var(--blue);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;">✅ Resultado</th>
                        <th style="padding:12px 14px;color:var(--green);font-size:0.68rem;text-transform:uppercase;letter-spacing:1.5px;text-align:center;">🎯 Exacto</th>
                    </tr>
                </thead>
                <tbody>{filas_pts}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Resultado = acertás ganador o empate. Exacto = clavás el marcador completo.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="info-card info-card--warm">
                <div class="info-card__title">🍻 Puntos extra</div>
                <div class="info-card__text">El admin puede sumar puntos por consumo, presencia en eventos o dinámicas especiales del torneo.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="info-card info-card--cool">
                <div class="info-card__title">📊 Ranking en tiempo real</div>
                <div class="info-card__text">El total se arma con resultados, exactos, consumo y especiales. Siempre ves tu posición actualizada.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title" style="font-size:1.2rem;margin-top:1rem;">Pronósticos especiales</div>', unsafe_allow_html=True)
    st.markdown("Además de los partidos, hay elecciones extra para rascar puntos importantes al cierre del torneo.")

    especiales_filas = [
        ("🏆", "Campeón del mundo", "20 pts"),
        ("⚽", "Goleador del torneo", "10 pts"),
        ("🧤", "Mejor arquero", "8 pts"),
        ("⭐", "Mejor jugador", "8 pts"),
    ]
    cards_esp = ""
    for icono, label, pts in especiales_filas:
        cards_esp += f"""
        <div class="special-pill-row">
            <div class="special-pill-row__left"><span>{icono}</span><strong>{label}</strong></div>
            <div class="special-pill-row__right">+{pts}</div>
        </div>
        """
    st.markdown(cards_esp, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-note glass-note--gold" style="margin-top:1rem;">
            <div class="glass-note__title">🎁 Premios</div>
            <div class="glass-note__text">Habrá premios para los primeros puestos del ranking general y también acciones sorpresa durante el torneo.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("¿Puedo cambiar un pronóstico después de confirmarlo?"):
        st.write("No. Una vez confirmado con tu clave, queda bloqueado.")
    with st.expander("¿Qué pasa si no cargo una fase?"):
        st.write("Esa fase queda en cero. No suma puntos.")
    with st.expander("¿Hasta cuándo puedo cargar pronósticos?"):
        st.write("Hasta que el administrador cierre manualmente la fase.")
    with st.expander("¿Qué hago si olvidé mi contraseña?"):
        st.write("Contactá al administrador para que la reinicie.")

    st.button("← Volver", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
