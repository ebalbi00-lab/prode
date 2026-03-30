import streamlit as st



def stepper(key, min_value=0, max_value=10):
    val_key = f"{key}_val"

    if val_key not in st.session_state:
        st.session_state[val_key] = 0

    cols = st.columns([1,2,1])

    with cols[0]:
        if st.button("−", key=f"{key}_minus", type="secondary", use_container_width=True):
            st.session_state[val_key] = max(min_value, st.session_state[val_key] - 1)
            st.rerun()

    with cols[1]:
        st.markdown(
            f"<div style='text-align:center;font-size:20px;font-weight:700'>{st.session_state[val_key]}</div>",
            unsafe_allow_html=True
        )

    with cols[2]:
        if st.button("+", key=f"{key}_plus", type="secondary", use_container_width=True):
            st.session_state[val_key] = min(max_value, st.session_state[val_key] + 1)
            st.rerun()

    return st.session_state[val_key]
