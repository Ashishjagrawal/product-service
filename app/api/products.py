from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import get_product_by_id, list_products
from app.schemas.product import ProductOut, ProductListOut
from typing import List
from app.ai.summaries import get_marketing_summary

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=ProductListOut)
def get_products(
    page: int = Query(1, ge=1, description="Page number, minimum 1"),
    size: int = Query(20, ge=1, le=100, description="Page size, 1-100"),
    min_price: float = Query(None, ge=0, description="Minimum price filter"),
    max_price: float = Query(None, ge=0, description="Maximum price filter"),
    min_rating: float = Query(None, ge=0, le=5, description="Minimum rating from 0 to 5"),
    q: str = Query(None, min_length=1, max_length=100, description="Search keyword"),
    db: Session = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="Minimum price cannot be greater than maximum price")

    filters = {}
    if min_price is not None: filters['min_price'] = min_price
    if max_price is not None: filters['max_price'] = max_price
    if min_rating is not None: filters['min_rating'] = min_rating
    if q: filters['q'] = q

    products = list_products(db, skip=(page-1)*size, limit=size, filters=filters)
    return ProductListOut(
        items=[ProductOut.from_orm(p) for p in products],
        page=page,
        size=size,
        total=len(products)
    )

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_text = product.description or product.name
    summary = get_marketing_summary(db, product_id, product_text)
    
    # Build Pydantic model including summary
    product_data = ProductOut.model_validate(product).model_dump()
    product_data['marketing_summary'] = summary
    return product_data