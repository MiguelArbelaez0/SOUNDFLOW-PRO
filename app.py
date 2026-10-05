"""SoundFlow Streamlit entry point and navigation."""

import streamlit as st

from config.settings import EMBEDDING_DIMENSION, MATCH_COUNT, MATCH_THRESHOLD, MODEL_NAME
from services.song_service import SongService
from ui.add_song import render_add_song
from ui.home import render_home
from ui.search import render_search
from ui.styles import apply_styles


@st.cache_data(ttl=30)
def _get_songs():
    return SongService().get_songs()


def main():
    st.set_page_config(
        page_title="SoundFlow",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    apply_styles()
    service = SongService()
    st.title("🎵 SoundFlow")
    st.write("Descubre música por significado, género y emociones.")

    home_tab, search_tab, add_tab = st.tabs(
        ["🏠 Inicio", "🔎 Buscar canciones", "➕ Agregar canción"]
    )
    with home_tab:
        render_home(_get_songs())
    with search_tab:
        render_search(service)
    with add_tab:
        render_add_song(service, _get_songs.clear)

    with st.sidebar:
        st.title("🎵 SoundFlow")
        st.write("Sistema de búsqueda semántica musical.")
        st.divider()
        st.write("Modelo")
        st.code(MODEL_NAME)
        st.write("Dimensión")
        st.code(str(EMBEDDING_DIMENSION))
        st.write("Base de datos")
        st.code("Supabase")
        st.write("Motor")
        st.code("PostgreSQL + pgvector")
        st.write("Umbral")
        st.code(str(MATCH_THRESHOLD))
        st.write("Resultados máximos")
        st.code(str(MATCH_COUNT))


if __name__ == "__main__":
    main()
