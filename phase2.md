Research Paper Ingestion (arXiv → Structured Data Layer)
```
            ┌────────────────────┐
            │  FastAPI Endpoint  │
            │ /ingest/arxiv      │
            └─────────┬──────────┘
                      │
                      ▼
            ┌────────────────────┐
            │ Ingestion Service  │
            │ - fetch arXiv API  │
            │ - pagination       │
            └─────────┬──────────┘
                      ▼
            ┌────────────────────┐
            │ Parser Layer       │
            │ - XML → JSON       │
            │ - normalize fields │
            └─────────┬──────────┘
                      ▼
            ┌────────────────────┐
            │ Data Model Layer   │
            │ Paper schema       │
            └─────────┬──────────┘
                      ▼
            ┌────────────────────┐
            │ Database (SQLite   │
            │ for Phase 2)       │
            └────────────────────┘
```

So far: 

```
FastAPI Layer
    ↓
Ingestion API (/ingest/arxiv)
    ↓
IngestionPipeline
    ↓
ArxivClient (HTTP layer)
    ↓
Arxiv XML Feed
    ↓
ArxivParser (XML → Paper objects)
    ↓
Deduplication Layer (SQLite check)
    ↓
PaperRepository
    ↓
SQLite Storage (papers table)
```

```
curl -X POST "http://127.0.0.1:8000/api/v1/ingest/arxiv" \
-H "Content-Type: application/json" \
-d '{"query":"transformers","max_results":5}'

Expectation - {"query":"transformers","fetched":5,"inserted":5,"skipped":0}% 

```