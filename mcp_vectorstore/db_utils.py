import os
import psycopg2
from psycopg2.extras import register_uuid, DictCursor

register_uuid()  # make sure UUID works transparently


def get_pg_conn():
    """Return a fresh Postgres connection to Supabase (blocking)."""
    dsn = (
        f"dbname={os.getenv('PG_DB')} "
        f"user={os.getenv('PG_USER')} "
        f"password={os.getenv('PG_PASS')} "
        f"host={os.getenv('PG_HOST')} "
        f"port={os.getenv('PG_PORT', 5432)}"
    )
    # Use DictCursor to get rows as dictionaries
    return psycopg2.connect(dsn, sslmode="require", cursor_factory=DictCursor)