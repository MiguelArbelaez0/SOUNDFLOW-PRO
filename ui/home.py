"""Home, category browsing, and song library view."""

import streamlit as st


def category_visual(genre: str) -> str:
    genre = genre.lower().strip()
    if "rock" in genre:
        return "🎸 Rock"
    if "salsa" in genre:
        return "💃 Salsa"
    if "reggaetón" in genre or "reggaeton" in genre or "trap" in genre:
        return "🔥 Reggaetón"
    if "hip-hop" in genre or "hip hop" in genre or "rap" in genre:
        return "🎤 Hip-Hop"
    if "electrónica" in genre or "electronica" in genre or "house" in genre:
        return "🎧 Electrónica"
    if "pop" in genre:
        return "🎶 Pop"
    if "regional" in genre:
        return "🌵 Regional"
    if "vallenato" in genre:
        return "🪗 Vallenato"
    if "bolero" in genre:
        return "🌹 Bolero"
    return "🎵 Otros"


def group_songs(songs: list[dict]) -> dict[str, list[dict]]:
    groups = {}
    for song in songs:
        category = category_visual(song.get("genero", "Otros"))
        groups.setdefault(category, []).append(song)
    return groups


def render_home(songs: list[dict]):
    if not songs:
        st.info("No hay canciones registradas.")
        return

    groups = group_songs(songs)
    st.header("🎧 Explora por categorías")
    st.caption("Selecciona una categoría para explorar sus canciones.")
    categories = ["🌟 Todas", *groups.keys()]
    selected = st.radio("Categorías", categories, horizontal=True, label_visibility="collapsed")
    shown = songs if selected == "🌟 Todas" else groups.get(selected, [])
    st.divider()
    st.header("🎵 Toda tu música" if selected == "🌟 Todas" else selected)
    st.caption(f"{len(shown)} canciones")
    columns = st.columns(3)
    for index, song in enumerate(shown):
        with columns[index % 3]:
            st.subheader(f"🎵 {song.get('titulo', 'Sin título')}")
            st.write(f"**Artista:** {song.get('artista', 'Desconocido')}")
            st.caption(f"🎧 {song.get('genero', 'Sin género')}")
            with st.expander("Ver descripción"):
                st.write(song.get("descripcion", ""))
