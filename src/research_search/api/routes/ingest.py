from fastapi import APIRouter
from pydantic import BaseModel

from research_search.ingestion.pipeline import IngestionPipeline

router = APIRouter()

pipeline = IngestionPipeline()


# =========================================================
# REQUEST MODEL (Pydantic)
# =========================================================
class IngestRequest(BaseModel):
    """
    WHY PYDANTIC HERE?

    This model defines the *input contract* for the ingestion API.

    It ensures:
    - Query is always a string (prevents invalid API calls)
    - max_results is always an integer
    - Missing or malformed fields are rejected BEFORE pipeline execution

    In production ML systems, this prevents:
    - corrupt ingestion jobs
    - silent data quality issues
    - invalid downstream embeddings
    """

    query: str
    max_results: int = 10


# =========================================================
# RESPONSE MODEL (Pydantic)
# =========================================================
class IngestResponse(BaseModel):
    """
    WHY PYDANTIC HERE?

    This defines the *output contract* of the ingestion system.

    It ensures:
    - consistent API responses
    - predictable metrics for monitoring
    - stable interface for future services (UI, logs, orchestration)

    This is critical for observability in ML systems.
    """

    query: str
    fetched: int
    inserted: int
    skipped: int


# =========================================================
# ROUTE
# =========================================================
@router.post("/ingest/arxiv", response_model=IngestResponse)
def ingest_arxiv(request: IngestRequest):
    """
    Trigger arXiv ingestion pipeline.

    HIGH-LEVEL FLOW:
    1. Validate request (handled by Pydantic automatically)
    2. Run ingestion pipeline
    3. Return structured metrics response

    IMPORTANT:
    - This endpoint is synchronous (Phase 2 design choice)
    - Later we will convert this into async/background jobs
    - Later phases will add retries, logging, and observability
    """

    result = pipeline.run(
        query=request.query,
        max_results=request.max_results
    )

    return IngestResponse(
        query=request.query,
        fetched=result["fetched"],
        inserted=result["inserted"],
        skipped=result["skipped"],
    )