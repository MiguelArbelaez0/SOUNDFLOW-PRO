"""Representación vectorial del texto musical.

Un embedding convierte texto en una lista de números que permite comparar
significados mediante cercanía vectorial. SoundFlow usa
``all-MiniLM-L6-v2`` para canciones y consultas; mantener el mismo modelo
coloca ambos tipos de texto en un espacio común de 384 dimensiones.

Flujos:
* Canción: título + artista + género + descripción → texto → embedding.
* Búsqueda: consulta del usuario → embedding comparable con las canciones.

Este módulo carga y utiliza el modelo, pero no conoce la interfaz ni guarda
datos en Supabase.
"""

import streamlit as st
from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_DIMENSION, MODEL_NAME


@st.cache_resource
def _load_model() -> SentenceTransformer:
    """Carga una única instancia compartida del modelo de lenguaje.

    El modelo es costoso de inicializar. El caché de recursos de Streamlit
    lo mantiene en memoria entre interacciones y búsquedas.
    """
    return SentenceTransformer(MODEL_NAME)


class EmbeddingService:
    """Construye el texto de una canción y lo convierte en un vector.

    Las consultas usan el mismo codificador que las canciones para que
    PostgreSQL pueda compararlas en el mismo espacio vectorial.
    """

    @staticmethod
    def build_song_text(
        title: str, artist: str, genre: str, description: str
    ) -> str:
        """Combina los cuatro campos que describen semánticamente una canción.

        Args:
            title: Título de la canción.
            artist: Nombre del artista.
            genre: Género musical.
            description: Descripción de estilo, ambiente o contenido.

        Returns:
            Texto unificado que se utilizará para generar el embedding.
        """
        return (
            f"Título: {title}. Artista: {artist}. Género: {genre}. "
            f"Descripción: {description}."
        )

    def generate(self, text: str) -> list[float]:
        """Convierte texto en el vector de salida de all-MiniLM-L6-v2.

        Se usa para consultas y para el texto de canciones. Verificar la
        dimensión detecta incompatibilidades antes de enviar el vector a la BD.

        Args:
            text: Texto que se representará como embedding.

        Returns:
            Lista de valores float con 384 componentes.
        """
        vector = _load_model().encode(text).tolist()
        if len(vector) != EMBEDDING_DIMENSION:
            raise ValueError(
                f"El modelo generó {len(vector)} dimensiones; "
                f"se esperaban {EMBEDDING_DIMENSION}."
            )
        return vector

    def generate_song(self, song: dict) -> list[float]:
        """Genera el embedding de una canción usando el formato compartido.

        ``song`` debe incluir título, artista y descripción; el género puede
        faltar en registros antiguos y entonces se representa como texto vacío.

        Args:
            song: Datos de canción con las claves usadas por la tabla.

        Returns:
            Embedding de 384 dimensiones para esos datos.
        """
        return self.generate(
            self.build_song_text(
                title=song["titulo"],
                artist=song["artista"],
                genre=song.get("genero", ""),
                description=song["descripcion"],
            )
        )
