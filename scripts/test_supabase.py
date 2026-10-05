"""Read-only Supabase connectivity diagnostic."""

from repositories.song_repository import SongRepository


def main():
    try:
        songs = SongRepository().get_all()
        print("¡Puente establecido!")
        print(f"Canciones encontradas: {len(songs)}")
    except Exception as error:
        print("Error al conectar con Supabase:")
        print(error)


if __name__ == "__main__":
    main()
