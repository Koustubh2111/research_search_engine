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
            │ - normalize fields  │
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