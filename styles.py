"""
styles_final.py — tema visual premium corregido.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg_html="#06101d",
    bg="#07111f",
    bg2="#0c1728",
    bg3="#111f35",
    surface="rgba(10, 20, 36, 0.82)",
    surface_elevated="rgba(14, 26, 46, 0.92)",
    surface_soft="rgba(120, 140, 180, 0.08)",
    surface2="rgba(120, 140, 180, 0.12)",
    text="#f5f7fb",
    text2="#c7d4e8",
    text3="#91a5c3",
    border="rgba(143, 170, 214, 0.18)",
    border2="rgba(143, 170, 214, 0.30)",
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
    blue_dim="rgba(110, 231, 255, 0.14)",
    blue_border="rgba(110, 231, 255, 0.30)",
    cyan="#22d3ee",
    cyan_dim="rgba(34, 211, 238, 0.12)",
    cyan_border="rgba(34, 211, 238, 0.26)",
    red="#ff5959",
    red_dim="rgba(255, 89, 89, 0.14)",
    red_border="rgba(255, 89, 89, 0.26)",
    orange="#fb923c",
    orange_dim="rgba(251, 146, 60, 0.14)",
    orange_border="rgba(251, 146, 60, 0.28)",
    green="#34d399",
    green2="#10b981",
    green_dim="rgba(52, 211, 153, 0.14)",
    green_border="rgba(52, 211, 153, 0.28)",
    green_glow="rgba(52, 211, 153, 0.20)",
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
        --radius: 20px;
        --radius-sm: 14px;
        --radius-lg: 28px;
    }}

    html, body, [class*="css"] {{
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }}

    html, body {{
        background: {v['bg_html']} !important;
        color: var(--text) !important;
    }}

    body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(circle at 0% 0%, rgba(110,231,255,0.12), transparent 22%),
            radial-gradient(circle at 100% 0%, rgba(139,92,246,0.16), transparent 20%),
            radial-gradient(circle at 50% 100%, rgba(52,211,153,0.08), transparent 24%),
            linear-gradient(180deg, #06101d 0%, #091626 45%, #0b1220 100%) !important;
        color: var(--text) !important;
    }}

    [data-testid="stHeader"], header, #MainMenu, footer {{
        visibility: hidden !important;
        height: 0 !important;
    }}

    .block-container {{
        max-width: 1180px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 3rem !important;
    }}

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small {{ color: inherit; }}
    a {{ color: var(--accent) !important; text-decoration: none !important; }}
    hr {{ border-color: rgba(143,170,214,0.14) !important; }}

    .stForm {{
        background: linear-gradient(180deg, rgba(13,24,42,0.92) 0%, rgba(8,16,30,0.94) 100%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.24) !important;
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
        background: linear-gradient(180deg, rgba(7,18,34,0.98) 0%, rgba(9,21,39,0.98) 100%) !important;
        color: var(--input-text) !important;
        border: 1.5px solid rgba(110,231,255,0.18) !important;
        border-radius: 16px !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 12px 28px rgba(0,0,0,0.16) !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.9rem 1rem !important;
        font-size: 1rem !important;
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
        box-shadow: 0 0 0 3px rgba(110,231,255,0.10), 0 12px 32px rgba(110,231,255,0.10) !important;
    }}

    .stTextInput label,
    .stPasswordInput label,
    .stSelectbox label,
    .stNumberInput label,
    .stDateInput label,
    .stFileUploader label,
    .stTextArea label,
    .stMultiSelect label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] * {{
        color: var(--text2) !important;
        font-size: 0.73rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }}

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {{
        border-radius: 16px !important;
        padding: 0.78rem 1rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 14px 28px rgba(0,0,0,0.18) !important;
        transition: all 0.18s ease !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {{
        transform: translateY(-1px);
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #23d5ee 0%, #7c5cff 100%) !important;
        color: #04111f !important;
        border: 0 !important;
        box-shadow: 0 18px 38px rgba(34,211,238,0.18), 0 10px 24px rgba(139,92,246,0.14) !important;
    }}

    .stButton > button:not([kind="primary"]),
    .stDownloadButton > button:not([kind="primary"]),
    .stFormSubmitButton > button:not([kind="primary"]) {{
        background: linear-gradient(180deg, rgba(12,23,41,0.96) 0%, rgba(10,18,33,0.96) 100%) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
    }}

    .stButton > button[kind="secondary"],
    .stFormSubmitButton > button[kind="secondary"],
    .stPasswordInput button,
    .stTextInput button,
    .stNumberInput button {{
        background: linear-gradient(180deg, rgba(18,44,74,0.98) 0%, rgba(11,31,55,0.98) 100%) !important;
        color: var(--blue) !important;
        border: 1px solid var(--blue-border) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 10px 22px rgba(0,0,0,0.18) !important;
    }}

    .stButton > button[kind="secondary"]:hover,
    .stFormSubmitButton > button[kind="secondary"]:hover,
    .stPasswordInput button:hover,
    .stTextInput button:hover,
    .stNumberInput button:hover {{
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 2px rgba(110,231,255,0.10), 0 12px 24px rgba(0,0,0,0.20) !important;
    }}

    [data-testid="stSuccess"], [data-testid="stInfo"], [data-testid="stWarning"], [data-testid="stError"] {{
        border-radius: 18px !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 12px 26px rgba(0,0,0,0.18) !important;
        backdrop-filter: blur(10px);
    }}
    [data-testid="stSuccess"] {{ background: rgba(16, 185, 129, 0.12) !important; }}
    [data-testid="stInfo"] {{ background: rgba(34, 211, 238, 0.10) !important; }}
    [data-testid="stWarning"] {{ background: rgba(245, 158, 11, 0.12) !important; }}
    [data-testid="stError"] {{ background: rgba(251, 113, 133, 0.12) !important; }}

    div[data-testid="stMetric"], details, .stDataFrame, div[data-testid="stTable"] {{
        border-radius: 18px !important;
        overflow: hidden !important;
    }}

    .auth-hero {{ padding: 1rem 0.2rem 0.8rem 0; }}
    .hero-shell {{ max-width: 620px; }}
    .hero-shell--center {{ max-width: 760px; margin: 0 auto 1rem auto; text-align: center; }}
    .hero-orb {{
        width: 72px; height: 72px; border-radius: 22px; display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, rgba(110,231,255,0.16) 0%, rgba(139,92,246,0.18) 100%);
        border: 1px solid rgba(110,231,255,0.22); font-size: 1.9rem; box-shadow: 0 20px 48px rgba(0,0,0,0.26);
        margin-bottom: 1rem;
    }}
    .hero-shell--center .hero-orb {{ margin-left: auto; margin-right: auto; }}
    .hero-badge {{
        display:inline-flex; align-items:center; gap:8px; padding:7px 14px; border-radius:999px;
        background: rgba(110,231,255,0.10); border:1px solid rgba(110,231,255,0.18); color: var(--blue2);
        font-size: 0.77rem; font-weight: 800; letter-spacing: 0.3px; margin-bottom: 1rem;
    }}
    .hero-eyebrow {{ color: var(--blue); font-size: 0.84rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 0.75rem; }}
    .hero-title {{ font-size: clamp(2.3rem, 4vw, 4.2rem); line-height: 0.95; font-weight: 900; margin-bottom: 0.8rem; }}
    .hero-subtitle {{ color: var(--text2); font-size: 1.05rem; line-height: 1.6; max-width: 58ch; }}
    .hero-kpis {{ display:flex; gap:12px; flex-wrap:wrap; margin-top:1.2rem; }}
    .hero-kpi {{
        min-width: 150px; background: rgba(255,255,255,0.03); border:1px solid var(--border);
        border-radius: 18px; padding: 0.9rem 1rem;
    }}
    .hero-kpi strong {{ display:block; font-size: 1rem; color: var(--text); margin-bottom: 0.18rem; }}
    .hero-kpi span {{ color: var(--text3); font-size: 0.85rem; }}

    .section-header-card, .auth-card, .payment-card, .review-shell, .glass-note, .info-card, .table-shell {{
        background: linear-gradient(180deg, rgba(13,24,42,0.92) 0%, rgba(8,16,30,0.94) 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: 0 20px 44px rgba(0,0,0,0.24);
    }}

    .auth-card {{ padding: 1.15rem; }}
    .section-header-card {{ padding: 1.1rem 1.15rem; margin-bottom: 1rem; }}
    .section-title {{ font-size: 1.5rem; font-weight: 900; margin-bottom: 0.3rem; }}
    .section-subtitle {{ color: var(--text2); line-height: 1.6; }}

    .glass-note {{ padding: 1rem 1.05rem; margin-top: 0.9rem; }}
    .glass-note__title {{ font-weight: 800; margin-bottom: 0.35rem; }}
    .glass-note__text {{ color: var(--text2); line-height: 1.55; }}
    .glass-note--success {{ border-color: var(--green-border); background: linear-gradient(180deg, rgba(14,31,32,0.96) 0%, rgba(10,21,24,0.96) 100%); }}
    .glass-note--gold {{ border-color: var(--gold-border); background: linear-gradient(180deg, rgba(36,27,15,0.96) 0%, rgba(24,18,10,0.96) 100%); }}

    .feature-list {{ display:grid; grid-template-columns:1fr; gap:12px; margin-top:1rem; }}
    .feature-item {{
        display:flex; gap:12px; align-items:flex-start; padding:0.95rem 1rem;
        background: rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:18px;
    }}
    .feature-item__icon {{
        width:40px; height:40px; flex-shrink:0; border-radius:12px; display:flex; align-items:center; justify-content:center;
        background: rgba(110,231,255,0.10); border:1px solid rgba(110,231,255,0.18); font-size: 1rem;
    }}
    .feature-item__title {{ font-weight: 800; margin-bottom: 0.18rem; }}
    .feature-item__text {{ color: var(--text2); font-size: 0.92rem; line-height: 1.55; }}

    .social-cta {{
        display:flex; align-items:center; justify-content:center; gap:10px; min-height: 48px; width:100%;
        border-radius:16px; background: linear-gradient(180deg, rgba(12,23,41,0.96) 0%, rgba(10,18,33,0.96) 100%);
        border:1px solid var(--border2); color: var(--text) !important; font-weight:800;
        box-shadow: 0 14px 28px rgba(0,0,0,0.18);
    }}

    .payment-card {{ padding: 1.05rem; margin-bottom: 1rem; border-color: var(--gold-border); }}
    .payment-card__title {{ font-size: 1.02rem; font-weight: 900; margin-bottom: 0.75rem; }}
    .payment-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom: 0.75rem; }}
    .payment-grid > div {{ background: rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:16px; padding: 0.8rem 0.9rem; }}
    .payment-grid span {{ display:block; color: var(--text3); font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.2rem; }}
    .payment-grid strong {{ font-size: 0.98rem; }}
    .payment-cvu-label {{ color: var(--gold2); font-size: 0.78rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; margin: 0.2rem 0 0.45rem 0; }}
    .payment-help {{ color: var(--text2); margin-top: 0.8rem; line-height: 1.55; }}

    .field-subtitle {{ color: var(--text2); font-size: 0.74rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; margin: 0.15rem 0 0.55rem 0; }}

    .review-shell {{ padding: 2.2rem 1.2rem; text-align:center; }}
    .review-shell__icon {{ font-size: 3rem; margin-bottom: 0.8rem; }}

    .info-card {{ padding: 1rem; height: 100%; }}
    .info-card__title {{ font-weight: 900; margin-bottom: 0.32rem; }}
    .info-card__text {{ color: var(--text2); line-height: 1.55; }}
    .info-card--warm {{ border-color: var(--gold-border); }}
    .info-card--cool {{ border-color: var(--blue-border); }}

    .table-shell {{ padding: 0.35rem; }}
    .special-pill-row {{
        display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0.9rem 1rem;
        background: rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:18px; margin-bottom:0.6rem;
    }}
    .special-pill-row__left {{ display:flex; align-items:center; gap:10px; font-weight: 800; }}
    .special-pill-row__right {{ color: var(--gold); font-weight: 900; }}

    @media (max-width: 900px) {{
        .block-container {{ padding-top: 1.1rem !important; }}
        .hero-title {{ font-size: 2.2rem; }}
        .hero-subtitle {{ font-size: 0.98rem; }}
        .payment-grid {{ grid-template-columns: 1fr; }}
        .hero-kpis {{ display:grid; grid-template-columns: 1fr 1fr; }}
    }}

    @media (max-width: 640px) {{
        .stForm {{ padding: 0.95rem 0.95rem 0.7rem 0.95rem !important; }}
        .hero-kpis {{ grid-template-columns: 1fr; }}
        .section-title {{ font-size: 1.28rem; }}
        .hero-orb {{ width: 62px; height: 62px; border-radius: 18px; }}
    }}
    </style>
    """, unsafe_allow_html=True)
