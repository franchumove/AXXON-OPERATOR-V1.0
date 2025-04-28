import streamlit as st
import datetime

# Config inicial
st.set_page_config(
    page_title="AXXON Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores simbólicos
AXXON_BLUE = "#3B82F6"
AXXON_PURPLE = "#8B5CF6"
AXXON_GRAY = "#1F2937"
AXXON_BG = "#F9FAFB"

# Estilo CSS embebido estilo Tailwind
st.markdown(f"""
    <style>
        body {{
            background-color: {AXXON_BG};
        }}
        .title-block {{
            background-color: {AXXON_PURPLE};
            color: white;
            padding: 1rem;
            border-radius: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .card {{
            background-color: white;
            padding: 1.2rem;
            margin-bottom: 1rem;
            border-radius: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }}
    </style>
""", unsafe_allow_html=True)

# Fallback visual si Streamlit está embebido en iframe y falla
st.warning("Si no ves el dashboard correctamente, abre este link en nueva pestaña o desactiva el iframe.", icon="⚠️")

# Título central
st.markdown('<div class="title-block"><h1>AXXON Dashboard Cognitivo</h1></div>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Última Extracción de Notion")
    st.write("Fecha:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    st.success("Extracción completada con éxito.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Estado de Embeddings")
    st.error("EmbeddingError: openai.Embedding deprecated. Usar `openai.Embedding.create()`")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Eventos Cognitivos Clave")
    st.info("• Mutación simbólica detectada.\n• Contradicción emocional procesada.\n• Nueva narrativa activada.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Espacios Cargados")
    st.success("• Diccionario Simbólico\n• Bitácora Interpretativa\n• Mapa de Mutación")
    st.markdown('</div>', unsafe_allow_html=True)