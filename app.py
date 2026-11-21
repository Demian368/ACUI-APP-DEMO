import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="Gestor Acuícola", layout="wide")

st.title("🔬 Módulo de Cámara de Neubauer")

# Inicializar historial en sesión
if 'historial_conteos' not in st.session_state:
    st.session_state['historial_conteos'] = []

# Sidebar para configuración
st.sidebar.header("Parámetros de Cálculo")
factor_dilucion = st.sidebar.number_input("Factor de Dilución", min_value=1.0, value=1.0, step=0.1)
volumen_inocular = st.sidebar.number_input("Volumen Objetivo (Litros)", min_value=1.5, value=40.0, step=0.5)

# Pestañas para dinamismo
aba1, aba2 = st.tabs(["Cálculo Rápido", "Registro e Historial"])

with aba1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cuadrantes Superiores")
        c1 = st.number_input("Cuadrante 1", min_value=0, value=0)
        c2 = st.number_input("Cuadrante 2", min_value=0, value=0)
        c3 = st.number_input("Cuadrante 3", min_value=0, value=0)
    with col2:
        st.subheader("Cuadrantes Inferiores")
        c4 = st.number_input("Cuadrante 4", min_value=0, value=0)
        c5 = st.number_input("Cuadrante 5", min_value=0, value=0)
        # Viabilidad opcional
        vivas = st.number_input("Células Vivas (Total aproximado)", min_value=0, value=0)
        muertas = st.number_input("Células Muertas (Total aproximado)", min_value=0, value=0)

    if st.button("Calcular Concentración"):
        conteos = [c1, c2, c3, c4, c5]
        promedio = sum(conteos) / len(conteos)
        constante_neubauer = 10000 # 10^4
        concentracion = promedio * factor_dilucion * constante_neubauer
        
        st.metric(label="Concentración Estimada", value=f"{len(concentracion):,.0f} cél/mL")
        
        # Cálculo de viabilidad si aplica
        if vivas + muertas > 0:
            porcentaje_viva = (vivas / (vivas + muertas)) * 100
            st.info(f"Viabilidad celular: {porcentaje_viva:.2f}%")
            
        # Guardar en estado temporal
        st.session_state['ultimo_calculo'] = {
            "concentracion": concentracion,
            "promedio": promedio
        }

with aba2:
    st.subheader("Bitácora de Conteos")
    identificador = st.text_input("Nombre de la muestra / Especie (ej. Chaetoceros)")
    
    if st.button("Guardar en Bitácora"):
        if 'ultimo_calculo' in st.session_state and identificador:
            registro = {
                "muestra": identificador,
                "concentracion": st.session_state['ultimo_calculo']['concentracion']
            }
            st.session_state['historial_conteos'].append(registro)
            st.success("Guardado exitosamente.")
        else:
            st.warning("Por favor realiza un cálculo primero y asigna un nombre.")
            
    if st.session_state['historial_conteos']:
        st.table(st.session_state['historial_conteos'])