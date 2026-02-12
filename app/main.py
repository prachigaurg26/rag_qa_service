from fastapi import FastAPI
from app.api.ingest import router as ingest_router
from app.api.query import router as query_router

app = FastAPI(title="RAG QA Service")

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(query_router, prefix="/query", tags=["Query"])