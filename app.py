import datetime
import pandas as pd
import streamlit as st

# Configuración de página extendida
st.set_page_config(
    page_title="AquiApp Integral",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS coherentes (Tema Ink Oscuro)
st.markdown(
    """
    <style>
    /* Fondo general y contenedores */
    .stApp {
        background-color: #0B1120;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #1E293B;
        color: #38BDF8 !important;
        font-weight: 600;
        border: 1px solid #334155;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        background-color: #334155;
        border-color: #38BDF8;
        color: #FFFFFF !important;
    }

    .metric-card {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #0EA5E9;
        margin-bottom: 10px;
    }
    
    /* Cifras tabulares para datos técnicos */
    .jst-number {
        font-family: monospace;
        font-variant-numeric: tabular-nums;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicialización de estado de sesión
if "pagina" not in st.session_state:
  st.session_state["pagina"] = "Inicio"
if "historial_conteos" not in st.session_state:
  st.session_state["historial_conteos"] = []
if "bitacora_campo" not in st.session_state:
  st.session_state["bitacora_campo"] = []

# Barra Lateral de Navegación
with st.sidebar:
  st.header("🦐 AquiApp Integral")
  st.caption("Estación de Control Acuícola")
  st.markdown("---")

  if st.button("Inicio / Panel General"):
    st.session_state["pagina"] = "Inicio"
    st.rerun()
  if st.button("🔬 Cámara de Neubauer"):
    st.session_state["pagina"] = "Neubauer"
    st.rerun()
  if st.button("🧪 Balance Iónico"):
    st.session_state["pagina"] = "Balance"
    st.rerun()
  if st.button("🦐 Patología y Alimento"):
    st.session_state["pagina"] = "Patologia"
    st.rerun()

  st.markdown("---")
  st.info("Estado del Sistema: Operativo\nModo: Técnico de Campo")

# LÓGICA DE PÁGINAS

# ----------------------------------------------------------------------
# PÁGINA 1: INICIO Y PANEL DE CONTROL
# ----------------------------------------------------------------------
if st.session_state["pagina"] == "Inicio":
  st.title("Sistema de Gestión Acuícola")
  st.subheader("Consola Central de Operaciones")

  st.markdown("""
    Bienvenido a **AquiApp Integral**. Esta plataforma consolida las herramientas críticas para el monitoreo de laboratorio y campo. Seleccione un módulo para iniciar el procesamiento de datos.
    """)

  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric(label="Módulos Activos", value="3/3")
    if st.button("Acceder a Neubauer"):
      st.session_state["pagina"] = "Neubauer"
      st.rerun()

  with col2:
    st.metric(
        label="Bitácoras Guardadas", value=len(st.session_state["bitacora_campo"])
    )
    if st.button("Acceder a Balance"):
      st.session_state["pagina"] = "Balance"
      st.rerun()

  with col3:
    st.info(
        "Protocolo vigente: Inspección clínica y ajuste de ración diaria."
    )
    if st.button("Acceder a Patología"):
      st.session_state["pagina"] = "Patologia"
      st.rerun()

# ----------------------------------------------------------------------
# PÁGINA 2: CÁMARA DE NEUBAUER
# ----------------------------------------------------------------------
elif st.session_state["pagina"] == "Neubauer":
  st.title("🔬 Módulo de Cámara de Neubauer")
  st.markdown("Cálculo automatizado de densidad celular y viabilidad.")

  aba1, aba2 = st.tabs(["Cálculo y Retícula", "Bitácora de Muestreo"])

  with aba1:
    col_param1, col_param2 = st.columns(2)
    with col_param1:
      factor_dilucion = st.number_input(
          "Factor de Dilución", min_value=1.0, value=10.0, step=0.5
      )
    with col_param2:
      volumen_objetivo = st.number_input(
          "Volumen de Inóculo (Litros)", min_value=1.0, value=500.0, step=10.0
      )

    st.markdown("---")
    st.markdown(
        "### 📐 Conteo de Cuadrantes de las Esquinas (16 Sub-cuadros c/u)"
    )
    col_c1, col_c2 = st.columns(2)
    with col_c1:
      c1 = st.number_input(
          "Cuadrante 1 (Sup. Izq)", min_value=0, value=45, step=1
      )
      c2 = st.number_input(
          "Cuadrante 2 (Sup. Der)", min_value=0, value=50, step=1
      )
    with col_c2:
      c3 = st.number_input(
          "Cuadrante 3 (Inf. Izq)", min_value=0, value=48, step=1
      )
      c4 = st.number_input(
          "Cuadrante 4 (Inf. Der)", min_value=0, value=52, step=1
      )

    st.markdown("---")
    st.markdown("### 🎯 Cuadrante Central (Cuadrante 5 - 25 Sub-cuadros)")
    st.info(
        "Nota técnica: Este cuadrante central se subdivide habitualmente en 25"
        " cuadros para conteos de alta densidad."
    )
    c5 = st.number_input(
        "Cuadrante 5 (Central)", min_value=0, value=125, step=1
    )

    st.markdown("---")
    st.markdown("### 🔬 Evaluación de Viabilidad Celular")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
      vivas = st.number_input("Células Vivas observadas", min_value=0, value=202, step=1)
    with col_v2:
      muertas = st.number_input("Células Muertas observadas", min_value=0, value=40, step=1)

    if st.button("Ejecutar Cálculo Hematológico"):
      # Promedio basado en los 4 cuadrantes de esquina
      promedio_esquinas = sum([c1, c2, c3, c4]) / 4
      constante_neubauer = 10000
      concentracion = promedio_esquinas * factor_dilucion * constante_neubauer
      volumen_total_celulas = concentracion * volumen_objetivo

      st.markdown("### Resultados del Análisis")
      st.metric(
          label="Concentración Estimada (Base Cuadrantes Esquina)",
          value=f"{concentracion:,.0f} cél/mL",
      )
      st.metric(
          label="Carga Celular Total en Volumen Objetivo",
          value=f"{volumen_total_celulas:,.0e} células",
      )

      total_evaluadas = vivas + muertas
      if total_evaluadas > 0:
        porcentaje_viva = (vivas / total_evaluadas) * 100
        st.info(f"Viabilidad Celular: {porcentaje_viva:.2f}%")
        if porcentaje_viva < 80:
          st.warning("Alerta: Baja viabilidad celular detectada.")

      st.session_state["ultimo_calculo_neubauer"] = {
          "concentracion": concentracion,
          "viabilidad": (
              (vivas / total_evaluadas * 100) if total_evaluadas > 0 else 100
          ),
          "volumen": volumen_objetivo,
      }

  with aba2:
    st.subheader("Registro Histórico de Conteos")
    identificador = st.text_input("Identificación de la Muestra / Estanque")
    observaciones = st.text_area("Notas de Campo / Estado del Cultivo")

    if st.button("Registrar en Bitácora"):
      if "ultimo_calculo_neubauer" in st.session_state and identificador:
        registro = {
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Muestra": identificador,
            "Concentración (cél/mL)": (
                f"{st.session_state['ultimo_calculo_neubauer']['concentracion']:,.0f}"
            ),
            "Viabilidad (%)": (
                f"{st.session_state['ultimo_calculo_neubauer']['viabilidad']:.2f}%"
            ),
            "Observaciones": observaciones,
        }
        st.session_state["bitacora_campo"].append(registro)
        st.success("Registro añadido a la base de datos local.")
      else:
        st.error("Realice el cálculo previo y asigne un identificador.")

    if st.session_state["bitacora_campo"]:
      df_historial = pd.DataFrame(st.session_state["bitacora_campo"])
      st.table(df_historial)

      csv = df_historial.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="Descargar Bitácora en CSV",
          data=csv,
          file_name="bitacora_neubauer.csv",
          mime="text/csv",
      )

# ----------------------------------------------------------------------
# PÁGINA 3: BALANCE IÓNICO
# ----------------------------------------------------------------------
elif st.session_state["pagina"] == "Balance":
  st.title("🧪 Módulo de Balance Iónico")
  st.markdown(
      "Monitoreo de proporciones de Calcio ($Ca^{2+}$), Magnesio ($Mg^{2+}$) y"
      " Potasio ($K^+$)."
  )

  salinidad = st.number_input(
      "Salinidad del Agua (ppt / PSU)", min_value=0.0, value=25.0, step=0.5
  )

  st.markdown("### Concentraciones Medidas en Laboratorio (mg/L)")
  calcio_medido = st.number_input(
      "Calcio ($Ca^{2+}$) [mg/L]", min_value=0.0, value=350.0, step=5.0
  )
  magnesio_medido = st.number_input(
      "Magnesio ($Mg^{2+}$) [mg/L]", min_value=0.0, value=1100.0, step=10.0
  )
  potasio_medido = st.number_input(
      "Potasio ($K^+$) [mg/L]", min_value=0.0, value=35.0, step=1.0
  )

  if st.button("Calcular Relaciones Iónicas y Déficit"):
    rel_mg_ca_ideal = 3.1
    rel_ca_k_ideal = 10.0

    rel_mg_ca = magnesio_medido / calcio_medido if calcio_medido > 0 else 0
    rel_ca_k = calcio_medido / potasio_medido if potasio_medido > 0 else 0

    st.markdown("### Resultados del Diagnóstico Iónico")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
      st.metric(
          label="Relación Magnesio:Calcio",
          value=f"{rel_mg_ca:.2f}",
          help=f"Objetivo: ~{rel_mg_ca_ideal}",
      )
    with col_res2:
      st.metric(
          label="Relación Calcio:Potasio",
          value=f"{rel_ca_k:.2f}",
          help=f"Objetivo: ~{rel_ca_k_ideal}",
      )

    st.markdown("### Estimación de Dosificación de Sales (Correctoras)")
    volumen_estanque = st.number_input(
        "Volumen del Estanque (Metros Cúbicos - $m^3$)",
        min_value=100,
        value=2500,
        step=100,
    )

    meta_k = salinidad * 28.0
    deficit_k = max(0, meta_k - potasio_medido)
    kg_kcl_requeridos = (deficit_k * volumen_estanque) / 524000

    meta_ca = salinidad * 11.6
    deficit_ca = max(0, meta_ca - calcio_medido)
    kg_caso4_requeridos = (deficit_ca * volumen_estanque) / 232000

    st.info(f"Déficit estimado de Potasio: {deficit_k:.2f} mg/L")
    st.metric(
        label="Sulfato de Calcio ($CaSO_4$) a aplicar",
        value=f"{kg_caso4_requeridos:.2f} kg",
    )
    st.metric(
        label="Cloruro de Potasio ($KCl$) a aplicar",
        value=f"{kg_kcl_requeridos:.2f} kg",
    )

# ----------------------------------------------------------------------
# PÁGINA 4: PATOLOGÍA Y ALIMENTACIÓN
# ----------------------------------------------------------------------
elif st.session_state["pagina"] == "Patologia":
  st.title("🦐 Módulo de Patología y Alimentación")
  st.markdown(
      "Evaluación clínica en fresco y cálculo de biomasa para ajuste de"
      " raciones."
  )

  aba1, aba2 = st.tabs(
      ["Calculadora de Ración", "Lista de Verificación Clínica"]
  )

  with aba1:
    st.markdown("### Parámetros Poblacionales")
    poblacion = st.number_input(
        "Población Total Estimada (Organismos)",
        min_value=1000,
        value=500000,
        step=10000,
    )
    peso_promedio = st.number_input(
        "Peso Promedio Actual (Gramos)", min_value=0.1, value=12.5, step=0.5
    )
    factor_conversion = st.number_input(
        "Tasa de Alimentación (% Biomasa)", min_value=0.5, value=2.5, step=0.1
    )

    if st.button("Calcular Biomasa y Ración"):
      biomasa_kg = (poblacion * peso_promedio) / 1000
      racion_diaria_kg = biomasa_kg * (factor_conversion / 100)
      racion_por_toma_kg = racion_diaria_kg / 4

      st.metric(label="Biomasa Total Estimada", value=f"{biomasa_kg:,.2f} kg")
      st.metric(
          label="Ración Diaria Recomendada", value=f"{racion_diaria_kg:,.2f} kg/día"
      )
      st.metric(
          label="Ración por Suministro (4 tomas)",
          value=f"{racion_por_toma_kg:,.2f} kg/toma",
      )

  with aba2:
    st.markdown("### Inspección Clínico-Patológica en Fresco")
    st.write(
        "Marque solo las anomalías detectadas durante la necropsia de campo:"
    )

    hepatopancreas_normal = st.checkbox(
        "Hepatopáncreas: Lóbulos definidos, color ámbar, lípidos presentes.",
        value=True,
    )
    hp_anomalia = (
        False
        if hepatopancreas_normal
        else st.multiselect(
            "Anomalías en Hepatopáncreas",
            ["Atrofia / Pálido", "Flácido", "Presencia de melanización"],
        )
    )

    branquias_normales = st.checkbox(
        "Branquias: Limpias, sin obstrucción ni epibiontes.", value=True
    )
    branquias_anomalia = (
        False
        if branquias_normales
        else st.multiselect(
            "Anomalías en Branquias",
            [
                "Sucias / Acumulación de sedimentos",
                "Presencia de hongos/protozoarios",
                "Necrosis",
            ],
        )
    )

    intestino_normal = st.checkbox(
        "Intestino: Compacto, tracto lleno de alimento.", value=True
    )
    int_anomalia = (
        False
        if intestino_normal
        else st.multiselect(
            "Anomalías Intestinales",
            ["Vacío", "Presencia de fluido amarillento / discontinuidad"],
        )
    )

    cuticula_normal = st.checkbox(
        "Cutícula: Dura, sin signos de síndrome de caparazón blando.",
        value=True,
    )

    if st.button("Generar Dictamen Clínico"):
      if (
          hepatopancreas_normal
          and branquias_normales
          and intestino_normal
          and cuticula_normal
      ):
        st.success(
            "Dictamen: Población sin signos clínicos patológicos aparentes."
            " Mantener tasa de alimentación."
        )
      else:
        st.error(
            "Dictamen: Se detectaron anomalías morfológicas. Se recomienda"
            " restringir alimentación y enviar muestras a laboratorio PCR."
        )