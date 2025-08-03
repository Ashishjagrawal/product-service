import pytest
from app.db.crud import get_or_create_product, get_product_by_id
from app.db.models import Product

def test_create_and_get_product(db_session):
    data = {
        "name": "Test Book",
        "price": 10.99,
        "rating": 4.5,
        "description": "A test book.",
        "url": "http://example.com/test-book",
        "category": "Test Category",
        "availability": "In stock"
    }
    product = get_or_create_product(db_session, data)
    assert product.id is not None

    fetched = get_product_by_id(db_session, product.id)
    assert fetched.name == "Test Book"