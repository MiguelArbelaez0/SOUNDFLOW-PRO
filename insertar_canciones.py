from database import supabase
from sentence_transformers import SentenceTransformer

# Cargar el modelo que genera vectores de 384 dimensiones
modelo = SentenceTransformer("all-MiniLM-L6-v2")

canciones = [
    {
        "titulo": "Weightless",
        "artista": "Marconi Union",
        "descripcion": "Música muy tranquila y relajante para dormir y descansar."
    },
    {
        "titulo": "Eye of the Tiger",
        "artista": "Survivor",
        "descripcion": "Canción energética y motivadora para hacer ejercicio y entrenar."
    }
]

for cancion in canciones:
    embedding = modelo.encode(cancion["descripcion"]).tolist()

    datos = {
        "titulo": cancion["titulo"],
        "artista": cancion["artista"],
        "descripcion": cancion["descripcion"],
        "embedding": embedding
    }

    respuesta = supabase.table("canciones_vectoriales").insert(datos).execute()

    print(f"Insertada: {cancion['titulo']}")
    print(f"Dimensiones del vector: {len(embedding)}")

print("¡Canciones insertadas correctamente!")