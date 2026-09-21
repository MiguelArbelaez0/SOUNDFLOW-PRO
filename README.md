import pypandoc

readme = r"""# 🎵 SoundFlow

Sistema de recomendación de canciones basado en **búsqueda semántica con embeddings**.

SoundFlow permite escribir una descripción de lo que se quiere escuchar y encuentra las canciones más relacionadas según el significado de la consulta, aunque las palabras utilizadas no coincidan exactamente con las descripciones almacenadas.

## 📌 Descripción del proyecto

Este proyecto fue desarrollado como parte de la actividad de bases de datos y utiliza:

- **Python** como lenguaje principal.
- **Supabase / PostgreSQL** como base de datos.
- **pgvector** para almacenar y comparar vectores.
- **Sentence Transformers** para generar embeddings.
- **Streamlit** para la interfaz web.
- El modelo `all-MiniLM-L6-v2` para convertir textos en vectores de **384 dimensiones**.

El flujo general es:

```text
Consulta del usuario
        ↓
Sentence Transformer
        ↓
Embedding de 384 dimensiones
        ↓
Supabase + pgvector
        ↓
Búsqueda por similitud
        ↓
Canciones recomendadas
