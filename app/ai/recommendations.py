import numpy as np
from app.db.crud import get_product_by_id, get_embedding_by_product_id
from app.ai.embeddings import json_to_embedding
from sqlalchemy.orm import Session
from app.db.models import Embedding, Product
from fastapi import HTTPException

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(vec_a, vec_b) / (norm_a * norm_b)

def get_similar_products(db: Session, product_id: int, top_k: int = 5):
    anchor_product = get_product_by_id(db, product_id)
    if not anchor_product:
        raise HTTPException(status_code=404, detail="Product not found")

    anchor_emb_row = get_embedding_by_product_id(db, product_id)
    if not anchor_emb_row or not anchor_emb_row.vector:
        return []

    anchor_vec = json_to_embedding(anchor_emb_row.vector)

    # Correct query: get Embedding and Product, exclude anchor product
    embeddings = db.query(Embedding, Product).join(Product, Embedding.product_id == Product.id).filter(Product.id != product_id).all()

    if not embeddings:
        return []

    vectors = []
    products = []
    for emb, prod in embeddings:
        if emb.vector:
            vectors.append(json_to_embedding(emb.vector))
            products.append(prod)

    if not vectors:
        return []

    vectors_np = np.vstack(vectors)
    anchor_vec = anchor_vec.reshape(1, -1)

    # Cosine similarity calculation
    dot_prods = np.dot(vectors_np, anchor_vec.T).flatten()
    norms = np.linalg.norm(vectors_np, axis=1) * np.linalg.norm(anchor_vec)
    sim_scores = np.divide(dot_prods, norms, out=np.zeros_like(dot_prods), where=norms!=0)

    top_k_indices = np.argsort(sim_scores)[::-1][:top_k]

    similar_products = [products[i] for i in top_k_indices]

    return similar_products