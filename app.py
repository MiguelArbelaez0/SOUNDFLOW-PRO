import streamlit as st
from database import supabase
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="SoundFlow",
    page_icon="🎵",
    layout="centered"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0d1117;
    }

    .main .block-container {
        max-width: 850px;
        padding-top: 45px;
        padding-bottom: 60px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CARGAR MODELO
# ============================================================

@st.cache_resource
def cargar_modelo():
    return SentenceTransformer("all-MiniLM-L6-v2")


modelo = cargar_modelo()


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    "# 🎵 SoundFlow"
)

st.markdown(
    "### Encuentra música según lo que estás buscando"
)

st.write("")


# ============================================================
# BUSCADOR
# ============================================================

consulta = st.text_input(
    "¿Qué tipo de música estás buscando?",
    placeholder="Ejemplo: quiero una canción para entrenar"
)


buscar = st.button(
    "🔎 Buscar canciones",
    use_container_width=True
)


# ============================================================
# PROCESAR BÚSQUEDA
# ============================================================

if buscar:

    # --------------------------------------------------------
    # Comprobar que escribió algo
    # --------------------------------------------------------

    if not consulta.strip():

        st.warning(
            "⚠️ Escribe qué tipo de música estás buscando."
        )

        st.stop()


    # --------------------------------------------------------
    # Mostrar mensaje mientras busca
    # --------------------------------------------------------

    with st.spinner("🎧 Buscando canciones similares..."):

        try:

            # =================================================
            # CREAR EMBEDDING
            # =================================================

            embedding = modelo.encode(
                consulta,
                normalize_embeddings=True
            ).tolist()


            # =================================================
            # BUSCAR EN SUPABASE
            # =================================================

            respuesta = supabase.rpc(
                "buscar_canciones",
                {
                    "query_embedding": embedding,
                    "match_threshold": 0.5,
                    "match_count": 5
                }
            ).execute()


            resultados = respuesta.data


            # =================================================
            # RESULTADOS
            # =================================================

            st.divider()

            st.subheader("🎧 Recomendaciones")


            # -------------------------------------------------
            # Si no hay resultados
            # -------------------------------------------------

            if not resultados:

                st.info(
                    "No encontramos canciones relacionadas "
                    "con tu búsqueda."
                )


            # -------------------------------------------------
            # Mostrar canciones
            # -------------------------------------------------

            else:

                for i, cancion in enumerate(resultados):

                    titulo = cancion.get(
                        "titulo",
                        "Sin título"
                    )

                    artista = cancion.get(
                        "artista",
                        "Artista desconocido"
                    )

                    similitud = cancion.get(
                        "similitud",
                        0
                    )


                    # -----------------------------------------
                    # Convertir similitud a porcentaje
                    # -----------------------------------------

                    porcentaje = float(similitud) * 100


                    # -----------------------------------------
                    # TARJETA
                    # -----------------------------------------

                    with st.container(border=True):

                        st.markdown(
                            f"### {i + 1}. {titulo}"
                        )

                        st.write(
                            f"🎤 **Artista:** {artista}"
                        )

                        st.write(
                            f"🎧 **Coincidencia:** "
                            f"{porcentaje:.1f}%"
                        )


                        # Barra visual de coincidencia
                        st.progress(
                            min(
                                max(
                                    porcentaje / 100,
                                    0.0
                                ),
                                1.0
                            )
                        )


        # =====================================================
        # MANEJO DE ERRORES
        # =====================================================

        except Exception as e:

            st.error(
                "❌ Ocurrió un error al realizar la búsqueda."
            )

            st.code(
                str(e)
            )
            