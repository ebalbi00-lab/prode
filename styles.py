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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Bebas+Neue&family=JetBrains+Mono:wght@700;800&display=swap');

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
        --radius: 20px;
        --radius-sm: 14px;
        --radius-lg: 28px;
        --maxw: 960px;
        --transition: 0.18s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Base ─────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    html, body {
        background: __bg_html__ !important;
        color: var(--text) !important;
    }

    body {
        background:
            radial-gradient(ellipse 80% 40% at 0% 0%, rgba(110,231,255,0.13), transparent),
            radial-gradient(ellipse 60% 35% at 100% 5%, rgba(139,92,246,0.13), transparent),
            radial-gradient(ellipse 50% 30% at 50% 100%, rgba(52,211,153,0.07), transparent),
            linear-gradient(175deg, #060e1a 0%, #081220 50%, #091422 100%) !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
        background:
            radial-gradient(ellipse 80% 40% at 0% 0%, rgba(110,231,255,0.11), transparent),
            radial-gradient(ellipse 60% 35% at 100% 5%, rgba(139,92,246,0.12), transparent),
            radial-gradient(ellipse 50% 30% at 50% 100%, rgba(52,211,153,0.06), transparent),
            linear-gradient(175deg, #060e1a 0%, #081220 50%, #091422 100%) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"], header, #MainMenu, footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    .block-container {
        max-width: var(--maxw) !important;
        padding-top: 1.6rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    h1, h2, h3, h4, h5, h6, p, li, label, span, div, strong, small, code { color: inherit; }
    a { color: var(--accent) !important; text-decoration: none !important; }
    hr { border-color: rgba(143,170,214,0.13) !important; margin: 1.2rem 0 !important; }

    /* ── Cards & Shells ───────────────────────────── */
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
        border: 1px solid rgba(143,170,214,0.14) !important;
        background: linear-gradient(160deg, rgba(16,28,50,0.88) 0%, rgba(10,20,38,0.94) 100%) !important;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.04) inset,
            0 24px 48px rgba(0,0,0,0.28),
            0 4px 12px rgba(0,0,0,0.18) !important;
        backdrop-filter: blur(20px) saturate(1.4);
        -webkit-backdrop-filter: blur(20px) saturate(1.4);
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
        background: linear-gradient(135deg, rgba(110,231,255,0.06) 0%, transparent 45%, rgba(139,92,246,0.06) 100%);
        border-radius: inherit;
    }

    /* ── Form ─────────────────────────────────────── */
    .stForm { padding: 1.4rem 1.2rem 1.1rem 1.2rem !important; margin-top: .3rem; }

    /* ── Hero ─────────────────────────────────────── */
    .hero-shell { padding: 1.6rem 1.4rem 1.4rem 1.4rem; margin-bottom: 1.2rem; }
    .hero-shell--center { text-align: center; }

    .hero-orb {
        width: 80px; height: 80px; margin: 0 auto 1rem auto;
        border-radius: 22px; display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem;
        background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(139,92,246,0.15));
        border: 1px solid rgba(110,231,255,0.20);
        box-shadow: 0 0 0 6px rgba(110,231,255,0.06), 0 16px 32px rgba(34,211,238,0.08);
    }

    .hero-eyebrow {
        color: var(--text3);
        font-size: .72rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: 2.5px;
        margin-bottom: .4rem;
    }

    .hero-title, .section-title {
        font-family: "Bebas Neue", Impact, "Arial Narrow Bold", sans-serif !important;
        letter-spacing: 2.5px; line-height: 1.05; color: var(--text);
    }

    .hero-title {
        font-size: clamp(3.6rem, 9vw, 6rem);
        margin-bottom: .4rem;
        background: linear-gradient(135deg, #e8f4ff 0%, var(--blue) 42%, var(--gold2) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 2px 12px rgba(110,231,255,0.18));
    }

    .hero-subtitle, .section-subtitle {
        color: var(--text2); font-size: .96rem; line-height: 1.7;
        max-width: 680px; margin: 0 auto;
        font-weight: 400;
    }

    .section-header-card { padding: 1.1rem 1.2rem; margin-bottom: 1.1rem; }
    .section-title { font-size: 1.95rem; margin-bottom: .2rem; }
    .field-subtitle {
        color: var(--text3); font-size: .75rem; font-weight: 800;
        margin: .45rem 0 .25rem; text-transform: uppercase; letter-spacing: 1.2px;
    }

    /* ── Mini stat cards ──────────────────────────── */
    .mini-stat-card {
        padding: 1rem 1.1rem; min-height: 104px;
        display: flex; flex-direction: column; gap: .3rem;
        justify-content: center; margin-bottom: .8rem;
    }
    .mini-stat-card span:first-child { font-size: 1.4rem; }
    .mini-stat-card strong { font-size: .95rem; font-weight: 800; color: var(--text); }
    .mini-stat-card small { color: var(--text3); font-size: .8rem; line-height: 1.5; }

    /* ── Glass notes ──────────────────────────────── */
    .glass-note { padding: 1rem 1.1rem; margin-bottom: .9rem; }
    .glass-note--success {
        border-color: rgba(52,211,153,0.22) !important;
        background: linear-gradient(160deg, rgba(10,28,22,0.90), rgba(8,20,16,0.95)) !important;
    }
    .glass-note--gold {
        border-color: rgba(245,199,107,0.22) !important;
        background: linear-gradient(160deg, rgba(30,24,10,0.90), rgba(20,16,8,0.95)) !important;
    }
    .glass-note__title {
        font-size: .72rem; font-weight: 900;
        text-transform: uppercase; letter-spacing: 1.6px;
        color: var(--blue); margin-bottom: .4rem;
    }
    .glass-note--success .glass-note__title { color: var(--green); }
    .glass-note--gold .glass-note__title { color: var(--gold); }
    .glass-note__text { color: var(--text2); font-size: .9rem; line-height: 1.68; }

    /* ── Payment card ─────────────────────────────── */
    .payment-card {
        padding: 1.1rem 1.15rem; margin-bottom: 1rem;
        border-color: rgba(245,199,107,0.20) !important;
        background: linear-gradient(160deg, rgba(28,22,8,0.90), rgba(16,14,6,0.95)) !important;
    }
    .payment-card__title {
        font-size: .72rem; font-weight: 900; letter-spacing: 1.6px;
        text-transform: uppercase; color: var(--gold); margin-bottom: .8rem;
    }
    .payment-grid {
        display: grid; grid-template-columns: repeat(2, minmax(0,1fr));
        gap: .75rem; margin-bottom: .85rem;
    }
    .payment-grid span { display: block; color: var(--text3); font-size: .7rem; text-transform: uppercase; letter-spacing: 1.3px; margin-bottom: .2rem; }
    .payment-grid strong { color: var(--text); font-size: .95rem; font-weight: 800; }
    .payment-cvu-label { color: var(--gold2); font-size: .7rem; font-weight: 800; letter-spacing: 1.3px; text-transform: uppercase; margin-bottom: .38rem; }
    .payment-help { color: var(--text2); font-size: .84rem; line-height: 1.65; margin-top: .8rem; }

    /* ── Review shell ─────────────────────────────── */
    .review-shell { text-align: center; padding: 2.4rem 1.4rem; margin-bottom: 1.1rem; }
    .review-shell__icon {
        width: 88px; height: 88px; margin: 0 auto 1.1rem auto;
        border-radius: 26px; display: flex; align-items: center; justify-content: center;
        font-size: 2.5rem;
        background: linear-gradient(135deg, rgba(245,199,107,0.16), rgba(110,231,255,0.10));
        border: 1px solid rgba(245,199,107,0.22);
        box-shadow: 0 0 0 8px rgba(245,199,107,0.06);
    }

    /* ── Info cards ───────────────────────────────── */
    .info-card { padding: 1.05rem 1.1rem .95rem; min-height: 128px; margin-top: .4rem; }
    .info-card--warm { border-color: rgba(251,146,60,0.22) !important; }
    .info-card--cool { border-color: rgba(110,231,255,0.18) !important; }
    .info-card__title { font-size: .78rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: .5rem; }
    .info-card--warm .info-card__title { color: var(--orange); }
    .info-card--cool .info-card__title { color: var(--blue); }
    .info-card__text { color: var(--text2); font-size: .9rem; line-height: 1.65; }

    /* ── Special pill rows ────────────────────────── */
    .special-pill-row {
        display: flex; justify-content: space-between; align-items: center; gap: 1rem;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(143,170,214,0.12);
        border-radius: 14px; padding: .9rem 1.1rem; margin-bottom: .6rem;
        transition: background var(--transition), border-color var(--transition);
    }
    .special-pill-row:hover {
        background: rgba(110,231,255,0.04);
        border-color: rgba(110,231,255,0.18);
    }
    .special-pill-row__left { display: flex; align-items: center; gap: .75rem; min-width: 0; }
    .special-pill-row__left span { font-size: 1.2rem; }
    .special-pill-row__left strong { font-size: .95rem; color: var(--text); font-weight: 700; }
    .special-pill-row__right { color: var(--gold); font-weight: 900; font-family: Inter, sans-serif; font-size: .9rem; }

    /* ── Social CTA ───────────────────────────────── */
    .social-cta {
        display: flex; align-items: center; justify-content: center; gap: .55rem;
        min-height: 46px; width: 100%; border-radius: var(--radius-sm);
        border: 1px solid rgba(143,170,214,0.18);
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        color: var(--text) !important; font-weight: 800; font-size: .9rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.16);
        transition: all var(--transition);
    }
    .social-cta:hover {
        border-color: rgba(110,231,255,0.28);
        background: rgba(110,231,255,0.05);
        transform: translateY(-1px);
    }

    /* ── Inputs ───────────────────────────────────── */
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    div[data-testid="stTextInputRootElement"] input,
    .stDateInput input,
    .stTextArea textarea,
    textarea,
    [data-baseweb="select"] > div,
    [data-baseweb="base-input"] > div,
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(6,14,26,0.96) !important;
        color: var(--input-text) !important;
        border: 1.5px solid rgba(143,170,214,0.18) !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.02) !important;
        transition: border-color var(--transition), box-shadow var(--transition) !important;
    }

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    div[data-testid="stTextInputRootElement"] input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {
        padding: .95rem 1.1rem !important;
        font-size: .97rem !important;
        font-weight: 500 !important;
        caret-color: var(--accent) !important;
        line-height: 1.5 !important;
    }

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder,
    .stTextArea textarea::placeholder,
    textarea::placeholder { color: var(--text3) !important; opacity: 1 !important; font-weight: 400 !important; }

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stNumberInput input:focus,
    div[data-testid="stTextInputRootElement"] input:focus,
    .stDateInput input:focus,
    .stTextArea textarea:focus,
    textarea:focus,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="base-input"] > div:focus-within {
        border-color: rgba(110,231,255,0.50) !important;
        box-shadow: 0 0 0 3px rgba(110,231,255,0.10), 0 4px 16px rgba(110,231,255,0.08) !important;
        outline: none !important;
    }

    /* ── Labels ───────────────────────────────────── */
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
        color: var(--text3) !important;
        font-size: .7rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.4px !important;
        margin-bottom: .3rem !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        min-height: 120px !important;
        border-style: dashed !important;
        border-color: rgba(143,170,214,0.18) !important;
    }

    /* ── Select dropdowns ─────────────────────────── */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {
        background: rgba(6,14,26,0.96) !important;
        color: var(--text) !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"] {
        background: rgba(8,16,30,0.98) !important;
        color: var(--text) !important;
        border: 1px solid rgba(143,170,214,0.18) !important;
        box-shadow: 0 20px 48px rgba(0,0,0,0.40), 0 4px 12px rgba(0,0,0,0.20) !important;
        border-radius: var(--radius-sm) !important;
    }

    [role="option"][aria-selected="true"],
    [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover {
        background: rgba(110,231,255,0.10) !important;
        color: var(--text) !important;
    }

    /* ── Buttons ──────────────────────────────────── */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        min-height: 48px !important;
        background: rgba(255,255,255,0.05) !important;
        color: var(--text2) !important;
        border: 1px solid rgba(143,170,214,0.18) !important;
        border-radius: var(--radius-sm) !important;
        padding: .82rem 1.1rem !important;
        font-weight: 700 !important;
        font-size: .88rem !important;
        letter-spacing: .3px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.14), inset 0 1px 0 rgba(255,255,255,0.04) !important;
        transition: all var(--transition) !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        border-color: rgba(110,231,255,0.32) !important;
        color: var(--text) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.22), 0 0 0 1px rgba(110,231,255,0.08) inset !important;
    }

    .stButton > button:active,
    .stFormSubmitButton > button:active {
        transform: translateY(0) !important;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3dd6f5 0%, #6c63ff 54%, #9b7cff 100%) !important;
        color: #02101e !important;
        border: 0 !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 20px rgba(61,214,245,0.20), 0 8px 32px rgba(108,99,255,0.18) !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 28px rgba(61,214,245,0.28), 0 10px 40px rgba(108,99,255,0.24) !important;
        transform: translateY(-2px) !important;
        filter: brightness(1.06) !important;
    }


    /* ── Stepper +/− buttons ──────────────────────── */
    button[data-testid*="_minus"],
    button[data-testid*="_plus"] {
        background: rgba(110,231,255,0.08) !important;
        border-color: rgba(110,231,255,0.25) !important;
        color: var(--accent) !important;
        font-size: 1.25rem !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }
    button[data-testid*="_minus"]:hover,
    button[data-testid*="_plus"]:hover {
        background: rgba(110,231,255,0.16) !important;
        border-color: rgba(110,231,255,0.50) !important;
        color: #fff !important;
        box-shadow: 0 0 0 3px rgba(110,231,255,0.12), 0 4px 16px rgba(110,231,255,0.14) !important;
    }
    button[data-testid*="_minus"]:active,
    button[data-testid*="_plus"]:active {
        background: rgba(110,231,255,0.24) !important;
        transform: scale(0.95) !important;
    }

    /* ── Tabs ─────────────────────────────────────── */
    button[role="tab"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(143,170,214,0.14) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text3) !important;
        padding: .75rem 1rem !important;
        font-weight: 700 !important;
        font-size: .85rem !important;
        margin-right: .4rem !important;
        transition: all var(--transition) !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        border-color: rgba(110,231,255,0.30) !important;
        background: linear-gradient(135deg, rgba(110,231,255,0.10), rgba(139,92,246,0.10)) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.14) !important;
    }

    /* ── Radio & Checkbox ─────────────────────────── */
    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(143,170,214,0.13);
        border-radius: 12px; padding: .5rem .75rem;
        transition: all var(--transition);
    }
    .stRadio [role="radiogroup"] > label:hover,
    .stCheckbox > label:hover {
        background: rgba(110,231,255,0.05);
        border-color: rgba(110,231,255,0.22);
    }

    /* ── Alerts ───────────────────────────────────── */
    [data-testid="stSuccess"],
    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stError"] {
        border-radius: var(--radius-sm) !important;
        border: 1px solid rgba(143,170,214,0.14) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.14) !important;
        font-size: .9rem !important;
    }
    [data-testid="stSuccess"] { background: rgba(16,185,129,0.10) !important; border-color: rgba(52,211,153,0.20) !important; }
    [data-testid="stInfo"]    { background: rgba(34,211,238,0.08) !important; border-color: rgba(110,231,255,0.18) !important; }
    [data-testid="stWarning"] { background: rgba(245,158,11,0.10) !important; border-color: rgba(245,158,11,0.22) !important; }
    [data-testid="stError"]   { background: rgba(251,113,133,0.10) !important; border-color: rgba(251,113,133,0.22) !important; }

    /* ── Tables ───────────────────────────────────── */
    .stDataFrame, div[data-testid="stTable"], .table-shell {
        background: var(--table-bg) !important;
        border: 1px solid rgba(143,170,214,0.14) !important;
        border-radius: var(--radius) !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
    }
    table { border-collapse: collapse !important; }
    thead tr { background: rgba(110,231,255,0.08) !important; }
    tbody tr:nth-child(even) { background: rgba(255,255,255,0.02) !important; }
    tbody tr:hover { background: rgba(110,231,255,0.04) !important; transition: background var(--transition); }
    th, td { border-color: rgba(143,170,214,0.09) !important; }

    /* ── Metrics ──────────────────────────────────── */
    div[data-testid="stMetric"] { padding: 1rem 1.1rem !important; }
    div[data-testid="stMetric"] label {
        color: var(--text3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-size: .66rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 800 !important; }
    div[data-testid="stMetricDelta"] { font-size: .82rem !important; font-weight: 700 !important; }

    /* ── Progress ─────────────────────────────────── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22d3ee 0%, #818cf8 50%, #8b5cf6 100%) !important;
        border-radius: 999px !important;
    }
    .stProgress > div > div { background: rgba(255,255,255,0.06) !important; border-radius: 999px !important; }

    /* ── Expander ─────────────────────────────────── */
    div[data-testid="stExpander"] summary,
    details summary {
        padding: .85rem 1rem !important;
        font-weight: 700 !important;
        font-size: .9rem !important;
        color: var(--text2) !important;
        cursor: pointer;
    }
    div[data-testid="stExpander"] summary:hover,
    details summary:hover { color: var(--text) !important; }

    /* ── Sidebar ──────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(6,14,26,0.97) 0%, rgba(10,20,38,0.97) 100%) !important;
        border-right: 1px solid rgba(143,170,214,0.12) !important;
    }

    /* ── Misc ─────────────────────────────────────── */
    input, textarea, select, button { color: var(--text) !important; }
    select, option, optgroup { background-color: #080f1e !important; color: var(--text) !important; }

    /* ── Scrollbar ────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); border-radius: 999px; }
    ::-webkit-scrollbar-thumb { background: rgba(143,170,214,0.22); border-radius: 999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(110,231,255,0.35); }

    /* ── Spinner ──────────────────────────────────── */
    [data-testid="stSpinner"] > div { border-top-color: var(--accent) !important; }

    /* ── Caption / small text ─────────────────────── */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text3) !important;
        font-size: .78rem !important;
    }

    /* ── Divider ──────────────────────────────────── */
    [data-testid="stMarkdownContainer"] hr {
        border: 0 !important;
        border-top: 1px solid rgba(143,170,214,0.12) !important;
        margin: 1.2rem 0 !important;
    }

    /* ── Mobile ───────────────────────────────────── */
    @media (max-width: 768px) {
        .block-container {
            padding-top: .9rem !important;
            padding-left: .8rem !important;
            padding-right: .8rem !important;
        }
        .hero-shell { padding: 1.2rem 1rem 1.1rem 1rem; }
        .hero-orb { width: 68px; height: 68px; border-radius: 20px; font-size: 1.9rem; }
        .hero-title { font-size: 3.2rem; }
        .section-title { font-size: 1.65rem; }
        .payment-grid { grid-template-columns: 1fr; gap: .6rem; }
        .stForm { padding: 1.1rem .9rem .9rem .9rem !important; }
    }

    /* ── Score inputs sin bug en eliminatorias ──── */
    div[data-testid="stTextInputRootElement"] input {
        text-align: center !important;
        font-family: Bebas Neue, sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        padding-left: .55rem !important;
        padding-right: .55rem !important;
    }

    /* ── Number input: mostrar flechas en compu y celular ── */
    .stNumberInput input[type="number"],
    input[type="number"] {
        -webkit-appearance: auto !important;
        -moz-appearance: auto !important;
        appearance: auto !important;
    }

    .stNumberInput input[type="number"]::-webkit-inner-spin-button,
    .stNumberInput input[type="number"]::-webkit-outer-spin-button,
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: auto !important;
        margin: 0 !important;
        opacity: 1 !important;
        display: block !important;
    }

    div[data-testid="stNumberInput"] button,
    [data-testid="stNumberInputStepUp"],
    [data-testid="stNumberInputStepDown"] {
        display: flex !important;
        visibility: visible !important;
        pointer-events: auto !important;
        opacity: 1 !important;
    }

    </style>
    """
    for k, val in v.items():
        css = css.replace(f"__{k}__", str(val))
    st.markdown(css, unsafe_allow_html=True)
