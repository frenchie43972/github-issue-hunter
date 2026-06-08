"""Database helpers for the backend.

This module owns low-level PostgreSQL connection behavior for the FastAPI app.
It provides issue query functions that can build on the same connection pattern.
"""

import psycopg

from app.config import settings

def check_database_connection() -> bool:
  with psycopg.connect(settings.database_url) as conn:
    with conn.cursor() as cur:
      cur.execute('SELECT 1;')
      result = cur.fetchone()
      
  return result == (1,)