import streamlit as st
from styles import inject_css

inject_css()

st.title("Demo")

clave = st.text_input("Clave", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("-"):
        st.write("menos")

with col2:
    if st.button("+"):
        st.write("mas")

with st.spinner("Cargando..."):
    import time
    time.sleep(2)

st.success("Listo")
