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
    # Rate limiting — máx 5 intentos fallidos por sesión
    intentos = st.session_state.get("login_intentos", 0)
    if intentos >= 5:
        st.session_state.login_error = "Demasiados intentos fallidos. Recargá la página."
        st.rerun()
    u = db_get_usuario(usuario.strip().lower())
    if not u:
        st.session_state["login_intentos"] = intentos + 1
        st.session_state.login_error = "Usuario o clave incorrectos"
        st.rerun()
    elif u["clave"] != hash_clave(clave):
        st.session_state["login_intentos"] = intentos + 1
        st.session_state.login_error = "Usuario o clave incorrectos"
        st.rerun()
    else:
        st.session_state["login_intentos"] = 0
        st.session_state.usuario = usuario.strip().lower()
        db_touch_usuario(st.session_state.usuario)
        st.session_state.step = 9 if db_get_tipo_usuario(st.session_state.usuario) in ("admin", "consumo") else 5
        st.rerun()


def avanzar_datos_personales(nombre, nacimiento, localidad, celular, mail, desde=""):
    mail_valido = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", mail.strip())
    if not (nombre.strip() and localidad.strip() and celular.strip() and mail.strip()):
        st.session_state.reg_error = "Completá todos los campos"
    elif not mail_valido:
        st.session_state.reg_error = "El mail no tiene formato válido"
    else:
        st.session_state.registro_temp = {
            "nombre": nombre.strip(), "nacimiento": str(nacimiento),
            "localidad": localidad.strip(), "celular": celular.strip(),
            "mail": mail.strip(), "desde": desde
        }
        st.session_state.step = 2


# ─── Pantallas ────────────────────────────────────────────────────────────────

def pantalla_login():
    st.markdown("""
    <div style="text-align:center; padding: 2.5rem 0 1.5rem 0;">
        <div style="font-size:3.2rem; margin-bottom:0.6rem; filter:drop-shadow(0 4px 16px rgba(0,200,96,0.3));">⚽</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:3.8rem; letter-spacing:5px;
                    background:linear-gradient(135deg,#00e87a 0%,#80ffbb 60%,#00c860 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; line-height:1.0; margin-bottom:0.3rem;">PRODE IL BAIGO</div>
        <div style="display:inline-block; background:linear-gradient(135deg,rgba(255,210,76,0.18),rgba(255,190,32,0.12)); border:1px solid rgba(228,175,33,0.35);
                    border-radius:20px; padding:3px 16px; font-size:0.75rem; color:#d49a00;
                    font-weight:800; letter-spacing:3px; text-transform:uppercase; box-shadow:0 4px 14px rgba(212,154,0,0.10);">⚽ MUNDIAL 2026</div>
    </div>
    """, unsafe_allow_html=True)

    if "login_error" in st.session_state:
        st.error(st.session_state.pop("login_error"))

    with st.form("form_login"):
        usuario = st.text_input("Usuario", placeholder="tu_usuario")
        clave = password_input_with_toggle("Clave", "login_clave", placeholder="••••••••")
        col1, col2 = st.columns(2)
        ingresar = col1.form_submit_button("Ingresar", type="primary", use_container_width=True)
        registrarse = col2.form_submit_button("Registrarse", use_container_width=True)

    if ingresar:
        with st.spinner("Ingresando..."):
            login(usuario, clave)
    if registrarse:
        cambiar_pantalla(1)
        st.rerun()

    st.divider()
    st.button("ℹ️ Acerca del prode", on_click=cambiar_pantalla, args=(10,), use_container_width=True)
    st.markdown("""
    <div style="text-align:center; margin-top:0.8rem;">
        <a href="https://www.instagram.com/il_baigo" target="_blank"
           style="display:inline-flex; align-items:center; gap:7px; text-decoration:none;
                  background:var(--surface); border:1.5px solid var(--border2);
                  border-radius:20px; padding:6px 16px; transition:all 0.16s ease;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                <rect x="2" y="2" width="20" height="20" rx="6" stroke="currentColor" stroke-width="2" style="color:var(--text2);"/>
                <circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2" style="color:var(--text2);"/>
                <circle cx="17.5" cy="6.5" r="1.2" fill="currentColor" style="color:var(--text2);"/>
            </svg>
            <span style="color:var(--text2); font-size:0.82rem; font-weight:600; letter-spacing:0.3px;">
                Seguinos <strong style="color:var(--text);">@il_baigo</strong></span>
        </a>
    </div>
    """, unsafe_allow_html=True)


def pantalla_registro_datos():
    st.markdown("""
    <div style="padding:0.5rem 0 1rem 0;">
        <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:2px;
                    color:var(--text3); margin-bottom:0.3rem;">Paso 1 de 2</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:2.2rem; letter-spacing:3px; color:var(--text);">
            Datos personales</div>
    </div>
    """, unsafe_allow_html=True)

    if not db_registro_abierto():
        st.error("⛔ El registro está cerrado. No se aceptan nuevas inscripciones.")
        st.button("Volver", on_click=cambiar_pantalla, args=(0,))
        return

    meses_es = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    with st.form("form_registro_datos"):
        nombre  = st.text_input("Nombre y apellido")
        st.markdown("**Fecha de nacimiento**")
        año_sel = st.selectbox("Año de nacimiento", options=list(range(1930, datetime.date.today().year + 1))[::-1])
        mes_sel = st.selectbox("Mes de nacimiento", options=list(range(1, 13)), format_func=lambda x: meses_es[x - 1])
        dia_sel = st.selectbox("Día de nacimiento", options=list(range(1, 32)))
        localidad = st.text_input("Localidad")
        celular   = st.text_input("Celular")
        mail      = st.text_input("Mail")
        desde     = st.text_input("¿Desde dónde te estás inscribiendo? Nombrá comercio, institución o redes")
        if "reg_error" in st.session_state:
            st.error(st.session_state.pop("reg_error"))
        col1, col2 = st.columns(2)
        volver    = col1.form_submit_button("Volver")
        continuar = col2.form_submit_button("Continuar", type="primary")

    if volver:
        cambiar_pantalla(0)
        st.rerun()
    if continuar:
        try:
            nacimiento = datetime.date(año_sel, mes_sel, dia_sel)
        except ValueError:
            st.session_state.reg_error = "Fecha inválida. Revisá el día seleccionado."
            st.rerun()
        avanzar_datos_personales(nombre, nacimiento, localidad, celular, mail, desde)
        st.rerun()


def pantalla_registro_cuenta():
    pago = db_get_pago_config()
    titular_pago = pago.get("titular", "Il Baigo")
    alias_pago = pago.get("alias", "prode.mundial.2026")
    cvu_pago = pago.get("cvu", "0000003100000000000000")
    instrucciones_pago = pago.get("instrucciones", "")

    st.markdown("""
    <div style="padding:0.5rem 0 1rem 0;">
        <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:2px;
                    color:var(--text3); margin-bottom:0.3rem;">Paso 2 de 2</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:2.2rem; letter-spacing:3px; color:var(--text);">
            Cuenta y pago</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_registro_cuenta"):
        usuario = st.text_input("Usuario", placeholder="sin espacios, ej: juan123")
        clave = password_input_with_toggle("Clave (mínimo 4 caracteres)", "reg_clave", placeholder="••••••••")
        confirmar = password_input_with_toggle("Confirmar clave", "reg_confirmar", placeholder="••••••••")
        st.markdown(f"""
        <div style="background:var(--gold-dim); border:1.5px solid var(--gold-border);
                    border-radius:10px; padding:12px 16px; margin:0.5rem 0;">
            <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px;
                        color:var(--gold); margin-bottom:10px;">💰 Datos de pago</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="color:var(--text2); font-size:0.82rem;">Titular</span>
                <span style="color:var(--text); font-weight:700; font-size:0.88rem;">{titular_pago or '—'}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="color:var(--text2); font-size:0.82rem;">Alias</span>
                <span style="color:var(--text); font-weight:700; font-family:JetBrains Mono,monospace; font-size:0.88rem;">{alias_pago or '—'}</span>
            </div>
            <div style="margin-bottom:2px;">
                <span style="color:var(--text2); font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;">CVU — tocá para copiar</span>
            </div>
            <input type="text" value="{cvu_pago or ''}" readonly onclick="this.select();" ontouchstart="this.select();"
                style="width:100%; background:var(--bg3); border:1.5px solid var(--border2); border-radius:7px;
                       color:var(--text); font-family:JetBrains Mono,monospace; font-size:0.88rem; font-weight:700;
                       padding:8px 12px; cursor:pointer; outline:none; box-sizing:border-box;
                       -webkit-user-select:all; user-select:all;" />
            {"<div style='margin-top:10px; color:var(--text2); font-size:0.82rem; line-height:1.6;'>" + instrucciones_pago + "</div>" if instrucciones_pago else ""}
        </div>
        """, unsafe_allow_html=True)
        comprobante = st.file_uploader("Comprobante de pago")
        if "reg_error" in st.session_state:
            st.error(st.session_state.pop("reg_error"))
        col1, col2 = st.columns(2)
        volver = col1.form_submit_button("← Volver")
        enviar = col2.form_submit_button("Enviar solicitud", type="primary")

    if volver:
        cambiar_pantalla(1)
        st.rerun()

    if enviar:
        u_strip = usuario.strip().lower()
        if not u_strip:
            st.session_state.reg_error = "Ingresá un nombre de usuario"
        elif not re.match(r'^[a-zA-Z0-9._-]+$', u_strip):
            st.session_state.reg_error = "El usuario solo puede tener letras, números, puntos, guiones o guiones bajos"
        elif len(u_strip) < 3:
            st.session_state.reg_error = "El usuario debe tener al menos 3 caracteres"
        elif db_get_usuario(u_strip):
            st.session_state.reg_error = "Usuario ya existe"
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
            with st.spinner("Enviando solicitud."):
                db_agregar_pendiente({
                    "username": u_strip, "clave": hash_clave(clave),
                    "comprobante": comprobante_data,
                    **st.session_state.registro_temp
                })
            st.session_state.step = 4
            st.rerun()


def pantalla_en_revision():
    st.markdown("""
    <div style="text-align:center; padding:3.5rem 1rem 2rem 1rem;">
        <div style="width:72px; height:72px; margin:0 auto 1.2rem auto;
                    background:var(--gold-dim); border:2px solid rgba(255,200,64,0.3);
                    border-radius:50%; display:flex; align-items:center; justify-content:center;
                    font-size:2.2rem;">⏳</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:2.3rem; letter-spacing:3px; color:var(--gold); margin-bottom:0.8rem;">
            INSCRIPCIÓN EN REVISIÓN</div>
        <div style="color:var(--text2); font-size:0.95rem; line-height:1.8; max-width:380px; margin:0 auto;">
            Tu solicitud está siendo revisada por el administrador.<br>
            <span style="color:var(--text); font-weight:600;">Te avisamos cuando sea aprobada.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("← Volver al inicio", on_click=cambiar_pantalla, args=(0,), use_container_width=True)


def pantalla_acerca():
    st.markdown("""
    <div style="padding:0.5rem 0 1.2rem 0;">
        <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:2px;
                    color:var(--text3); margin-bottom:0.3rem;">Guía del participante</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:2.8rem; letter-spacing:3px;
                    color:var(--text); line-height:1.05;">ℹ️ PRODE IL BAIGO</div>
        <div style="font-family:Bebas Neue,sans-serif; font-size:1.3rem; letter-spacing:2px;
                    color:var(--text3);">MUNDIAL 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:16px 18px; margin-bottom:14px; line-height:1.75;">
        <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:1.5px; color:var(--text3); margin-bottom:8px;">Cómo funciona</div>
        <div style="color:var(--text2); font-size:0.95rem;">
            Registrate, cargá tus pronósticos por fase y confirmalos con tu contraseña antes de que arranque cada etapa.
            Después podés seguir el ranking, los puntos y las estadísticas del torneo desde la misma app.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:16px 18px; margin-bottom:14px; line-height:1.75;">
        <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:1.5px; color:var(--text3); margin-bottom:8px;">Fases del juego</div>
        <div style="color:var(--text2); font-size:0.95rem;">
            """ + " · ".join(FASES) + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.button("← Volver", on_click=cambiar_pantalla, args=(0,), use_container_width=True)
