"""
Ingestion pipeline orchestrates the full flow:

arXiv API → Parser → Paper objects → (DB layer later)

This module should contain NO HTTP logic or XML parsing.
It only coordinates steps.
"""

from research_search.ingestion.arxiv_client import ArxivClient
from research_search.ingestion.parser import ArxivParser


class IngestionPipeline:
    """
    High-level orchestration of ingestion workflow.

    This is the closest thing to a "business logic" layer in Phase 2.
    """

    def __init__(self):
        self.client = ArxivClient()
        self.parser = ArxivParser()

    def run(self, query: str, max_results: int = 10):
        """
        Run full ingestion pipeline.

        Steps:
        1. Fetch raw data from arXiv
        2. Parse XML into structured Paper objects
        3. (Future) deduplicate and store in DB

        Returns:
            List of Paper objects
        """

        # Step 1: Fetch raw XML
        xml_data = self.client.fetch(query=query, max_results=max_results)

        # Step 2: Convert to structured format
        papers = self.parser.parse(xml_data)

        # Step 3: Return normalized objects (DB layer added later)
        return papers