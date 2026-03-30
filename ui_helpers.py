import streamlit as st


def password_input(label, key, placeholder=""):
    """
    Campo de contraseña con botón ojo incrustado dentro del input,
    implementado con CSS+JS puro. No usa st.button, funciona dentro
    y fuera de st.form.
    """
    value = st.text_input(
        label,
        type="password",
        key=key,
        placeholder=placeholder,
    )

    # Inyectamos CSS+JS que busca el input por aria-label o data-testid
    # y le agrega el botón ojo directamente dentro del wrapper del DOM.
    st.markdown(f"""
    <style>
    /* Wrapper relativo para poder posicionar el botón */
    div[data-testid="stTextInput"]:has(input[aria-label="{label}"]) > div > div {{
        position: relative;
    }}
    div[data-testid="stTextInput"]:has(input[aria-label="{label}"]) input {{
        padding-right: 2.8rem !important;
    }}
    .pw-eye-btn-{key} {{
        position: absolute;
        right: 0.75rem;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        line-height: 1;
        font-size: 1.05rem;
        color: var(--text3, #8ea4c4);
        z-index: 10;
        transition: color 0.15s;
    }}
    .pw-eye-btn-{key}:hover {{
        color: var(--accent, #78ecff);
    }}
    </style>
    <script>
    (function() {{
        function init() {{
            const inputs = document.querySelectorAll('input[aria-label="{label}"]');
            inputs.forEach(function(input) {{
                const wrapper = input.parentElement;
                if (wrapper.querySelector('.pw-eye-btn-{key}')) return;
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'pw-eye-btn-{key}';
                btn.innerHTML = '&#128065;';
                btn.setAttribute('aria-label', 'Mostrar/ocultar contraseña');
                btn.addEventListener('mousedown', function(e) {{
                    e.preventDefault();
                }});
                btn.addEventListener('click', function() {{
                    if (input.type === 'password') {{
                        input.type = 'text';
                        btn.innerHTML = '&#128584;';
                    }} else {{
                        input.type = 'password';
                        btn.innerHTML = '&#128065;';
                    }}
                }});
                wrapper.style.position = 'relative';
                wrapper.appendChild(btn);
            }});
        }}
        // Retry until Streamlit renders the input
        let tries = 0;
        const interval = setInterval(function() {{
            init();
            tries++;
            if (tries > 30) clearInterval(interval);
        }}, 120);
    }})();
    </script>
    """, unsafe_allow_html=True)

    return value


def stepper(key, min_value=0, max_value=10):
    val_key = f"{key}_val"

    if val_key not in st.session_state:
        st.session_state[val_key] = 0

    cols = st.columns([1, 2, 1])

    with cols[0]:
        if st.button("−", key=f"{key}_minus", type="secondary", use_container_width=True):
            st.session_state[val_key] = max(min_value, st.session_state[val_key] - 1)
            st.rerun()

    with cols[1]:
        st.markdown(
            f"<div style='text-align:center;font-size:20px;font-weight:700'>{st.session_state[val_key]}</div>",
            unsafe_allow_html=True,
        )

    with cols[2]:
        if st.button("+", key=f"{key}_plus", type="secondary", use_container_width=True):
            st.session_state[val_key] = min(max_value, st.session_state[val_key] + 1)
            st.rerun()

    return st.session_state[val_key]
