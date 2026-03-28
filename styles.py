"""
Sistema visual reconstruido desde cero.
"""
import streamlit as st

ULTRA_THEME = {
    "scheme": "dark",
    "bg_html": "#130a2a",
    "bg": "#130a2a",
    "bg2": "#1a0f3d",
    "bg3": "#24135c",
    "surface": "rgba(48, 20, 110, 0.56)",
    "surface_elevated": "rgba(63, 21, 138, 0.70)",
    "surface_soft": "rgba(99, 44, 201, 0.20)",
    "surface2": "rgba(135, 56, 255, 0.18)",
    "text": "#f4dcff",
    "text2": "#e4bbff",
    "text3": "#b682ff",
    "border": "rgba(160, 92, 255, 0.28)",
    "border2": "rgba(61, 234, 255, 0.36)",
    "hover_border": "rgba(255, 118, 224, 0.56)",
    "shadow": "rgba(91, 24, 188, 0.34)",
    "input_bg": "rgba(41, 13, 98, 0.82)",
    "input_text": "#f7deff",
    "table_bg": "rgba(31, 11, 79, 0.82)",
    "table_head": "rgba(59, 238, 255, 0.16)",
    "table_row": "rgba(255, 118, 224, 0.05)",
    "accent": "#3beeff",
    "accent_2": "#ff4fd8",
    "accent_3": "#8cff62",
    "gold": "#ffb438",
    "gold2": "#ffd95f",
    "gold_dim": "rgba(255, 180, 56, 0.16)",
    "gold_glow": "rgba(255, 180, 56, 0.24)",
    "gold_border": "rgba(255, 180, 56, 0.34)",
    "blue": "#3beeff",
    "blue2": "#7cf7ff",
    "blue_dim": "rgba(59, 238, 255, 0.15)",
    "blue_border": "rgba(59, 238, 255, 0.32)",
    "cyan": "#00f0ff",
    "cyan_dim": "rgba(0, 240, 255, 0.14)",
    "cyan_border": "rgba(0, 240, 255, 0.30)",
    "red": "#ff5c9f",
    "red_dim": "rgba(255, 92, 159, 0.16)",
    "red_border": "rgba(255, 92, 159, 0.34)",
    "orange": "#ff8d3b",
    "orange_dim": "rgba(255, 141, 59, 0.16)",
    "orange_border": "rgba(255, 141, 59, 0.34)",
    "green": "#8cff62",
    "green2": "#45ffa2",
    "green_dim": "rgba(140, 255, 98, 0.15)",
    "green_border": "rgba(69, 255, 162, 0.34)",
    "green_glow": "rgba(69, 255, 162, 0.26)",
    "success": "#45ffa2",
    "warning": "#ffb438",
    "danger": "#ff5c9f",
}


def get_tema() -> str:
    return "ultra-neon-remix"


def render_tema_boton():
    return None


def inject_css():
    v = ULTRA_THEME
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Sora:wght@400;600;700;800&family=Bebas+Neue&display=swap');

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
        --radius: 24px;
        --radius-sm: 18px;
        --radius-lg: 34px;
    }}

    html, body, [class*="css"], .stApp, button, input, textarea, select {{
        font-family: 'Space Grotesk', sans-serif !important;
    }}

    h1, h2, h3, h4, .app-title, .display-font {{
        font-family: 'Sora', 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.03em;
    }}

    html, body {{
        background:
            radial-gradient(circle at 8% 12%, rgba(255, 79, 216, 0.24), transparent 18%),
            radial-gradient(circle at 88% 10%, rgba(59, 238, 255, 0.20), transparent 18%),
            radial-gradient(circle at 22% 88%, rgba(140, 255, 98, 0.16), transparent 20%),
            radial-gradient(circle at 82% 80%, rgba(255, 180, 56, 0.12), transparent 24%),
            linear-gradient(135deg, #130a2a 0%, #240f55 34%, #3b1177 62%, #130a2a 100%) !important;
        color: var(--text) !important;
    }}

    body::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(115deg, rgba(255,79,216,0.05), transparent 28%, rgba(59,238,255,0.06) 54%, transparent 78%),
            repeating-linear-gradient(90deg, rgba(255,79,216,0.025) 0 1px, transparent 1px 84px),
            repeating-linear-gradient(0deg, rgba(59,238,255,0.020) 0 1px, transparent 1px 84px);
        mix-blend-mode: screen;
        opacity: 0.85;
        z-index: 0;
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background: transparent !important;
        color: var(--text) !important;
    }}

    [data-testid="stHeader"], header, #MainMenu, footer {{
        visibility: hidden !important;
        height: 0 !important;
    }}

    .block-container {{
        max-width: 1180px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        position: relative;
        z-index: 1;
    }}

    .block-container::before {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 38px;
        background:
            linear-gradient(145deg, rgba(88, 23, 180, 0.26), rgba(17, 189, 255, 0.08) 38%, rgba(255, 79, 216, 0.14) 72%, rgba(140, 255, 98, 0.08));
        filter: blur(0px);
        z-index: -2;
    }}

    .block-container::after {{
        content: "";
        position: absolute;
        inset: 8px;
        border-radius: 30px;
        background: linear-gradient(180deg, rgba(24, 10, 57, 0.56), rgba(35, 12, 87, 0.36));
        border: 1px solid rgba(173, 103, 255, 0.16);
        box-shadow:
            0 30px 80px rgba(78, 18, 181, 0.24),
            0 0 0 1px rgba(59, 238, 255, 0.06) inset,
            0 0 48px rgba(255, 79, 216, 0.10) inset;
        z-index: -1;
        backdrop-filter: blur(14px);
    }}

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small, code {{
        color: inherit;
    }}

    [data-testid="stMarkdownContainer"],
    [data-testid="stText"],
    .stCaption,
    .stMarkdown,
    .st-emotion-cache-10trblm,
    .st-emotion-cache-16idsys p {{
        color: var(--text) !important;
    }}

    a {{
        color: var(--accent) !important;
        text-decoration: none !important;
    }}

    hr, .stDivider {{
        border-color: rgba(188, 105, 255, 0.18) !important;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(35, 12, 87, 0.92), rgba(22, 10, 53, 0.92)) !important;
        border-right: 1px solid rgba(59, 238, 255, 0.12) !important;
    }}

    /* Cards / containers */
    .stForm,
    div[data-testid="stMetric"],
    div[data-testid="stAlert"],
    div[data-testid="stExpander"],
    div[data-testid="stVerticalBlockBorderWrapper"] > div:has(> div[data-testid="stMarkdownContainer"]),
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background:
            linear-gradient(160deg, rgba(56, 18, 128, 0.72) 0%, rgba(34, 10, 84, 0.80) 48%, rgba(20, 67, 138, 0.38) 100%) !important;
        border: 1px solid rgba(173, 103, 255, 0.28) !important;
        border-radius: var(--radius) !important;
        box-shadow:
            0 18px 48px rgba(81, 18, 190, 0.22),
            0 0 0 1px rgba(59, 238, 255, 0.08) inset,
            0 0 36px rgba(255, 79, 216, 0.08) inset !important;
        backdrop-filter: blur(16px);
    }}

    .stForm {{
        padding: 1.1rem 1.1rem 0.85rem 1.1rem !important;
        position: relative;
        overflow: hidden;
    }}

    .stForm::before,
    div[data-testid="stMetric"]::before {{
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(59, 238, 255, 0.9), rgba(255, 79, 216, 0.8), rgba(140, 255, 98, 0.8), transparent);
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
        background: linear-gradient(180deg, rgba(43, 14, 101, 0.92), rgba(31, 10, 76, 0.94)) !important;
        color: var(--input-text) !important;
        border: 1.5px solid rgba(59, 238, 255, 0.22) !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 34px rgba(93, 22, 216, 0.16), 0 0 0 1px rgba(255, 79, 216, 0.10) inset !important;
    }}

    input, textarea {{
        caret-color: var(--accent-2) !important;
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
    .stTextArea textarea:focus,
    textarea:focus,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="base-input"] > div:focus-within {{
        border-color: rgba(255, 79, 216, 0.54) !important;
        box-shadow: 0 0 0 3px rgba(255, 79, 216, 0.13), 0 0 30px rgba(59, 238, 255, 0.12) !important;
    }}

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"] {{
        border-radius: 999px !important;
        border: 1px solid rgba(59, 238, 255, 0.26) !important;
        background:
            linear-gradient(135deg, rgba(255, 79, 216, 0.96) 0%, rgba(138, 70, 255, 0.94) 42%, rgba(59, 238, 255, 0.96) 100%) !important;
        color: #250545 !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
        min-height: 2.95rem !important;
        box-shadow:
            0 16px 34px rgba(255, 79, 216, 0.18),
            0 10px 28px rgba(59, 238, 255, 0.16),
            0 0 0 1px rgba(255, 209, 248, 0.20) inset !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="baseButton-secondary"]:hover,
    [data-testid="baseButton-primary"]:hover {{
        transform: translateY(-2px) scale(1.01) !important;
        filter: saturate(1.12) brightness(1.05) !important;
        box-shadow:
            0 22px 44px rgba(255, 79, 216, 0.24),
            0 16px 34px rgba(59, 238, 255, 0.18),
            0 0 0 1px rgba(255, 222, 250, 0.24) inset !important;
    }}

    .stButton > button:focus,
    .stDownloadButton > button:focus {{
        box-shadow: 0 0 0 3px rgba(59, 238, 255, 0.16), 0 0 0 7px rgba(255, 79, 216, 0.10) !important;
    }}

    .stButton > button[kind="secondary"],
    .stButton > button:has(span:contains("Acerca")) {{
        background: linear-gradient(135deg, rgba(59, 238, 255, 0.20), rgba(255, 79, 216, 0.18)) !important;
    }}

    /* Tabs */
    [data-baseweb="tab-list"] {{
        gap: 0.5rem !important;
        background: rgba(60, 18, 139, 0.32) !important;
        padding: 0.45rem !important;
        border-radius: 999px !important;
        border: 1px solid rgba(173, 103, 255, 0.18) !important;
    }}

    [data-baseweb="tab"] {{
        border-radius: 999px !important;
        color: var(--text2) !important;
        background: transparent !important;
        font-weight: 700 !important;
    }}

    [aria-selected="true"][data-baseweb="tab"] {{
        background: linear-gradient(135deg, rgba(255, 79, 216, 0.95), rgba(59, 238, 255, 0.92)) !important;
        color: #2d094d !important;
        box-shadow: 0 10px 24px rgba(255, 79, 216, 0.18) !important;
    }}

    /* Alerts */
    [data-testid="stSuccess"] {{ background: linear-gradient(135deg, rgba(69,255,162,0.18), rgba(140,255,98,0.12)) !important; }}
    [data-testid="stInfo"] {{ background: linear-gradient(135deg, rgba(59,238,255,0.16), rgba(110,102,255,0.12)) !important; }}
    [data-testid="stWarning"] {{ background: linear-gradient(135deg, rgba(255,180,56,0.18), rgba(255,141,59,0.12)) !important; }}
    [data-testid="stError"] {{ background: linear-gradient(135deg, rgba(255,92,159,0.18), rgba(255,79,216,0.12)) !important; }}

    div[data-testid="stAlert"] {{
        border-radius: 22px !important;
        border-width: 1.5px !important;
    }}

    /* Tables */
    table {{
        border-collapse: separate !important;
        border-spacing: 0 !important;
    }}

    thead tr {{
        background: linear-gradient(90deg, rgba(59,238,255,0.18), rgba(255,79,216,0.16), rgba(255,180,56,0.14)) !important;
    }}

    tbody tr {{
        background: rgba(255, 79, 216, 0.03) !important;
        transition: transform 0.14s ease, background 0.14s ease;
    }}

    tbody tr:nth-child(even) {{
        background: rgba(59, 238, 255, 0.04) !important;
    }}

    tbody tr:hover {{
        background: rgba(140, 255, 98, 0.08) !important;
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        padding: 1rem 1rem 0.85rem 1rem !important;
    }}

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
        color: var(--text3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.16em !important;
        font-size: 0.68rem !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: var(--text) !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 800 !important;
    }}

    /* Selects / radio / checkbox */
    .stRadio > div,
    .stCheckbox,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        color: var(--text) !important;
    }}

    [data-baseweb="tag"] {{
        background: linear-gradient(135deg, rgba(59,238,255,0.16), rgba(255,79,216,0.16)) !important;
        border: 1px solid rgba(59, 238, 255, 0.20) !important;
        color: var(--text) !important;
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, rgba(59,238,255,1), rgba(255,79,216,1), rgba(255,180,56,1)) !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        border-style: dashed !important;
        border-width: 2px !important;
    }}

    iframe {{
        border-radius: 24px !important;
        border: 1px solid rgba(173, 103, 255, 0.18) !important;
        box-shadow: 0 20px 54px rgba(81, 18, 190, 0.20) !important;
    }}

    /* scrollbars */
    ::-webkit-scrollbar {{ width: 12px; height: 12px; }}
    ::-webkit-scrollbar-track {{ background: rgba(64, 18, 144, 0.34); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb {{ background: linear-gradient(180deg, rgba(59,238,255,0.78), rgba(255,79,216,0.78)); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(180deg, rgba(140,255,98,0.84), rgba(255,180,56,0.84)); }}

    /* small helper override for inline blocks */
    [style*="box-shadow:0 18px 36px rgba(0,0,0,0.18)"],
    [style*="box-shadow:0 16px 32px rgba(0,0,0,0.16)"],
    [style*="box-shadow:0 10px 24px rgba(0,0,0,0.12)"],
    [style*="box-shadow:0 18px 36px rgba(0,0,0,0.16)"] {{
        box-shadow:
            0 18px 42px rgba(97, 22, 226, 0.22),
            0 0 0 1px rgba(59, 238, 255, 0.08) inset !important;
    }}

    [style*="background:var(--bg3)"] {{
        background: linear-gradient(160deg, rgba(70, 21, 153, 0.64), rgba(37, 12, 87, 0.76)) !important;
    }}

    [style*="background:var(--surface)"] {{
        background: linear-gradient(160deg, rgba(60, 18, 139, 0.50), rgba(37, 12, 87, 0.54)) !important;
    }}

    [style*="background:var(--table-bg)"] {{
        background: linear-gradient(180deg, rgba(36, 12, 89, 0.90), rgba(26, 10, 66, 0.94)) !important;
    }}

    .st-emotion-cache-1kyxreq, .st-emotion-cache-ocqkz7 {{
        gap: 1rem !important;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )
