from sqlalchemy.orm import Session
from .models import Product, Embedding

def get_or_create_product(db: Session, product_data: dict):
    """Insert product if new, else return existing."""
    product = db.query(Product).filter_by(url=product_data['url']).first()
    if product:
        return product
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter_by(id=product_id).first()

def list_products(db: Session, skip=0, limit=20, filters=None):
    query = db.query(Product)
    if filters:
        if 'min_price' in filters:
            query = query.filter(Product.price >= filters['min_price'])
        if 'max_price' in filters:
            query = query.filter(Product.price <= filters['max_price'])
        if 'min_rating' in filters:
            query = query.filter(Product.rating >= filters['min_rating'])
        if 'q' in filters:
            query = query.filter(Product.name.ilike(f"%{filters['q']}%"))
    return query.offset(skip).limit(limit).all()

def create_or_update_embedding(db: Session, product_id: int, vector_json: str):
    embedding = db.query(Embedding).filter_by(product_id=product_id).first()
    if embedding:
        embedding.vector = vector_json
    else:
        embedding = Embedding(product_id=product_id, vector=vector_json)
        db.add(embedding)
    db.commit()
    db.refresh(embedding)
    return embedding

def get_embedding_by_product_id(db: Session, product_id: int):
    return db.query(Embedding).filter_by(product_id=product_id).first()

def get_product_summary(db: Session, product_id: int) -> str | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    return product.marketing_summary if product else None

def save_product_summary(db: Session, product_id: int, summary: str):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    product.marketing_summary = summary
    db.commit()
    db.refresh(product)
    return product