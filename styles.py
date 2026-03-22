"""
styles.py — CSS global. Los colores base en .streamlit/config.toml.
"""
import streamlit as st

DARK = dict(
    bg="#0f1923", bg2="#162030", bg3="#1c2e3f",
    text="#e8edf8", text2="#8898bb", text3="#445070",
    border="rgba(100,160,255,0.18)", border2="rgba(100,160,255,0.40)",
    hover_border="rgba(100,180,255,0.6)",
    shadow="rgba(0,5,20,0.55)", surface2="rgba(255,255,255,0.10)",
    input_bg="#1c2e3f", input_text="#e8edf8",
    grad1="rgba(30,80,200,0.15)", grad2="rgba(0,180,255,0.08)", grad3="rgba(0,220,110,0.07)",
    green="#00e87a", green2="#00c860",
    green_dim="rgba(0,220,110,0.12)", green_glow="rgba(0,200,96,0.28)",
    gold="#ffc840", gold_dim="rgba(255,200,64,0.12)", gold_border="rgba(255,200,64,0.30)",
    blue="#5599ff", blue_dim="rgba(85,153,255,0.10)", blue_border="rgba(85,153,255,0.30)",
    red="#ff5566", red_dim="rgba(255,85,102,0.10)", red_border="rgba(255,85,102,0.30)",
    orange="#ff8844", orange_dim="rgba(255,136,68,0.12)", orange_border="rgba(255,136,68,0.30)",
    table_bg="#162030", table_head="rgba(100,160,255,0.07)", table_row="rgba(100,160,255,0.03)",
    scheme="dark", bg_html="#0f1923",
)

LIGHT = dict(
    bg="#f0f4fb", bg2="#e4eaf5", bg3="#ffffff",
    text="#111827", text2="#4a5568", text3="#9aa5b4",
    border="rgba(0,60,180,0.15)", border2="rgba(0,60,180,0.30)",
    hover_border="rgba(0,60,180,0.5)",
    shadow="rgba(0,0,0,0.10)", surface2="rgba(0,0,0,0.07)",
    input_bg="#ffffff", input_text="#111827",
    grad1="rgba(30,80,200,0.05)", grad2="rgba(0,150,255,0.04)", grad3="rgba(0,180,80,0.04)",
    green="#007a40", green2="#005c30",
    green_dim="rgba(0,122,64,0.10)", green_glow="rgba(0,100,50,0.22)",
    gold="#9a6800", gold_dim="rgba(154,104,0,0.10)", gold_border="rgba(154,104,0,0.28)",
    blue="#1a56db", blue_dim="rgba(26,86,219,0.10)", blue_border="rgba(26,86,219,0.28)",
    red="#c81e3a", red_dim="rgba(200,30,58,0.10)", red_border="rgba(200,30,58,0.28)",
    orange="#b45309", orange_dim="rgba(180,83,9,0.10)", orange_border="rgba(180,83,9,0.28)",
    table_bg="#ffffff", table_head="rgba(0,60,180,0.05)", table_row="rgba(0,60,180,0.02)",
    scheme="light", bg_html="#f0f4fb",
)


def get_tema() -> str:
    t = st.query_params.get("t", "dark")
    return t if t in ("dark", "light") else "dark"


def toggle_tema():
    actual = get_tema()
    st.query_params["t"] = "light" if actual == "dark" else "dark"
    st.rerun()


def render_tema_boton():
    tema = get_tema()
    icono = "☀️" if tema == "dark" else "🌙"
    col1, col2 = st.columns([11, 1])
    with col2:
        if st.button(icono, key="_tema_btn"):
            toggle_tema()


def inject_css():
    tema = get_tema()
    v = DARK if tema == "dark" else LIGHT

    # CSS de botones con valores interpolados directamente (sin variables CSS)
    btn_bg     = v['bg3']
    btn_border = v['border2']
    btn_text   = v['text']
    btn_green  = v['green']
    btn_green2 = v['green2']
    btn_glow   = v['green_glow']

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

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
        --green:        {v['green']};
        --green2:       {v['green2']};
        --green-dim:    {v['green_dim']};
        --green-glow:   {v['green_glow']};
        --gold:         {v['gold']};
        --gold-dim:     {v['gold_dim']};
        --gold-border:  {v['gold_border']};
        --blue:         {v['blue']};
        --blue-dim:     {v['blue_dim']};
        --blue-border:  {v['blue_border']};
        --red:          {v['red']};
        --red-dim:      {v['red_dim']};
        --red-border:   {v['red_border']};
        --orange:       {v['orange']};
        --orange-dim:   {v['orange_dim']};
        --orange-border:{v['orange_border']};
        --radius:       14px;
        --radius-sm:    9px;
    }}

    html, body {{ background-color: {v['bg_html']} !important; color: {v['text']} !important; }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, .block-container {{
        background-color: var(--bg) !important; color: var(--text) !important;
    }}
    .stApp {{
        background: var(--bg) !important;
        background-image:
            radial-gradient(ellipse 70% 50% at 10% 60%, {v['grad1']} 0%, transparent 100%),
            radial-gradient(ellipse 55% 40% at 90% 15%, {v['grad2']} 0%, transparent 100%),
            radial-gradient(ellipse 45% 35% at 50% 95%, {v['grad3']} 0%, transparent 100%) !important;
        min-height: 100vh;
    }}
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{ font-family: 'Outfit', sans-serif; -webkit-font-smoothing: antialiased; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 2.5rem !important; padding-bottom: 4rem !important; max-width: 860px !important; }}

    h1 {{
        font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; letter-spacing: 3px !important;
        background: linear-gradient(135deg, var(--green) 0%, var(--green2) 100%) !important;
        -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
        background-clip: text !important; margin-bottom: 0.15rem !important; line-height: 1.05 !important;
    }}
    h2 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 1.7rem !important; letter-spacing: 2px !important; color: var(--text) !important; margin-top: 0.3rem !important; }}
    h3 {{ font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; color: var(--text2) !important; font-size: 0.72rem !important; text-transform: uppercase !important; letter-spacing: 2px !important; }}

    .stTextInput > div > div > input, .stPasswordInput > div > div > input {{
        background: var(--input-bg) !important; border: 1.5px solid var(--border2) !important;
        border-radius: var(--radius-sm) !important; color: var(--input-text) !important;
        padding: 0.65rem 1rem !important; font-family: 'Outfit', sans-serif !important;
        font-size: 0.97rem !important; font-weight: 500 !important;
        -webkit-text-fill-color: var(--input-text) !important; caret-color: var(--green) !important;
    }}
    .stTextInput > div > div > input:focus, .stPasswordInput > div > div > input:focus {{
        border-color: var(--green2) !important; box-shadow: 0 0 0 3px var(--green-dim) !important;
        -webkit-text-fill-color: var(--input-text) !important;
    }}
    .stTextInput > div > div > input::placeholder, .stPasswordInput > div > div > input::placeholder {{
        color: var(--text3) !important; -webkit-text-fill-color: var(--text3) !important;
    }}
    .stTextInput label, .stPasswordInput label, .stSelectbox label, .stNumberInput label,
    .stFileUploader label, .stRadio label, .stDateInput label {{
        color: var(--text2) !important; font-size: 0.75rem !important; font-weight: 600 !important;
        text-transform: uppercase !important; letter-spacing: 1.2px !important;
    }}
    .stSelectbox > div > div {{
        background: var(--input-bg) !important; border: 1.5px solid var(--border2) !important;
        border-radius: var(--radius-sm) !important; color: var(--input-text) !important;
        -webkit-text-fill-color: var(--input-text) !important;
    }}
    .stSelectbox > div > div > div {{ color: var(--input-text) !important; -webkit-text-fill-color: var(--input-text) !important; }}
    .stNumberInput > div > div > input {{
        background: var(--input-bg) !important; border: 1.5px solid var(--border2) !important;
        border-radius: var(--radius-sm) !important; color: var(--input-text) !important;
        -webkit-text-fill-color: var(--input-text) !important; caret-color: var(--green) !important;
        text-align: center !important; font-size: 1.5rem !important; font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }}
    .stNumberInput > div > div > input:focus {{ border-color: var(--green2) !important; box-shadow: 0 0 0 3px var(--green-dim) !important; }}

    .stSuccess {{ background: var(--green-dim) !important; border: 1px solid var(--green-glow) !important; border-radius: var(--radius-sm) !important; color: var(--green) !important; }}
    .stError   {{ background: var(--red-dim)   !important; border: 1px solid var(--red-border)   !important; border-radius: var(--radius-sm) !important; color: var(--red)   !important; }}
    .stWarning {{ background: var(--gold-dim)   !important; border: 1px solid var(--gold-border)  !important; border-radius: var(--radius-sm) !important; color: var(--gold)  !important; }}
    .stInfo    {{ background: var(--blue-dim)   !important; border: 1px solid var(--blue-border)  !important; border-radius: var(--radius-sm) !important; color: var(--blue)  !important; }}

    [data-testid="stMetric"] {{ background: var(--bg3) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; padding: 1.1rem 1.3rem !important; position: relative !important; overflow: hidden !important; }}
    [data-testid="stMetric"]::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--green2), transparent); opacity: 0.5; }}
    [data-testid="stMetricLabel"] {{ color: var(--text2) !important; font-size: 0.72rem !important; text-transform: uppercase !important; letter-spacing: 1.4px !important; font-weight: 600 !important; }}
    [data-testid="stMetricValue"] {{ color: var(--green) !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 2.4rem !important; letter-spacing: 1.5px !important; line-height: 1.1 !important; }}

    [data-testid="stDataFrame"] {{ border-radius: var(--radius) !important; overflow: hidden !important; border: 1px solid var(--border) !important; }}

    .stTabs [data-baseweb="tab-list"] {{ background: var(--bg3) !important; border-radius: var(--radius) !important; padding: 5px !important; gap: 3px !important; border: 1.5px solid var(--border) !important; }}
    .stTabs [data-baseweb="tab"] {{ background: transparent !important; border-radius: var(--radius-sm) !important; color: var(--text2) !important; font-family: 'Outfit', sans-serif !important; font-weight: 600 !important; font-size: 0.78rem !important; padding: 0.42rem 0.85rem !important; }}
    .stTabs [data-baseweb="tab"]:hover {{ color: var(--text) !important; background: var(--surface2) !important; }}
    .stTabs [aria-selected="true"] {{ background: var(--green-dim) !important; color: var(--green) !important; border: 1px solid var(--green-glow) !important; }}

    .stRadio [data-testid="stMarkdownContainer"] p {{ color: var(--text) !important; font-weight: 500 !important; }}
    .stRadio > div {{ background: var(--bg3) !important; border-radius: var(--radius) !important; padding: 0.55rem 1rem !important; border: 1.5px solid var(--border) !important; }}
    .stCheckbox, [data-testid="stToggle"] {{ color: var(--text) !important; }}

    .streamlit-expanderHeader {{ background: var(--bg3) !important; border-radius: var(--radius-sm) !important; border: 1.5px solid var(--border) !important; color: var(--text) !important; font-weight: 600 !important; }}
    .streamlit-expanderContent {{ background: var(--surface) !important; border: 1.5px solid var(--border) !important; border-top: none !important; border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important; }}

    hr {{ border: none !important; border-top: 1px solid var(--border) !important; margin: 1.6rem 0 !important; }}
    .stCaption, caption {{ color: var(--text3) !important; font-size: 0.78rem !important; }}
    .stMarkdown p {{ color: var(--text2) !important; line-height: 1.75 !important; }}
    .stMarkdown strong {{ color: var(--text) !important; font-weight: 700 !important; }}
    [data-testid="stFileUploader"] {{ background: var(--surface) !important; border: 1.5px dashed var(--border2) !important; border-radius: var(--radius) !important; }}
    [data-testid="stForm"] {{ background: var(--bg3) !important; border: 1.5px solid var(--border) !important; border-radius: var(--radius) !important; padding: 1.6rem !important; }}
    .stSpinner > div {{ border-top-color: var(--green) !important; }}

    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border2); border-radius: 4px; }}

    @media (max-width: 768px) {{
        .block-container {{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; padding-top: 1rem !important; }}
        h1 {{ font-size: 2.3rem !important; }}
        h2 {{ font-size: 1.4rem !important; }}
        .stTabs [data-baseweb="tab"] {{ font-size: 0.68rem !important; padding: 0.3rem 0.45rem !important; }}
        .stTabs [data-baseweb="tab-list"] {{ flex-wrap: wrap !important; gap: 2px !important; }}
        .stTextInput > div > div > input, .stPasswordInput > div > div > input {{ font-size: 16px !important; }}
        [data-testid="stMetricValue"] {{ font-size: 1.8rem !important; }}
        .stNumberInput > div > div > input {{ font-size: 1.5rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # Botones — CSS separado con valores hardcodeados interpolados desde Python
    st.markdown(f"""
    <style>
    [data-testid="stButton"] button,
    [data-testid="stFormSubmitButton"] button {{
        background-color: {btn_bg} !important;
        border: 1.5px solid {btn_border} !important;
        border-radius: 8px !important;
        color: {btn_text} !important;
        -webkit-text-fill-color: {btn_text} !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.5rem 1.2rem !important;
        min-height: 2.4rem !important;
        transition: all 0.16s ease !important;
    }}
    [data-testid="stButton"] button:hover,
    [data-testid="stFormSubmitButton"] button:hover {{
        filter: brightness(1.3) !important;
    }}
    [data-testid="stButton"] button p,
    [data-testid="stButton"] button span,
    [data-testid="stButton"] button div,
    [data-testid="stFormSubmitButton"] button p,
    [data-testid="stFormSubmitButton"] button span {{
        color: {btn_text} !important;
        -webkit-text-fill-color: {btn_text} !important;
    }}
    [data-testid="stButton"] button[data-testid="baseButton-primary"],
    [data-testid="stFormSubmitButton"] button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, {btn_green2} 0%, {btn_green} 100%) !important;
        border: none !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 18px {btn_glow} !important;
    }}
    [data-testid="stButton"] button[data-testid="baseButton-primary"] p,
    [data-testid="stButton"] button[data-testid="baseButton-primary"] span,
    [data-testid="stFormSubmitButton"] button[data-testid="baseButton-primary"] p,
    [data-testid="stFormSubmitButton"] button[data-testid="baseButton-primary"] span {{
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }}
    </style>
    """, unsafe_allow_html=True)