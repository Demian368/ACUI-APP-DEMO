import streamlit as st

st.set_page_config(page_title="AquiApp", layout="wide")

# Estilo azul y cabecera
st.markdown("""
    <style>
    .main { background-color: #f0f8ff; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #0066cc;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🦐 AquiApp: Sistema de Gestión Acuícola")
st.subheader("Panel Principal de Control")

# Columnas para botones en la interfaz
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔬 Cámara de Neubauer"):
        st.session_state['pagina'] = 'Neubauer'
with col2:
    if st.button("🧪 Balance Iónico"):
        st.session_button("🦐 Patología y Alimentación"):
        st.session_state['pagina'] = 'Patologia'

# Lógica de navegación
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'Inicio'

if st.session_state['pagina'] == 'Inicio':
    st.info("Selecciona una herramienta arriba para comenzar.")
elif st.session_state['pagina'] == 'Neubauer':
    st.write("Cargando módulo de conteo...")
    # Aquí irá el código de Neubauer