from database import supabase
from sentence_transformers import SentenceTransformer


# ============================================================
# CARGAR MODELO
# ============================================================

modelo = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# CANCIONES PARA LAS PRUEBAS DE LA ACTIVIDAD
# ============================================================

canciones = [

    {
        "titulo": "Rain Sounds",
        "artista": "Nature Sounds",
        "descripcion": (
            "Sonidos suaves de lluvia cayendo sobre la naturaleza, "
            "ambiente tranquilo, agua, bosque y relajación. "
            "Ideal para dormir, meditar, descansar y reducir el estrés."
        )
    },

    {
        "titulo": "Thunderstruck",
        "artista": "AC/DC",
        "descripcion": (
            "Canción de rock muy energética, intensa y potente, "
            "ideal para entrenar en el gimnasio, hacer ejercicio, "
            "correr y mantener la motivación durante una rutina."
        )
    },

    {
        "titulo": "Clair de Lune",
        "artista": "Claude Debussy",
        "descripcion": (
            "Música clásica suave, calmada y relajante, perfecta "
            "para descansar, dormir, meditar y crear un ambiente "
            "tranquilo durante la noche."
        )
    }

]


# ============================================================
# INSERTAR CANCIONES
# ============================================================

for cancion in canciones:

    print(f"\nProcesando: {cancion['titulo']}")

    # Crear embedding usando título + artista + descripción
    texto = (
        f"{cancion['titulo']}. "
        f"{cancion['artista']}. "
        f"{cancion['descripcion']}"
    )

    embedding = modelo.encode(
        texto,
        normalize_embeddings=True
    ).tolist()


    # Datos que se enviarán a Supabase
    datos = {
        "titulo": cancion["titulo"],
        "artista": cancion["artista"],
        "descripcion": cancion["descripcion"],
        "embedding": embedding
    }


    # Insertar
    respuesta = (
        supabase
        .table("canciones_vectoriales")
        .insert(datos)
        .execute()
    )


    print(f"Insertada: {cancion['titulo']}")
    print(f"Dimensiones del vector: {len(embedding)}")


print("\n========================================")
print("✅ Canciones insertadas correctamente")
print("========================================")