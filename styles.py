import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg="#07111f",
    bg2="#0b1729",
    bg3="#0f1d33",
    text="#f4f7fb",
    text2="#c6d3e6",
    text3="#8da2c0",
    border="rgba(143,170,214,0.18)",
    blue="#6ee7ff",
    blue_dim="rgba(110,231,255,0.12)",
    blue_border="rgba(110,231,255,0.28)",
)

def inject_css():
    v = PREMIUM_THEME
    st.markdown(f"""
    <style>
    :root {{
        --bg: {v['bg']};
        --bg2: {v['bg2']};
        --bg3: {v['bg3']};
        --text: {v['text']};
        --text2: {v['text2']};
        --text3: {v['text3']};
        --border: {v['border']};
        --blue: {v['blue']};
        --blue-dim: {v['blue_dim']};
        --blue-border: {v['blue_border']};
    }}

    body {{
        background: var(--bg);
        color: var(--text);
    }}

    .stTextInput input,
    .stNumberInput input {{
        background: var(--bg2);
        color: var(--text);
        border-radius: 10px;
        border: 1px solid var(--border);
    }}

    .stButton button {{
        border-radius: 10px;
        font-weight: 600;
    }}

    button[kind="secondary"] {{
        background: var(--blue-dim) !important;
        color: var(--blue) !important;
        border: 1px solid var(--blue-border) !important;
    }}

    button[kind="secondary"]:hover {{
        background: var(--blue) !important;
        color: #07111f !important;
    }}

    div[data-testid="column"] button {{
        border-radius: 10px;
        font-weight: 700;
    }}
    </style>
    """, unsafe_allow_html=True)
