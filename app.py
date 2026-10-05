import streamlit as st
from sentence_transformers import SentenceTransformer
from database import supabase


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="SoundFlow",
    page_icon="🎵",
    layout="wide"
)


# ============================================================
# CONFIGURACIÓN DE BÚSQUEDA
# ============================================================

MATCH_THRESHOLD = 0.35
MATCH_COUNT = 5


# ============================================================
# MODELO DE EMBEDDINGS
# ============================================================

@st.cache_resource
def cargar_modelo():
    return SentenceTransformer("all-MiniLM-L6-v2")


modelo = cargar_modelo()


# ============================================================
# GENERAR EMBEDDING
# ============================================================

def generar_embedding(texto: str):
    """
    Genera un embedding de 384 dimensiones
    utilizando all-MiniLM-L6-v2.
    """

    embedding = modelo.encode(texto)

    return embedding.tolist()


# ============================================================
# CONSTRUIR TEXTO SEMÁNTICO
# ============================================================

def construir_texto_embedding(
    titulo: str,
    artista: str,
    genero: str,
    descripcion: str
):
    """
    Construye el texto utilizado para generar
    el embedding de la canción.
    """

    return (
        f"Título: {titulo}. "
        f"Artista: {artista}. "
        f"Género: {genero}. "
        f"Descripción: {descripcion}."
    )


# ============================================================
# AGREGAR CANCIÓN
# ============================================================

def agregar_cancion(
    titulo: str,
    artista: str,
    genero: str,
    descripcion: str
):
    """
    Genera el embedding y guarda la canción
    directamente en Supabase.
    """

    # --------------------------------------------------------
    # Construir texto para embedding
    # --------------------------------------------------------

    texto_embedding = construir_texto_embedding(
        titulo=titulo,
        artista=artista,
        genero=genero,
        descripcion=descripcion
    )

    # --------------------------------------------------------
    # Generar embedding
    # --------------------------------------------------------

    vector = generar_embedding(
        texto_embedding
    )

    # --------------------------------------------------------
    # Datos de la canción
    # --------------------------------------------------------

    datos = {
        "titulo": titulo,
        "artista": artista,
        "genero": genero,
        "descripcion": descripcion,
        "embedding": vector
    }

    # --------------------------------------------------------
    # Insertar en Supabase
    # --------------------------------------------------------

    respuesta = (
        supabase
        .table("canciones_vectoriales")
        .insert(datos)
        .execute()
    )

    return respuesta


# ============================================================
# BUSCAR CANCIONES
# ============================================================

def buscar_canciones(texto_busqueda: str):
    """
    Realiza una búsqueda híbrida.

    Combina:
    - búsqueda semántica mediante embeddings
    - filtro estructurado utilizando el texto original
    - similitud mediante pgvector
    """

    # --------------------------------------------------------
    # Generar embedding de la consulta
    # --------------------------------------------------------

    embedding = generar_embedding(
        texto_busqueda
    )

    # --------------------------------------------------------
    # Ejecutar función RPC
    # --------------------------------------------------------

    respuesta = supabase.rpc(
        "buscar_canciones",
        {
            "query_embedding": embedding,
            "query_text": texto_busqueda,
            "match_threshold": MATCH_THRESHOLD,
            "match_count": MATCH_COUNT
        }
    ).execute()

    return respuesta.data


# ============================================================
# ENCABEZADO
# ============================================================

st.title("🎵 SoundFlow")

st.subheader(
    "Búsqueda semántica de canciones"
)

st.write(
    "Busca canciones utilizando lenguaje natural "
    "o agrega nuevas canciones directamente desde "
    "la aplicación."
)


# ============================================================
# PESTAÑAS
# ============================================================

tab_buscar, tab_agregar = st.tabs(
    [
        "🔎 Buscar canciones",
        "🎵 Agregar canción"
    ]
)


# ============================================================
# PESTAÑA BUSCAR
# ============================================================

with tab_buscar:

    st.header(
        "🔎 Buscar canciones"
    )

    st.write(
        "Describe qué tipo de canción estás buscando "
        "y SoundFlow encontrará resultados "
        "semánticamente similares."
    )

    # --------------------------------------------------------
    # CONSULTA
    # --------------------------------------------------------

    consulta = st.text_input(
        "¿Qué tipo de canción estás buscando?",
        placeholder=(
            "Ejemplo: salsa romántica, "
            "rock alternativo, música para dormir..."
        )
    )

    # --------------------------------------------------------
    # BOTÓN
    # --------------------------------------------------------

    buscar = st.button(
        "🔎 Buscar canciones",
        type="primary"
    )

    # --------------------------------------------------------
    # EJECUTAR BÚSQUEDA
    # --------------------------------------------------------

    if buscar:

        if not consulta.strip():

            st.warning(
                "Escribe una descripción para "
                "realizar la búsqueda."
            )

        else:

            with st.spinner(
                "🤖 Generando embedding y "
                "buscando canciones..."
            ):

                try:

                    resultados = buscar_canciones(
                        consulta.strip()
                    )

                    # ----------------------------------------
                    # SIN RESULTADOS
                    # ----------------------------------------

                    if not resultados:

                        st.info(
                            "No se encontraron "
                            "canciones similares."
                        )

                    # ----------------------------------------
                    # RESULTADOS
                    # ----------------------------------------

                    else:

                        st.success(
                            f"Se encontraron "
                            f"{len(resultados)} resultados."
                        )

                        for i, cancion in enumerate(
                            resultados,
                            start=1
                        ):

                            # --------------------------------
                            # DATOS
                            # --------------------------------

                            titulo = cancion.get(
                                "titulo",
                                "Sin título"
                            )

                            artista = cancion.get(
                                "artista",
                                "Desconocido"
                            )

                            genero = cancion.get(
                                "genero",
                                ""
                            )

                            descripcion = cancion.get(
                                "descripcion",
                                ""
                            )

                            similitud = cancion.get(
                                "similitud"
                            )

                            # --------------------------------
                            # TÍTULO
                            # --------------------------------

                            st.markdown(
                                f"### 🎵 {i}. {titulo}"
                            )

                            # --------------------------------
                            # ARTISTA
                            # --------------------------------

                            st.write(
                                f"**Artista:** {artista}"
                            )

                            # --------------------------------
                            # GÉNERO
                            # --------------------------------

                            if genero:

                                st.write(
                                    f"**Género:** {genero}"
                                )

                            # --------------------------------
                            # DESCRIPCIÓN
                            # --------------------------------

                            if descripcion:

                                st.write(
                                    f"**Descripción:** "
                                    f"{descripcion}"
                                )

                            # --------------------------------
                            # SIMILITUD
                            # --------------------------------

                            if similitud is not None:

                                try:

                                    similitud = float(
                                        similitud
                                    )

                                    porcentaje = (
                                        similitud * 100
                                    )

                                    st.write(
                                        f"**Similitud:** "
                                        f"{porcentaje:.2f}%"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                similitud,
                                                0.0
                                            ),
                                            1.0
                                        )
                                    )

                                except (
                                    TypeError,
                                    ValueError
                                ):

                                    st.write(
                                        f"**Similitud:** "
                                        f"{similitud}"
                                    )

                            # --------------------------------
                            # SEPARADOR
                            # --------------------------------

                            st.divider()

                except Exception as error:

                    st.error(
                        "❌ Error realizando "
                        "la búsqueda."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# PESTAÑA AGREGAR CANCIÓN
# ============================================================

with tab_agregar:

    st.header(
        "🎵 Agregar nueva canción"
    )

    st.write(
        "Completa los datos de la canción. "
        "SoundFlow generará automáticamente "
        "el embedding y almacenará la información "
        "en Supabase."
    )

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    with st.form(
        "formulario_cancion"
    ):

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        titulo = st.text_input(
            "Título *",
            placeholder=(
                "Ejemplo: La Innombrable"
            )
        )

        # ----------------------------------------------------
        # ARTISTA
        # ----------------------------------------------------

        artista = st.text_input(
            "Artista *",
            placeholder=(
                "Ejemplo: Julius Popper"
            )
        )

        # ----------------------------------------------------
        # GÉNERO
        # ----------------------------------------------------

        genero = st.text_input(
            "Género *",
            placeholder=(
                "Ejemplo: Rock alternativo"
            )
        )

        # ----------------------------------------------------
        # DESCRIPCIÓN
        # ----------------------------------------------------

        descripcion = st.text_area(
            "Descripción *",
            placeholder=(
                "Describe las características "
                "de la canción. Ejemplo: rock "
                "alternativo con una atmósfera "
                "romántica y emocional."
            ),
            height=150
        )

        # ----------------------------------------------------
        # BOTÓN
        # ----------------------------------------------------

        enviar = st.form_submit_button(
            "🎵 Agregar canción",
            type="primary"
        )

    # --------------------------------------------------------
    # PROCESAR FORMULARIO
    # --------------------------------------------------------

    if enviar:

        # ----------------------------------------------------
        # VALIDAR TÍTULO
        # ----------------------------------------------------

        if not titulo.strip():

            st.error(
                "❌ El título es obligatorio."
            )

        # ----------------------------------------------------
        # VALIDAR ARTISTA
        # ----------------------------------------------------

        elif not artista.strip():

            st.error(
                "❌ El artista es obligatorio."
            )

        # ----------------------------------------------------
        # VALIDAR GÉNERO
        # ----------------------------------------------------

        elif not genero.strip():

            st.error(
                "❌ El género es obligatorio."
            )

        # ----------------------------------------------------
        # VALIDAR DESCRIPCIÓN
        # ----------------------------------------------------

        elif not descripcion.strip():

            st.error(
                "❌ La descripción es obligatoria."
            )

        else:

            with st.spinner(
                "🤖 Generando embedding y "
                "guardando canción..."
            ):

                try:

                    respuesta = agregar_cancion(
                        titulo=titulo.strip(),
                        artista=artista.strip(),
                        genero=genero.strip(),
                        descripcion=descripcion.strip()
                    )

                    # ----------------------------------------
                    # ÉXITO
                    # ----------------------------------------

                    if respuesta.data:

                        st.success(
                            "✅ Canción agregada "
                            "correctamente."
                        )

                        st.markdown(
                            "### Información guardada"
                        )

                        st.write(
                            f"**Título:** "
                            f"{titulo.strip()}"
                        )

                        st.write(
                            f"**Artista:** "
                            f"{artista.strip()}"
                        )

                        st.write(
                            f"**Género:** "
                            f"{genero.strip()}"
                        )

                        st.write(
                            f"**Descripción:** "
                            f"{descripcion.strip()}"
                        )

                        st.info(
                            "🤖 Embedding de 384 "
                            "dimensiones generado "
                            "automáticamente."
                        )

                        st.success(
                            "☁️ Registro guardado "
                            "correctamente en Supabase."
                        )

                    else:

                        st.warning(
                            "La operación terminó, "
                            "pero Supabase no devolvió datos."
                        )

                except Exception as error:

                    st.error(
                        "❌ Error agregando "
                        "la canción."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚙️ SoundFlow"
)

st.sidebar.write(
    "Sistema de búsqueda semántica musical."
)


# ============================================================
# MODELO DE EMBEDDINGS
# ============================================================

st.sidebar.write(
    "Modelo de embeddings:"
)

st.sidebar.code(
    "all-MiniLM-L6-v2"
)


# ============================================================
# DIMENSIÓN DEL VECTOR
# ============================================================

st.sidebar.write(
    "Dimensión del vector:"
)

st.sidebar.code(
    "384"
)


# ============================================================
# BASE DE DATOS
# ============================================================

st.sidebar.write(
    "Base de datos:"
)

st.sidebar.code(
    "Supabase"
)


# ============================================================
# MOTOR
# ============================================================

st.sidebar.write(
    "Motor:"
)

st.sidebar.code(
    "PostgreSQL + pgvector"
)


# ============================================================
# UMBRAL
# ============================================================

st.sidebar.write(
    "Umbral de similitud:"
)

st.sidebar.code(
    "0.35"
)


# ============================================================
# RESULTADOS
# ============================================================

st.sidebar.write(
    "Máximo de resultados:"
)

st.sidebar.code(
    "5"
)