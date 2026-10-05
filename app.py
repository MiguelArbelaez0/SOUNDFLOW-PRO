import streamlit as st
from sentence_transformers import SentenceTransformer
from database import supabase


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="SoundFlow",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MATCH_THRESHOLD = 0.35
MATCH_COUNT = 5


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f1117;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Título principal */
    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 28px !important;
        font-weight: 750 !important;
    }

    h3 {
        font-size: 20px !important;
    }

    /* Botones */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    /* Inputs */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;
    }

    /* Separadores */
    hr {
        margin-top: 25px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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

    embedding = modelo.encode(texto)

    return embedding.tolist()


# ============================================================
# CONSTRUIR TEXTO PARA EMBEDDING
# ============================================================

def construir_texto_embedding(
    titulo: str,
    artista: str,
    genero: str,
    descripcion: str
):

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

    texto_embedding = construir_texto_embedding(
        titulo=titulo,
        artista=artista,
        genero=genero,
        descripcion=descripcion
    )

    vector = generar_embedding(texto_embedding)

    datos = {
        "titulo": titulo,
        "artista": artista,
        "genero": genero,
        "descripcion": descripcion,
        "embedding": vector
    }

    respuesta = (
        supabase
        .table("canciones_vectoriales")
        .insert(datos)
        .execute()
    )

    return respuesta


# ============================================================
# BÚSQUEDA SEMÁNTICA
# ============================================================

def buscar_canciones(texto_busqueda: str):

    embedding = generar_embedding(texto_busqueda)

    respuesta = supabase.rpc(
        "buscar_canciones",
        {
            "query_embedding": embedding,
            "query_text": texto_busqueda.strip(),
            "match_threshold": MATCH_THRESHOLD,
            "match_count": MATCH_COUNT
        }
    ).execute()

    return respuesta.data


# ============================================================
# OBTENER CANCIONES
# ============================================================

@st.cache_data(ttl=30)
def obtener_canciones():

    respuesta = (
        supabase
        .table("canciones_vectoriales")
        .select(
            "id,titulo,artista,genero,descripcion"
        )
        .order("id")
        .execute()
    )

    return respuesta.data


# ============================================================
# OBTENER CATEGORÍAS
# ============================================================

def obtener_categorias(canciones):

    categorias = {}

    for cancion in canciones:

        genero = cancion.get(
            "genero",
            "Sin género"
        )

        if genero not in categorias:
            categorias[genero] = []

        categorias[genero].append(cancion)

    return categorias


# ============================================================
# ENCABEZADO
# ============================================================

st.title("🎵 SoundFlow")

st.write(
    "Descubre música por significado, género y emociones."
)


# ============================================================
# NAVEGACIÓN
# ============================================================

tab_inicio, tab_buscar, tab_agregar = st.tabs(
    [
        "🏠 Inicio",
        "🔎 Buscar canciones",
        "➕ Agregar canción"
    ]
)


# ============================================================
# INICIO
# ============================================================

with tab_inicio:

    canciones = obtener_canciones()

    if not canciones:

        st.info(
            "No hay canciones registradas todavía."
        )

    else:

        categorias = obtener_categorias(
            canciones
        )

        # ----------------------------------------------------
        # CATEGORÍAS
        # ----------------------------------------------------

        st.header("🎧 Explora por categorías")

        st.caption(
            "Selecciona una categoría para ver sus canciones."
        )

        nombres_categorias = list(
            categorias.keys()
        )

        # Mostrar categorías en columnas
        columnas = st.columns(
            min(len(nombres_categorias), 5)
        )

        for indice, categoria in enumerate(
            nombres_categorias
        ):

            columna = columnas[
                indice % len(columnas)
            ]

            with columna:

                if st.button(
                    f"🎵 {categoria}",
                    key=f"categoria_{indice}",
                    use_container_width=True
                ):

                    st.session_state[
                        "categoria_seleccionada"
                    ] = categoria


        # ----------------------------------------------------
        # CATEGORÍA SELECCIONADA
        # ----------------------------------------------------

        categoria_seleccionada = st.session_state.get(
            "categoria_seleccionada"
        )

        if categoria_seleccionada:

            st.divider()

            st.subheader(
                f"🎵 {categoria_seleccionada}"
            )

            canciones_categoria = categorias[
                categoria_seleccionada
            ]

            columnas_canciones = st.columns(3)

            for indice, cancion in enumerate(
                canciones_categoria
            ):

                with columnas_canciones[
                    indice % 3
                ]:

                    st.markdown(
                        f"### 🎵 {cancion.get('titulo', 'Sin título')}"
                    )

                    st.write(
                        f"**Artista:** "
                        f"{cancion.get('artista', 'Desconocido')}"
                    )

                    st.caption(
                        cancion.get(
                            "descripcion",
                            ""
                        )
                    )


        # ----------------------------------------------------
        # BIBLIOTECA
        # ----------------------------------------------------

        st.divider()

        st.header("🎵 Biblioteca")

        st.write(
            f"{len(canciones)} canciones disponibles"
        )

        # ----------------------------------------------------
        # FILTRO DE BIBLIOTECA
        # ----------------------------------------------------

        filtro = st.text_input(
            "🔎 Filtrar biblioteca",
            placeholder=(
                "Busca por título, artista o género..."
            ),
            key="filtro_biblioteca"
        )

        canciones_filtradas = canciones

        if filtro.strip():

            texto = filtro.lower().strip()

            canciones_filtradas = [
                cancion
                for cancion in canciones
                if (
                    texto in cancion.get(
                        "titulo",
                        ""
                    ).lower()
                    or
                    texto in cancion.get(
                        "artista",
                        ""
                    ).lower()
                    or
                    texto in cancion.get(
                        "genero",
                        ""
                    ).lower()
                )
            ]


        # ----------------------------------------------------
        # MOSTRAR BIBLIOTECA
        # ----------------------------------------------------

        columnas = st.columns(3)

        for indice, cancion in enumerate(
            canciones_filtradas
        ):

            with columnas[
                indice % 3
            ]:

                st.markdown(
                    f"### 🎵 {cancion.get('titulo', 'Sin título')}"
                )

                st.write(
                    f"**{cancion.get('artista', 'Desconocido')}**"
                )

                st.caption(
                    cancion.get(
                        "genero",
                        "Sin género"
                    )
                )

                with st.expander(
                    "Ver descripción"
                ):

                    st.write(
                        cancion.get(
                            "descripcion",
                            ""
                        )
                    )


# ============================================================
# BUSCAR CANCIONES
# ============================================================

with tab_buscar:

    st.header("🔎 Buscar canciones")

    st.write(
        "Describe qué quieres escuchar y SoundFlow "
        "encontrará canciones relacionadas "
        "semánticamente."
    )

    consulta = st.text_input(
        "¿Qué quieres escuchar?",
        placeholder=(
            "Ejemplo: salsa romántica, "
            "rap, música para entrenar..."
        ),
        key="consulta_busqueda"
    )

    buscar = st.button(
        "🔎 Buscar canciones",
        type="primary"
    )

    if buscar:

        if not consulta.strip():

            st.warning(
                "Escribe una consulta para buscar."
            )

        else:

            with st.spinner(
                "🤖 Analizando tu búsqueda..."
            ):

                try:

                    resultados = buscar_canciones(
                        consulta
                    )

                    if not resultados:

                        st.info(
                            "No se encontraron canciones "
                            "relacionadas."
                        )

                    else:

                        st.success(
                            f"Se encontraron "
                            f"{len(resultados)} resultados."
                        )

                        for indice, cancion in enumerate(
                            resultados,
                            start=1
                        ):

                            st.subheader(
                                f"🎵 {indice}. "
                                f"{cancion.get('titulo', 'Sin título')}"
                            )

                            st.write(
                                f"**Artista:** "
                                f"{cancion.get('artista', 'Desconocido')}"
                            )

                            st.write(
                                f"**Género:** "
                                f"{cancion.get('genero', '')}"
                            )

                            st.write(
                                f"**Descripción:** "
                                f"{cancion.get('descripcion', '')}"
                            )

                            similitud = cancion.get(
                                "similitud"
                            )

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

                                    pass

                            st.divider()

                except Exception as error:

                    st.error(
                        "❌ Error realizando la búsqueda."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# AGREGAR CANCIÓN
# ============================================================

with tab_agregar:

    st.header("➕ Agregar canción")

    st.write(
        "Agrega una canción y SoundFlow generará "
        "automáticamente su embedding de 384 dimensiones."
    )

    with st.form(
        "formulario_cancion"
    ):

        titulo = st.text_input(
            "Título *",
            placeholder="Ejemplo: Innerbloom"
        )

        artista = st.text_input(
            "Artista *",
            placeholder="Ejemplo: RÜFÜS DU SOL"
        )

        genero = st.text_input(
            "Género *",
            placeholder="Ejemplo: Electrónica / Deep House"
        )

        descripcion = st.text_area(
            "Descripción *",
            placeholder=(
                "Describe el estilo, emociones, "
                "energía y características de la canción."
            ),
            height=150
        )

        enviar = st.form_submit_button(
            "🎵 Guardar canción",
            type="primary"
        )

    if enviar:

        if not titulo.strip():

            st.error(
                "❌ El título es obligatorio."
            )

        elif not artista.strip():

            st.error(
                "❌ El artista es obligatorio."
            )

        elif not genero.strip():

            st.error(
                "❌ El género es obligatorio."
            )

        elif not descripcion.strip():

            st.error(
                "❌ La descripción es obligatoria."
            )

        else:

            with st.spinner(
                "🤖 Generando embedding..."
            ):

                try:

                    respuesta = agregar_cancion(
                        titulo=titulo.strip(),
                        artista=artista.strip(),
                        genero=genero.strip(),
                        descripcion=descripcion.strip()
                    )

                    if respuesta.data:

                        obtener_canciones.clear()

                        st.success(
                            "✅ Canción agregada correctamente."
                        )

                        st.info(
                            "🤖 Embedding de 384 dimensiones "
                            "generado automáticamente."
                        )

                        st.write(
                            f"**Canción:** "
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

                    else:

                        st.warning(
                            "La operación terminó, "
                            "pero Supabase no devolvió datos."
                        )

                except Exception as error:

                    st.error(
                        "❌ Error agregando la canción."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎵 SoundFlow")

    st.write(
        "Sistema de búsqueda semántica musical."
    )

    st.divider()

    st.write("**Modelo de embeddings**")
    st.code("all-MiniLM-L6-v2")

    st.write("**Dimensión**")
    st.code("384")

    st.write("**Base de datos**")
    st.code("Supabase")

    st.write("**Motor**")
    st.code("PostgreSQL + pgvector")

    st.write("**Umbral**")
    st.code("0.35")

    st.write("**Resultados máximos**")
    st.code("5")