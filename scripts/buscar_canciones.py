"""Run semantic song search from the terminal."""

from services.song_service import SongService


def main():
    query = input("\n¿Qué tipo de canción estás buscando? ").strip()
    if not query:
        print("Escribe una consulta para buscar.")
        return
    try:
        results = SongService().search(query)
    except Exception as error:
        print("Error realizando la búsqueda:", error)
        return
    print("\nResultados para:", query)
    print("-" * 50)
    if not results:
        print("No se encontraron canciones.")
        return
    for song in results:
        print(f"Título: {song.get('titulo', 'Sin título')}")
        print(f"Artista: {song.get('artista', 'Desconocido')}")
        print(f"Similitud: {song.get('similitud', 0):.4f}\n")


if __name__ == "__main__":
    main()
