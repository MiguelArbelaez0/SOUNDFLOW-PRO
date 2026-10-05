"""Create the shared Supabase client from local environment settings."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Configura SUPABASE_URL y SUPABASE_KEY en .env.")
    return create_client(url, key)
