"""Lógica de negocio que coordina canciones, embeddings y persistencia.

La capa de servicio evita que Streamlit y los scripts deban conocer el orden
de los pasos o cómo se conectan el codificador y el repositorio. No presenta
componentes visuales ni ejecuta directamente consultas de Supabase.
"""

from core.embeddings import EmbeddingService
from repositories.song_repository import SongRepository
from config.settings import (
    ACCEPTABLE_RELEVANCE_THRESHOLD,
    HIGH_RELEVANCE_THRESHOLD,
    MAX_RESULTS,
)


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
        """Busca canciones y descarta candidatos con relevancia insuficiente.

        Flujo: consulta → ``EmbeddingService`` → vector → ``SongRepository``
        → RPC ``buscar_canciones()`` → resultados.

        Args:
            query: Texto escrito por la persona que busca música.

        Returns:
            Hasta ``MAX_RESULTS`` canciones relevantes, ordenadas por score.
        """
        if not isinstance(query, str) or not query.strip():
            return []

        embedding = self.embeddings.generate(query)
        candidates = self.repository.search(embedding, query)

        high_relevance = []
        acceptable_relevance = []
        for candidate in candidates or []:
            try:
                score = float(candidate.get("similitud"))
            except (AttributeError, TypeError, ValueError):
                continue

            if not score == score or score in (float("inf"), float("-inf")):
                continue
            normalized_score = round(score / 100, 10) if score > 1 else score
            if normalized_score < ACCEPTABLE_RELEVANCE_THRESHOLD:
                continue

            # No mutar el diccionario recibido del repositorio. Los scores
            # decimales originales se conservan; solo se escala formato %.
            result = candidate.copy()
            if score > 1:
                result["similitud"] = normalized_score
            entry = (normalized_score, result)
            if normalized_score >= HIGH_RELEVANCE_THRESHOLD:
                high_relevance.append(entry)
            else:
                acceptable_relevance.append(entry)

        ordered = sorted(high_relevance, key=lambda item: item[0], reverse=True)
        ordered.extend(sorted(acceptable_relevance, key=lambda item: item[0], reverse=True))
        return [result for _, result in ordered[:MAX_RESULTS]]

    def update_song_embedding(self, song: dict):
        """Regenera el vector de una canción y actualiza solo ese campo."""
        embedding = self.embeddings.generate_song(song)
        return self.repository.update_embedding(song["id"], embedding)
