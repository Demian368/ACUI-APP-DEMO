import streamlit as st

st.set_page_config(page_title="Gestor Acuícola", layout="wide")
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