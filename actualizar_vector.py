from database import supabase
from sentence_transformers import SentenceTransformer

# Cargar modelo
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Buscar Rain Sounds
respuesta = (
    supabase
    .table("canciones_vectoriales")
    .select("id, titulo, artista, descripcion")
    .eq("titulo", "Rain Sounds")
    .eq("artista", "Nature Sounds")
    .execute()
)

if not respuesta.data:
    print("❌ No se encontró Rain Sounds")
    exit()

cancion = respuesta.data[0]

print("Canción encontrada:")
print(f"Título: {cancion['titulo']}")
print(f"Artista: {cancion['artista']}")
print(f"ID: {cancion['id']}")
print(f"Descripción: {cancion['descripcion']}")

# Generar nuevo embedding
embedding = modelo.encode(cancion["descripcion"]).tolist()

print(f"\nDimensiones del nuevo vector: {len(embedding)}")

# Actualizar solamente el embedding
supabase \
    .table("canciones_vectoriales") \
    .update({"embedding": embedding}) \
    .eq("id", cancion["id"]) \
    .execute()

print("\n✅ VECTOR ACTUALIZADO CORRECTAMENTE")