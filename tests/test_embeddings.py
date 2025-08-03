from app.ai.embeddings import get_embedding
import numpy as np

def test_get_embedding_returns_vector():
    vec = get_embedding("some text")
    assert isinstance(vec, (list, np.ndarray))
    assert len(vec) > 0