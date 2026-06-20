"""
Ingestion Pipeline (Core Orchestration Layer)

This module defines the end-to-end workflow for ingesting arXiv papers:

    arXiv API → Raw XML → Parsed Papers → Deduplication → Database Storage

This is the "brain" of Phase 2.

Design philosophy:
- NO HTTP logic here (handled by ArxivClient)
- NO parsing logic here (handled by Parser)
- NO SQL here (handled by Repository)
- ONLY orchestration and control flow

Why this separation matters:
In production ML systems, pipelines must be:
- testable (each dependency mockable)
- observable (metrics at each stage)
- replaceable (swap components independently)
"""

from research_search.ingestion.arxiv_client import ArxivClient
from research_search.ingestion.parser import ArxivParser
from research_search.db.repository import PaperRepository


class IngestionPipeline:
    """
    High-level orchestrator for ingestion workflow.

    This class coordinates all components required to:
    1. Fetch raw research data
    2. Convert it into structured objects
    3. Ensure deduplication
    4. Persist clean data

    Think of this as:
    → "workflow controller" or "ETL orchestrator"
    """

    def __init__(self):
        # External system connector (arXiv API)
        self.client = ArxivClient()

        # Data transformation layer (XML → Paper objects)
        self.parser = ArxivParser()

        # Persistence + deduplication layer (SQLite repository)
        self.repo = PaperRepository()

    def run(self, query: str, max_results: int = 10):
        """
        Execute full ingestion pipeline for a search query.

        Args:
            query: Search term for arXiv (e.g., "transformers", "diffusion models")
            max_results: Number of papers to fetch

        Returns:
            Dictionary with ingestion metrics:
            - fetched: total papers retrieved from arXiv
            - inserted: newly stored papers
            - skipped: already-existing papers (deduplicated)

        Why return metrics:
        - critical for observability
        - helps detect duplicates in upstream data
        - useful for debugging ingestion quality
        """

        # STEP 1: Fetch raw XML from arXiv API
        # At this stage, data is unstructured and noisy
        xml_data = self.client.fetch(query=query, max_results=max_results)

        # print("===== RAW XML START =====")
        # # print(xml_data[:1000])
        # print("===== RAW XML END =====")

        # STEP 2: Convert XML → structured Paper objects
        # This normalizes external data into internal schema
        papers = self.parser.parse(xml_data)

        print(f"Parsed {len(papers)} papers from arXiv response.")

        inserted = 0
        skipped = 0

        # STEP 3: Deduplication + persistence loop
        # Each paper is processed independently to ensure partial failure safety
        for paper in papers:

            # Check if we already processed this paper before
            # (prevents duplicate ingestion runs)
            if self.repo.exists(paper.id):
                skipped += 1
                continue

            # Store clean structured data
            self.repo.insert_paper(paper)
            inserted += 1

        # STEP 4: Return ingestion summary for observability
        return {
            "fetched": len(papers),
            "inserted": inserted,
            "skipped": skipped,
        }