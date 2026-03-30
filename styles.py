"""
styles.py — Tema visual premium unificado para toda la app.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg_html="#06101d",
    bg="#07111f",
    bg2="#0b1729",
    bg3="#10203a",
    surface="rgba(12, 22, 40, 0.78)",
    surface_elevated="rgba(16, 28, 50, 0.92)",
    surface_soft="rgba(120, 140, 180, 0.08)",
    surface2="rgba(120, 140, 180, 0.12)",
    text="#f5f8fc",
    text2="#cfdbeb",
    text3="#8ea4c4",
    border="rgba(143, 170, 214, 0.18)",
    border2="rgba(143, 170, 214, 0.28)",
    hover_border="rgba(110, 231, 255, 0.42)",
    shadow="rgba(2, 8, 20, 0.44)",
    input_bg="rgba(9, 18, 33, 0.96)",
    input_text="#f4f7fb",
    table_bg="rgba(9, 18, 33, 0.94)",
    table_head="rgba(110, 231, 255, 0.10)",
    table_row="rgba(255, 255, 255, 0.02)",
    accent="#78ecff",
    accent_2="#8b5cf6",
    accent_3="#22c55e",
    gold="#f5c76b",
    gold2="#ffe1a8",
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
    return "premium-launch"


def render_tema_boton():
    return None


def inject_css():
    v = PREMIUM_THEME
    css = """
    <style>
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
        --radius: 22px;
        --radius-sm: 16px;
        --radius-lg: 30px;
        --maxw: 1120px;
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
            radial-gradient(circle at 0% 0%, rgba(110,231,255,0.18), transparent 26%),
            radial-gradient(circle at 100% 0%, rgba(139,92,246,0.18), transparent 22%),
            radial-gradient(circle at 50% 100%, rgba(52,211,153,0.08), transparent 30%),
            linear-gradient(180deg, #07111f 0%, #081320 36%, #0a1522 100%) !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
        background:
            radial-gradient(circle at top left, rgba(110,231,255,0.14), transparent 23%),
            radial-gradient(circle at top right, rgba(139,92,246,0.16), transparent 22%),
            radial-gradient(circle at bottom center, rgba(52,211,153,0.08), transparent 28%),
            linear-gradient(180deg, #06101d 0%, #091524 44%, #0a1320 100%) !important;
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
            linear-gradient(180deg, rgba(255,255,255,0.02), transparent 14%),
            radial-gradient(circle at 20% 18%, rgba(255,255,255,0.045), transparent 0.8%),
            radial-gradient(circle at 72% 12%, rgba(255,255,255,0.04), transparent 0.7%),
            radial-gradient(circle at 30% 64%, rgba(255,255,255,0.035), transparent 0.9%),
            radial-gradient(circle at 86% 74%, rgba(255,255,255,0.04), transparent 0.8%);
        opacity: .75;
        z-index: 0;
    }

    .block-container {
        max-width: var(--maxw) !important;
        padding-top: 1.45rem !important;
        padding-bottom: 3rem !important;
    }

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small, code { color: inherit; }
    a { color: var(--accent) !important; text-decoration: none !important; }
    hr { border-color: rgba(143,170,214,0.16) !important; }

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
        background: linear-gradient(180deg, rgba(14,26,46,0.92) 0%, rgba(9,19,35,0.94) 100%) !important;
        box-shadow: 0 22px 54px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.03);
        backdrop-filter: blur(14px);
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
        background: linear-gradient(135deg, rgba(110,231,255,0.08), transparent 40%, rgba(139,92,246,0.08));
        opacity: .9;
    }

    .stForm { padding: 1.1rem 1rem 0.9rem 1rem !important; margin-top: .25rem; }
    .hero-shell { padding: 1.35rem 1.35rem 1.25rem 1.35rem; margin-bottom: 1rem; }
    .hero-shell--center { text-align: center; }

    .hero-orb {
        width: 84px; height: 84px; margin: 0 auto 0.9rem auto; border-radius: 24px; display: flex; align-items: center; justify-content: center;
        font-size: 2.35rem; background: linear-gradient(135deg, rgba(34,211,238,0.18), rgba(139,92,246,0.18));
        border: 1px solid rgba(110,231,255,0.24); box-shadow: 0 18px 34px rgba(34,211,238,0.10), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .hero-eyebrow { color: var(--text3); font-size: .74rem; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; margin-bottom: .35rem; }
    .hero-title, .section-title {
        font-family: "Bebas Neue", Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif !important;
        letter-spacing: 2px; line-height: 1; color: var(--text);
    }

    .hero-title {
        font-size: clamp(2.6rem, 6vw, 4.4rem); margin-bottom: .35rem;
        background: linear-gradient(135deg, var(--text) 0%, var(--blue) 46%, var(--gold2) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }

    .hero-subtitle, .section-subtitle { color: var(--text2); font-size: .95rem; line-height: 1.65; max-width: 720px; margin: 0 auto; }
    .section-header-card { padding: 1rem 1.1rem; margin-bottom: 1rem; }
    .section-title { font-size: 2rem; margin-bottom: .2rem; }
    .field-subtitle { color: var(--text2); font-size: .8rem; font-weight: 800; margin: .35rem 0 .2rem; }

    .mini-stat-card { padding: .95rem 1rem; min-height: 108px; display: flex; flex-direction: column; gap: .25rem; justify-content: center; margin-bottom: .75rem; }
    .mini-stat-card span:first-child { font-size: 1.35rem; }
    .mini-stat-card strong { font-size: .96rem; font-weight: 800; color: var(--text); }
    .mini-stat-card small { color: var(--text3); font-size: .8rem; line-height: 1.45; }

    .glass-note { padding: 1rem 1.05rem; margin-bottom: .8rem; }
    .glass-note--success { border-color: var(--green-border) !important; background: linear-gradient(180deg, rgba(12,32,27,0.86), rgba(10,22,18,0.92)) !important; }
    .glass-note--gold { border-color: var(--gold-border) !important; background: linear-gradient(180deg, rgba(38,31,14,0.86), rgba(23,19,10,0.92)) !important; }
    .glass-note__title { font-size: .76rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.4px; color: var(--blue); margin-bottom: .35rem; }
    .glass-note--success .glass-note__title { color: var(--green); }
    .glass-note--gold .glass-note__title { color: var(--gold); }
    .glass-note__text { color: var(--text2); font-size: .9rem; line-height: 1.65; }

    .payment-card { padding: 1rem 1.05rem; margin-bottom: .95rem; border-color: var(--gold-border) !important; }
    .payment-card__title { font-size: .76rem; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gold); margin-bottom: .75rem; }
    .payment-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: .7rem; margin-bottom: .8rem; }
    .payment-grid span { display: block; color: var(--text3); font-size: .72rem; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: .2rem; }
    .payment-grid strong { color: var(--text); font-size: .95rem; font-weight: 800; }
    .payment-cvu-label { color: var(--gold2); font-size: .72rem; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: .35rem; }
    .payment-help { color: var(--text2); font-size: .84rem; line-height: 1.6; margin-top: .75rem; }

    .review-shell { text-align: center; padding: 2.3rem 1.2rem; margin-bottom: 1rem; }
    .review-shell__icon {
        width: 88px; height: 88px; margin: 0 auto 1rem auto; border-radius: 28px; display:flex; align-items:center; justify-content:center;
        font-size: 2.5rem; background: linear-gradient(135deg, rgba(245,199,107,0.18), rgba(110,231,255,0.12)); border: 1px solid var(--gold-border);
    }

    .info-card { padding: 1rem 1rem .95rem; min-height: 132px; margin-top: .35rem; }
    .info-card--warm { border-color: var(--orange-border) !important; }
    .info-card--cool { border-color: var(--blue-border) !important; }
    .info-card__title { font-size: .82rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.4px; margin-bottom: .45rem; }
    .info-card--warm .info-card__title { color: var(--orange); }
    .info-card--cool .info-card__title { color: var(--blue); }
    .info-card__text { color: var(--text2); font-size: .9rem; line-height: 1.6; }

    .special-pill-row { display:flex; justify-content:space-between; align-items:center; gap:1rem; background: rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:16px; padding:.85rem 1rem; margin-bottom:.55rem; }
    .special-pill-row__left { display:flex; align-items:center; gap:.75rem; min-width:0; }
    .special-pill-row__left span { font-size:1.2rem; }
    .special-pill-row__left strong { font-size:.95rem; color:var(--text); }
    .special-pill-row__right { color:var(--gold); font-weight:900; letter-spacing:.5px; font-family: Inter, sans-serif; }

    .social-cta {
        display:flex; align-items:center; justify-content:center; gap:.5rem; min-height: 44px; width:100%; margin-top: .02rem; border-radius:16px;
        border:1px solid var(--border2); background:linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        color: var(--text) !important; font-weight:800; box-shadow:0 12px 28px rgba(0,0,0,0.18);
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
        background: linear-gradient(180deg, rgba(8,18,32,0.98) 0%, rgba(11,23,41,0.98) 100%) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--border2) !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18) !important;
    }

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea { padding: .9rem 1rem !important; font-size: .98rem !important; caret-color: var(--accent) !important; }

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder,
    .stTextArea textarea::placeholder,
    textarea::placeholder { color: var(--text3) !important; opacity: 1 !important; }

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus,
    .stTextArea textarea:focus,
    textarea:focus,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="base-input"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(110,231,255,0.12), 0 12px 34px rgba(110,231,255,0.10) !important;
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
        letter-spacing: 1.2px !important;
    }

    [data-testid="stFileUploaderDropzone"] { min-height: 124px !important; border-style: dashed !important; }

    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {
        background: linear-gradient(180deg, rgba(8,18,32,0.98) 0%, rgba(11,23,41,0.98) 100%) !important;
        color: var(--text) !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"] {
        background: rgba(10, 19, 35, 0.985) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.36) !important;
        border-radius: 16px !important;
    }

    [role="option"][aria-selected="true"],
    [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover { background: rgba(110,231,255,0.14) !important; }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        min-height: 46px !important;
        background: linear-gradient(135deg, rgba(232,244,255,0.96) 0%, rgba(198,235,255,0.94) 100%) !important;
        color: #06101d !important;
        border: 1px solid rgba(110,231,255,0.35) !important;
        border-radius: 16px !important;
        padding: .78rem 1rem !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        letter-spacing: .2px !important;
        text-shadow: none !important;
        box-shadow: 0 14px 32px rgba(0,0,0,0.18) !important;
        transition: all .18s ease !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        border-color: var(--accent) !important;
        box-shadow: 0 18px 38px rgba(0,0,0,0.24), 0 0 0 1px rgba(110,231,255,0.10) inset !important;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5ee7ff 0%, #7c6cff 54%, #a78bfa 100%) !important;
        color: #03111d !important;
        border: 0 !important;
        box-shadow: 0 18px 40px rgba(34,211,238,0.18), 0 12px 30px rgba(139,92,246,0.18) !important;
    }

    .stButton > button[kind="secondary"],
    .stFormSubmitButton > button[kind="secondary"],
    .stDownloadButton > button[kind="secondary"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(236,244,255,0.96) 100%) !important;
        color: #06101d !important;
        border: 1.5px solid rgba(6,16,29,0.22) !important;
        box-shadow: 0 10px 24px rgba(0,0,0,0.14) !important;
    }

    .stButton > button[kind="secondary"] p,
    .stFormSubmitButton > button[kind="secondary"] p,
    .stDownloadButton > button[kind="secondary"] p,
    .stButton > button p,
    .stFormSubmitButton > button p,
    .stDownloadButton > button p {
        color: inherit !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
    }

    button[role="tab"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text2) !important;
        padding: .78rem 1rem !important;
        font-weight: 800 !important;
        margin-right: .35rem !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        border-color: var(--accent) !important;
        background: linear-gradient(135deg, rgba(110,231,255,0.12) 0%, rgba(139,92,246,0.12) 100%) !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.16) !important;
    }

    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label { background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 14px; padding: .5rem .72rem; }

    [data-testid="stSuccess"],
    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stError"] {
        border-radius: 18px !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 12px 26px rgba(0,0,0,0.18) !important;
    }
    [data-testid="stSuccess"] { background: rgba(16, 185, 129, 0.12) !important; }
    [data-testid="stInfo"] { background: rgba(34, 211, 238, 0.10) !important; }
    [data-testid="stWarning"] { background: rgba(245, 158, 11, 0.12) !important; }
    [data-testid="stError"] { background: rgba(251, 113, 133, 0.12) !important; }

    .stDataFrame, div[data-testid="stTable"], .table-shell {
        background: var(--table-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.20) !important;
    }
    table { border-collapse: collapse !important; }
    thead tr { background: var(--table-head) !important; }
    tbody tr:nth-child(even) { background: var(--table-row) !important; }
    th, td { border-color: rgba(143,170,214,0.12) !important; }

    div[data-testid="stMetric"] { padding: .95rem 1rem !important; }
    div[data-testid="stMetric"] label {
        color: var(--text3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: .68rem !important;
    }
    div[data-testid="stMetricValue"] { color: var(--text) !important; }
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #22d3ee 0%, #8b5cf6 100%) !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(7,17,31,0.96) 0%, rgba(11,23,41,0.96) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }

    input, textarea, select, button { color: var(--text) !important; }
    select, option, optgroup { background-color: #0a1323 !important; color: var(--text) !important; }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.04); }
    ::-webkit-scrollbar-thumb { background: rgba(143,170,214,0.30); border-radius: 999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(110,231,255,0.40); }

    @media (max-width: 820px) {
        .block-container { padding-top: 1rem !important; }
        .hero-shell { padding: 1.1rem .95rem 1rem .95rem; }
        .hero-orb { width: 72px; height: 72px; border-radius: 22px; font-size: 2rem; }
        .hero-title { font-size: 2.75rem; }
        .section-title { font-size: 1.7rem; }
        .payment-grid { grid-template-columns: 1fr; }
    }
    </style>
    """
    for k, val in v.items():
        css = css.replace(f"__{k}__", str(val))
    st.markdown(css, unsafe_allow_html=True)
