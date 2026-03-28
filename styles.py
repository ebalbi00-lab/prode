"""
styles.py — Sistema visual premium azul, consistente en móvil y desktop.
"""
import streamlit as st

PREMIUM_THEME = dict(
    scheme="dark",
    bg_html="#06101d",
    bg="#06101d",
    bg2="#0a1728",
    bg3="#0e2036",
    bg4="#102845",
    surface="rgba(10, 23, 40, 0.82)",
    surface_elevated="rgba(12, 28, 49, 0.94)",
    surface_soft="rgba(102, 177, 255, 0.08)",
    surface2="rgba(102, 177, 255, 0.12)",
    text="#f5f9ff",
    text2="#cad8ee",
    text3="#8fa6c7",
    border="rgba(128, 165, 214, 0.16)",
    border2="rgba(128, 165, 214, 0.28)",
    hover_border="rgba(103, 190, 255, 0.42)",
    shadow="rgba(1, 8, 20, 0.52)",
    input_bg="rgba(6, 17, 30, 0.96)",
    input_text="#f5f9ff",
    table_bg="rgba(7, 19, 34, 0.96)",
    table_head="rgba(103, 190, 255, 0.10)",
    table_row="rgba(255, 255, 255, 0.018)",
    accent="#67beff",
    accent_2="#2f7ef7",
    accent_3="#38bdf8",
    gold="#8fc9ff",
    gold2="#dbeeff",
    gold_dim="rgba(103, 190, 255, 0.12)",
    gold_glow="rgba(103, 190, 255, 0.22)",
    gold_border="rgba(103, 190, 255, 0.30)",
    blue="#67beff",
    blue2="#d8eeff",
    blue_dim="rgba(103, 190, 255, 0.12)",
    blue_border="rgba(103, 190, 255, 0.30)",
    cyan="#38bdf8",
    cyan_dim="rgba(56, 189, 248, 0.12)",
    cyan_border="rgba(56, 189, 248, 0.28)",
    red="#fb7185",
    red_dim="rgba(251, 113, 133, 0.12)",
    red_border="rgba(251, 113, 133, 0.28)",
    orange="#7dd3fc",
    orange_dim="rgba(125, 211, 252, 0.14)",
    orange_border="rgba(125, 211, 252, 0.28)",
    green="#60a5fa",
    green2="#3b82f6",
    green_dim="rgba(96, 165, 250, 0.14)",
    green_border="rgba(96, 165, 250, 0.28)",
    green_glow="rgba(96, 165, 250, 0.20)",
    success="#60a5fa",
    warning="#7dd3fc",
    danger="#fb7185",
)


def get_tema() -> str:
    return "premium-blue"


def render_tema_boton():
    return None


def inject_css():
    v = PREMIUM_THEME
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@500;600;700;800&display=swap');

    :root {{
        color-scheme: {v['scheme']};
        --bg: {v['bg']};
        --bg2: {v['bg2']};
        --bg3: {v['bg3']};
        --bg4: {v['bg4']};
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
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    html, body {{
        background: {v['bg_html']} !important;
        color: var(--text) !important;
        color-scheme: dark !important;
        accent-color: {v['accent']};
    }}

    html {{
        background-color: {v['bg_html']} !important;
    }}

    body {{
        background:
            radial-gradient(circle at 0% 0%, rgba(103,190,255,0.20), transparent 24%),
            radial-gradient(circle at 100% 0%, rgba(47,126,247,0.22), transparent 20%),
            radial-gradient(circle at 50% 100%, rgba(56,189,248,0.10), transparent 24%),
            linear-gradient(180deg, #06101d 0%, #081625 35%, #0b1a2c 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
        overscroll-behavior-y: none;
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {{
        background:
            radial-gradient(circle at top left, rgba(103,190,255,0.16), transparent 22%),
            radial-gradient(circle at top right, rgba(47,126,247,0.16), transparent 20%),
            radial-gradient(circle at bottom center, rgba(56,189,248,0.08), transparent 24%),
            linear-gradient(180deg, #06101d 0%, #081625 35%, #0b1a2c 100%) !important;
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
        max-width: 1120px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        position: relative;
    }}

    .block-container::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.016), transparent 20%),
            radial-gradient(circle at 20% 18%, rgba(103,190,255,0.08), transparent 18%),
            radial-gradient(circle at 78% 8%, rgba(47,126,247,0.08), transparent 18%);
        mix-blend-mode: screen;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Outfit', 'Inter', sans-serif !important;
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
        border-color: rgba(128,165,214,0.12) !important;
    }}

    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stExpander"],
    .stForm,
    div[data-testid="stMetric"] {{
        border-radius: var(--radius) !important;
    }}

    .stForm {{
        background: linear-gradient(180deg, rgba(15,32,54,0.88) 0%, rgba(7,18,31,0.96) 100%) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 24px 60px var(--shadow-clr) !important;
        padding: 1.1rem 1.1rem 0.85rem 1.1rem !important;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(14px);
    }}

    .stForm::before {{
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(103,190,255,0.7) 24%, rgba(47,126,247,0.58) 68%, transparent 100%);
        pointer-events: none;
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
        background: linear-gradient(180deg, rgba(6,16,29,0.98) 0%, rgba(10,22,38,0.98) 100%) !important;
        color: var(--input-text) !important;
        border: 1.5px solid var(--border2) !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.20) !important;
    }}

    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea,
    textarea {{
        padding: 0.84rem 0.96rem !important;
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
        box-shadow: 0 0 0 3px rgba(103,190,255,0.12), 0 12px 32px rgba(47,126,247,0.10) !important;
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

    [data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [aria-haspopup="listbox"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] * {{
        background: linear-gradient(180deg, rgba(6,16,29,0.98) 0%, rgba(10,22,38,0.98) 100%) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [role="listbox"],
    ul[role="listbox"],
    div[role="listbox"] {{
        background: rgba(7, 19, 34, 0.985) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        box-shadow: 0 20px 44px rgba(0,0,0,0.36) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(14px);
    }}

    [role="option"], li[role="option"], div[role="option"] {{
        background: rgba(7, 19, 34, 0.985) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}

    [role="option"]:hover,
    [role="option"][aria-selected="true"],
    li[role="option"]:hover,
    div[role="option"]:hover {{
        background: rgba(103,190,255,0.14) !important;
        color: var(--text) !important;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        background: linear-gradient(135deg, rgba(103,190,255,0.14) 0%, rgba(47,126,247,0.18) 100%) !important;
        color: var(--text) !important;
        border: 1px solid rgba(103,190,255,0.20) !important;
        border-radius: 16px !important;
        padding: 0.76rem 1rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 14px 30px rgba(0,0,0,0.18) !important;
        transition: all 0.2s ease !important;
        min-height: 48px !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        transform: translateY(-1px);
        border-color: var(--accent) !important;
        box-shadow: 0 18px 36px rgba(0,0,0,0.24), 0 0 0 1px rgba(103,190,255,0.12) inset !important;
    }}

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    .stDownloadButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #67beff 0%, #2f7ef7 100%) !important;
        color: #04111f !important;
        border: 0 !important;
        box-shadow: 0 18px 38px rgba(47,126,247,0.26), 0 10px 24px rgba(103,190,255,0.16) !important;
        min-height: 48px !important;
    }}

    .stButton > button:focus,
    .stFormSubmitButton > button:focus {{
        box-shadow: 0 0 0 3px rgba(103,190,255,0.16) !important;
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

    [data-testid="stSuccess"] {{ background: rgba(59, 130, 246, 0.12) !important; }}
    [data-testid="stInfo"] {{ background: rgba(56, 189, 248, 0.10) !important; }}
    [data-testid="stWarning"] {{ background: rgba(125, 211, 252, 0.12) !important; }}
    [data-testid="stError"] {{ background: rgba(251, 113, 133, 0.12) !important; }}

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
        background: linear-gradient(135deg, rgba(103,190,255,0.12) 0%, rgba(47,126,247,0.12) 100%) !important;
        box-shadow: 0 10px 22px rgba(0,0,0,0.16) !important;
    }}

    .stDataFrame, div[data-testid="stTable"] {{
        background: var(--table-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.20) !important;
    }}

    thead tr {{ background: var(--table-head) !important; }}
    tbody tr:nth-child(even) {{ background: var(--table-row) !important; }}
    th, td {{ border-color: rgba(128,165,214,0.10) !important; }}

    details {{
        background: rgba(10, 23, 40, 0.78) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: 0 14px 28px rgba(0,0,0,0.18) !important;
    }}

    div[data-testid="stMetric"] {{
        background: linear-gradient(180deg, rgba(14,32,55,0.92) 0%, rgba(8,18,31,0.96) 100%) !important;
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
        background: linear-gradient(180deg, rgba(103,190,255,0.95) 0%, rgba(47,126,247,0.95) 100%);
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #67beff 0%, #2f7ef7 100%) !important;
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
        -webkit-box-shadow: 0 0 0px 1000px rgba(6,16,29,0.98) inset !important;
        transition: background-color 9999s ease-out 0s;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(6,16,29,0.98) 0%, rgba(10,23,40,0.98) 100%) !important;
        border-right: 1px solid var(--border) !important;
    }}

    @media (prefers-color-scheme: light), (prefers-color-scheme: dark) {{
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
            color-scheme: dark !important;
            background-color: {v['bg_html']} !important;
        }}
        input, textarea, select {{
            background-color: rgba(6,16,29,0.98) !important;
            color: var(--text) !important;
        }}
    }}

    ::selection {{
        background: rgba(103,190,255,0.28);
        color: var(--text);
    }}

    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.04); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(128,165,214,0.30); border-radius: 999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(103,190,255,0.40); }}

    .stPasswordInput button,
    .stPasswordInput button[kind="secondary"],
    .stPasswordInput button[kind="secondary"]:hover,
    .stPasswordInput button[kind="secondary"]:focus,
    .stPasswordInput button[kind="secondary"]:active,
    .stPasswordInput [data-baseweb="input"] button,
    .stPasswordInput [data-baseweb="base-input"] button,
    .stPasswordInput [aria-label*="password" i],
    .stPasswordInput [title*="password" i],
    .stPasswordInput [aria-label*="contraseña" i],
    .stPasswordInput [title*="contraseña" i],
    .stNumberInput button,
    .stNumberInput button:hover,
    .stNumberInput button:focus,
    .stNumberInput button:active,
    .stNumberInput [data-baseweb="input"] button,
    .stNumberInput [data-baseweb="base-input"] button {{
        background: linear-gradient(135deg, rgba(219,238,255,0.92) 0%, rgba(167,211,255,0.96) 36%, rgba(103,190,255,0.92) 100%) !important;
        background-color: rgba(167,211,255,0.95) !important;
        color: #0b2545 !important;
        -webkit-text-fill-color: #0b2545 !important;
        border: 1px solid rgba(47,126,247,0.30) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 22px rgba(10,33,66,0.18) !important;
        outline: none !important;
        min-height: 36px !important;
        min-width: 36px !important;
        padding: 0 !important;
    }}

    .stPasswordInput [data-baseweb="input"] > div:last-child,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child {{
        background: transparent !important;
        margin-right: 0.2rem !important;
    }}

    .stPasswordInput [data-baseweb="input"] button,
    .stPasswordInput [data-baseweb="base-input"] button,
    .stPasswordInput button,
    .stPasswordInput button[kind="secondary"] {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 40px !important;
        min-width: 40px !important;
        height: 40px !important;
        min-height: 40px !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #2f7ef7 0%, #1459c7 100%) !important;
        background-color: #1459c7 !important;
        border: 1px solid rgba(103,190,255,0.60) !important;
        box-shadow: 0 10px 22px rgba(10,33,66,0.24) !important;
        padding: 0 !important;
        margin: 0 !important;
        outline: none !important;
    }}

    .stPasswordInput [data-baseweb="input"] button:hover,
    .stPasswordInput [data-baseweb="base-input"] button:hover,
    .stPasswordInput button:hover,
    .stPasswordInput button[kind="secondary"]:hover,
    .stPasswordInput [data-baseweb="input"] button:focus,
    .stPasswordInput [data-baseweb="base-input"] button:focus,
    .stPasswordInput button:focus,
    .stPasswordInput button[kind="secondary"]:focus {{
        background: linear-gradient(135deg, #4895ff 0%, #1b67d9 100%) !important;
        border-color: #8fc9ff !important;
        box-shadow: 0 14px 26px rgba(10,33,66,0.28), 0 0 0 1px rgba(143,201,255,0.22) inset !important;
    }}

    .stPasswordInput button svg,
    .stPasswordInput button[kind="secondary"] svg,
    .stPasswordInput [data-baseweb="input"] button svg,
    .stPasswordInput [data-baseweb="base-input"] button svg,
    .stPasswordInput button [data-testid="stIconMaterial"],
    .stPasswordInput [aria-label*="password" i] svg,
    .stPasswordInput [title*="password" i] svg,
    .stPasswordInput [aria-label*="contraseña" i] svg,
    .stPasswordInput [title*="contraseña" i] svg {{
        width: 20px !important;
        height: 20px !important;
        color: #0b2545 !important;
        fill: #0b2545 !important;
        stroke: #0b2545 !important;
        opacity: 1 !important;
        filter: drop-shadow(0 1px 1px rgba(255,255,255,0.22)) !important;
    }}

    .stPasswordInput button svg *,
    .stPasswordInput button[kind="secondary"] svg *,
    .stPasswordInput [data-baseweb="input"] button svg *,
    .stPasswordInput [data-baseweb="base-input"] button svg *,
    .stPasswordInput button [data-testid="stIconMaterial"] *,
    .stPasswordInput [aria-label*="password" i] svg *,
    .stPasswordInput [title*="password" i] svg *,
    .stPasswordInput [aria-label*="contraseña" i] svg *,
    .stPasswordInput [title*="contraseña" i] svg * {{
        color: #0b2545 !important;
        fill: #0b2545 !important;
        stroke: #0b2545 !important;
        opacity: 1 !important;
    }}

    .stPasswordInput [data-baseweb="input"] > div:last-child,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child,
    .stPasswordInput [data-baseweb="input"] > div:last-child > div,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child > div,
    .stPasswordInput [data-baseweb="input"] > div:last-child > button,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child > button,
    .stPasswordInput [data-baseweb="input"] > div:last-child > button *,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child > button *,
    .stPasswordInput [data-baseweb="input"] > div:last-child [role="button"],
    .stPasswordInput [data-baseweb="base-input"] > div:last-child [role="button"] {{
        background-color: #7db8ff !important;
        background-image: linear-gradient(135deg, #bfe0ff 0%, #7db8ff 46%, #4f93ff 100%) !important;
        color: #0b2545 !important;
        border-color: rgba(11,37,69,0.12) !important;
    }}

    .stPasswordInput input[type="password"]::-ms-reveal,
    .stPasswordInput input[type="password"]::-ms-clear {{
        display: none !important;
    }}

    .stNumberInput button svg,
    .stNumberInput [data-baseweb="input"] button svg,
    .stNumberInput [data-baseweb="base-input"] button svg {{
        color: #1459c7 !important;
        fill: currentColor !important;
        stroke: currentColor !important;
    }}

    .stNumberInput > div > div,
    .stPasswordInput > div > div,
    .stPasswordInput [data-baseweb="base-input"],
    .stNumberInput [data-baseweb="base-input"] {{
        gap: 0.35rem !important;
    }}

    .stNumberInput button:hover,
    .stPasswordInput button:hover,
    .stPasswordInput button[kind="secondary"]:hover {{
        border-color: #2f7ef7 !important;
        box-shadow: 0 14px 26px rgba(10,33,66,0.22), 0 0 0 1px rgba(47,126,247,0.16) inset !important;
        background: linear-gradient(135deg, #4895ff 0%, #1b67d9 100%) !important;
    }}

    [data-testid="stSpinner"],
    [data-testid="stSpinner"] > div,
    [data-testid="stSpinner"] > div > div,
    [data-testid="stStatusWidget"],
    [data-testid="stStatusWidget"] > div,
    [data-testid="stStatusWidget"] > div > div {{
        background: linear-gradient(180deg, rgba(10,23,40,0.90) 0%, rgba(7,18,31,0.96) 100%) !important;
        border: 1px solid var(--blue-border) !important;
        border-radius: 18px !important;
        box-shadow: 0 16px 34px rgba(0,0,0,0.22) !important;
        color: var(--text) !important;
    }}

    [data-testid="stSpinner"] *,
    [data-testid="stStatusWidget"] * {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }}


    [data-testid="stStatusWidget"] code,
    [data-testid="stSpinner"] code,
    .element-container code {{
        background: rgba(103,190,255,0.10) !important;
        color: var(--blue2) !important;
        border: 1px solid rgba(103,190,255,0.16) !important;
        border-radius: 10px !important;
        padding: 0.15rem 0.38rem !important;
    }}

    [data-testid="stHorizontalBlock"] > div {{ gap: 0.9rem !important; }}



    .stPasswordInput [data-baseweb="input"] > div:last-child button,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child button,
    .stPasswordInput [data-baseweb="input"] > div:last-child button:hover,
    .stPasswordInput [data-baseweb="base-input"] > div:last-child button:hover {{
        background: linear-gradient(135deg, #2f7ef7 0%, #1459c7 100%) !important;
        color: #ffffff !important;
    }}


    .stPasswordInput [data-testid="stTextInputRootElement"],
    .stPasswordInput [data-testid="stTextInputRootElement"] > div,
    .stPasswordInput [data-baseweb="base-input"],
    .stPasswordInput [data-baseweb="input"] {{
        background: var(--input-bg) !important;
    }}


    .stToggle label,
    .stCheckbox label {
        color: var(--text2) !important;
        font-weight: 600 !important;
    }

    .stToggle [data-baseweb="checkbox"] > div,
    .stCheckbox [data-baseweb="checkbox"] > div {
        background: rgba(103,190,255,0.10) !important;
        border-color: var(--blue-border) !important;
    }

    .stToggle [data-baseweb="checkbox"] input:checked + div,
    .stCheckbox [data-baseweb="checkbox"] input:checked + div {
        background: linear-gradient(135deg, #2f7ef7 0%, #1459c7 100%) !important;
        border-color: rgba(103,190,255,0.60) !important;
    }


    @media (max-width: 768px) {{
        .block-container {{
            padding-top: 0.9rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}
        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {{
            border-radius: 14px !important;
            padding: 0.82rem 0.95rem !important;
            min-height: 50px !important;
        }}
        button[role="tab"] {{
            padding: 0.7rem 0.85rem !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
