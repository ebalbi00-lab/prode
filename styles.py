"""
styles.py — Tema visual premium máximo para Prode Il Baigo.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg_html="#05101e",
    bg="#05101e",
    bg2="#091628",
    bg3="#0d1d35",
    surface="rgba(10, 20, 38, 0.82)",
    surface_elevated="rgba(14, 26, 48, 0.95)",
    surface_soft="rgba(110, 140, 190, 0.07)",
    surface2="rgba(110, 140, 190, 0.11)",
    text="#f0f5fc",
    text2="#b8cce0",
    text3="#7a97bb",
    border="rgba(130, 165, 220, 0.16)",
    border2="rgba(130, 165, 220, 0.26)",
    hover_border="rgba(100, 220, 255, 0.45)",
    shadow="rgba(1, 6, 18, 0.52)",
    input_bg="rgba(7, 16, 30, 0.97)",
    input_text="#f0f5fc",
    table_bg="rgba(7, 16, 30, 0.96)",
    table_head="rgba(100, 220, 255, 0.09)",
    table_row="rgba(255, 255, 255, 0.018)",
    accent="#5ee8ff",
    accent_2="#9b6df5",
    accent_3="#1fd47a",
    gold="#f7cc6a",
    gold2="#ffe09a",
    gold_dim="rgba(247, 204, 106, 0.11)",
    gold_glow="rgba(247, 204, 106, 0.20)",
    gold_border="rgba(247, 204, 106, 0.30)",
    blue="#5ee8ff",
    blue2="#b8f0ff",
    blue_dim="rgba(94, 232, 255, 0.11)",
    blue_border="rgba(94, 232, 255, 0.26)",
    cyan="#1af0cc",
    cyan_dim="rgba(26, 240, 204, 0.11)",
    cyan_border="rgba(26, 240, 204, 0.24)",
    red="#ff6b85",
    red_dim="rgba(255, 107, 133, 0.11)",
    red_border="rgba(255, 107, 133, 0.26)",
    orange="#ff9a4a",
    orange_dim="rgba(255, 154, 74, 0.13)",
    orange_border="rgba(255, 154, 74, 0.26)",
    green="#2ef890",
    green2="#0fca72",
    green_dim="rgba(46, 248, 144, 0.12)",
    green_border="rgba(46, 248, 144, 0.26)",
    green_glow="rgba(46, 248, 144, 0.18)",
    success="#2ef890",
    warning="#f5a623",
    danger="#ff6b85",
)


def get_tema() -> str:
    return "premium-dark"


def render_tema_boton():
    return None


def inject_css():
    v = PREMIUM_THEME
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

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
        --radius: 20px;
        --radius-sm: 14px;
        --radius-lg: 28px;
        --font-display: 'Bebas Neue', sans-serif;
        --font-body: 'Outfit', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }}

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    html, body {{
        background: {v['bg_html']} !important;
        color: var(--text) !important;
    }}

    body {{
        background:
            radial-gradient(ellipse 80% 60% at -10% -5%, rgba(94,232,255,0.14) 0%, transparent 55%),
            radial-gradient(ellipse 60% 50% at 110% -5%, rgba(155,109,245,0.18) 0%, transparent 50%),
            radial-gradient(ellipse 50% 40% at 50% 105%, rgba(46,248,144,0.09) 0%, transparent 55%),
            radial-gradient(ellipse 30% 25% at 90% 60%, rgba(247,204,106,0.06) 0%, transparent 45%),
            linear-gradient(170deg, #05101e 0%, #081525 35%, #070e1c 70%, #050e1a 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(ellipse 80% 60% at -10% -5%, rgba(94,232,255,0.13) 0%, transparent 55%),
            radial-gradient(ellipse 60% 50% at 110% -5%, rgba(155,109,245,0.16) 0%, transparent 50%),
            radial-gradient(ellipse 50% 40% at 50% 105%, rgba(46,248,144,0.08) 0%, transparent 55%),
            linear-gradient(170deg, #05101e 0%, #081525 35%, #070e1c 70%, #050e1a 100%) !important;
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
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
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
        transition: color 0.18s ease;
    }}
    a:hover {{ color: var(--blue2) !important; }}

    hr {{
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(130,165,220,0.22) 20%, rgba(94,232,255,0.18) 50%, rgba(130,165,220,0.22) 80%, transparent) !important;
        margin: 1.2rem 0 !important;
    }}

    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stExpander"],
    .stForm,
    div[data-testid="stMetric"] {{
        border-radius: var(--radius) !important;
    }}

    .stForm {{
        background: linear-gradient(160deg,
            rgba(14,27,50,0.92) 0%,
            rgba(9,18,34,0.95) 100%) !important;
        border: 1px solid rgba(130,165,220,0.18) !important;
        box-shadow:
            0 24px 60px rgba(1,6,18,0.52),
            0 0 0 1px rgba(255,255,255,0.03) inset,
            0 1px 0 rgba(255,255,255,0.06) inset !important;
        padding: 1.2rem 1.1rem 0.9rem 1.1rem !important;
        backdrop-filter: blur(18px) !important;
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
        background: linear-gradient(180deg,
            rgba(6,14,28,0.98) 0%,
            rgba(9,19,36,0.98) 100%) !important;
        color: var(--input-text) !important;
        border: 1.5px solid rgba(130,165,220,0.22) !important;
        border-radius: 16px !important;
        box-shadow:
            0 8px 24px rgba(0,0,0,0.22),
            0 0 0 1px rgba(255,255,255,0.02) inset !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.85rem 1rem !important;
        font-size: 0.97rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        caret-color: var(--accent) !important;
        letter-spacing: 0.1px !important;
    }}

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder,
    .stTextArea textarea::placeholder,
    textarea::placeholder {{
        color: var(--text3) !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }}

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus,
    .stTextArea textarea:focus,
    textarea:focus,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="base-input"] > div:focus-within {{
        border-color: rgba(94,232,255,0.55) !important;
        box-shadow:
            0 0 0 3px rgba(94,232,255,0.10),
            0 8px 28px rgba(94,232,255,0.08),
            0 0 0 1px rgba(255,255,255,0.03) inset !important;
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
        font-size: 0.70rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1.4px !important;
    }}

    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {{
        background: linear-gradient(180deg, rgba(6,14,28,0.98) 0%, rgba(9,19,36,0.98) 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [data-baseweb="select"] svg,
    [data-baseweb="popover"] svg,
    [role="listbox"] svg {{
        fill: var(--text3) !important;
        color: var(--text3) !important;
    }}

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"] {{
        background: rgba(8, 16, 32, 0.98) !important;
        color: var(--text) !important;
        border: 1px solid rgba(130,165,220,0.22) !important;
        box-shadow:
            0 24px 56px rgba(1,6,18,0.48),
            0 0 0 1px rgba(255,255,255,0.03) inset !important;
        border-radius: 18px !important;
        backdrop-filter: blur(20px) !important;
    }}

    [role="option"],
    li[role="option"],
    div[role="option"] {{
        background: transparent !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        transition: background 0.14s ease !important;
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
        background: rgba(94,232,255,0.12) !important;
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
    .stDownloadButton > button {{
        background: linear-gradient(135deg,
            rgba(94,232,255,0.13) 0%,
            rgba(155,109,245,0.13) 100%) !important;
        color: var(--text) !important;
        border: 1px solid rgba(94,232,255,0.20) !important;
        border-radius: 16px !important;
        padding: 0.75rem 1.1rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.3px !important;
        box-shadow:
            0 10px 28px rgba(0,0,0,0.22),
            0 1px 0 rgba(255,255,255,0.05) inset !important;
        transition: all 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        transform: translateY(-2px) scale(1.01) !important;
        border-color: rgba(94,232,255,0.45) !important;
        box-shadow:
            0 18px 40px rgba(0,0,0,0.28),
            0 0 20px rgba(94,232,255,0.10),
            0 1px 0 rgba(255,255,255,0.07) inset !important;
    }}

    .stButton > button:active,
    .stDownloadButton > button:active {{
        transform: translateY(0px) scale(0.99) !important;
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    .stDownloadButton > button[kind="primary"] {{
        background: linear-gradient(135deg,
            #1de8cc 0%,
            #5ee8ff 40%,
            #9b6df5 100%) !important;
        color: #030d1a !important;
        -webkit-text-fill-color: #030d1a !important;
        border: 0 !important;
        font-weight: 900 !important;
        letter-spacing: 0.4px !important;
        box-shadow:
            0 20px 44px rgba(30,232,204,0.18),
            0 10px 26px rgba(155,109,245,0.16),
            0 1px 0 rgba(255,255,255,0.20) inset !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {{
        transform: translateY(-2px) scale(1.015) !important;
        box-shadow:
            0 26px 52px rgba(30,232,204,0.24),
            0 12px 32px rgba(155,109,245,0.20),
            0 1px 0 rgba(255,255,255,0.22) inset !important;
    }}

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {{
        box-shadow: 0 0 0 3px rgba(94,232,255,0.20) !important;
    }}

    [data-testid="stSuccess"],
    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stError"] {{
        border-radius: 18px !important;
        border: 1px solid var(--border) !important;
        box-shadow:
            0 14px 32px rgba(0,0,0,0.22),
            0 1px 0 rgba(255,255,255,0.04) inset !important;
        backdrop-filter: blur(12px) !important;
    }}

    [data-testid="stSuccess"] {{ background: rgba(15, 202, 114, 0.10) !important; border-color: rgba(46,248,144,0.22) !important; }}
    [data-testid="stInfo"] {{    background: rgba(94, 232, 255, 0.09) !important; border-color: rgba(94,232,255,0.22) !important; }}
    [data-testid="stWarning"] {{ background: rgba(245, 166, 35, 0.10) !important; border-color: rgba(247,204,106,0.22) !important; }}
    [data-testid="stError"] {{   background: rgba(255, 107, 133, 0.10) !important; border-color: rgba(255,107,133,0.22) !important; }}

    button[role="tab"] {{
        background: rgba(255,255,255,0.025) !important;
        border: 1px solid rgba(130,165,220,0.15) !important;
        border-radius: 14px !important;
        color: var(--text3) !important;
        padding: 0.72rem 1.05rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        margin-right: 0.35rem !important;
        transition: all 0.2s ease !important;
    }}

    button[role="tab"]:hover {{
        background: rgba(94,232,255,0.07) !important;
        border-color: rgba(94,232,255,0.25) !important;
        color: var(--text2) !important;
    }}

    button[role="tab"][aria-selected="true"] {{
        color: var(--text) !important;
        border-color: rgba(94,232,255,0.40) !important;
        background: linear-gradient(135deg,
            rgba(94,232,255,0.12) 0%,
            rgba(155,109,245,0.10) 100%) !important;
        box-shadow:
            0 8px 20px rgba(0,0,0,0.18),
            0 0 14px rgba(94,232,255,0.08) !important;
    }}

    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {{
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(130,165,220,0.15);
        border-radius: 14px;
        padding: 0.45rem 0.75rem;
        transition: all 0.18s ease;
    }}

    .stRadio [role="radiogroup"] > label:hover,
    .stCheckbox > label:hover {{
        border-color: rgba(94,232,255,0.30);
        background: rgba(94,232,255,0.06);
    }}

    .stDataFrame, div[data-testid="stTable"] {{
        background: var(--table-bg) !important;
        border: 1px solid rgba(130,165,220,0.16) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow:
            0 20px 44px rgba(0,0,0,0.26),
            0 1px 0 rgba(255,255,255,0.04) inset !important;
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
        border-color: rgba(130,165,220,0.10) !important;
    }}

    details {{
        background: linear-gradient(160deg,
            rgba(12,22,42,0.82) 0%,
            rgba(8,16,30,0.88) 100%) !important;
        border: 1px solid rgba(130,165,220,0.16) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow:
            0 16px 36px rgba(0,0,0,0.22),
            0 1px 0 rgba(255,255,255,0.04) inset !important;
        backdrop-filter: blur(12px) !important;
        transition: border-color 0.2s ease !important;
    }}

    details:hover {{
        border-color: rgba(94,232,255,0.22) !important;
    }}

    details[open] {{
        border-color: rgba(94,232,255,0.28) !important;
    }}

    details summary {{
        background: rgba(255,255,255,0.02) !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
    }}

    div[data-testid="stMetric"] {{
        background: linear-gradient(160deg,
            rgba(14,27,52,0.90) 0%,
            rgba(9,18,34,0.94) 100%) !important;
        border: 1px solid rgba(130,165,220,0.18) !important;
        padding: 1rem 1.1rem !important;
        box-shadow:
            0 18px 40px rgba(0,0,0,0.24),
            0 1px 0 rgba(255,255,255,0.05) inset !important;
        backdrop-filter: blur(14px) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-1px) !important;
        box-shadow:
            0 22px 48px rgba(0,0,0,0.28),
            0 0 18px rgba(94,232,255,0.06),
            0 1px 0 rgba(255,255,255,0.06) inset !important;
    }}

    div[data-testid="stMetric"] label {{
        color: var(--text3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-size: 0.67rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: var(--text) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
    }}

    div[data-testid="stMetricDelta"] {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg,
            #1de8cc 0%,
            #5ee8ff 50%,
            #9b6df5 100%) !important;
        border-radius: 999px !important;
        box-shadow: 0 0 12px rgba(94,232,255,0.30) !important;
    }}

    .stProgress > div > div > div {{
        background: rgba(130,165,220,0.12) !important;
        border-radius: 999px !important;
    }}

    .stNumberInput [data-testid="stNumberInputStepUp"],
    .stNumberInput [data-testid="stNumberInputStepDown"] {{
        background: rgba(94,232,255,0.10) !important;
        border-color: rgba(94,232,255,0.22) !important;
        color: var(--accent) !important;
        transition: all 0.18s ease !important;
        border-radius: 10px !important;
    }}

    .stNumberInput [data-testid="stNumberInputStepUp"]:hover,
    .stNumberInput [data-testid="stNumberInputStepDown"]:hover {{
        background: rgba(94,232,255,0.20) !important;
        border-color: rgba(94,232,255,0.40) !important;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg,
            rgba(5,16,30,0.97) 0%,
            rgba(9,22,42,0.97) 100%) !important;
        border-right: 1px solid rgba(130,165,220,0.14) !important;
        backdrop-filter: blur(20px) !important;
    }}

    .stCaption, [data-testid="stCaptionContainer"] {{
        color: var(--text3) !important;
        font-size: 0.80rem !important;
        font-family: 'Outfit', sans-serif !important;
    }}

    [data-testid="column"] {{
        padding: 0 0.35rem !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        border: 2px dashed rgba(130,165,220,0.22) !important;
        border-radius: 18px !important;
        transition: border-color 0.2s ease, background 0.2s ease !important;
    }}
    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: rgba(94,232,255,0.40) !important;
        background: rgba(94,232,255,0.04) !important;
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
        -webkit-box-shadow: 0 0 0px 1000px rgba(6,14,28,0.98) inset !important;
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

    .stFormSubmitButton > button p,
    .stButton > button[kind="primary"] p {{
        color: #030d1a !important;
        -webkit-text-fill-color: #030d1a !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stMultiSelect"] [data-baseweb="select"] * {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    select, option, optgroup {{
        background-color: #080f1e !important;
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
        background: linear-gradient(180deg, rgba(5,16,30,0.97) 0%, rgba(9,22,42,0.97) 100%) !important;
        border-right: 1px solid rgba(130,165,220,0.14) !important;
    }}

    @media (prefers-color-scheme: light) {{
        html, body {{
            color-scheme: dark !important;
        }}
    }}

    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.03); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, rgba(94,232,255,0.35), rgba(155,109,245,0.30));
        border-radius: 999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, rgba(94,232,255,0.55), rgba(155,109,245,0.48));
    }}

    [data-testid="stDivider"] hr {{
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(94,232,255,0.15) 20%,
            rgba(155,109,245,0.12) 50%,
            rgba(94,232,255,0.15) 80%,
            transparent 100%) !important;
        height: 1px !important;
        border: none !important;
    }}

    [data-testid="toastContainer"] > div {{
        background: rgba(10,20,38,0.96) !important;
        border: 1px solid rgba(94,232,255,0.24) !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.38) !important;
        backdrop-filter: blur(20px) !important;
        color: var(--text) !important;
    }}

    </style>
    """, unsafe_allow_html=True)
