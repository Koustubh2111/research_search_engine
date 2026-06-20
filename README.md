# research_search_engine
Phased development of a research search engine 


Basic Test
```
PYTHONPATH=src uvicorn research_search.api.app:app --reload
```
On terminal
```
curl http://localhost:8000/api/v1/health
```
Expected
```
{"status": "ok"}
```

