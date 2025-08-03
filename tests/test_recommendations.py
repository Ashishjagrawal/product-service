import numpy as np
from app.ai.recommendations import cosine_similarity

def test_cosine_similarity_basic():
    a = np.array([1, 0])
    b = np.array([0, 1])
    c = np.array([1, 0])
    assert cosine_similarity(a, b) == 0.0
    assert cosine_similarity(a, c) == 1.0