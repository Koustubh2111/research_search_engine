"""
Embedding module
=================

Responsible for converting raw text (paper title + abstract)
into dense vector representations using a pretrained transformer model.

This is the core ML component of the retrieval system.

We use sentence-transformers because:
- fast inference
- strong semantic representations
- widely used in production RAG systems
"""

from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Wrapper around a sentence-transformer model.

    Responsibilities:
    - Load embedding model once
    - Convert text → vector embeddings
    - Support batch encoding for efficiency
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load pretrained transformer model
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        """
        Convert a single text string into a vector embedding.
        """
        return self.model.encode(text, normalize_embeddings=True)

    def embed_batch(self, texts: list[str]):
        """
        Convert multiple texts into embeddings efficiently.
        """
        return self.model.encode(texts, normalize_embeddings=True)