"""Song text preparation and cached sentence embeddings."""

import streamlit as st
from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_DIMENSION, MODEL_NAME


@st.cache_resource
def _load_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


class EmbeddingService:
    """Build consistent song text and encode text with the shared model."""

    @staticmethod
    def build_song_text(
        title: str, artist: str, genre: str, description: str
    ) -> str:
        return (
            f"Título: {title}. Artista: {artist}. Género: {genre}. "
            f"Descripción: {description}."
        )

    def generate(self, text: str) -> list[float]:
        vector = _load_model().encode(text).tolist()
        if len(vector) != EMBEDDING_DIMENSION:
            raise ValueError(
                f"El modelo generó {len(vector)} dimensiones; "
                f"se esperaban {EMBEDDING_DIMENSION}."
            )
        return vector

    def generate_song(self, song: dict) -> list[float]:
        return self.generate(
            self.build_song_text(
                title=song["titulo"],
                artist=song["artista"],
                genre=song.get("genero", ""),
                description=song["descripcion"],
            )
        )
