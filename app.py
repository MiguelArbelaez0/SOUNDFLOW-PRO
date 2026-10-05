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
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODELO
# ============================================================

@st.cache_resource
def cargar_modelo():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


modelo = cargar_modelo()


# ============================================================
# EMBEDDING
# ============================================================

def generar_embedding(texto: str):

    embedding = modelo.encode(texto)

    return embedding.tolist()


# ============================================================
# TEXTO PARA EMBEDDING
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

    vector = generar_embedding(
        texto_embedding
    )

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

def buscar_canciones(
    texto_busqueda: str
):

    embedding = generar_embedding(
        texto_busqueda
    )

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
# CATEGORÍAS VISUALES
# ============================================================

def categoria_visual(genero):

    genero = genero.lower().strip()

    if "rock" in genero:
        return "🎸 Rock"

    if "salsa" in genero:
        return "💃 Salsa"

    if (
        "reggaetón" in genero
        or "reggaeton" in genero
        or "trap" in genero
    ):
        return "🔥 Reggaetón"

    if (
        "hip-hop" in genero
        or "hip hop" in genero
        or "rap" in genero
    ):
        return "🎤 Hip-Hop"

    if (
        "electrónica" in genero
        or "electronica" in genero
        or "house" in genero
    ):
        return "🎧 Electrónica"

    if "pop" in genero:
        return "🎶 Pop"

    if "regional" in genero:
        return "🌵 Regional"

    if "vallenato" in genero:
        return "🪗 Vallenato"

    if "bolero" in genero:
        return "🌹 Bolero"

    return "🎵 Otros"


# ============================================================
# AGRUPAR CANCIONES
# ============================================================

def agrupar_canciones(canciones):

    grupos = {}

    for cancion in canciones:

        genero = cancion.get(
            "genero",
            "Otros"
        )

        categoria = categoria_visual(
            genero
        )

        if categoria not in grupos:

            grupos[categoria] = []

        grupos[categoria].append(
            cancion
        )

    return grupos


# ============================================================
# HEADER
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
            "No hay canciones registradas."
        )

    else:

        grupos = agrupar_canciones(
            canciones
        )

        # ----------------------------------------------------
        # CATEGORÍAS
        # ----------------------------------------------------

        st.header(
            "🎧 Explora por categorías"
        )

        st.caption(
            "Selecciona una categoría para explorar sus canciones."
        )

        categorias = [
            "🌟 Todas",
            *grupos.keys()
        ]

        categoria_seleccionada = st.radio(
            "Categorías",
            categorias,
            horizontal=True,
            label_visibility="collapsed"
        )

        # ----------------------------------------------------
        # FILTRAR
        # ----------------------------------------------------

        if categoria_seleccionada == "🌟 Todas":

            canciones_mostradas = canciones

        else:

            canciones_mostradas = grupos.get(
                categoria_seleccionada,
                []
            )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        st.divider()

        if categoria_seleccionada == "🌟 Todas":

            st.header(
                "🎵 Toda tu música"
            )

        else:

            st.header(
                categoria_seleccionada
            )

        st.caption(
            f"{len(canciones_mostradas)} canciones"
        )

        # ----------------------------------------------------
        # CANCIONES
        # ----------------------------------------------------

        columnas = st.columns(3)

        for indice, cancion in enumerate(
            canciones_mostradas
        ):

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
                "Sin género"
            )

            descripcion = cancion.get(
                "descripcion",
                ""
            )

            with columnas[
                indice % 3
            ]:

                st.subheader(
                    f"🎵 {titulo}"
                )

                st.write(
                    f"**Artista:** {artista}"
                )

                st.caption(
                    f"🎧 {genero}"
                )

                with st.expander(
                    "Ver descripción"
                ):

                    st.write(
                        descripcion
                    )


# ============================================================
# BUSCAR
# ============================================================

with tab_buscar:

    st.header(
        "🔎 Buscar canciones"
    )

    st.write(
        "Describe lo que quieres escuchar "
        "y SoundFlow encontrará canciones "
        "semánticamente relacionadas."
    )

    consulta = st.text_input(
        "¿Qué quieres escuchar?",
        placeholder=(
            "Ejemplo: salsa, rap, "
            "música triste, música para entrenar..."
        )
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

                            st.subheader(
                                f"🎵 {indice}. {titulo}"
                            )

                            st.write(
                                f"**Artista:** {artista}"
                            )

                            st.write(
                                f"**Género:** {genero}"
                            )

                            st.write(
                                f"**Descripción:** "
                                f"{descripcion}"
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
# AGREGAR
# ============================================================

with tab_agregar:

    st.header(
        "➕ Agregar canción"
    )

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

    st.write("Modelo")
    st.code("all-MiniLM-L6-v2")

    st.write("Dimensión")
    st.code("384")

    st.write("Base de datos")
    st.code("Supabase")

    st.write("Motor")
    st.code("PostgreSQL + pgvector")

    st.write("Umbral")
    st.code("0.35")

    st.write("Resultados máximos")
    st.code("5")