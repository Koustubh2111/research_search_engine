FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn

#Must be set for the API to find the src directory
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "research_search.api.app:app", "--host", "0.0.0.0", "--port", "8000"]`