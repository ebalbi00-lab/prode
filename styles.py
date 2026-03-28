"""
styles.py — Rediseño visual integral de la app.
Mantiene la lógica intacta y rehace completamente la interfaz.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="light",
    bg_html="#f4f1ea",
    bg="#f8f5ef",
    bg2="#f2eee7",
    bg3="#ffffff",
    surface="rgba(255, 255, 255, 0.82)",
    surface_elevated="rgba(255, 255, 255, 0.96)",
    surface_soft="rgba(120, 113, 108, 0.06)",
    surface2="rgba(120, 113, 108, 0.10)",
    text="#191616",
    text2="#4b4645",
    text3="#7a7370",
    border="rgba(38, 28, 20, 0.10)",
    border2="rgba(38, 28, 20, 0.16)",
    hover_border="rgba(143, 98, 54, 0.34)",
    shadow="rgba(42, 26, 12, 0.10)",
    input_bg="#fffdf8",
    input_text="#191616",
    table_bg="#fffdfa",
    table_head="rgba(196, 167, 122, 0.16)",
    table_row="rgba(97, 84, 71, 0.03)",
    accent="#8f6236",
    accent_2="#b78a57",
    accent_3="#3e6b66",
    gold="#b78a57",
    gold2="#d3ae7d",
    gold_dim="rgba(183, 138, 87, 0.12)",
    gold_glow="rgba(183, 138, 87, 0.16)",
    gold_border="rgba(183, 138, 87, 0.28)",
    blue="#56748f",
    blue2="#8ba4ba",
    blue_dim="rgba(86, 116, 143, 0.12)",
    blue_border="rgba(86, 116, 143, 0.24)",
    cyan="#3e6b66",
    cyan_dim="rgba(62, 107, 102, 0.12)",
    cyan_border="rgba(62, 107, 102, 0.24)",
    red="#b04c4c",
    red_dim="rgba(176, 76, 76, 0.10)",
    red_border="rgba(176, 76, 76, 0.24)",
    orange="#c17a34",
    orange_dim="rgba(193, 122, 52, 0.12)",
    orange_border="rgba(193, 122, 52, 0.24)",
    green="#2f7a58",
    green2="#3e8f6b",
    green_dim="rgba(47, 122, 88, 0.12)",
    green_border="rgba(47, 122, 88, 0.24)",
    green_glow="rgba(47, 122, 88, 0.16)",
    success="#2f7a58",
    warning="#b6722b",
    danger="#b04c4c",
)


def get_tema() -> str:
    return "atelier-editorial"


def render_tema_boton():
    return None


def inject_css():
    v = PREMIUM_THEME
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

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
        --radius: 26px;
        --radius-sm: 18px;
        --radius-lg: 34px;
        --panel-bg: linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(255,251,245,0.98) 100%);
        --panel-stroke: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(92,72,52,0.10) 100%);
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
            radial-gradient(circle at top left, rgba(183,138,87,0.16), transparent 23%),
            radial-gradient(circle at top right, rgba(86,116,143,0.12), transparent 20%),
            radial-gradient(circle at bottom center, rgba(62,107,102,0.10), transparent 24%),
            linear-gradient(180deg, #f6f2ea 0%, #f8f5ef 48%, #f2ede6 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(circle at 0% 0%, rgba(183,138,87,0.12), transparent 18%),
            radial-gradient(circle at 100% 10%, rgba(86,116,143,0.10), transparent 22%),
            radial-gradient(circle at 50% 100%, rgba(62,107,102,0.08), transparent 24%),
            linear-gradient(180deg, #f7f3ec 0%, #f8f5ef 42%, #f1ece4 100%) !important;
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
        max-width: 1240px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
    }}

    .block-container > div {{
        position: relative;
        z-index: 1;
    }}

    .block-container::before {{
        content: "";
        position: fixed;
        inset: 18px 18px auto 18px;
        height: 86px;
        border-radius: 28px;
        background: linear-gradient(180deg, rgba(255,255,255,0.86), rgba(255,255,255,0.58));
        border: 1px solid rgba(49,36,22,0.08);
        box-shadow: 0 12px 34px rgba(42,26,12,0.08);
        backdrop-filter: blur(20px);
        pointer-events: none;
        z-index: 0;
        opacity: 0.88;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Manrope', 'Inter', sans-serif !important;
        letter-spacing: -0.04em;
        color: var(--text) !important;
    }}

    /* Convierte títulos viejos tipo "Bebas" a un look editorial moderno */
    [style*="font-family:Bebas Neue"],
    [style*="font-family: Bebas Neue"],
    [style*="letter-spacing:3px"],
    [style*="letter-spacing: 3px"],
    [style*="text-transform:uppercase"],
    [style*="text-transform: uppercase"] {{
        font-family: 'Manrope', 'Inter', sans-serif !important;
        letter-spacing: -0.03em !important;
        text-transform: none !important;
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
        border-color: rgba(38,28,20,0.10) !important;
    }}

    [data-testid="stHorizontalBlock"] > div {{
        gap: 1rem !important;
    }}

    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stExpander"],
    .stForm,
    div[data-testid="stMetric"],
    div[style*="background:var(--bg3)"],
    div[style*="background: var(--bg3)"],
    div[style*="background:var(--blue-dim)"],
    div[style*="background: var(--blue-dim)"],
    div[style*="background:var(--gold-dim)"],
    div[style*="background: var(--gold-dim)"] {{
        border-radius: var(--radius) !important;
    }}

    .stForm,
    div[data-testid="stMetric"],
    details,
    .stDataFrame,
    div[data-testid="stTable"],
    div[style*="background:var(--bg3);border:1px solid var(--border)"],
    div[style*="background: var(--bg3); border:1px solid var(--border)"],
    div[style*="background:var(--bg3); border:1px solid var(--border)"],
    div[style*="background:var(--blue-dim); border:1.5px solid var(--blue-border)"],
    div[style*="background:var(--gold-dim);border:1.5px solid var(--gold-border)"] {{
        background: var(--panel-bg) !important;
        border: 1px solid rgba(55, 40, 24, 0.10) !important;
        box-shadow: 0 18px 42px var(--shadow-clr) !important;
        backdrop-filter: blur(16px);
    }}

    .stForm {{
        padding: 1.2rem 1.2rem 0.8rem 1.2rem !important;
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
        background: linear-gradient(180deg, #fffdfa 0%, #fcf8f1 100%) !important;
        color: var(--input-text) !important;
        border: 1px solid rgba(55,40,24,0.10) !important;
        border-radius: 18px !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.95), 0 8px 22px rgba(40,26,12,0.04) !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.92rem 1rem !important;
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
        border-color: rgba(143,98,54,0.45) !important;
        box-shadow: 0 0 0 4px rgba(183,138,87,0.10), 0 10px 28px rgba(143,98,54,0.10) !important;
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
        letter-spacing: 1.2px !important;
    }}

    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {{
        background: linear-gradient(180deg, #fffdfa 0%, #fcf8f1 100%) !important;
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
        background: rgba(255, 252, 246, 0.98) !important;
        color: var(--text) !important;
        border: 1px solid rgba(55,40,24,0.12) !important;
        box-shadow: 0 18px 36px rgba(40,26,12,0.08) !important;
        border-radius: 18px !important;
        backdrop-filter: blur(16px);
    }}

    [role="option"],
    li[role="option"],
    div[role="option"] {{
        background: rgba(255,252,246,0.98) !important;
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
        background: rgba(183,138,87,0.12) !important;
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
        min-height: 48px !important;
        border-radius: 999px !important;
        font-weight: 800 !important;
        letter-spacing: 0 !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 10px 24px rgba(40,26,12,0.06) !important;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,243,234,0.95) 100%) !important;
        color: var(--text) !important;
        border: 1px solid rgba(55,40,24,0.10) !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {{
        transform: translateY(-1px);
        border-color: rgba(143,98,54,0.32) !important;
        box-shadow: 0 16px 32px rgba(40,26,12,0.10) !important;
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    .stDownloadButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #8f6236 0%, #b78a57 55%, #3e6b66 100%) !important;
        color: #fffdf9 !important;
        border: 0 !important;
        box-shadow: 0 18px 34px rgba(143,98,54,0.16) !important;
    }}

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {{
        box-shadow: 0 0 0 4px rgba(183,138,87,0.12) !important;
    }}

    [data-testid="stSuccess"],
    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stError"] {{
        border-radius: 20px !important;
        border: 1px solid rgba(55,40,24,0.10) !important;
        box-shadow: 0 12px 26px rgba(40,26,12,0.06) !important;
        backdrop-filter: blur(10px);
    }}

    [data-testid="stSuccess"] {{ background: rgba(47, 122, 88, 0.10) !important; }}
    [data-testid="stInfo"] {{ background: rgba(86, 116, 143, 0.10) !important; }}
    [data-testid="stWarning"] {{ background: rgba(193, 122, 52, 0.10) !important; }}
    [data-testid="stError"] {{ background: rgba(176, 76, 76, 0.10) !important; }}

    button[role="tab"] {{
        background: rgba(255,255,255,0.75) !important;
        border: 1px solid rgba(55,40,24,0.08) !important;
        border-radius: 999px !important;
        color: var(--text2) !important;
        padding: 0.82rem 1.1rem !important;
        font-weight: 700 !important;
        margin-right: 0.45rem !important;
        box-shadow: 0 8px 20px rgba(40,26,12,0.04) !important;
    }}

    button[role="tab"][aria-selected="true"] {{
        color: #fffdf9 !important;
        border-color: transparent !important;
        background: linear-gradient(135deg, #8f6236 0%, #b78a57 55%, #3e6b66 100%) !important;
        box-shadow: 0 12px 28px rgba(143,98,54,0.16) !important;
    }}

    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {{
        background: rgba(255,255,255,0.66);
        border: 1px solid rgba(55,40,24,0.08);
        border-radius: 16px;
        padding: 0.45rem 0.7rem;
    }}

    .stDataFrame, div[data-testid="stTable"] {{
        border-radius: 22px !important;
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
        border-color: rgba(55,40,24,0.08) !important;
    }}

    details {{
        border-radius: 20px !important;
        overflow: hidden !important;
    }}

    details summary {{
        background: rgba(255,255,255,0.58) !important;
    }}

    div[data-testid="stMetric"] {{
        padding: 1rem 1.05rem !important;
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
        background: linear-gradient(90deg, #8f6236 0%, #b78a57 60%, #3e6b66 100%) !important;
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
        -webkit-box-shadow: 0 0 0px 1000px #fffdfa inset !important;
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
        background-color: #fffdfa !important;
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
        background: linear-gradient(180deg, rgba(255,250,243,0.94) 0%, rgba(247,241,231,0.94) 100%) !important;
        border-right: 1px solid rgba(55,40,24,0.08) !important;
        box-shadow: inset -1px 0 0 rgba(255,255,255,0.60) !important;
    }}

    [data-testid="stDivider"] {{
        margin: 1rem 0 !important;
    }}

    /* Retoca bloques HTML heredados para que no se sigan viendo como la versión anterior */
    div[style*="border-radius:10px"],
    div[style*="border-radius:12px"],
    div[style*="border-radius:14px"],
    div[style*="border-radius:16px"] {{
        border-radius: 22px !important;
    }}

    div[style*="font-size:0.6rem;color:var(--text3);text-transform:uppercase"],
    div[style*="font-size:0.7rem; font-weight:700; text-transform:uppercase"],
    div[style*="font-size:0.72rem; font-weight:700; text-transform:uppercase"] {{
        color: var(--text3) !important;
        opacity: 0.95;
        letter-spacing: 1.3px !important;
    }}

    @media (max-width: 900px) {{
        .block-container {{
            padding-top: 0.85rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        .block-container::before {{
            inset: 12px 12px auto 12px;
            height: 74px;
            border-radius: 24px;
        }}

        .stForm {{
            padding: 0.95rem 0.95rem 0.7rem 0.95rem !important;
        }}
    }}

    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: rgba(80,58,38,0.05); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(143,98,54,0.26); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(143,98,54,0.40); }}
    </style>
    """,
        unsafe_allow_html=True,
    )
