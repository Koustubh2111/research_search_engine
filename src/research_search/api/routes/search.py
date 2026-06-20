"""
Semantic Search API
====================

Exposes FAISS-based semantic search over arXiv papers.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from research_search.services.search_service import SearchService

router = APIRouter()

# Initialize once (important for performance)
service = SearchService()
service.build_index()


# -----------------------------
# REQUEST MODEL
# -----------------------------
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# -----------------------------
# ENDPOINT
# -----------------------------
@router.post("/semantic")
def semantic_search(request: SearchRequest):
    """
    Semantic search over research papers.

    Flow:
    query → embedding → FAISS → SQLite enrichment → response
    """

    results = service.search(
        query=request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "results": results
    }