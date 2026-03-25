"""
styles.py — Tema claro original con ajustes finos de jerarquía y contraste.
"""
import streamlit as st

LIGHT_THEME = dict(
    bg="#eef5ff",
    bg2="#f6faff",
    bg3="#ffffff",
    text="#10243f",
    text2="#35527d",
    text3="#6683ac",
    border="rgba(57,110,201,0.14)",
    border2="rgba(57,110,201,0.26)",
    hover_border="rgba(47,124,255,0.32)",
    shadow="rgba(34,84,170,0.08)",
    surface2="rgba(47,124,255,0.045)",
    input_bg="#ffffff",
    input_text="#10243f",
    gold="#c89a2b",
    gold2="#e2c16a",
    gold_dim="rgba(200,154,43,0.10)",
    gold_glow="rgba(200,154,43,0.18)",
    gold_border="rgba(200,154,43,0.24)",
    blue="#2f7cff",
    blue2="#7bb4ff",
    blue_dim="rgba(47,124,255,0.10)",
    blue_border="rgba(47,124,255,0.22)",
    cyan="#2aa7d6",
    cyan_dim="rgba(42,167,214,0.10)",
    cyan_border="rgba(42,167,214,0.22)",
    red="#dd5c72",
    red_dim="rgba(221,92,114,0.12)",
    red_border="rgba(221,92,114,0.24)",
    orange="#ee9b3a",
    orange_dim="rgba(238,155,58,0.12)",
    orange_border="rgba(238,155,58,0.24)",
    green="#2cae82",
    green2="#1f8d69",
    green_dim="rgba(44,174,130,0.12)",
    green_border="rgba(44,174,130,0.22)",
    green_glow="rgba(44,174,130,0.18)",
    table_bg="#ffffff",
    table_head="rgba(47,124,255,0.055)",
    table_row="rgba(47,124,255,0.020)",
    scheme="light",
    bg_html="#eef5ff",
)


def get_tema() -> str:
    return "light"


def render_tema_boton():
    return None


def inject_css():
    v = LIGHT_THEME
    st.markdown(f"""
    <style>
    :root {{
        color-scheme: {v['scheme']};
        --bg: {v['bg']};
        --bg2: {v['bg2']};
        --bg3: {v['bg3']};
        --text: {v['text']};
        --text2: {v['text2']};
        --text3: {v['text3']};
        --border: {v['border']};
        --border2: {v['border2']};
        --hover-border: {v['hover_border']};
        --shadow-clr: {v['shadow']};
        --surface: rgba(255,255,255,0.78);
        --surface2: {v['surface2']};
        --input-bg: {v['input_bg']};
        --input-text: {v['input_text']};
        --table-bg: {v['table_bg']};
        --table-head: {v['table_head']};
        --table-row: {v['table_row']};
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
        --radius: 16px;
        --radius-sm: 12px;
        --radius-lg: 22px;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    html, body {{
        background: {v['bg_html']} !important;
        color: var(--text) !important;
    }}

    body {{
        background: linear-gradient(180deg, #f9fbff 0%, #eff5ff 52%, #eaf2ff 100%) !important;
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(circle at top left, rgba(106,168,255,0.14), transparent 25%),
            radial-gradient(circle at top right, rgba(47,124,255,0.06), transparent 26%),
            linear-gradient(180deg, #f9fbff 0%, #eff5ff 52%, #eaf2ff 100%) !important;
        color: var(--text) !important;
    }}

    [data-testid="stHeader"], header, #MainMenu, footer {{
        visibility: hidden !important;
        height: 0 !important;
    }}

    .block-container {{
        max-width: 980px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }}

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small {{
        color: inherit;
    }}

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stText"],
    .stCaption,
    .st-emotion-cache-10trblm,
    .st-emotion-cache-16idsys {{
        color: var(--text) !important;
    }}

    a {{
        color: var(--blue) !important;
        text-decoration: none !important;
    }}

    hr {{ border-color: rgba(47,124,255,0.10) !important; }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea,
    [data-baseweb="select"] > div,
    [data-baseweb="base-input"] > div {{
        background: rgba(255,255,255,0.96) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--border2) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px {v['shadow']} !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.78rem 0.95rem !important;
        font-size: 0.96rem !important;
        caret-color: var(--blue) !important;
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
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(47,124,255,0.12), 0 8px 20px rgba(47,124,255,0.10) !important;
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
    .stCheckbox label {{
        color: var(--text2) !important;
        font-size: 0.74rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }}

    /* Select dropdown / popovers */
    [data-baseweb="popover"],
    [role="listbox"],
    ul[role="listbox"] {{
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid rgba(47,124,255,0.12) !important;
        box-shadow: 0 14px 28px rgba(47,124,255,0.12) !important;
        border-radius: 14px !important;
    }}

    [role="option"] {{
        color: var(--text) !important;
        background: #ffffff !important;
    }}

    [role="option"][aria-selected="true"],
    [role="option"]:hover {{
        background: rgba(47,124,255,0.08) !important;
        color: var(--text) !important;
    }}

    [data-baseweb="select"] input,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {{
        color: var(--text) !important;
    }}

    svg {{ fill: none; }}
    [data-baseweb="select"] svg,
    .stDateInput svg,
    .stDownloadButton svg,
    .stButton svg,
    .stFormSubmitButton svg {{
        color: var(--text2) !important;
        fill: currentColor !important;
    }}

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {{
        border: 0 !important;
        border-radius: 14px !important;
        min-height: 46px !important;
        padding: 0.72rem 1.15rem !important;
        font-weight: 800 !important;
        font-size: 0.94rem !important;
        letter-spacing: 0.2px !important;
        color: #ffffff !important;
        background: linear-gradient(135deg, #2f7cff 0%, #64a6ff 100%) !important;
        box-shadow: 0 10px 24px rgba(47,124,255,0.22) !important;
        cursor: pointer !important;
        transition: transform .16s ease, box-shadow .16s ease, filter .16s ease !important;
    }}

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 14px 28px rgba(47,124,255,0.28) !important;
        filter: saturate(1.05) !important;
    }}

    .stButton > button:active,
    .stFormSubmitButton > button:active,
    .stDownloadButton > button:active {{
        transform: translateY(0) !important;
    }}

    .stButton > button:disabled,
    .stFormSubmitButton > button:disabled,
    .stDownloadButton > button:disabled {{
        opacity: .55 !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
    }}

    .stButton > button[kind="secondary"],
    .stFormSubmitButton > button[kind="secondary"],
    .stDownloadButton > button[kind="secondary"] {{
        background: rgba(255,255,255,0.96) !important;
        color: var(--blue) !important;
        border: 1.5px solid rgba(47,124,255,0.18) !important;
        box-shadow: 0 8px 18px rgba(57,110,201,0.08) !important;
    }}

    /* Forms and containers */
    .stForm {{
        background: rgba(255,255,255,0.74) !important;
        border: 1px solid rgba(47,124,255,0.10) !important;
        border-radius: 22px !important;
        padding: 1.2rem 1.1rem 0.9rem 1.1rem !important;
        box-shadow: 0 18px 40px rgba(47,124,255,0.08) !important;
        backdrop-filter: blur(6px);
    }}

    [data-testid="stExpander"] {{
        background: rgba(255,255,255,0.74) !important;
        border: 1px solid rgba(47,124,255,0.10) !important;
        border-radius: 16px !important;
        box-shadow: 0 14px 30px rgba(47,124,255,0.07) !important;
        overflow: hidden !important;
    }}

    [data-testid="stExpander"] details summary,
    [data-testid="stExpander"] details summary * {{
        background: rgba(47,124,255,0.035) !important;
        color: var(--text) !important;
    }}

    /* Alerts */
    [data-testid="stAlert"] {{
        border-radius: 16px !important;
        border: 1px solid var(--border2) !important;
        box-shadow: 0 10px 24px rgba(47,124,255,0.07) !important;
        background: rgba(255,255,255,0.88) !important;
    }}
    [data-testid="stAlert"] *,
    [data-testid="stAlertContainer"] * {{ color: var(--text) !important; }}

    /* Tabs */
    .stTabs [role="tablist"] {{
        gap: 0.45rem !important;
        padding: 0.2rem !important;
        background: rgba(255,255,255,0.62) !important;
        border: 1px solid rgba(47,124,255,0.10) !important;
        border-radius: 999px !important;
        box-shadow: 0 8px 20px rgba(47,124,255,0.07) !important;
    }}
    .stTabs [role="tab"],
    .stTabs [role="tab"] * {{
        border-radius: 999px !important;
        padding: 0.55rem 1rem !important;
        color: var(--text2) !important;
        font-weight: 700 !important;
        border: none !important;
        background: transparent !important;
    }}
    .stTabs [aria-selected="true"],
    .stTabs [aria-selected="true"] * {{
        background: linear-gradient(135deg, #2f7cff 0%, #6aa8ff 100%) !important;
        color: #fff !important;
        box-shadow: 0 8px 18px rgba(47,124,255,0.20) !important;
    }}

    /* Dataframes / tables */
    .stDataFrame, .stTable {{
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(47,124,255,0.10) !important;
        box-shadow: 0 10px 24px rgba(47,124,255,0.07) !important;
        background: #fff !important;
    }}
    [data-testid="stDataFrameResizable"] *,
    .stTable * {{ color: var(--text) !important; }}

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {{
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(237,245,255,0.96)) !important;
        border: 2px dashed rgba(47,124,255,0.26) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
    }}
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] div,
    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileUploaderDropzone"] section,
    [data-testid="stFileUploaderDropzone"] p {{
        color: var(--text) !important;
        fill: var(--text) !important;
    }}
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] button *,
    .stFileUploader button,
    .stFileUploader button * {{
        color: #ffffff !important;
    }}

    /* Toggle / checkbox / radio */
    .stRadio > div, .stCheckbox, [data-testid="stWidgetLabel"], .stToggle {{
        color: var(--text) !important;
    }}

    /* Spinner */
    [data-testid="stSpinner"] *, [data-testid="stSpinner"] div {{ color: var(--text) !important; }}

    /* Generic cards created by markdown html should feel integrated */
    [data-testid="stMarkdownContainer"] > div[style*="background:"],
    [data-testid="stVerticalBlock"] [style*="background:var(--bg3)"],
    [data-testid="stVerticalBlock"] [style*="background:var(--gold-dim)"],
    [data-testid="stVerticalBlock"] [style*="background:var(--blue-dim)"],
    [data-testid="stVerticalBlock"] [style*="background:var(--green-dim)"] {{
        box-shadow: 0 10px 24px rgba(47,124,255,0.07) !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: rgba(47,124,255,0.04); border-radius: 99px; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(47,124,255,0.22); border-radius: 99px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(47,124,255,0.40); }}
    </style>
    """, unsafe_allow_html=True)
