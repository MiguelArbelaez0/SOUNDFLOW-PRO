"""Lógica de negocio que coordina canciones, embeddings y persistencia.

La capa de servicio evita que Streamlit y los scripts deban conocer el orden
de los pasos o cómo se conectan el codificador y el repositorio. No presenta
componentes visuales ni ejecuta directamente consultas de Supabase.
"""

from core.embeddings import EmbeddingService
from repositories.song_repository import SongRepository


class SongService:
    """Orquesta los casos de uso principales de la biblioteca musical."""

    def __init__(self, repository=None, embeddings=None):
        """Permite usar dependencias compartidas o crear las predeterminadas."""
        self.repository = repository or SongRepository()
        self.embeddings = embeddings or EmbeddingService()

    def get_songs(self):
        """Entrega al consumidor la biblioteca obtenida por el repositorio."""
        return self.repository.get_all()

    def add_song(self, title: str, artist: str, genre: str, description: str):
        """Prepara una canción, genera su embedding y solicita guardarla.

        El texto y el vector se generan aquí en coordinación con
        ``EmbeddingService``; ``SongRepository`` se ocupa de la inserción.
        Así la UI solo entrega campos y recibe el resultado de persistencia.
        """
        song = {
            "titulo": title,
            "artista": artist,
            "genero": genre,
            "descripcion": description,
        }
        song["embedding"] = self.embeddings.generate_song(song)
        return self.repository.insert(song)

    def search(self, query: str):
        """Convierte la consulta en vector y devuelve sus coincidencias.

        Flujo: consulta → ``EmbeddingService`` → vector → ``SongRepository``
        → RPC ``buscar_canciones()`` → resultados.

        Args:
            query: Texto escrito por la persona que busca música.

        Returns:
            Resultados de la búsqueda semántica, con los campos de la RPC.
        """
        embedding = self.embeddings.generate(query)
        return self.repository.search(embedding, query)

    def update_song_embedding(self, song: dict):
        """Regenera el vector de una canción y actualiza solo ese campo."""
        embedding = self.embeddings.generate_song(song)
        return self.repository.update_embedding(song["id"], embedding)
