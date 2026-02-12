import faiss
import numpy as np
from typing import List, Dict

VECTOR_DIM = 384

class VectorStore:
    def __init__(self, dim: int = VECTOR_DIM):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata: List[Dict] = []

    def add(self, embeddings: List[List[float]], metadata: List[Dict]):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_embedding: List[float], top_k: int = 3):
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.metadata[idx])

        return results

vector_store = VectorStore()