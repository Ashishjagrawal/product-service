import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.db.crud import get_embedding_by_product_id, create_or_update_embedding, save_product_summary
from app.db.models import Product
from sqlalchemy.orm import Session
from app.ai.summaries import generate_summary_from_llm

# Load model once
MODEL_NAME = "paraphrase-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def get_embedding(text: str):
    if not text:
        # Return zero-vector if no text
        return np.zeros(model.get_sentence_embedding_dimension())
    emb = model.encode(text)
    return emb

def embedding_to_json(embedding: np.ndarray):
    return json.dumps(embedding.tolist())

def json_to_embedding(embedding_str: str):
    return np.array(json.loads(embedding_str))

def generate_and_store_embeddings_and_summaries(db: Session):
    products = db.query(Product).all()
    print(f"Processing {len(products)} products for embeddings and summaries...")
    count = 0
    for product in products:
        # Check if embedding exists
        existing_emb = get_embedding_by_product_id(db, product.id)
        if existing_emb:
            print(f"Embedding exists for Product ID={product.id}, skipping.")
            continue
        fields = ["name", "price", "rating", "description", "category", "availability"]
        product_text = " | ".join(
            f"{field.capitalize()}: {getattr(product, field)}"
            for field in fields if getattr(product, field, None)
        ).strip()

        if not product_text:
            product_text = f"Book titled '{product.name or 'unknown'}'"
        
        embedding_vector = get_embedding(product_text)
        embedding_json = embedding_to_json(embedding_vector)

        # Save embedding
        create_or_update_embedding(db, product.id, embedding_json)

        count += 1
        if count % 10 == 0:
            print(f"Generated embeddings for {count} products.")

        summary = generate_summary_from_llm(product_text)

        product.marketing_summary = summary
        db.add(product) 
        db.commit()

    print("Completed embedding and marketing summary generation.")