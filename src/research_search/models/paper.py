from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Paper(BaseModel):
    """
    Canonical internal representation of an arXiv paper.

    This is the *core data contract* of the system.

    Every stage of the pipeline (ingestion → storage → retrieval → embeddings)
    must convert data into this format before passing it downstream.

    Why this matters:
    - Prevents leaking raw arXiv XML structures into the system
    - Ensures consistency across ingestion + search + future RAG pipeline
    - Makes downstream systems (vector DB, ranking, evaluation) deterministic
    """

    id: str = Field(..., description="Unique arXiv identifier (e.g., 1706.03762)")

    title: str
    abstract: str

    authors: list[str]

    categories: list[str]

    published: datetime

    updated: Optional[datetime] = None

    url: str

    # Optional fields reserved for future phases
    # (kept now to avoid schema migration pain later)
    pdf_url: Optional[str] = None