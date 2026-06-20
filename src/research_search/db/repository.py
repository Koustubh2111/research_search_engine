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
    
    def get_all_papers(self):
        """
        Fetch all papers from SQLite for indexing.

        This is used by:
        - FAISS indexing pipeline
        - semantic search service

        Returns:
            List[Paper]
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, abstract, authors, categories,
                published, updated, url
            FROM papers
            """
        )

        rows = cursor.fetchall()
        conn.close()

        papers = []

        for r in rows:
            papers.append(
                Paper(
                    id=r[0],
                    title=r[1],
                    abstract=r[2],
                    authors=json.loads(r[3]),
                    categories=json.loads(r[4]),
                    published=r[5],  # keep as string for now (or parse later)
                    updated=r[6],
                    url=r[7],
                )
            )

        return papers