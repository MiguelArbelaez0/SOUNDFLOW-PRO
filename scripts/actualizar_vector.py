"""Herramienta de mantenimiento para regenerar el vector de Rain Sounds.

Localiza el registro con el repositorio y delega la generación y actualización
del embedding en las capas existentes. No implementa su propio codificador.
Al ejecutarse, modifica el embedding de esa canción en Supabase.
"""

from repositories.song_repository import SongRepository
from services.song_service import SongService
from config.settings import EMBEDDING_DIMENSION


def main():
    """Busca Rain Sounds, muestra sus datos y solicita regenerar su vector."""
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
