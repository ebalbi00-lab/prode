import streamlit as st


def password_input_with_toggle(label: str, key: str, placeholder: str = "", value: str = "", help_text: str | None = None):
    show_key = f"{key}__show"
    shown = st.session_state.get(show_key, False)
    cols = st.columns([12, 2], gap="small")
    with cols[0]:
        val = st.text_input(
            label,
            value=value,
            key=key,
            type="default" if shown else "password",
            placeholder=placeholder,
            help=help_text,
        )
    with cols[1]:
        st.markdown("<div style='height:1.72rem'></div>", unsafe_allow_html=True)
        if st.button("🙈" if shown else "👁️", key=f"{key}__toggle", use_container_width=True, type="secondary"):
            st.session_state[show_key] = not shown
            st.rerun()
    return val



def integrated_stepper(label: str, key: str, value: int = 0, min_value: int = 0, max_value: int = 10):
    state_key = f"{key}__val"
    if state_key not in st.session_state:
        st.session_state[state_key] = int(value)
    else:
        try:
            st.session_state[state_key] = int(st.session_state[state_key])
        except Exception:
            st.session_state[state_key] = int(value)

    cols = st.columns([1.15, 2.2, 1.15], gap="small")
    with cols[0]:
        st.markdown("<div style='height:1.72rem'></div>", unsafe_allow_html=True)
        if st.button("−", key=f"{key}__minus", use_container_width=True, type="secondary"):
            st.session_state[state_key] = max(min_value, int(st.session_state[state_key]) - 1)
            st.rerun()
    with cols[1]:
        st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            step=1,
            key=state_key,
            label_visibility="collapsed",
        )
    with cols[2]:
        st.markdown("<div style='height:1.72rem'></div>", unsafe_allow_html=True)
        if st.button("+", key=f"{key}__plus", use_container_width=True, type="secondary"):
            st.session_state[state_key] = min(max_value, int(st.session_state[state_key]) + 1)
            st.rerun()

    return int(st.session_state[state_key])
