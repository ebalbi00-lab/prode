/* INPUT + OJO */
button[kind="secondary"],
button[kind="secondary"]:hover,
button[kind="secondary"]:active {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

button[kind="secondary"] svg {
    fill: #AFC8FF !important;
}

.stTextInput > div > div > input {
    background: transparent !important;
    color: #E6F0FF !important;
}

.stTextInput > div > div {
    background: linear-gradient(180deg, #07111f 0%, #0A1F44 100%) !important;
    border: 1px solid #1E6BFF33 !important;
    border-radius: 12px !important;
}

/* BOTONES + - */
button {
    background: transparent !important;
}

button:hover {
    background: rgba(30,107,255,0.15) !important;
}

/* STATUS / SPINNER */
[data-testid="stStatusWidget"],
[data-testid="stSpinner"],
.stStatus {
    background: linear-gradient(180deg, #07111f 0%, #0A1F44 100%) !important;
    border: 1px solid #1E6BFF33 !important;
    border-radius: 12px !important;
    color: #E6F0FF !important;
}

[data-testid="stStatusWidget"] * {
    color: #E6F0FF !important;
}

[data-testid="stSpinner"] svg {
    stroke: #1E6BFF !important;
}

[data-testid="stStatusWidget"] > div {
    background: transparent !important;
}

/* eliminar grises globales */
div[data-testid="stMarkdownContainer"],
div[data-testid="stAlert"],
div[data-testid="stInfo"] {
    background: transparent !important;
}
