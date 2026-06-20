```
User Query
    ↓
Embedding Model
    ↓
Vector DB (pgvector / FAISS)
    ↓
Top-K retrieval
    ↓
(optional reranker later)
    ↓
Search results API
```

```
            ┌─────────────────────┐
            │   FastAPI Layer     │
            └─────────┬───────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
Ingestion API                Search API (NEW)
        │                           │
        ↓                           ↓
SQLite (papers)          Embedding Service (NEW)
        │                           │
        └─────────────┬─────────────┘
                      ↓
              Vector Store (NEW)
            (FAISS or pgvector)
                      ↓
             Top-K semantic results
```