"""Valores compartidos por las capas de SoundFlow.

Centralizarlos evita que la interfaz, los servicios y los scripts diverjan
en la selección del modelo, el formato vectorial o los parámetros de búsqueda.
"""

# El mismo modelo debe representar tanto las canciones como las consultas.
MODEL_NAME = "all-MiniLM-L6-v2"
# all-MiniLM-L6-v2 produce vectores de salida de 384 dimensiones.
EMBEDDING_DIMENSION = 384
# Similitud mínima que la RPC debe aceptar para incluir una coincidencia.
MATCH_THRESHOLD = 0.35
# Número máximo de coincidencias solicitadas a la RPC.
MATCH_COUNT = 5
# Umbrales y límite del filtro final aplicado por SongService.
HIGH_RELEVANCE_THRESHOLD = 0.50
ACCEPTABLE_RELEVANCE_THRESHOLD = 0.40
MAX_RESULTS = 5
# Tabla existente de canciones y sus embeddings en Supabase.
SONGS_TABLE = "canciones_vectoriales"
# RPC existente que realiza la búsqueda vectorial en PostgreSQL/pgvector.
SEARCH_FUNCTION = "buscar_canciones"
