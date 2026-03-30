import streamlit as st
from ui_helpers import password_input_with_toggle

def pantalla_login():
    usuario = st.text_input("Usuario")
    clave = password_input_with_toggle("Clave", "login_clave", placeholder="••••••")

    if st.button("Ingresar"):
        st.write("Login simulado")
