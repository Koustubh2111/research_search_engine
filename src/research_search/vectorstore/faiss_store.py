"""
FAISS Vector Store
===================

This module is responsible for:
- Storing embeddings (dense vectors)
- Performing similarity search
- Returning top-K nearest neighbors

FAISS = fast approximate nearest neighbor search library.

Used by:
- Google
- Meta
- OpenAI-like retrieval systems
"""

import faiss
import numpy as np


class FaissStore:
    """
    Simple FAISS-based vector store.

    Stores:
        - embeddings (numpy arrays)
        - mapping from index → paper_id
    """

    def __init__(self, dimension: int):
        # IndexFlatIP = cosine similarity (with normalized vectors)
        self.index = faiss.IndexFlatIP(dimension)

        # Maps FAISS index positions → paper IDs
        self.id_map = []

    def add(self, embeddings: np.ndarray, ids: list[str]):
        """
        Add embeddings to FAISS index.

        Args:
            embeddings: shape (n, d)
            ids: list of paper IDs
        """
        self.index.add(embeddings)
        self.id_map.extend(ids)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        """
        Perform semantic search.

        Returns:
            List of (paper_id, similarity_score)
        """

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.id_map[idx], float(score)))

        return results