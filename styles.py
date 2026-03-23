"""
styles.py — CSS global. Tema profesional premium: Azul oscuro + Modo claro elegante.
"""
import streamlit as st

DARK_THEME = dict(
    bg="#0f1419", bg2="#151b24", bg3="#1a2332",
    text="#f5f7fa", text2="#b8c5d6", text3="#7a8a9e",
    border="rgba(255,255,255,0.08)", border2="rgba(255,255,255,0.12)",
    hover_border="rgba(212,175,55,0.5)",
    shadow="rgba(0,0,0,0.3)", surface2="rgba(255,255,255,0.04)",
    input_bg="#111820", input_text="#f5f7fa",
    grad1="rgba(212,175,55,0.06)", grad2="rgba(79,172,254,0.05)", grad3="rgba(212,175,55,0.04)",
    gold="#d4af37", gold2="#e6c547", gold3="#b8941f",
    gold_dim="rgba(212,175,55,0.10)", gold_glow="rgba(212,175,55,0.25)",
    blue="#4facfe", blue2="#00f2fe", blue_dim="rgba(79,172,254,0.10)", blue_border="rgba(79,172,254,0.25)",
    cyan="#00f2fe", cyan_dim="rgba(0,242,254,0.10)", cyan_border="rgba(0,242,254,0.25)",
    red="#ff6b6b", red_dim="rgba(255,107,107,0.10)", red_border="rgba(255,107,107,0.25)",
    orange="#ff922b", orange_dim="rgba(255,146,43,0.10)", orange_border="rgba(255,146,43,0.25)",
    green="#51cf66", green2="#37b24d", green_dim="rgba(81,207,102,0.10)", green_border="rgba(81,207,102,0.25)",
    table_bg="#111820", table_head="rgba(212,175,55,0.08)", table_row="rgba(212,175,55,0.03)",
    scheme="dark", bg_html="#0f1419",
)

LIGHT_THEME = dict(
    bg="#fafbfc", bg2="#f6f8fa", bg3="#ffffff",
    text="#0d1117", text2="#424a55", text3="#57606a",
    border="rgba(27,31,36,0.08)", border2="rgba(27,31,36,0.15)",
    hover_border="rgba(184,148,31,0.6)",
    shadow="rgba(0,0,0,0.06)", surface2="rgba(27,31,36,0.04)",
    input_bg="#ffffff", input_text="#0d1117",
    grad1="rgba(212,175,55,0.04)", grad2="rgba(79,172,254,0.03)", grad3="rgba(212,175,55,0.02)",
    gold="#b8861b", gold2="#d4af37", gold3="#9a6b14",
    gold_dim="rgba(184,134,27,0.10)", gold_glow="rgba(184,134,27,0.20)",
    blue="#0969da", blue2="#0a63d4", blue_dim="rgba(9,105,218,0.10)", blue_border="rgba(9,105,218,0.20)",
    cyan="#0891b2", cyan_dim="rgba(8,145,178,0.10)", cyan_border="rgba(8,145,178,0.20)",
    red="#cf222e", red_dim="rgba(207,34,46,0.10)", red_border="rgba(207,34,46,0.20)",
    orange="#fb8500", orange_dim="rgba(251,133,0,0.10)", orange_border="rgba(251,133,0,0.20)",
    green="#1a7f37", green2="#0d4a1a", green_dim="rgba(26,127,55,0.10)", green_border="rgba(26,127,55,0.20)",
    table_bg="#ffffff", table_head="rgba(212,175,55,0.06)", table_row="rgba(212,175,55,0.02)",
    scheme="light", bg_html="#fafbfc",
)


def get_tema() -> str:
    """Retorna el tema actual."""
    return st.query_params.get("t", "dark")


def toggle_tema():
    """Alterna entre tema claro y oscuro."""
    actual = get_tema()
    st.query_params["t"] = "light" if actual == "dark" else "dark"
    st.rerun()


def render_tema_boton():
    """Renderiza el botón para cambiar de tema."""
    tema = get_tema()
    icono = "☀️" if tema == "dark" else "🌙"
    
    col1, col2 = st.columns([11, 1])
    with col2:
        if st.button(icono, key="_tema_btn", help="Cambiar tema", use_container_width=True):
            toggle_tema()


def inject_css():
    """Inyecta CSS con tema profesional premium."""
    tema = get_tema()
    v = DARK_THEME if tema == "dark" else LIGHT_THEME

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    :root {{
        color-scheme: {v['scheme']};
        --bg:           {v['bg']};
        --bg2:          {v['bg2']};
        --bg3:          {v['bg3']};
        --text:         {v['text']};
        --text2:        {v['text2']};
        --text3:        {v['text3']};
        --border:       {v['border']};
        --border2:      {v['border2']};
        --hover-border: {v['hover_border']};
        --shadow-clr:   {v['shadow']};
        --surface:      rgba(255,255,255,0.05);
        --surface2:     {v['surface2']};
        --input-bg:     {v['input_bg']};
        --input-text:   {v['input_text']};
        --table-bg:     {v['table_bg']};
        --table-head:   {v['table_head']};
        --table-row:    {v['table_row']};
        --gold:         {v['gold']};
        --gold2:        {v['gold2']};
        --gold-dim:     {v['gold_dim']};
        --gold-glow:    {v['gold_glow']};
        --blue:         {v['blue']};
        --blue2:        {v['blue2']};
        --blue-dim:     {v['blue_dim']};
        --cyan:         {v['cyan']};
        --cyan-dim:     {v['cyan_dim']};
        --red:          {v['red']};
        --red-dim:      {v['red_dim']};
        --orange:       {v['orange']};
        --orange-dim:   {v['orange_dim']};
        --green:        {v['green']};
        --green2:       {v['green2']};
        --green-dim:    {v['green_dim']};
        --radius:       12px;
        --radius-sm:    8px;
        --radius-lg:    16px;
    }}

    html, body {{ 
        background-color: {v['bg_html']} !important; 
        color: {v['text']} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
    }}
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, .block-container {{
        background-color: var(--bg) !important; 
        color: var(--text) !important;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {v['bg']} 0%, {v['bg2']} 50%, {v['bg']} 100%) !important;
        background-attachment: fixed !important;
        min-height: 100vh;
    }}
    
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ 
        padding-top: 2.5rem !important; 
        padding-bottom: 3.5rem !important; 
        max-width: 900px !important; 
    }}

    /* ===== TYPOGRAPHY ===== */
    h1 {{
        font-family: 'Inter', sans-serif !important; 
        font-size: 3.2rem !important; 
        font-weight: 900 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(135deg, {v['gold']} 0%, {v['gold2']} 100%) !important;
        -webkit-background-clip: text !important; 
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important; 
        margin: 1.5rem 0 1rem 0 !important; 
        line-height: 1.1 !important;
    }}
    
    h2 {{ 
        font-family: 'Inter', sans-serif !important; 
        font-size: 2rem !important; 
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        color: var(--text) !important; 
        margin: 1.5rem 0 0.8rem 0 !important; 
        line-height: 1.2 !important;
    }}
    
    h3 {{ 
        font-family: 'Inter', sans-serif !important; 
        font-weight: 700 !important; 
        color: var(--gold) !important; 
        font-size: 1rem !important; 
        text-transform: uppercase !important; 
        letter-spacing: 1px !important;
        margin: 1rem 0 0.5rem 0 !important;
    }}

    p, div, span, li {{
        color: var(--text) !important;
    }}

    /* ===== INPUTS ===== */
    .stTextInput > div > div > input, 
    .stPasswordInput > div > div > input,
    .stNumberInput > div > div > input {{
        background: var(--input-bg) !important; 
        border: 1.5px solid var(--border2) !important;
        border-radius: var(--radius-sm) !important; 
        color: var(--input-text) !important;
        padding: 0.85rem 1.1rem !important; 
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important; 
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
    }}
    
    .stTextInput > div > div > input:focus, 
    .stPasswordInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--gold) !important; 
        box-shadow: 0 0 0 3px var(--gold-dim), 0 4px 12px {v['shadow']} !important;
        outline: none !important;
        background: var(--bg3) !important;
    }}
    
    .stTextInput > div > div > input::placeholder, 
    .stPasswordInput > div > div > input::placeholder {{
        color: var(--text3) !important; 
    }}
    
    .stTextInput label, 
    .stPasswordInput label, 
    .stSelectbox label, 
    .stNumberInput label,
    .stFileUploader label, 
    .stRadio label, 
    .stDateInput label {{
        color: var(--text2) !important; 
        font-size: 0.75rem !important; 
        font-weight: 700 !important;
        text-transform: uppercase !important; 
        letter-spacing: 1.5px !important;
        margin-bottom: 0.6rem !important;
    }}
    
    .stSelectbox > div > div {{
        background: var(--input-bg) !important; 
        border: 1.5px solid var(--border2) !important;
        border-radius: var(--radius-sm) !important; 
        color: var(--input-text) !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
    }}
    
    .stSelectbox > div > div > div {{ 
        color: var(--input-text) !important; 
    }}

    /* ===== BUTTONS SECUNDARIOS ===== */
    .stButton > button {{
        background-color: var(--bg3) !important;
        color: var(--text) !important;
        border: 2px solid var(--border2) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    
    .stButton > button::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.15), transparent) !important;
        transition: left 0.5s ease !important;
    }}
    
    .stButton > button:hover {{
        border-color: var(--gold) !important;
        background-color: rgba(212,175,55,0.08) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px {v['shadow']} !important;
    }}

    .stButton > button:hover::before {{
        left: 100% !important;
    }}

    .stButton > button:active {{
        transform: translateY(0) !important;
        box-shadow: 0 1px 4px {v['shadow']} !important;
    }}

    .stButton > button:disabled {{
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }}

    /* ===== BUTTONS PRIMARY (Ingresar, Registrarse) - VERDE ===== */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--green) 0%, var(--green2) 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(81,207,102,0.3) !important;
    }}

    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(81,207,102,0.4) !important;
    }}

    .stButton > button[kind="primary"]:active {{
        transform: translateY(-1px) !important;
    }}

    /* ===== BOTÓN TEMA ===== */
    #_tema_btn {{
        font-size: 1.5rem !important;
        padding: 0.5rem 0.8rem !important;
        border: 2px solid var(--gold) !important;
        background: var(--bg3) !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
        transition: all 0.3s ease !important;
    }}

    #_tema_btn:hover {{
        background: rgba(212,175,55,0.12) !important;
        box-shadow: 0 4px 12px rgba(212,175,55,0.2) !important;
        transform: scale(1.05) !important;
    }}

    #_tema_btn:active {{
        transform: scale(0.95) !important;
    }}

    /* ===== DIVIDERS ===== */
    .stDivider {{ 
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--border2), transparent) !important;
        margin: 1.5rem 0 !important;
    }}

    /* ===== MESSAGES ===== */
    .stSuccess, .stError, .stWarning, .stInfo {{
        border-radius: var(--radius-sm) !important;
        border-left: 4px solid !important;
        padding: 1.1rem 1.4rem !important;
        margin: 1.2rem 0 !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
        font-weight: 500 !important;
        color: var(--text) !important;
    }}

    .stSuccess {{ 
        background-color: var(--green-dim) !important;
        border-left-color: var(--green) !important;
    }}
    
    .stError {{ 
        background-color: var(--red-dim) !important;
        border-left-color: var(--red) !important;
    }}
    
    .stWarning {{ 
        background-color: var(--orange-dim) !important;
        border-left-color: var(--orange) !important;
    }}
    
    .stInfo {{ 
        background-color: var(--blue-dim) !important;
        border-left-color: var(--blue) !important;
    }}

    /* ===== CHECKBOX ===== */
    .stCheckbox > label {{
        color: var(--text) !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        margin-bottom: 0.5rem !important;
    }}

    /* ===== FORM ===== */
    .stForm {{
        background: var(--bg3) !important;
        border-radius: var(--radius) !important;
        padding: 2rem !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
    }}

    /* ===== MARKDOWN ===== */
    .markdown-text-container {{
        color: var(--text) !important;
    }}

    /* ===== SUBHEADER ===== */
    .stSubheader {{
        color: var(--text) !important;
        font-weight: 700 !important;
    }}

    /* ===== CAPTION ===== */
    .stCaption {{
        color: var(--text3) !important;
        font-size: 0.85rem !important;
    }}

    /* ===== METRIC ===== */
    [data-testid="stMetricContainer"] {{
        background: var(--bg3) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
    }}

    /* ===== TABLE ===== */
    .stDataFrame {{
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 2px 8px {v['shadow']} !important;
    }}

    thead {{
        background-color: var(--table-head) !important;
    }}

    tbody tr {{
        border-color: var(--border) !important;
    }}

    tbody tr:nth-child(odd) {{
        background-color: var(--table-row) !important;
    }}

    /* ===== EXPANDABLE ===== */
    .streamlit-expanderHeader {{
        background: var(--bg2) !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border) !important;
    }}

    /* ===== TABS ===== */
    [data-testid="stTabs"] button {{
        color: var(--text2) !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: var(--gold) !important;
        border-bottom-color: var(--gold) !important;
    }}

    /* ===== SCROLL ===== */
    ::-webkit-scrollbar {{
        width: 8px !important;
    }}

    ::-webkit-scrollbar-track {{
        background: var(--bg2) !important;
    }}

    ::-webkit-scrollbar-thumb {{
        background: var(--gold) !important;
        border-radius: 4px !important;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: var(--gold2) !important;
    }}

    /* ===== SPINNER ===== */
    .stSpinner {{
        color: var(--gold) !important;
    }}

    /* ===== GENERAL ===== */
    [data-testid="column"] {{
        padding: 0.5rem !important;
    }}

    .stWarning, .stError, .stInfo, .stSuccess {{
        animation: slideIn 0.3s ease !important;
    }}

    @keyframes slideIn {{
        from {{
            opacity: 0 !important;
            transform: translateY(-10px) !important;
        }}
        to {{
            opacity: 1 !important;
            transform: translateY(0) !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)