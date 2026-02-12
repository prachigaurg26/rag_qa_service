from fastapi import APIRouter
from pydantic import BaseModel
import logging

from app.utils.text_splitter import split_text
from app.services.embedding import embed_text
from app.services.vector_store import vector_store

router = APIRouter()

logging.basicConfig(level=logging.INFO)

class IngestRequest(BaseModel):
    text: str
    source: str = "unknown"
    user_id: str = "default"   # ✅ ADDED (NO LOGIN)


@router.post("/ingest/")
def ingest_data(request: IngestRequest):

    logging.info(f"Ingest request from user: {request.user_id}")

    try:
        chunks = split_text(request.text)
        embeddings = embed_text(chunks)
    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        return {
            "message": "Ingestion failed",
            "num_chunks": 0,
            "source": request.source
        }

    metadata = []
    for chunk in chunks:
        metadata.append({
            "text": chunk,
            "source": request.source,
            "user_id": request.user_id
        })

    vector_store.add(embeddings, metadata)

    logging.info(f"Ingested {len(chunks)} chunks")

    return {
        "message": "Text ingested successfully",
        "num_chunks": len(chunks),
        "source": request.source
    }