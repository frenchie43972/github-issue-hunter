"""Database connectivity check 

Its only job is to prove that the collector
can connect to PostgreSQL using DATABASE_URL from the root .env file.
"""

import psycopg # type: ignore

from collector.config import settings

def check_database_connection() -> None:
  """Connect to PostgreSQL and count rows in the github_issues table."""
  with psycopg.connect(settings.database_url) as conn:
    with conn.cursor() as cur:
      cur.execute('SELECT COUNT(*) FROM github_issues;')
      row = cur.fetchone()
      
  print(f'Database connection successful. github_issues tow count: {row[0]}')
  
if __name__ == '__main__':
  check_database_connection()