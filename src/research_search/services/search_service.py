"""
Search Service (Integrated version)
===================================

Now connects:
- SQLite (Phase 2)
- Embeddings (Phase 3)
- FAISS vector store

This is the first end-to-end retrieval system.
"""

import numpy as np

from research_search.embeddings.embedder import Embedder
from research_search.vectorstore.faiss_store import FaissStore
from research_search.db.repository import PaperRepository


class SearchService:
    """
    Full retrieval pipeline:
    SQLite → Embeddings → FAISS → Results
    """

    def __init__(self, embedding_dim: int = 384):
        self.embedder = Embedder()
        self.vector_store = FaissStore(dimension=embedding_dim)
        self.repo = PaperRepository()

        # In-memory cache (for simplicity in Phase 3)
        self.paper_cache = {}

    # -----------------------------
    # STEP 1: BUILD INDEX FROM DB
    # -----------------------------
    def build_index(self):
        """
        Loads all papers from SQLite and builds FAISS index.

        This is your "offline indexing step".
        """

        papers = self.repo.get_all_papers()

        texts = []
        ids = []

        for p in papers:
            text = f"{p.title} {p.abstract}"
            texts.append(text)
            ids.append(p.id)

            # cache full paper for later retrieval
            self.paper_cache[p.id] = p

        embeddings = self.embedder.embed_batch(texts)

        self.vector_store.add(
            np.array(embeddings).astype("float32"),
            ids
        )

        print(f"Indexed {len(papers)} papers into FAISS")

    # -----------------------------
    # STEP 2: SEMANTIC SEARCH
    # -----------------------------
    def search(self, query: str, top_k: int = 5):
        """
        Full semantic search pipeline.
        """

        query_vec = self.embedder.embed(query)
        query_vec = np.array([query_vec]).astype("float32")

        results = self.vector_store.search(query_vec, top_k)

        enriched = []
        for paper_id, score in results:
            paper = self.paper_cache.get(paper_id)

            if paper:
                enriched.append({
                    "id": paper.id,
                    "title": paper.title,
                    "abstract": paper.abstract,
                    "score": score
                })

        return enriched