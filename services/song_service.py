"""Coordinate song embedding generation and persistence/search."""

from core.embeddings import EmbeddingService
from repositories.song_repository import SongRepository


class SongService:
    def __init__(self, repository=None, embeddings=None):
        self.repository = repository or SongRepository()
        self.embeddings = embeddings or EmbeddingService()

    def get_songs(self):
        return self.repository.get_all()

    def add_song(self, title: str, artist: str, genre: str, description: str):
        song = {
            "titulo": title,
            "artista": artist,
            "genero": genre,
            "descripcion": description,
        }
        song["embedding"] = self.embeddings.generate_song(song)
        return self.repository.insert(song)

    def search(self, query: str):
        embedding = self.embeddings.generate(query)
        return self.repository.search(embedding, query)

    def update_song_embedding(self, song: dict):
        embedding = self.embeddings.generate_song(song)
        return self.repository.update_embedding(song["id"], embedding)
