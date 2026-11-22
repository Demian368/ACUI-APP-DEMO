import streamlit as st

# Configuración de página
st.set_page_config(page_title="AquiApp Integral", layout="wide")

# Estilos personalizados (Diseño Azul)
st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .stApp {
        background-color: #f0f4f8;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 5em;
        background-color: #004080;
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: 2px solid #00264d;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background-color: #0059b3;
        border-color: #004080;
    }
    .title-text {
        color: #00264d;
        text-align: center;
        font-weight: 800;
    }
    .sub-text {
        color: #4da6ff;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de navegación
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'Inicio'

# Cabecera
st.markdown("<h1 class='title-text'>🦐 AquiApp: Sistema de Gestión Acuícola</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-text'>Plataforma Profesional de Control y Análisis</h4>", unsafe_allow_html=True)

st.write("---")

# Interfaz Principal (Inicio)
if st.session_state['pagina'] == 'Inicio':
    st.subheader("Panel de Control Principal")
    st.write("Selecciona uno de los siguientes módulos para acceder a las herramientas de trabajo:")
    
    # Espaciado
    st.write("###")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔬 Cámara de Neubauer\n(Conteo Celular)"):
            st.session_state['pagina'] = 'Neubauer'
            st.rerun()
            
    with col2:
        if st.button("🧪 Balance Iónico\n(Calidad de Agua)"):
            st.session_state['pagina'] = 'Balance'
            st.rerun()
            
    with col3:
        if st.button("🦐 Patología y Alimento\n(Diagnóstico y Raciones)"):
            st.session_state['pagina'] = 'Patologia'
            st.rerun()

# Módulo 1: Cámara de Neubauer
elif st.session_state['pagina'] == 'Neubauer':
    if st.button("⬅️ Volver al Inicio"):
        st.session_state['pagina'] = 'Inicio'
        st.rerun()
        
    st.title("🔬 Módulo de Cámara de Neubauer")
    
    if 'historial_conteos' not in st.session_state:
        st.session_state['historial_conteos'] = []

    st.sidebar.header("Parámetros de Cálculo")
    factor_dilucion = st.sidebar.number_input("Factor de Dilución", min_value=1.0, value=1.0, step=0.1)
    volumen_inocular = st.sidebar.number_input("Volumen Objetivo (Litros)", min_value=0.1, value=40.0, step=0.5)

    aba1, aba2 = st.tabs(["Cálculo Rápido", "Registro e Historial"])

    with aba1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cuadrantes Superiores")
            c1 = st.number_input("Cuadrante 1", min_value=0, value=0, step=1)
            c2 = st.number_input("Cuadrante 2", min_value=0, value=0, step=1)
            c3 = st.number_input("Cuadrante 3", min_value=0, value=0, step=1)
        with col2:
            st.subheader("Cuadrantes Inferiores")
            c4 = st.number_input("Cuadrante 4", min_value=0, value=0, step=1)
            c5 = st.number_input("Cuadrante 5", min_value=0, value=0, step=1)
            vivas = st.number_input("Células Vivas (Opcional)", min_value=0, value=0, step=1)
            muertas = st.number_input("Células Muertas (Opcional)", min_value=0, value=0, step=1)

        if st.button("Calcular Concentración"):
            conteos = [c1, c2, c3, c4, c5]
            promedio = sum(conteos) / len(conteos)
            constante_neubauer = 10000 
            concentracion = promedio * factor_dilucion * constante_neubauer
            
            st.metric(label="Concentración Estimada", value=f"{concentracion:,.0f} cél/mL")
            
            if vivas + muertas > 0:
                porcentaje_viva = (vivas / (vivas + muertas)) * 100
                st.info(f"Viabilidad celular: {porcentaje_viva:.2f}%")
                
            st.session_state['ultimo_calculo'] = {
                "concentracion": concentracion
            }

    with aba2:
        st.subheader("Bitácora de Conteos")
        identificador = st.text_input("Nombre de la muestra / Especie")
        
        if st.button("Guardar en Bitácora"):
            if 'ultimo_calculo' in st.session_state and identificador:
                registro = {
                    "muestra": identificador,
                    "concentracion": f"{st.session_state['ultimo_calculo']['concentracion']:,.0f} cél/mL"
                }
                st.session_state['historial_conteos'].append(registro)
                st.success("Guardado exitosamente.")
            else:
                st.warning("Por favor realiza un cálculo primero y asigna un nombre.")
                
        if st.session_state['historial_conteos']:
            st.table(st.session_state['historial_conteos'])

# Módulo 2: Balance Iónico
elif st.session_state['pagina'] == 'Balance':
    if st.button("⬅️ Volver al Inicio"):
        st.session_state['pagina'] = 'Inicio'
        st.rerun()
        
    st.title("🧪 Módulo de Balance Iónico")
    st.write("Espacio reservado para el cálculo de proporciones de Calcio, Magnesio y Potasio.")

# Módulo 3: Patología y Alimentación
elif st.session_state['pagina'] == 'Patologia':
    if st.button("⬅️ Volver al Inicio"):
        st.session_state['pagina'] = 'Inicio'
        st.rerun()
        
    st.title("🦐 Módulo de Patología y Alimentación")
    st.write("Espacio reservado para diagnósticos y cálculo de biomasa/ración.")