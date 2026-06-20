"""
Database schema definition.

This is the SOURCE OF TRUTH for how papers are stored.

We intentionally keep schema simple in Phase 2.
"""

from .session import get_connection


def create_tables():
    """
    Create tables if they do not exist.

    Why explicit schema creation matters:
    - makes system reproducible
    - avoids "it worked locally" DB drift
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT,
            abstract TEXT,
            authors TEXT,
            categories TEXT,
            published TEXT,
            updated TEXT,
            url TEXT
        )
        """
    )

    conn.commit()
    conn.close()