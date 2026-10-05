"""Estilos visuales compartidos por la interfaz de SoundFlow.

Separar el CSS de las vistas facilita ajustar la apariencia global sin mezclar
reglas visuales con la lógica de presentación de cada pantalla.
"""

import streamlit as st


def apply_styles():
    """Aplica el fondo, el ancho del contenido y el aspecto de los botones."""
    st.markdown(
        """<style>
        .stApp { background-color: #0f1117; }
        .block-container { max-width: 1350px; padding-top: 2rem; padding-bottom: 4rem; }
        .stButton > button { border-radius: 10px; font-weight: 600; }
        </style>""",
        unsafe_allow_html=True,
    )
