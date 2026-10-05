"""Acceso a datos de canciones almacenadas en Supabase.

El patrón Repository concentra las consultas para que servicios y vistas no
dependan de detalles de PostgREST, tablas o RPC. Esta es la única capa del
proyecto que ejecuta ``table()`` o ``rpc()`` para canciones.
"""

from data.supabase_client import get_supabase_client
from config.settings import MATCH_COUNT, MATCH_THRESHOLD, SEARCH_FUNCTION, SONGS_TABLE


class SongRepository:
    """Encapsula las operaciones de persistencia y búsqueda musical."""

    def __init__(self, client=None):
        """Acepta un cliente existente o solicita el cliente compartido."""
        self.client = client or get_supabase_client()

    def get_all(self):
        """Obtiene los campos que necesita la biblioteca de la interfaz."""
        return (
            self.client.table(SONGS_TABLE)
            .select("id,titulo,artista,genero,descripcion")
            .order("id")
            .execute().data
        )

    def insert(self, song: dict):
        """Inserta en la tabla el registro de canción ya preparado por el servicio."""
        return self.client.table(SONGS_TABLE).insert(song).execute()

    def search(self, query_embedding: list[float], query_text: str):
        """Ejecuta la búsqueda semántica mediante la RPC existente.

        Se envían los nombres de parámetros que espera
        ``buscar_canciones()``: vector, texto original, umbral y cantidad.
        PostgreSQL + pgvector comparan el vector con los almacenados y devuelven
        las coincidencias, incluida la medida de similitud.

        Args:
            query_embedding: Vector de la consulta generado por el servicio.
            query_text: Consulta original, conservada para la RPC.

        Returns:
            Filas devueltas por Supabase para la consulta.
        """
        return self.client.rpc(
            SEARCH_FUNCTION,
            {
                "query_embedding": query_embedding,
                "query_text": query_text.strip(),
                "match_threshold": MATCH_THRESHOLD,
                "match_count": MATCH_COUNT,
            },
        ).execute().data

    def find_by_title_artist(self, title: str, artist: str):
        """Busca una canción concreta para una operación de mantenimiento."""
        return (
            self.client.table(SONGS_TABLE)
            .select("id,titulo,artista,genero,descripcion")
            .eq("titulo", title)
            .eq("artista", artist)
            .execute().data
        )

    def update_embedding(self, song_id, embedding: list[float]):
        """Actualiza únicamente la columna vectorial del registro indicado."""
        return (
            self.client.table(SONGS_TABLE)
            .update({"embedding": embedding})
            .eq("id", song_id)
            .execute()
        )
