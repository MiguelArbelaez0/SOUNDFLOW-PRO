"""Vista de búsqueda semántica desde la perspectiva de la persona usuaria.

Recibe ``SongService`` para enviarle la consulta y presenta sus resultados.
La conversión a embedding y la llamada a Supabase pertenecen a capas
inferiores, de modo que esta vista solo maneja interacción y presentación.
"""

import streamlit as st


def render_search(song_service):
    """Recoge una consulta y presenta canciones y su cercanía semántica.

    La similitud mostrada es una medida de cercanía entre vectores; no es una
    probabilidad de que la canción sea correcta. La vista no crea esos vectores.

    Args:
        song_service: Servicio que convierte la consulta y realiza la búsqueda.
    """
    st.header("🔎 Buscar canciones")
    st.write("Describe lo que quieres escuchar y SoundFlow encontrará canciones semánticamente relacionadas.")
    query = st.text_input(
        "¿Qué quieres escuchar?",
        placeholder="Ejemplo: salsa, rap, música triste, música para entrenar...",
    )
    if not st.button("🔎 Buscar canciones", type="primary"):
        return
    if not query.strip():
        st.warning("Escribe una consulta para buscar.")
        return
    with st.spinner("🤖 Analizando tu búsqueda..."):
        try:
            results = song_service.search(query)
            if not results:
                st.info("No se encontraron canciones relacionadas.")
                return
            st.success(f"Se encontraron {len(results)} resultados.")
            for index, song in enumerate(results, start=1):
                st.subheader(f"🎵 {index}. {song.get('titulo', 'Sin título')}")
                st.write(f"**Artista:** {song.get('artista', 'Desconocido')}")
                st.write(f"**Género:** {song.get('genero', '')}")
                st.write(f"**Descripción:** {song.get('descripcion', '')}")
                similarity = song.get("similitud")
                if similarity is not None:
                    try:
                        similarity = float(similarity)
                        st.write(f"**Similitud:** {similarity * 100:.2f}%")
                        st.progress(min(max(similarity, 0.0), 1.0))
                    except (TypeError, ValueError):
                        pass
                st.divider()
        except Exception as error:
            st.error("❌ Error realizando la búsqueda.")
            st.code(str(error))
