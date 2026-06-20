import httpx


class ArxivClient:
    """
    Thin HTTP client for the arXiv API.

    Design principle:
    - This layer MUST NOT contain business logic
    - It only knows how to fetch raw data from arXiv
    - It returns raw XML so parsing logic can evolve independently

    Why isolation matters:
    - If arXiv changes API format → only this file is affected
    - If we switch providers → only this file changes
    - Makes testing easy (mock HTTP responses)
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def fetch(self, query: str, start: int = 0, max_results: int = 10) -> str:
        """
        Fetch raw XML response from arXiv API.

        Args:
            query: search term (e.g., "transformers", "llm", "diffusion")
            start: pagination offset
            max_results: number of papers to fetch

        Returns:
            Raw XML string from arXiv API
        """

        params = {
            "search_query": f"all:{query}",
            "start": start,
            "max_results": max_results,
        }

        # NOTE: we intentionally return raw XML here.
        # Parsing is handled in a separate module to maintain separation of concerns.
        response = httpx.get(self.BASE_URL, params=params, timeout=30.0)
        response.raise_for_status()

        return response.text