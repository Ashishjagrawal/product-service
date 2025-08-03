import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def initialize_db(monkeypatch):
    # Use an in-memory SQLite and override DB dependency for tests
    from app.db.database import engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_list_products_empty():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

def test_product_detail_not_found():
    response = client.get("/api/v1/products/9999")
    assert response.status_code == 404

def test_recommendations_not_found():
    response = client.get("/api/v1/analytics/recommendations/9999")
    assert response.status_code == 404

def test_trends_success():
    response = client.get("/api/v1/analytics/trends")
    assert response.status_code == 200
    trend_data = response.json()
    assert "price_by_rating" in trend_data
    assert "top_adjectives" in trend_data