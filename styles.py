"""
styles.py — Tema visual premium unificado para toda la app.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg_html="#0b1020",
    bg="#0f172a",
    bg2="#131d34",
    bg3="#18233d",
    surface="rgba(18, 28, 50, 0.78)",
    surface_elevated="rgba(22, 34, 58, 0.94)",
    surface_soft="rgba(148, 163, 184, 0.08)",
    surface2="rgba(148, 163, 184, 0.12)",
    text="#f8fafc",
    text2="#cbd5e1",
    text3="#94a3b8",
    border="rgba(148, 163, 184, 0.16)",
    border2="rgba(148, 163, 184, 0.26)",
    hover_border="rgba(96, 165, 250, 0.44)",
    shadow="rgba(2, 6, 23, 0.50)",
    input_bg="rgba(10, 18, 34, 0.96)",
    input_text="#f8fafc",
    table_bg="rgba(10, 18, 34, 0.94)",
    table_head="rgba(96, 165, 250, 0.10)",
    table_row="rgba(255, 255, 255, 0.02)",
    accent="#60a5fa",
    accent_2="#a78bfa",
    accent_3="#2dd4bf",
    gold="#f8d38b",
    gold2="#fde7b0",
    gold_dim="rgba(248, 211, 139, 0.12)",
    gold_glow="rgba(248, 211, 139, 0.24)",
    gold_border="rgba(248, 211, 139, 0.30)",
    blue="#60a5fa",
    blue2="#bfdbfe",
    blue_dim="rgba(96, 165, 250, 0.12)",
    blue_border="rgba(96, 165, 250, 0.28)",
    cyan="#38bdf8",
    cyan_dim="rgba(56, 189, 248, 0.12)",
    cyan_border="rgba(56, 189, 248, 0.26)",
    red="#fb7185",
    red_dim="rgba(251, 113, 133, 0.12)",
    red_border="rgba(251, 113, 133, 0.28)",
    orange="#fb923c",
    orange_dim="rgba(251, 146, 60, 0.14)",
    orange_border="rgba(251, 146, 60, 0.28)",
    green="#34d399",
    green2="#2dd4bf",
    green_dim="rgba(52, 211, 153, 0.14)",
    green_border="rgba(52, 211, 153, 0.28)",
    green_glow="rgba(52, 211, 153, 0.20)",
    success="#34d399",
    warning="#f59e0b",
    danger="#fb7185",
)


def get_tema() -> str:
    return "executive-night"


def render_tema_boton():
    return None


def inject_css():
    v = PREMIUM_THEME
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

    :root {{
        color-scheme: {v['scheme']};
        --bg: {v['bg']};
        --bg2: {v['bg2']};
        --bg3: {v['bg3']};
        --surface: {v['surface']};
        --surface-elevated: {v['surface_elevated']};
        --surface-soft: {v['surface_soft']};
        --surface2: {v['surface2']};
        --text: {v['text']};
        --text2: {v['text2']};
        --text3: {v['text3']};
        --border: {v['border']};
        --border2: {v['border2']};
        --hover-border: {v['hover_border']};
        --shadow-clr: {v['shadow']};
        --input-bg: {v['input_bg']};
        --input-text: {v['input_text']};
        --table-bg: {v['table_bg']};
        --table-head: {v['table_head']};
        --table-row: {v['table_row']};
        --accent: {v['accent']};
        --accent-2: {v['accent_2']};
        --accent-3: {v['accent_3']};
        --gold: {v['gold']};
        --gold2: {v['gold2']};
        --gold-dim: {v['gold_dim']};
        --gold-glow: {v['gold_glow']};
        --gold-border: {v['gold_border']};
        --blue: {v['blue']};
        --blue2: {v['blue2']};
        --blue-dim: {v['blue_dim']};
        --blue-border: {v['blue_border']};
        --cyan: {v['cyan']};
        --cyan-dim: {v['cyan_dim']};
        --cyan-border: {v['cyan_border']};
        --red: {v['red']};
        --red-dim: {v['red_dim']};
        --red-border: {v['red_border']};
        --orange: {v['orange']};
        --orange-dim: {v['orange_dim']};
        --orange-border: {v['orange_border']};
        --green: {v['green']};
        --green2: {v['green2']};
        --green-dim: {v['green_dim']};
        --green-border: {v['green_border']};
        --green-glow: {v['green_glow']};
        --success: {v['success']};
        --warning: {v['warning']};
        --danger: {v['danger']};
        --radius: 22px;
        --radius-sm: 16px;
        --radius-lg: 30px;
        --panel-bg: linear-gradient(180deg, rgba(20, 30, 52, 0.82) 0%, rgba(12, 19, 35, 0.94) 100%);
        --panel-stroke: linear-gradient(180deg, rgba(255,255,255,0.14) 0%, rgba(255,255,255,0.04) 100%);
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    html, body {{
        background: {v['bg_html']} !important;
        color: var(--text) !important;
    }}

    body {{
        background:
            radial-gradient(circle at 0% 0%, rgba(96,165,250,0.16), transparent 26%),
            radial-gradient(circle at 100% 0%, rgba(167,139,250,0.14), transparent 22%),
            radial-gradient(circle at 50% 100%, rgba(45,212,191,0.10), transparent 24%),
            linear-gradient(180deg, #0b1020 0%, #10192c 38%, #0f172a 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(circle at top left, rgba(96,165,250,0.12), transparent 24%),
            radial-gradient(circle at top right, rgba(167,139,250,0.10), transparent 20%),
            radial-gradient(circle at bottom center, rgba(45,212,191,0.07), transparent 24%),
            linear-gradient(180deg, #0b1020 0%, #10192c 38%, #0f172a 100%) !important;
        color: var(--text) !important;
    }}

    [data-testid="stHeader"], header, #MainMenu, footer {{
        visibility: hidden !important;
        height: 0 !important;
    }}

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
    [data-testid="stAppViewBlockContainer"], section.main, section[data-testid="stSidebar"] {{
        color: var(--text) !important;
        background-color: transparent !important;
    }}

    [data-testid="stAppViewContainer"] * ,
    .stApp * ,
    section[data-testid="stSidebar"] * {{
        color: inherit;
    }}

    .block-container {{
        max-width: 1180px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
    }}

    .block-container > div {{
        position: relative;
        z-index: 1;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
    }}

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small {{
        color: inherit;
    }}

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stText"],
    .stCaption,
    code {{
        color: var(--text) !important;
    }}

    a {{
        color: var(--accent) !important;
        text-decoration: none !important;
    }}

    hr {{
        border-color: rgba(148,163,184,0.14) !important;
    }}

    [data-testid="stHorizontalBlock"] > div {{
        gap: 0.9rem !important;
    }}

    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stExpander"],
    .stForm,
    div[data-testid="stMetric"] {{
        border-radius: var(--radius) !important;
    }}

    .stForm,
    div[data-testid="stMetric"],
    details,
    .stDataFrame,
    div[data-testid="stTable"] {{
        background: var(--panel-bg) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 20px 50px var(--shadow-clr) !important;
        backdrop-filter: blur(18px);
    }}

    .stForm {{
        padding: 1.15rem 1.15rem 0.8rem 1.15rem !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea,
    [data-baseweb="select"] > div,
    [data-baseweb="base-input"] > div,
    [data-testid="stFileUploaderDropzone"] {{
        background: linear-gradient(180deg, rgba(8, 14, 28, 0.98) 0%, rgba(13, 22, 39, 0.98) 100%) !important;
        color: var(--input-text) !important;
        border: 1px solid rgba(148,163,184,0.20) !important;
        border-radius: 18px !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 8px 24px rgba(0,0,0,0.20) !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.88rem 0.98rem !important;
        font-size: 0.98rem !important;
        caret-color: var(--accent) !important;
    }}

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder,
    .stTextArea textarea::placeholder,
    textarea::placeholder {{
        color: var(--text3) !important;
        opacity: 1 !important;
    }}

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus,
    .stTextArea textarea:focus,
    textarea:focus,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="base-input"] > div:focus-within {{
        border-color: rgba(96,165,250,0.72) !important;
        box-shadow: 0 0 0 3px rgba(96,165,250,0.14), 0 10px 26px rgba(96,165,250,0.10) !important;
    }}

    .stTextInput label,
    .stPasswordInput label,
    .stSelectbox label,
    .stNumberInput label,
    .stDateInput label,
    .stFileUploader label,
    .stTextArea label,
    .stMultiSelect label,
    .stRadio label,
    .stCheckbox label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] * {{
        color: var(--text3) !important;
        -webkit-text-fill-color: var(--text3) !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.3px !important;
    }}

    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {{
        background: linear-gradient(180deg, rgba(8,14,28,0.98) 0%, rgba(13,22,39,0.98) 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [data-baseweb="select"] svg,
    [data-baseweb="popover"] svg,
    [role="listbox"] svg {{
        fill: var(--text2) !important;
        color: var(--text2) !important;
    }}

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"] {{
        background: rgba(9, 15, 29, 0.985) !important;
        color: var(--text) !important;
        border: 1px solid rgba(148,163,184,0.22) !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.36) !important;
        border-radius: 18px !important;
        backdrop-filter: blur(16px);
    }}

    [role="option"],
    li[role="option"],
    div[role="option"] {{
        background: rgba(9, 15, 29, 0.985) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [role="option"] *,
    li[role="option"] *,
    div[role="option"] * {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        background: transparent !important;
    }}

    [role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"],
    [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover {{
        background: rgba(96,165,250,0.14) !important;
        color: var(--text) !important;
    }}

    [data-baseweb="select"] input,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div,
    [data-baseweb="select"] p {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {{
        min-height: 46px !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px !important;
        transition: all 0.18s ease !important;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        background: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.03) 100%) !important;
        color: var(--text) !important;
        border: 1px solid rgba(148,163,184,0.20) !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18) !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {{
        transform: translateY(-1px);
        border-color: rgba(96,165,250,0.45) !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.24), 0 0 0 1px rgba(96,165,250,0.10) inset !important;
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    .stDownloadButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #60a5fa 0%, #818cf8 52%, #2dd4bf 100%) !important;
        color: #07111f !important;
        border: 0 !important;
        box-shadow: 0 18px 38px rgba(96,165,250,0.18), 0 10px 24px rgba(45,212,191,0.12) !important;
    }}

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {{
        box-shadow: 0 0 0 3px rgba(96,165,250,0.16) !important;
    }}

    [data-testid="stSuccess"],
    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stError"] {{
        border-radius: 18px !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 12px 26px rgba(0,0,0,0.18) !important;
        backdrop-filter: blur(10px);
    }}

    [data-testid="stSuccess"] {{ background: rgba(16, 185, 129, 0.12) !important; }}
    [data-testid="stInfo"] {{ background: rgba(96, 165, 250, 0.10) !important; }}
    [data-testid="stWarning"] {{ background: rgba(245, 158, 11, 0.12) !important; }}
    [data-testid="stError"] {{ background: rgba(251, 113, 133, 0.12) !important; }}

    button[role="tab"] {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text2) !important;
        padding: 0.76rem 1rem !important;
        font-weight: 700 !important;
        margin-right: 0.35rem !important;
    }}

    button[role="tab"][aria-selected="true"] {{
        color: var(--text) !important;
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(96,165,250,0.14) 0%, rgba(167,139,250,0.12) 100%) !important;
        box-shadow: 0 10px 22px rgba(0,0,0,0.16) !important;
    }}

    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {{
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.4rem 0.65rem;
    }}

    .stDataFrame, div[data-testid="stTable"] {{
        border-radius: 20px !important;
        overflow: hidden !important;
    }}

    table {{
        border-collapse: collapse !important;
    }}

    thead tr {{
        background: var(--table-head) !important;
    }}

    tbody tr:nth-child(even) {{
        background: var(--table-row) !important;
    }}

    th, td {{
        border-color: rgba(148,163,184,0.10) !important;
    }}

    details {{
        border-radius: 18px !important;
        overflow: hidden !important;
    }}

    details summary {{
        background: rgba(255,255,255,0.02) !important;
    }}

    div[data-testid="stMetric"] {{
        padding: 0.95rem 1rem !important;
    }}

    div[data-testid="stMetric"] label {{
        color: var(--text3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.68rem !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: var(--text) !important;
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #60a5fa 0%, #818cf8 60%, #2dd4bf 100%) !important;
    }}

    input, textarea, select, button {{
        color: var(--text) !important;
        -webkit-text-fill-color: currentColor !important;
    }}

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill {{
        -webkit-text-fill-color: var(--text) !important;
        -webkit-box-shadow: 0 0 0px 1000px rgba(8,14,28,0.98) inset !important;
        transition: background-color 9999s ease-out 0s;
    }}

    .stButton > button p,
    .stDownloadButton > button p,
    .stFormSubmitButton > button p,
    button[role="tab"] p,
    [role="option"] *,
    details summary *,
    .stAlert *,
    .stDataFrame *,
    div[data-testid="stTable"] *,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] strong {{
        color: inherit !important;
        -webkit-text-fill-color: currentColor !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] * ,
    [data-testid="stMultiSelect"] [data-baseweb="select"] * {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    select, option, optgroup {{
        background-color: #0a1323 !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [role="listbox"] div,
    [role="listbox"] span,
    [role="listbox"] p,
    [data-baseweb="popover"] div,
    [data-baseweb="popover"] span,
    [data-baseweb="popover"] p {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(10,16,31,0.96) 0%, rgba(14,22,39,0.96) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }}

    [data-testid="stDivider"] {{
        margin: 1rem 0 !important;
    }}

    @media (max-width: 900px) {{
        .block-container {{
            padding-top: 0.9rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        .stForm {{
            padding: 0.95rem 0.95rem 0.7rem 0.95rem !important;
        }}
    }}

    @media (prefers-color-scheme: light) {{
        html, body {{
            color-scheme: dark !important;
        }}
    }}

    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.04); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(148,163,184,0.30); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(96,165,250,0.42); }}
    </style>
    """, unsafe_allow_html=True)
