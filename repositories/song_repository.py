"""Supabase persistence operations for songs."""

from data.supabase_client import get_supabase_client
from config.settings import MATCH_COUNT, MATCH_THRESHOLD, SEARCH_FUNCTION, SONGS_TABLE


class SongRepository:
    def __init__(self, client=None):
        self.client = client or get_supabase_client()

    def get_all(self):
        return (
            self.client.table(SONGS_TABLE)
            .select("id,titulo,artista,genero,descripcion")
            .order("id")
            .execute().data
        )

    def insert(self, song: dict):
        return self.client.table(SONGS_TABLE).insert(song).execute()

    def search(self, query_embedding: list[float], query_text: str):
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
        return (
            self.client.table(SONGS_TABLE)
            .select("id,titulo,artista,genero,descripcion")
            .eq("titulo", title)
            .eq("artista", artist)
            .execute().data
        )

    def update_embedding(self, song_id, embedding: list[float]):
        return (
            self.client.table(SONGS_TABLE)
            .update({"embedding": embedding})
            .eq("id", song_id)
            .execute()
        )
