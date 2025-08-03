from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal
from app.schemas.product import ProductOut
from app.ai.recommendations import get_similar_products
from app.ai.analytics import get_trends

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommendations/{product_id}", response_model=List[ProductOut])
def recommendations(product_id: int, db: Session = Depends(get_db)):
    recs = get_similar_products(db, product_id, top_k=5)
    if not recs:
        raise HTTPException(status_code=404, detail="No recommendations found or product/embedding missing")
    return [ProductOut.model_validate(p) for p in recs]

@router.get("/trends")
def get_trends_endpoint(db: Session = Depends(get_db)):
    return get_trends(db)