"""Insert the project's sample songs through the shared SongService."""

from config.settings import EMBEDDING_DIMENSION
from services.song_service import SongService


SONGS = [
    {
        "titulo": "Rain Sounds",
        "artista": "Nature Sounds",
        "genero": "Sonidos de naturaleza",
        "descripcion": (
            "Sonidos suaves de lluvia cayendo sobre la naturaleza, ambiente tranquilo, "
            "agua, bosque y relajación. Ideal para dormir, meditar, descansar y reducir el estrés."
        ),
    },
    {
        "titulo": "Thunderstruck",
        "artista": "AC/DC",
        "genero": "Rock",
        "descripcion": (
            "Canción de rock muy energética, intensa y potente, ideal para entrenar en el gimnasio, "
            "hacer ejercicio, correr y mantener la motivación durante una rutina."
        ),
    },
    {
        "titulo": "Clair de Lune",
        "artista": "Claude Debussy",
        "genero": "Música clásica",
        "descripcion": (
            "Música clásica suave, calmada y relajante, perfecta para descansar, dormir, meditar "
            "y crear un ambiente tranquilo durante la noche."
        ),
    },
]


def main():
    service = SongService()
    for song in SONGS:
        print(f"\nProcesando: {song['titulo']}")
        response = service.add_song(**{
            "title": song["titulo"],
            "artist": song["artista"],
            "genre": song["genero"],
            "description": song["descripcion"],
        })
        print(f"Insertada: {song['titulo']}")
        print(f"Dimensiones del vector: {EMBEDDING_DIMENSION}")
        if not response.data:
            print("Aviso: Supabase no devolvió el registro insertado.")
    print("\n✅ Procesamiento terminado")


if __name__ == "__main__":
    main()
