
from typing import List
import numpy as np

VECTOR_DIM = 384

def embed_text(texts: List[str]) -> List[List[float]]:
    """
    Dummy embedding (task-friendly)
    """
    embeddings = []
    for text in texts:
        np.random.seed(abs(hash(text)) % (10**8))
        embeddings.append(np.random.rand(VECTOR_DIM).tolist())
    return embeddings