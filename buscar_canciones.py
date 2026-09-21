from database import supabase
from sentence_transformers import SentenceTransformer

# Cargar el modelo
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Pedir la búsqueda al usuario
consulta = input("\n¿Qué tipo de canción estás buscando? ")

# Convertir la consulta en vector
embedding = modelo.encode(consulta).tolist()

# Buscar canciones similares
respuesta = supabase.rpc(
    "buscar_canciones",
    {
        "query_embedding": embedding,
        "match_count": 5
    }
).execute()

# Mostrar resultados
print("\nResultados para:", consulta)
print("-" * 50)

if not respuesta.data:
    print("No se encontraron canciones.")
else:
    for cancion in respuesta.data:
        print(f"Título: {cancion['titulo']}")
        print(f"Artista: {cancion['artista']}")
        print(f"Similitud: {cancion['similitud']:.4f}")
        print()