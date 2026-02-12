from typing import List, Dict
import logging

from app.services.embedding import embed_text
from app.services.vector_store import vector_store

logging.basicConfig(level=logging.INFO)

def retrieve_context(question: str, top_k: int = 3) -> List[Dict]:

    logging.info("Retrieving context")

    query_embedding = embed_text([question])[0]
    results = vector_store.search(query_embedding, top_k=top_k)

    return results