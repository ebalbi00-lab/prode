import streamlit as st

def password_input_with_toggle(label: str, key: str, placeholder: str = "", value: str = "", help_text: str | None = None):
    show_key = f"{key}__show"
    shown = st.session_state.get(show_key, False)

    cols = st.columns([0.84, 0.16], gap="small")

    with cols[0]:
        val = st.text_input(label, value=value, key=key, type="default" if shown else "password", placeholder=placeholder, help=help_text)

    with cols[1]:
        st.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
        if st.button("🙈" if shown else "👁️", key=f"{key}__toggle", use_container_width=True):
            st.session_state[show_key] = not shown
            st.rerun()

    return val
