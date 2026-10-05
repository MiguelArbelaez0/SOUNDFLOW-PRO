"""Regenerate and update Rain Sounds using shared services."""

from repositories.song_repository import SongRepository
from services.song_service import SongService
from config.settings import EMBEDDING_DIMENSION


def main():
    repository = SongRepository()
    songs = repository.find_by_title_artist("Rain Sounds", "Nature Sounds")
    if not songs:
        print("❌ No se encontró Rain Sounds")
        return
    song = songs[0]
    print("Canción encontrada:")
    print(f"Título: {song['titulo']}")
    print(f"Artista: {song['artista']}")
    print(f"ID: {song['id']}")
    print(f"Descripción: {song['descripcion']}")

    service = SongService(repository=repository)
    service.update_song_embedding(song)
    print(f"\nDimensiones del nuevo vector: {EMBEDDING_DIMENSION}")
    print("\n✅ VECTOR ACTUALIZADO CORRECTAMENTE")


if __name__ == "__main__":
    main()
