"""
styles.py — Tema visual premium unificado para toda la app.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg_html="#07111f",
    bg="#07111f",
    bg2="#0b1729",
    bg3="#0f1d33",
    surface="rgba(12, 22, 40, 0.78)",
    surface_elevated="rgba(16, 28, 50, 0.92)",
    surface_soft="rgba(120, 140, 180, 0.08)",
    surface2="rgba(120, 140, 180, 0.12)",
    text="#f4f7fb",
    text2="#c6d3e6",
    text3="#8da2c0",
    border="rgba(143, 170, 214, 0.18)",
    border2="rgba(143, 170, 214, 0.28)",
    hover_border="rgba(110, 231, 255, 0.42)",
    shadow="rgba(2, 8, 20, 0.42)",
    input_bg="rgba(9, 18, 33, 0.96)",
    input_text="#f4f7fb",
    table_bg="rgba(9, 18, 33, 0.94)",
    table_head="rgba(110, 231, 255, 0.10)",
    table_row="rgba(255, 255, 255, 0.02)",
    accent="#6ee7ff",
    accent_2="#8b5cf6",
    accent_3="#22c55e",
    gold="#f5c76b",
    gold2="#ffd891",
    gold_dim="rgba(245, 199, 107, 0.12)",
    gold_glow="rgba(245, 199, 107, 0.22)",
    gold_border="rgba(245, 199, 107, 0.32)",
    blue="#6ee7ff",
    blue2="#bae6fd",
    blue_dim="rgba(110, 231, 255, 0.12)",
    blue_border="rgba(110, 231, 255, 0.28)",
    cyan="#22d3ee",
    cyan_dim="rgba(34, 211, 238, 0.12)",
    cyan_border="rgba(34, 211, 238, 0.26)",
    red="#fb7185",
    red_dim="rgba(251, 113, 133, 0.12)",
    red_border="rgba(251, 113, 133, 0.28)",
    orange="#fb923c",
    orange_dim="rgba(251, 146, 60, 0.14)",
    orange_border="rgba(251, 146, 60, 0.28)",
    green="#34d399",
    green2="#10b981",
    green_dim="rgba(52, 211, 153, 0.14)",
    green_border="rgba(52, 211, 153, 0.28)",
    green_glow="rgba(52, 211, 153, 0.20)",
    success="#34d399",
    warning="#f59e0b",
    danger="#fb7185",
)


def get_tema() -> str:
    return "premium-dark"


def render_tema_boton():
    return None


def inject_css():
    v = PREMIUM_THEME
    st.markdown(f"""
    <style>
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
        --radius: 18px;
        --radius-sm: 14px;
        --radius-lg: 26px;
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
            radial-gradient(circle at 0% 0%, rgba(110,231,255,0.18), transparent 28%),
            radial-gradient(circle at 100% 0%, rgba(139,92,246,0.20), transparent 24%),
            radial-gradient(circle at 50% 100%, rgba(52,211,153,0.10), transparent 26%),
            linear-gradient(180deg, #07111f 0%, #091626 42%, #0b1320 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(circle at top left, rgba(110,231,255,0.16), transparent 24%),
            radial-gradient(circle at top right, rgba(139,92,246,0.18), transparent 22%),
            radial-gradient(circle at bottom center, rgba(52,211,153,0.08), transparent 26%),
            linear-gradient(180deg, #07111f 0%, #091626 42%, #0b1320 100%) !important;
        color: var(--text) !important;
    }}

    [data-testid="stHeader"], header, #MainMenu, footer {{
        visibility: hidden !important;
        height: 0 !important;
    }}

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
    [data-testid="stAppViewBlockContainer"], section.main, section[data-testid="stSidebar"] {{
        color: var(--text) !important;
        background-color: var(--bg) !important;
    }}

    [data-testid="stAppViewContainer"] * ,
    .stApp * ,
    section[data-testid="stSidebar"] * {{
        color: inherit;
    }}

    .block-container {{
        max-width: 1080px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
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
        border-color: rgba(143,170,214,0.14) !important;
    }}

    /* Containers */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stExpander"],
    .stForm,
    div[data-testid="stMetric"] {{
        border-radius: var(--radius) !important;
    }}

    .stForm {{
        background: linear-gradient(180deg, rgba(15,29,51,0.92) 0%, rgba(10,20,36,0.95) 100%) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 20px 48px var(--shadow-clr) !important;
        padding: 1.05rem 1.05rem 0.8rem 1.05rem !important;
        position: relative;
        overflow: hidden;
    }}

    .stForm::before {{
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(110,231,255,0.65) 22%, rgba(139,92,246,0.55) 68%, transparent 100%);
        pointer-events: none;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea,
    [data-baseweb="select"] > div,
    [data-baseweb="base-input"] > div,
    [data-testid="stFileUploaderDropzone"] {{
        background: linear-gradient(180deg, rgba(8,18,32,0.98) 0%, rgba(11,23,41,0.98) 100%) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--border2) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 28px rgba(0,0,0,0.18) !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.82rem 0.95rem !important;
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
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(110,231,255,0.12), 0 10px 30px rgba(110,231,255,0.10) !important;
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
        color: var(--text2) !important;
        -webkit-text-fill-color: var(--text2) !important;
        font-size: 0.73rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }}

    /* Dropdowns */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {{
        background: linear-gradient(180deg, rgba(8,18,32,0.98) 0%, rgba(11,23,41,0.98) 100%) !important;
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
        background: rgba(10, 19, 35, 0.985) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.36) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(14px);
    }}

    [role="option"],
    li[role="option"],
    div[role="option"] {{
        background: rgba(10, 19, 35, 0.985) !important;
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
        background: rgba(110,231,255,0.14) !important;
        color: var(--text) !important;
    }}

    [data-baseweb="select"] input,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div,
    [data-baseweb="select"] p {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}



    /* Icon / utility buttons */
    .stNumberInput button,
    .stPasswordInput button,
    .stTextInput button,
    [data-baseweb="input"] button,
    [data-baseweb="base-input"] button {{
        background: linear-gradient(135deg, rgba(34,211,238,0.96) 0%, rgba(59,130,246,0.92) 100%) !important;
        color: #04111f !important;
        border: 1px solid rgba(110,231,255,0.34) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 22px rgba(34,211,238,0.18) !important;
        transition: all 0.18s ease !important;
    }}

    .stNumberInput button:hover,
    .stPasswordInput button:hover,
    .stTextInput button:hover,
    [data-baseweb="input"] button:hover,
    [data-baseweb="base-input"] button:hover {{
        border-color: var(--accent) !important;
        transform: translateY(-1px);
        box-shadow: 0 14px 26px rgba(34,211,238,0.22), 0 0 0 1px rgba(110,231,255,0.12) inset !important;
    }}

    .stNumberInput button svg,
    .stPasswordInput button svg,
    .stTextInput button svg,
    [data-baseweb="input"] button svg,
    [data-baseweb="base-input"] button svg {{
        fill: #04111f !important;
        color: #04111f !important;
    }}

    .stNumberInput [data-testid="stWidgetLabel"] + div,
    .stPasswordInput [data-testid="stWidgetLabel"] + div,
    .stTextInput [data-testid="stWidgetLabel"] + div {{
        box-shadow: 0 12px 28px rgba(0,0,0,0.16) !important;
        border-radius: 16px !important;
    }}

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {{
        background: linear-gradient(135deg, rgba(110,231,255,0.18) 0%, rgba(139,92,246,0.18) 100%) !important;
        color: var(--text) !important;
        border: 1px solid rgba(110,231,255,0.22) !important;
        border-radius: 16px !important;
        padding: 0.72rem 1rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18) !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        transform: translateY(-1px);
        border-color: var(--accent) !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.24), 0 0 0 1px rgba(110,231,255,0.12) inset !important;
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    .stDownloadButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #22d3ee 0%, #8b5cf6 100%) !important;
        color: #04111f !important;
        border: 0 !important;
        box-shadow: 0 18px 38px rgba(34,211,238,0.18), 0 10px 24px rgba(139,92,246,0.14) !important;
    }}

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {{
        box-shadow: 0 0 0 3px rgba(110,231,255,0.16) !important;
    }}

    /* Alerts */
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
    [data-testid="stInfo"] {{ background: rgba(34, 211, 238, 0.10) !important; }}
    [data-testid="stWarning"] {{ background: rgba(245, 158, 11, 0.12) !important; }}
    [data-testid="stError"] {{ background: rgba(251, 113, 133, 0.12) !important; }}

    /* Tabs */
    button[role="tab"] {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        color: var(--text2) !important;
        padding: 0.72rem 1rem !important;
        font-weight: 700 !important;
        margin-right: 0.35rem !important;
    }}

    button[role="tab"][aria-selected="true"] {{
        color: var(--text) !important;
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(110,231,255,0.12) 0%, rgba(139,92,246,0.12) 100%) !important;
        box-shadow: 0 10px 22px rgba(0,0,0,0.16) !important;
    }}

    /* Radio / Checkbox */
    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {{
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.4rem 0.65rem;
    }}

    /* Tables / Dataframes */
    .stDataFrame, div[data-testid="stTable"] {{
        background: var(--table-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.20) !important;
    }}

    table {{
        border-collapse: collapse !important;
    }}

    thead tr {{
        background: var(--table-head) !important;
    }}

    tbody tr:nth-child(even) {{
        background: var(--table_row) !important;
    }}

    th, td {{
        border-color: rgba(143,170,214,0.12) !important;
    }}

    /* Expanders */
    details {{
        background: rgba(12, 22, 40, 0.78) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: 0 14px 28px rgba(0,0,0,0.18) !important;
    }}

    details summary {{
        background: rgba(255,255,255,0.02) !important;
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        background: linear-gradient(180deg, rgba(15,29,51,0.90) 0%, rgba(10,20,36,0.95) 100%) !important;
        border: 1px solid var(--border) !important;
        padding: 0.95rem 1rem !important;
        box-shadow: 0 18px 38px rgba(0,0,0,0.20) !important;
        position: relative;
        overflow: hidden;
    }}

    div[data-testid="stMetric"]::after {{
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 3px;
        background: linear-gradient(180deg, rgba(34,211,238,0.95) 0%, rgba(139,92,246,0.95) 100%);
        opacity: 0.9;
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

    /* Progress */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #22d3ee 0%, #8b5cf6 100%) !important;
    }}



    /* Defensive contrast fixes for light-mode browsers / mobile webviews */
    input, textarea, select, button {{
        color: var(--text) !important;
        -webkit-text-fill-color: currentColor !important;
    }}

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill {{
        -webkit-text-fill-color: var(--text) !important;
        -webkit-box-shadow: 0 0 0px 1000px rgba(8,18,32,0.98) inset !important;
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

    /* Extra mobile/browser fixes for select menus */
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
        background: linear-gradient(180deg, rgba(7,17,31,0.96) 0%, rgba(11,23,41,0.96) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }}

    @media (prefers-color-scheme: light) {{
        html, body {{
            color-scheme: dark !important;
        }}
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.04); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(143,170,214,0.30); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(110,231,255,0.40); }}


    /* Premium polish */
    .block-container::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.015), transparent 22%),
            radial-gradient(circle at 20% 20%, rgba(110,231,255,0.06), transparent 18%),
            radial-gradient(circle at 80% 10%, rgba(139,92,246,0.07), transparent 16%);
        mix-blend-mode: screen;
    }}

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {{
        min-height: 46px !important;
    }}

    .stButton > button:active,
    .stFormSubmitButton > button:active {{
        transform: translateY(0) scale(0.99);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.4rem !important;
        margin-bottom: 0.8rem !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background: transparent !important;
    }}

    details summary {{
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
    }}

    details[open] {{
        border-color: var(--hover-border) !important;
        box-shadow: 0 18px 40px rgba(0,0,0,0.22), 0 0 0 1px rgba(110,231,255,0.08) inset !important;
    }}

    div[data-testid="stMetric"]:hover,
    .stForm:hover,
    div[data-testid="stExpander"]:hover {{
        border-color: var(--hover-border) !important;
        box-shadow: 0 20px 42px rgba(0,0,0,0.24) !important;
    }}

    [data-testid="stHorizontalBlock"] > div {{
        gap: 0.9rem !important;
    }}

    .stApp [data-testid="stCaptionContainer"],
    .stApp .stCaption {{
        color: var(--text3) !important;
    }}

    @media (max-width: 768px) {{
        .block-container {{
            padding-top: 1rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}

        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {{
            border-radius: 14px !important;
            padding: 0.78rem 0.95rem !important;
        }}

        button[role="tab"] {{
            padding: 0.68rem 0.85rem !important;
        }}
    }}

    /* ===== Ajustes puntuales sin romper la estética ===== */
    /* Ojo de contraseña: sin círculo/fondo aparte */
    .stPasswordInput button[kind="secondary"],
    .stPasswordInput button[kind="secondary"]:hover,
    .stPasswordInput button[kind="secondary"]:focus,
    .stPasswordInput button[kind="secondary"]:active {{
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    .stPasswordInput button[kind="secondary"] svg {{
        border-radius: 0 !important;
        background: transparent !important;
    }}

    /* + y - del number input: integrados al campo */
    .stNumberInput button,
    .stNumberInput button:hover,
    .stNumberInput button:focus,
    .stNumberInput button:active {{
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* Spinner/status: sin caja blanca ni hueco raro */
    [data-testid="stSpinner"],
    [data-testid="stSpinner"] > div,
    [data-testid="stSpinner"] > div > div,
    [data-testid="stStatusWidget"],
    [data-testid="stStatusWidget"] > div,
    [data-testid="stStatusWidget"] > div > div {{
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }}

    [data-testid="stSpinner"] {{
        margin: 0 0 .25rem 0 !important;
        padding: 0 !important;
    }}

    [data-testid="stSpinner"] p,
    [data-testid="stSpinner"] span,
    [data-testid="stStatusWidget"] p,
    [data-testid="stStatusWidget"] span {{
        margin: 0 !important;
    }}

    </style>
    """, unsafe_allow_html=True)
