"""Diagnóstico de solo lectura para comprobar acceso a la biblioteca.

Usa el repositorio para realizar una consulta representativa y muestra el
número de filas; no imprime credenciales ni cambia datos.
"""

from repositories.song_repository import SongRepository


def main():
    """Consulta la biblioteca e informa si se pudo establecer conexión."""
    try:
        songs = SongRepository().get_all()
        print("¡Puente establecido!")
        print(f"Canciones encontradas: {len(songs)}")
    except Exception as error:
        print("Error al conectar con Supabase:")
        print(error)


if __name__ == "__main__":
    main()
