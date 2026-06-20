"""
Database session manager.

This file is responsible for:
- creating SQLite connection
- ensuring tables exist
- providing reusable DB session

In production, this would be replaced with:
- PostgreSQL + SQLAlchemy engine pool
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data/research_search.db")


def get_connection():
    """
    Create a database connection.

    Why this exists:
    - centralizes DB configuration
    - makes it easy to swap SQLite → Postgres later
    """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # enables dict-like access

    return conn