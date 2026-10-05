"""Creación centralizada del cliente de Supabase.

Lee la URL y la clave desde el entorno (normalmente cargadas desde ``.env``)
y devuelve el cliente reutilizable. Mantener las credenciales fuera del código
evita exponerlas en archivos fuente. Este módulo no realiza consultas de canciones.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """Carga las credenciales locales y obtiene el cliente Supabase cacheado.

    Flujo: ``.env`` → ``SUPABASE_URL`` y ``SUPABASE_KEY`` → cliente.
    Los valores secretos se usan para crear la conexión y nunca se imprimen.

    Returns:
        Cliente oficial de Supabase para que lo utilice el repositorio.

    Raises:
        RuntimeError: Si falta alguna variable requerida.
    """
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Configura SUPABASE_URL y SUPABASE_KEY en .env.")
    return create_client(url, key)
