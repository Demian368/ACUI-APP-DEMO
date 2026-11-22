import datetime
import pandas as pd
import streamlit as st

# 1. Configuración de página
st.set_page_config(
    page_title="AquiApp Integral · Estación de Control Acuícola",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Sistema de diseño (Tema Ink Oscuro, Hairlines y Tipografía Técnica)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-deep: #07080d;
        --bg-page: #0b0d14;
        --bg-card: #11141c;
        --bg-elevated: #1a1e28;
        --border-hairline: rgba(238, 240, 245, 0.08);
        --border-active: rgba(56, 189, 248, 0.45);
        --text-primary: #eef0f5;
        --text-secondary: #a3a9b8;
        --text-muted: #7a8296;
        --accent: #38bdf8;
        --accent-soft: rgba(56, 189, 248, 0.12);
        --ok: #4cc38a;
        --warn: #e5a93b;
        --err: #e5484d;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg-page);
        color: var(--text-primary);
    }

    header[data-testid="stHeader"] {
        background-color: rgba(11, 13, 20, 0.85);
        border-bottom: 1px solid var(--border-hairline);
    }

    section[data-testid="stSidebar"] {
        background-color: var(--bg-deep);
        border-right: 1px solid var(--border-hairline);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent;
        color: var(--text-secondary);
        border: 1px solid transparent;
        border-radius: 8px;
        text-align: left;
        justify-content: flex-start;
        padding: 0.55rem 0.85rem;
        font-weight: 500;
        font-size: 0.9rem;
        height: auto;
        transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: var(--bg-elevated);
        color: var(--text-primary);
        border-color: var(--border-hairline);
    }

    div[data-testid="stMain"] div.stButton > button {
        background-color: var(--bg-elevated);
        color: var(--text-primary);
        border: 1px solid var(--border-hairline);
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.6rem 1.1rem;
        height: auto;
        transition: background-color 0.15s ease, border-color 0.15s ease;
    }

    div[data-testid="stMain"] div.stButton > button:hover {
        background-color: #222736;
        border-color: var(--accent);
        color: #ffffff;
    }

    div[data-testid="stMain"] div.stButton > button[kind="primary"] {
        background-color: var(--accent);
        color: #07080d;
        border: none;
        font-weight: 600;
    }

    div[data-testid="stMain"] div.stButton > button[kind="primary"]:hover {
        background-color: #5cc9fa;
        color: #07080d;
    }

    .pro-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-hairline);
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
    }

    .pro-card-header {
        font-size: 0.82rem;
        color: var(--text-muted);
        margin-bottom: 6px;
        letter-spacing: 0.01em;
    }

    .pro-kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-variant-numeric: tabular-nums;
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.15;
    }

    .pro-kpi-sub {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 6px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        background-color: var(--bg-elevated);
        border: 1px solid var(--border-hairline);
        color: var(--text-secondary);
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--ok);
        display: inline-block;
    }

    [data-testid="stMetric"] {
        background-color: var(--bg-card);
        border: 1px solid var(--border-hairline);
        border-radius: 12px;
        padding: 16px 20px;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums !important;
        font-size: 1.65rem !important;
        color: var(--text-primary) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }

    button[data-baseweb="tab"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--accent) !important;
    }

    h1, h2, h3 {
        font-weight: 500 !important;
        letter-spacing: -0.015em;
        color: var(--text-primary) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Estado inicial de sesión
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Inicio"
if "bitacora_campo" not in st.session_state:
    st.session_state["bitacora_campo"] = []
if "ultimo_calculo_neubauer" not in st.session_state:
    st.session_state["ultimo_calculo_neubauer"] = None

NEUBAUER_DEFAULTS = {
    "neubauer_dilucion": 1.0,
    "neubauer_volumen": 0.0,
    "neubauer_unidad": "Mililitros (mL)",
    "neubauer_c1": 0,
    "neubauer_c2": 0,
    "neubauer_c3": 0,
    "neubauer_c4": 0,
    "neubauer_c5": 0,
    "neubauer_vivas": 0,
    "neubauer_muertas": 0,
}

for k, default_val in NEUBAUER_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = default_val


def reset_neubauer_inputs():
    st.session_state["neubauer_dilucion"] = 1.0
    st.session_state["neubauer_volumen"] = 0.0
    st.session_state["neubauer_c1"] = 0
    st.session_state["neubauer_c2"] = 0
    st.session_state["neubauer_c3"] = 0
    st.session_state["neubauer_c4"] = 0
    st.session_state["neubauer_c5"] = 0
    st.session_state["neubauer_vivas"] = 0
    st.session_state["neubauer_muertas"] = 0


def render_neubauer_svg(c1: int, c2: int, c3: int, c4: int, c5: int) -> str:
    max_val = max(c1, c2, c3, c4, c5, 1)

    def opacity_for(val: int) -> float:
        if val <= 0:
            return 0.04
        return round(0.12 + 0.68 * (val / max_val), 2)

    def subgrid_lines(x0: float, y0: float, size: float, divisions: int) -> str:
        lines = []
        step = size / divisions
        for i in range(1, divisions):
            pos_x = x0 + i * step
            pos_y = y0 + i * step
            lines.append(
                f'<line x1="{pos_x:.1f}" y1="{y0}" x2="{pos_x:.1f}" y2="{y0 + size}" '
                'stroke="rgba(238,240,245,0.14)" stroke-width="0.6"/>'
            )
            lines.append(
                f'<line x1="{x0}" y1="{pos_y:.1f}" x2="{x0 + size}" y2="{pos_y:.1f}" '
                'stroke="rgba(238,240,245,0.14)" stroke-width="0.6"/>'
            )
        return "".join(lines)

    quads = [
        ("C1", 0, 0, c1, 4, "#38bdf8"),
        ("C2", 200, 0, c2, 4, "#38bdf8"),
        ("C3", 0, 200, c3, 4, "#38bdf8"),
        ("C4", 200, 200, c4, 4, "#38bdf8"),
        ("C5", 100, 100, c5, 5, "#4cc38a"),
    ]

    blocks_svg = []
    for label, x, y, val, div, color in quads:
        op = opacity_for(val)
        blocks_svg.append(
            f'<rect x="{x}" y="{y}" width="100" height="100" fill="{color}" fill-opacity="{op}"/>'
        )
        blocks_svg.append(subgrid_lines(x, y, 100, div))
        blocks_svg.append(
            f'<rect x="{x}" y="{y}" width="100" height="100" fill="none" '
            f'stroke="{color}" stroke-opacity="0.65" stroke-width="1.2"/>'
        )
        blocks_svg.append(
            f'<text x="{x + 8}" y="{y + 16}" fill="#eef0f5" font-family="JetBrains Mono, monospace" '
            f'font-size="10" font-weight="600">{label} ({div*div})</text>'
        )
        blocks_svg.append(
            f'<text x="{x + 50}" y="{y + 57}" text-anchor="middle" fill="#ffffff" '
            f'font-family="JetBrains Mono, monospace" font-size="16" font-weight="600">{val}</text>'
        )

    svg = f"""
    <div style="background:#11141c; border:1px solid rgba(238,240,245,0.08); border-radius:12px; padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="font-size:13px; font-weight:500; color:#eef0f5;">Esquema de retícula de Neubauer</span>
            <span style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#7a8296;">Profundidad 0.1 mm</span>
        </div>
        <svg viewBox="0 0 300 300" style="width:100%; max-width:320px; display:block; margin:0 auto; background:#0b0d14; border-radius:8px;">
            {''.join(blocks_svg)}
            <line x1="100" y1="0" x2="100" y2="300" stroke="rgba(238,240,245,0.22)" stroke-width="1"/>
            <line x1="200" y1="0" x2="200" y2="300" stroke="rgba(238,240,245,0.22)" stroke-width="1"/>
            <line x1="0" y1="100" x2="300" y2="100" stroke="rgba(238,240,245,0.22)" stroke-width="1"/>
            <line x1="0" y1="200" x2="300" y2="200" stroke="rgba(238,240,245,0.22)" stroke-width="1"/>
        </svg>
        <div style="display:flex; justify-content:space-between; margin-top:12px; font-size:11px; color:#a3a9b8;">
            <span><span style="color:#38bdf8;">■</span> C1–C4: Esquinas (16 cuadros c/u)</span>
            <span><span style="color:#4cc38a;">■</span> C5: Central (25 cuadros)</span>
        </div>
    </div>
    """
    return svg


def build_printable_html(df: pd.DataFrame) -> str:
    rows_html = ""
    for _, row in df.iterrows():
        rows_html += "<tr>" + "".join(f"<td>{str(val)}</td>" for val in row) + "</tr>"
    headers_html = "".join(f"<th>{col}</th>" for col in df.columns)
    fecha_emision = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reporte Bitácora Neubauer - AquiApp</title>
<style>
  body {{ font-family: 'Inter', Arial, sans-serif; color: #111827; margin: 36px; }}
  .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #111827; padding-bottom: 12px; margin-bottom: 24px; }}
  h1 {{ font-size: 20px; margin: 0; }}
  .meta {{ font-size: 12px; color: #4b5565; text-align: right; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  th, td {{ border: 1px solid #d1d5db; padding: 8px 10px; text-align: left; }}
  th {{ background-color: #f3f4f6; font-weight: 600; }}
  @media print {{ .no-print {{ display: none; }} }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>AquiApp Integral · Bitácora de Conteo Celular</h1>
      <div style="font-size:13px; color:#4b5565; margin-top:4px;">Registro técnico de Cámara de Neubauer</div>
    </div>
    <div class="meta">
      <div>Emitido: {fecha_emision}</div>
      <div>Total muestras: {len(df)}</div>
    </div>
  </div>
  <button class="no-print" onclick="window.print()" style="margin-bottom:16px; padding:8px 14px; cursor:pointer;">Imprimir / Guardar como PDF</button>
  <table>
    <thead><tr>{headers_html}</tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</body>
</html>"""


# 4. Barra lateral persistente
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 4px 4px 12px 4px;">
            <div style="font-size:1.05rem; font-weight:600; color:#eef0f5; letter-spacing:-0.01em;">AquiApp Integral</div>
            <div style="font-size:0.78rem; color:#7a8296; margin-top:2px;">Control técnico acuícola</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="status-badge"><span class="status-dot"></span>Sistema operativo</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
    st.caption("Módulos de trabajo")

    if st.button("Panel general", use_container_width=True):
        st.session_state["pagina"] = "Inicio"
        st.rerun()
    if st.button("Cámara de Neubauer", use_container_width=True):
        st.session_state["pagina"] = "Neubauer"
        st.rerun()
    if st.button("Balance iónico", use_container_width=True):
        st.session_state["pagina"] = "Balance"
        st.rerun()
    if st.button("Patología y alimento", use_container_width=True):
        st.session_state["pagina"] = "Patologia"
        st.rerun()

    st.markdown("---")
    st.caption("Resumen de sesión")
    st.markdown(
        f"<div style='font-size:0.82rem; color:#a3a9b8;'>Registros en bitácora: "
        f"<span style='font-family:JetBrains Mono,monospace; color:#eef0f5;'>{len(st.session_state['bitacora_campo'])}</span></div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# PÁGINA 1: PANEL DE CONTROL GENERAL
# ----------------------------------------------------------------------
if st.session_state["pagina"] == "Inicio":
    st.title("Panel de control acuícola")
    st.markdown(
        "<p style='color:#a3a9b8; max-width:640px; margin-bottom:24px;'>"
        "Estación unificada para conteo celular en cámara de Neubauer, diagnóstico de balance iónico "
        "y cálculo de raciones con verificación clínica en fresco."
        "</p>",
        unsafe_allow_html=True,
    )

    k1, k2, k3 = st.columns(3)
    ultima_conc = (
        f"{st.session_state['ultimo_calculo_neubauer']['conc_esquinas']:,.0f} cél/mL"
        if st.session_state["ultimo_calculo_neubauer"]
        else "Sin lectura"
    )
    with k1:
        st.markdown(
            f"""
            <div class="pro-card">
                <div class="pro-card-header">Última concentración medida</div>
                <div class="pro-kpi-value">{ultima_conc}</div>
                <div class="pro-kpi-sub">Base cuadrantes de esquina (16 cuadros)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="pro-card">
                <div class="pro-card-header">Muestras en bitácora</div>
                <div class="pro-kpi-value">{len(st.session_state['bitacora_campo'])}</div>
                <div class="pro-kpi-sub">Exportable en CSV y formato imprimible</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            """
            <div class="pro-card">
                <div class="pro-card-header">Relación iónica de referencia</div>
                <div class="pro-kpi-value">3.1 : 1</div>
                <div class="pro-kpi-sub">Proporción objetivo Mg:Ca en agua de cultivo</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.subheader("Acceso directo a módulos")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            """
            <div class="pro-card">
                <div style="font-weight:600; font-size:1rem; margin-bottom:6px;">Cámara de Neubauer</div>
                <div style="font-size:0.86rem; color:#a3a9b8; line-height:1.45;">
                    Conteo diferencial en las 4 esquinas (16 cuadros) y cuadrante central C5 (25 cuadros), viabilidad e historial.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Abrir Cámara de Neubauer", key="btn_home_neu", use_container_width=True):
            st.session_state["pagina"] = "Neubauer"
            st.rerun()

    with m2:
        st.markdown(
            """
            <div class="pro-card">
                <div style="font-weight:600; font-size:1rem; margin-bottom:6px;">Balance iónico</div>
                <div style="font-size:0.86rem; color:#a3a9b8; line-height:1.45;">
                    Evaluación de calcio, magnesio y potasio frente a salinidad y cálculo de sales correctivas por estanque.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Abrir Balance iónico", key="btn_home_bal", use_container_width=True):
            st.session_state["pagina"] = "Balance"
            st.rerun()

    with m3:
        st.markdown(
            """
            <div class="pro-card">
                <div style="font-weight:600; font-size:1rem; margin-bottom:6px;">Patología y alimento</div>
                <div style="font-size:0.86rem; color:#a3a9b8; line-height:1.45;">
                    Cálculo de biomasa viva, ración diaria por toma y protocolo de revisión clínica en fresco.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Abrir Patología y alimento", key="btn_home_pat", use_container_width=True):
            st.session_state["pagina"] = "Patologia"
            st.rerun()


# ----------------------------------------------------------------------
# PÁGINA 2: CÁMARA DE NEUBAUER
# ----------------------------------------------------------------------
elif st.session_state["pagina"] == "Neubauer":
    st.title("Cámara de Neubauer")
    st.markdown(
        "<p style='color:#a3a9b8; margin-bottom:18px;'>"
        "Conteo celular separado entre cuadrantes de esquina (16 subcuadros) y cuadrante central C5 (25 subcuadros)."
        "</p>",
        unsafe_allow_html=True,
    )

    tab_calc, tab_hist = st.tabs(["Conteo y retícula interactiva", "Bitácora e historial"])

    with tab_calc:
        col_form, col_vis = st.columns([1.35, 1], gap="large")

        with col_form:
            st.markdown("**Parámetros de dilución e inóculo**")
            p1, p2, p3 = st.columns(3)
            with p1:
                factor_dilucion = st.number_input(
                    "Factor de dilución",
                    min_value=0.0,
                    step=0.5,
                    format="%.4f",
                    key="neubauer_dilucion",
                )
            with p2:
                volumen_objetivo = st.number_input(
                    "Volumen objetivo",
                    min_value=0.0,
                    step=1.0,
                    format="%.1f",
                    key="neubauer_volumen",
                )
            with p3:
                unidad_vol = st.selectbox(
                    "Unidad de volumen",
                    ["Mililitros (mL)", "Litros (L)", "Toneladas (Ton)"],
                    key="neubauer_unidad",
                )

            st.markdown("---")
            st.markdown("**Cuadrantes de las esquinas (16 subcuadros cada uno)**")
            e1, e2 = st.columns(2)
            with e1:
                c1 = st.number_input(
                    "Cuadrante 1 (Superior izquierdo)",
                    min_value=0,
                    step=1,
                    key="neubauer_c1",
                )
                c3 = st.number_input(
                    "Cuadrante 3 (Inferior izquierdo)",
                    min_value=0,
                    step=1,
                    key="neubauer_c3",
                )
            with e2:
                c2 = st.number_input(
                    "Cuadrante 2 (Superior derecho)",
                    min_value=0,
                    step=1,
                    key="neubauer_c2",
                )
                c4 = st.number_input(
                    "Cuadrante 4 (Inferior derecho)",
                    min_value=0,
                    step=1,
                    key="neubauer_c4",
                )

            st.markdown("---")
            st.markdown("**Cuadrante central (Cuadrante 5 · 25 subcuadros)**")
            st.caption("Apartado independiente para el cuadrante central de 25 cuadros.")
            c5 = st.number_input(
                "Cuadrante 5 (Central · 25 cuadros)",
                min_value=0,
                step=1,
                key="neubauer_c5",
            )

            st.markdown("---")
            st.markdown("**Viabilidad celular diferencial (opcional)**")
            v1, v2 = st.columns(2)
            with v1:
                vivas = st.number_input(
                    "Células vivas",
                    min_value=0,
                    step=1,
                    key="neubauer_vivas",
                )
            with v2:
                muertas = st.number_input(
                    "Células muertas",
                    min_value=0,
                    step=1,
                    key="neubauer_muertas",
                )

            b_calc, b_reset = st.columns(2)
            with b_calc:
                calcular_btn = st.button(
                    "Calcular concentración y actualizar retícula",
                    type="primary",
                    use_container_width=True,
                )
            with b_reset:
                st.button(
                    "Limpiar / Comenzar de nuevo",
                    type="secondary",
                    use_container_width=True,
                    on_click=reset_neubauer_inputs,
                )

        if "Litros" in unidad_vol:
            volumen_mL = volumen_objetivo * 1000.0
            unidad_label = "L"
        elif "Toneladas" in unidad_vol:
            volumen_mL = volumen_objetivo * 1000000.0
            unidad_label = "Ton"
        else:
            volumen_mL = volumen_objetivo
            unidad_label = "mL"

        promedio_esquinas = sum([c1, c2, c3, c4]) / 4.0
        constante_neubauer = 10000
        conc_esquinas = promedio_esquinas * factor_dilucion * constante_neubauer
        conc_central = c5 * factor_dilucion * constante_neubauer
        celulas_totales = conc_esquinas * volumen_mL

        total_viab = vivas + muertas
        viabilidad_pct = (vivas / total_viab * 100.0) if total_viab > 0 else None

        if calcular_btn or st.session_state["ultimo_calculo_neubauer"] is None:
            st.session_state["ultimo_calculo_neubauer"] = {
                "c1": c1,
                "c2": c2,
                "c3": c3,
                "c4": c4,
                "c5": c5,
                "dilucion": factor_dilucion,
                "volumen": volumen_objetivo,
                "unidad_vol": unidad_vol,
                "conc_esquinas": conc_esquinas,
                "conc_central": conc_central,
                "viabilidad": viabilidad_pct,
                "celulas_totales": celulas_totales,
                "vivas": vivas,
                "muertas": muertas,
            }

        with col_vis:
            st.markdown(render_neubauer_svg(c1, c2, c3, c4, c5), unsafe_allow_html=True)

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            st.metric(
                label="Concentración · Cuadrantes esquina (C1–C4)",
                value=f"{conc_esquinas:,.0f} cél/mL",
                delta=f"Promedio: {promedio_esquinas:.1f} cél/cuadrante",
            )
            st.metric(
                label="Concentración · Cuadrante central (C5 · 25 cuadros)",
                value=f"{conc_central:,.0f} cél/mL",
                delta=f"Lectura directa C5: {c5} cél",
            )
            st.metric(
                label=f"Carga total en {volumen_objetivo:,.2f} {unidad_label}",
                value=f"{celulas_totales:,.0f} cél",
            )

            if viabilidad_pct is not None:
                color_bar = "#4cc38a" if viabilidad_pct >= 80 else "#e5484d"
                st.markdown(
                    f"""
                    <div class="pro-card" style="margin-top:10px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:8px;">
                            <span style="color:#a3a9b8;">Viabilidad celular</span>
                            <span style="font-family:'JetBrains Mono',monospace; font-weight:600; color:{color_bar};">{viabilidad_pct:.2f}%</span>
                        </div>
                        <div style="width:100%; height:8px; background:#1a1e28; border-radius:4px; overflow:hidden;">
                            <div style="width:{min(viabilidad_pct, 100):.1f}%; height:100%; background:{color_bar};"></div>
                        </div>
                        <div style="font-size:0.78rem; color:#7a8296; margin-top:8px;">
                            Vivas: {vivas} · Muertas: {muertas} (Total evaluado: {total_viab})
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab_hist:
        st.subheader("Bitácora de conteos")
        reg_col1, reg_col2 = st.columns([1.2, 1.8])
        with reg_col1:
            identificador = st.text_input(
                "Nombre de la muestra / Especie",
                placeholder="Ej. Chaetoceros gracilis - Tanque 04",
            )
        with reg_col2:
            notas_muestra = st.text_input(
                "Observaciones técnicas",
                placeholder="Ej. Fase exponencial, sin contaminación de ciliados",
            )

        if st.button("Guardar lectura actual en bitácora", type="primary"):
            if identificador.strip():
                datos = st.session_state["ultimo_calculo_neubauer"]
                viab_str = (
                    f"{datos['viabilidad']:.2f}%"
                    if datos["viabilidad"] is not None
                    else "N/A"
                )
                nuevo_registro = {
                    "Fecha y hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Muestra / Especie": identificador.strip(),
                    "C1–C4 (16c)": f"{datos['c1']}, {datos['c2']}, {datos['c3']}, {datos['c4']}",
                    "C5 Central (25c)": datos["c5"],
                    "Dilución": f"{datos['dilucion']}x",
                    "Vol. Objetivo": f"{datos['volumen']} {datos['unidad_vol'].split()[0]}",
                    "Conc. Esquinas (cél/mL)": f"{datos['conc_esquinas']:,.0f}",
                    "Conc. C5 (cél/mL)": f"{datos['conc_central']:,.0f}",
                    "Carga Total (cél)": f"{datos['celulas_totales']:,.0f}",
                    "Viabilidad": viab_str,
                    "Observaciones": notas_muestra.strip() or "—",
                }
                st.session_state["bitacora_campo"].append(nuevo_registro)
                st.success(f"Muestra '{identificador.strip()}' registrada en la bitácora.")
            else:
                st.warning("Asigna un nombre a la muestra o especie antes de guardar.")

        st.markdown("---")
        if st.session_state["bitacora_campo"]:
            df_bitacora = pd.DataFrame(st.session_state["bitacora_campo"])
            st.dataframe(df_bitacora, use_container_width=True, hide_index=True)

            exp1, exp2, exp3 = st.columns([1, 1, 1])
            with exp1:
                csv_bytes = df_bitacora.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    label="Exportar bitácora (CSV)",
                    data=csv_bytes,
                    file_name=f"bitacora_neubauer_{datetime.date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with exp2:
                html_report = build_printable_html(df_bitacora).encode("utf-8")
                st.download_button(
                    label="Exportar reporte imprimible / PDF",
                    data=html_report,
                    file_name=f"reporte_neubauer_{datetime.date.today()}.html",
                    mime="text/html",
                    use_container_width=True,
                )
            with exp3:
                if st.button("Vaciar historial", use_container_width=True):
                    st.session_state["bitacora_campo"] = []
                    st.rerun()
        else:
            st.info("No hay registros almacenados todavía. Guarda un conteo desde el formulario superior.")


# ----------------------------------------------------------------------
# PÁGINA 3: BALANCE IÓNICO
# ----------------------------------------------------------------------
elif st.session_state["pagina"] == "Balance":
    st.title("Balance iónico y calidad de agua")
    st.markdown(
        "<p style='color:#a3a9b8; margin-bottom:18px;'>"
        "Cálculo de proporciones críticas de Calcio, Magnesio y Potasio según salinidad del estanque."
        "</p>",
        unsafe_allow_html=True,
    )

    col_in, col_out = st