"""
Repository layer for database operations.

This isolates ALL SQL logic from business logic.

Pipeline should NEVER write SQL directly.
"""

import json
from typing import Optional

from .session import get_connection
from research_search.models.paper import Paper


class PaperRepository:
    """
    Handles all database operations for Paper objects.
    """

    def insert_paper(self, paper: Paper) -> None:
        """
        Insert paper into database.

        Deduplication is enforced at DB level via PRIMARY KEY (id).
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO papers (
                id, title, abstract, authors, categories,
                published, updated, url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                paper.id,
                paper.title,
                paper.abstract,
                json.dumps(paper.authors),
                json.dumps(paper.categories),
                paper.published.isoformat(),
                paper.updated.isoformat() if paper.updated else None,
                paper.url,
            ),
        )

        conn.commit()
        conn.close()

    def exists(self, paper_id: str) -> bool:
        """
        Check if paper already exists (dedup helper).
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM papers WHERE id = ?",
            (paper_id,),
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None