"""Formulario visual para incorporar canciones a la biblioteca.

La vista solicita título, artista, género y descripción, valida que no estén
vacíos y entrega esos datos a ``SongService``. No construye el texto vectorial,
no genera embeddings y no accede a Supabase directamente; el servicio coordina
ese flujo y esta vista comunica el resultado y actualiza la biblioteca en caché.
"""

import streamlit as st

from config.settings import EMBEDDING_DIMENSION


def render_add_song(song_service, refresh_songs):
    """Dibuja el formulario, valida sus campos y solicita guardar la canción.

    Tras el envío, el servicio construye el texto, ``EmbeddingService`` produce
    el vector de 384 dimensiones y ``SongRepository`` lo persiste en Supabase.
    Si la operación devuelve datos, se invalida el caché y se muestra éxito;
    si falla o no devuelve filas, se informa a la persona usuaria.

    Args:
        song_service: Servicio que coordina generación del embedding e inserción.
        refresh_songs: Función para invalidar el caché de la biblioteca.
    """
    st.header("➕ Agregar canción")
    st.write(
        "Agrega una canción y SoundFlow generará automáticamente su "
        f"embedding de {EMBEDDING_DIMENSION} dimensiones."
    )
    with st.form("formulario_cancion"):
        title = st.text_input("Título *", placeholder="Ejemplo: Innerbloom")
        artist = st.text_input("Artista *", placeholder="Ejemplo: RÜFÜS DU SOL")
        genre = st.text_input("Género *", placeholder="Ejemplo: Electrónica / Deep House")
        description = st.text_area(
            "Descripción *",
            placeholder="Describe el estilo, emociones, energía y características de la canción.",
            height=150,
        )
        submit = st.form_submit_button("🎵 Guardar canción", type="primary")
    if not submit:
        return
    values = [title, artist, genre, description]
    labels = ["El título", "El artista", "El género", "La descripción"]
    for value, label in zip(values, labels):
        if not value.strip():
            st.error(f"❌ {label} es obligatorio.")
            return
    with st.spinner("🤖 Generando embedding..."):
        try:
            response = song_service.add_song(
                title.strip(), artist.strip(), genre.strip(), description.strip()
            )
            if response.data:
                refresh_songs()
                st.success("✅ Canción agregada correctamente.")
                st.info(
                    "🤖 Embedding de "
                    f"{EMBEDDING_DIMENSION} dimensiones generado automáticamente."
                )
            else:
                st.warning("La operación terminó, pero Supabase no devolvió datos.")
        except Exception as error:
            st.error("❌ Error agregando la canción.")
            st.code(str(error))
