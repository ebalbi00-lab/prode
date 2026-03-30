"""
styles.py — Rediseño integral del tema visual.
"""
import streamlit as st

APP_THEME = dict(
    scheme="dark",
    bg_html="#060b08",
    bg="#08110d",
    bg2="#0d1813",
    bg3="#132119",
    surface="rgba(12, 20, 16, 0.86)",
    surface_elevated="rgba(18, 29, 23, 0.94)",
    surface_soft="rgba(126, 255, 194, 0.06)",
    surface2="rgba(255, 255, 255, 0.05)",
    text="#f5fbf7",
    text2="#d9e7de",
    text3="#90a99a",
    border="rgba(160, 191, 173, 0.14)",
    border2="rgba(160, 191, 173, 0.24)",
    hover_border="rgba(121, 255, 183, 0.44)",
    shadow="rgba(0, 0, 0, 0.42)",
    input_bg="rgba(10, 18, 14, 0.98)",
    input_text="#f4fbf7",
    table_bg="rgba(9, 16, 13, 0.98)",
    table_head="rgba(121, 255, 183, 0.10)",
    table_row="rgba(255,255,255,0.02)",
    accent="#79ffb7",
    accent_2="#d1ff5f",
    accent_3="#22c55e",
    gold="#f7d775",
    gold2="#fff0b8",
    gold_dim="rgba(247, 215, 117, 0.12)",
    gold_glow="rgba(247, 215, 117, 0.20)",
    gold_border="rgba(247, 215, 117, 0.30)",
    blue="#79ffb7",
    blue2="#d8ffe8",
    blue_dim="rgba(121,255,183,0.12)",
    blue_border="rgba(121,255,183,0.26)",
    cyan="#7cf7d4",
    cyan_dim="rgba(124,247,212,0.12)",
    cyan_border="rgba(124,247,212,0.24)",
    red="#ff7e8b",
    red_dim="rgba(255,126,139,0.12)",
    red_border="rgba(255,126,139,0.26)",
    orange="#ffb86b",
    orange_dim="rgba(255,184,107,0.14)",
    orange_border="rgba(255,184,107,0.28)",
    green="#79ffb7",
    green2="#43d67f",
    green_dim="rgba(121,255,183,0.14)",
    green_border="rgba(121,255,183,0.26)",
    green_glow="rgba(121,255,183,0.18)",
    success="#79ffb7",
    warning="#ffcf64",
    danger="#ff7e8b",
)


def get_tema() -> str:
    return "arena-2026"


def render_tema_boton():
    return None


def inject_css():
    v = APP_THEME
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Bebas+Neue&display=swap');

    :root {
        color-scheme: __scheme__;
        --bg: __bg__;
        --bg2: __bg2__;
        --bg3: __bg3__;
        --surface: __surface__;
        --surface-elevated: __surface_elevated__;
        --surface-soft: __surface_soft__;
        --surface2: __surface2__;
        --text: __text__;
        --text2: __text2__;
        --text3: __text3__;
        --border: __border__;
        --border2: __border2__;
        --hover-border: __hover_border__;
        --shadow-clr: __shadow__;
        --input-bg: __input_bg__;
        --input-text: __input_text__;
        --table-bg: __table_bg__;
        --table-head: __table_head__;
        --table-row: __table_row__;
        --accent: __accent__;
        --accent-2: __accent_2__;
        --accent-3: __accent_3__;
        --gold: __gold__;
        --gold2: __gold2__;
        --gold-dim: __gold_dim__;
        --gold-glow: __gold_glow__;
        --gold-border: __gold_border__;
        --blue: __blue__;
        --blue2: __blue2__;
        --blue-dim: __blue_dim__;
        --blue-border: __blue_border__;
        --cyan: __cyan__;
        --cyan-dim: __cyan_dim__;
        --cyan-border: __cyan_border__;
        --red: __red__;
        --red-dim: __red_dim__;
        --red-border: __red_border__;
        --orange: __orange__;
        --orange-dim: __orange_dim__;
        --orange-border: __orange_border__;
        --green: __green__;
        --green2: __green2__;
        --green-dim: __green_dim__;
        --green-border: __green_border__;
        --green-glow: __green_glow__;
        --success: __success__;
        --warning: __warning__;
        --danger: __danger__;
        --radius: 26px;
        --radius-sm: 18px;
        --radius-lg: 34px;
        --maxw: 1180px;
    }

    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }

    html, body {
        background: __bg_html__ !important;
        color: var(--text) !important;
    }

    body {
        background:
            radial-gradient(circle at 12% 12%, rgba(121,255,183,0.14), transparent 24%),
            radial-gradient(circle at 88% 10%, rgba(247,215,117,0.12), transparent 22%),
            radial-gradient(circle at 50% 100%, rgba(255,255,255,0.04), transparent 34%),
            linear-gradient(180deg, #060b08 0%, #09110d 42%, #0b120e 100%) !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.015), transparent 22%),
            radial-gradient(circle at 0% 0%, rgba(121,255,183,0.12), transparent 22%),
            radial-gradient(circle at 100% 0%, rgba(247,215,117,0.10), transparent 20%),
            linear-gradient(180deg, #060b08 0%, #0a120e 46%, #0d1611 100%) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"], header, #MainMenu, footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(180deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 32px 32px;
        mask-image: linear-gradient(180deg, rgba(0,0,0,0.18), transparent 70%);
        opacity: .22;
        z-index: 0;
    }

    .block-container {
        max-width: var(--maxw) !important;
        padding-top: 1.2rem !important;
        padding-bottom: 3.4rem !important;
    }

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small, code { color: inherit; }
    a { color: var(--accent) !important; text-decoration: none !important; }
    hr { border-color: rgba(160,191,173,0.16) !important; }

    .stForm,
    div[data-testid="stMetric"],
    div[data-testid="stExpander"],
    details,
    .table-shell,
    .section-header-card,
    .hero-shell,
    .glass-note,
    .mini-stat-card,
    .payment-card,
    .review-shell,
    .info-card {
        position: relative;
        overflow: hidden;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)),
            linear-gradient(180deg, rgba(12,20,16,0.96) 0%, rgba(8,14,11,0.98) 100%) !important;
        box-shadow:
            0 28px 60px rgba(0,0,0,0.26),
            inset 0 1px 0 rgba(255,255,255,0.05),
            inset 0 -1px 0 rgba(255,255,255,0.02);
        backdrop-filter: blur(18px);
    }

    .stForm::before,
    .section-header-card::before,
    .hero-shell::before,
    .glass-note::before,
    .mini-stat-card::before,
    .payment-card::before,
    .review-shell::before,
    .info-card::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at top left, rgba(121,255,183,0.10), transparent 34%),
            radial-gradient(circle at bottom right, rgba(247,215,117,0.08), transparent 32%);
        opacity: .9;
    }

    .stForm { padding: 1.15rem 1.05rem 1rem 1.05rem !important; margin-top: .25rem; }
    .hero-shell { padding: 1.4rem 1.35rem 1.3rem 1.35rem; margin-bottom: 1rem; }
    .hero-shell--center { text-align: center; }

    .hero-orb {
        width: 88px;
        height: 88px;
        margin: 0 auto 1rem auto;
        border-radius: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.35rem;
        background:
            linear-gradient(135deg, rgba(121,255,183,0.18), rgba(247,215,117,0.14));
        border: 1px solid rgba(121,255,183,0.26);
        box-shadow: 0 18px 40px rgba(121,255,183,0.10), inset 0 1px 0 rgba(255,255,255,0.06);
    }

    .hero-eyebrow {
        color: var(--accent);
        font-size: .72rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2.4px;
        margin-bottom: .45rem;
    }

    .hero-title, .section-title {
        font-family: "Bebas Neue", Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif !important;
        letter-spacing: 2px;
        line-height: 1;
        color: var(--text);
    }

    .hero-title {
        font-size: clamp(2.9rem, 6vw, 4.9rem);
        margin-bottom: .35rem;
        background: linear-gradient(180deg, #ffffff 0%, #dff9e8 36%, #fff1bf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }

    .hero-subtitle, .section-subtitle {
        color: var(--text2);
        font-size: .98rem;
        line-height: 1.7;
        max-width: 760px;
        margin: 0 auto;
    }

    .section-header-card { padding: 1rem 1.1rem; margin-bottom: 1rem; }
    .section-title { font-size: 2.15rem; margin-bottom: .2rem; }
    .field-subtitle { color: var(--text2); font-size: .8rem; font-weight: 800; margin: .35rem 0 .2rem; }

    .mini-stat-card {
        padding: 1rem 1rem;
        min-height: 112px;
        display: flex;
        flex-direction: column;
        gap: .28rem;
        justify-content: center;
        margin-bottom: .75rem;
    }

    .mini-stat-card span:first-child { font-size: 1.45rem; }
    .mini-stat-card strong { font-size: 1rem; font-weight: 900; color: var(--text); }
    .mini-stat-card small { color: var(--text3); font-size: .8rem; line-height: 1.45; }

    .glass-note { padding: 1rem 1.05rem; margin-bottom: .8rem; }
    .glass-note--success {
        border-color: var(--green-border) !important;
        background: linear-gradient(180deg, rgba(14,32,21,0.92), rgba(10,20,14,0.96)) !important;
    }
    .glass-note--gold {
        border-color: var(--gold-border) !important;
        background: linear-gradient(180deg, rgba(38,32,14,0.92), rgba(23,19,10,0.96)) !important;
    }
    .glass-note__title {
        font-size: .76rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--accent);
        margin-bottom: .35rem;
    }
    .glass-note--success .glass-note__title { color: var(--green); }
    .glass-note--gold .glass-note__title { color: var(--gold); }
    .glass-note__text { color: var(--text2); font-size: .92rem; line-height: 1.68; }

    .payment-card,
    .review-shell,
    .info-card { padding: 1rem 1.05rem; margin-bottom: .95rem; }

    .payment-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: .9rem;
        margin: .8rem 0 1rem 0;
    }

    .review-shell {
        text-align: center;
        max-width: 720px;
        margin: 1.2rem auto 0 auto;
        padding: 1.35rem 1.1rem;
    }

    .review-shell__icon {
        width: 84px;
        height: 84px;
        margin: 0 auto .9rem auto;
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.25rem;
        background: linear-gradient(135deg, rgba(121,255,183,0.18), rgba(247,215,117,0.16));
        border: 1px solid rgba(121,255,183,0.24);
    }

    .pill,
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: .42rem;
        min-height: 34px;
        padding: .38rem .82rem;
        border-radius: 999px;
        font-size: .74rem;
        font-weight: 900;
        letter-spacing: .4px;
        text-transform: uppercase;
        border: 1px solid var(--blue-border);
        background: linear-gradient(135deg, rgba(121,255,183,0.12), rgba(121,255,183,0.08));
        color: var(--accent) !important;
    }

    .status-pill--ok,
    .pill--success {
        border-color: var(--green-border);
        background: linear-gradient(135deg, rgba(121,255,183,0.14), rgba(67,214,127,0.10));
        color: var(--green) !important;
    }

    .status-pill--warn,
    .pill--warning {
        border-color: var(--orange-border);
        background: linear-gradient(135deg, rgba(255,184,107,0.14), rgba(255,184,107,0.08));
        color: var(--orange) !important;
    }

    .status-pill--danger,
    .pill--danger {
        border-color: var(--red-border);
        background: linear-gradient(135deg, rgba(255,126,139,0.14), rgba(255,126,139,0.08));
        color: var(--red) !important;
    }

    .social-cta {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: .5rem;
        min-height: 48px;
        width: 100%;
        margin-top: .02rem;
        border-radius: 18px;
        border: 1px solid var(--border2);
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        color: var(--text) !important;
        font-weight: 800;
        box-shadow: 0 14px 30px rgba(0,0,0,0.18);
    }

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea,
    [data-baseweb="select"] > div,
    [data-baseweb="base-input"] > div,
    [data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(180deg, rgba(9,16,13,0.98) 0%, rgba(12,20,16,0.99) 100%) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--border2) !important;
        border-radius: 18px !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 12px 28px rgba(0,0,0,0.20) !important;
    }

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {
        padding: .96rem 1rem !important;
        font-size: .98rem !important;
        caret-color: var(--accent) !important;
    }

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder,
    .stTextArea textarea::placeholder,
    textarea::placeholder {
        color: var(--text3) !important;
        opacity: 1 !important;
    }

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus,
    .stTextArea textarea:focus,
    textarea:focus,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="base-input"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(121,255,183,0.10), 0 14px 34px rgba(121,255,183,0.10) !important;
    }

    .stPasswordInput button,
    [data-testid="stPasswordInput"] button,
    [data-baseweb="base-input"] button[aria-label*="password" i],
    [data-baseweb="base-input"] button[title*="password" i],
    [data-baseweb="base-input"] button[aria-label*="contrase" i],
    [data-baseweb="base-input"] button[title*="contrase" i] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        min-width: 0 !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 0 !important;
    }

    .stPasswordInput [data-baseweb="base-input"],
    [data-testid="stPasswordInput"] [data-baseweb="base-input"] {
        grid-template-columns: minmax(0, 1fr) !important;
    }

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
    [data-testid="stWidgetLabel"] * {
        color: var(--text2) !important;
        font-size: .73rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.25px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        min-height: 128px !important;
        border-style: dashed !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {
        background: linear-gradient(180deg, rgba(9,16,13,0.98) 0%, rgba(12,20,16,0.99) 100%) !important;
        color: var(--text) !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"] {
        background: rgba(10, 16, 13, 0.985) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.36) !important;
        border-radius: 18px !important;
    }

    [role="option"][aria-selected="true"],
    [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover {
        background: rgba(121,255,183,0.12) !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        min-height: 48px !important;
        border-radius: 18px !important;
        padding: .82rem 1rem !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        letter-spacing: .2px !important;
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button,
    .stButton > button *,
    .stDownloadButton > button *,
    .stFormSubmitButton > button * {
        color: #04100a !important;
        fill: currentColor !important;
        stroke: currentColor !important;
        opacity: 1 !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #eaf8ef 58%, #dafce9 100%) !important;
        border: 1.5px solid rgba(121,255,183,0.42) !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.70) !important;
        text-shadow: none !important;
    }

    .stButton > button p,
    .stDownloadButton > button p,
    .stFormSubmitButton > button p {
        margin: 0 !important;
        color: #04100a !important;
        font-size: 1.08rem !important;
        font-weight: 900 !important;
        line-height: 1.05 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        border-color: var(--accent) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.22), 0 0 0 1px rgba(121,255,183,0.14) inset !important;
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus,
    .stFormSubmitButton > button:focus {
        box-shadow: 0 0 0 4px rgba(121,255,183,0.14), 0 16px 34px rgba(0,0,0,0.18) !important;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background: linear-gradient(135deg, #79ffb7 0%, #bfff7b 54%, #fff1b8 100%) !important;
        color: #04100a !important;
        border: 0 !important;
        box-shadow: 0 18px 40px rgba(121,255,183,0.16), 0 14px 34px rgba(247,215,117,0.16) !important;
    }

    button[role="tab"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        color: var(--text2) !important;
        padding: .82rem 1rem !important;
        font-weight: 800 !important;
        margin-right: .35rem !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(121,255,183,0.12) 0%, rgba(247,215,117,0.10) 100%) !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.16) !important;
    }

    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: .52rem .72rem;
    }

    [data-testid="stSuccess"],
    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stError"] {
        border-radius: 18px !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 12px 26px rgba(0,0,0,0.18) !important;
    }
    [data-testid="stSuccess"] { background: rgba(67, 214, 127, 0.12) !important; }
    [data-testid="stInfo"] { background: rgba(121,255,183,0.10) !important; }
    [data-testid="stWarning"] { background: rgba(255, 207, 100, 0.12) !important; }
    [data-testid="stError"] { background: rgba(255, 126, 139, 0.12) !important; }

    .stDataFrame, div[data-testid="stTable"], .table-shell {
        background: var(--table-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.20) !important;
    }

    table { border-collapse: collapse !important; }
    thead tr { background: var(--table-head) !important; }
    tbody tr:nth-child(even) { background: var(--table-row) !important; }
    th, td { border-color: rgba(160,191,173,0.10) !important; }

    div[data-testid="stMetric"] { padding: 1rem 1rem !important; }
    div[data-testid="stMetric"] label {
        color: var(--text3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: .68rem !important;
    }
    div[data-testid="stMetricValue"] { color: var(--text) !important; }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #79ffb7 0%, #d1ff5f 100%) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8,17,13,0.98) 0%, rgba(12,20,16,0.98) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }

    input, textarea, select, button { color: var(--text) !important; }
    select, option, optgroup { background-color: #0a100d !important; color: var(--text) !important; }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.04); }
    ::-webkit-scrollbar-thumb { background: rgba(160,191,173,0.28); border-radius: 999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(121,255,183,0.40); }

    @media (max-width: 820px) {
        .block-container { padding-top: 1rem !important; }
        .hero-shell { padding: 1.15rem .95rem 1rem .95rem; }
        .hero-orb { width: 74px; height: 74px; border-radius: 22px; font-size: 2rem; }
        .hero-title { font-size: 2.95rem; }
        .section-title { font-size: 1.8rem; }
        .payment-grid { grid-template-columns: 1fr; }
    }
    </style>
    """
    for k, val in v.items():
        css = css.replace(f"__{k}__", str(val))
    st.markdown(css, unsafe_allow_html=True)
