import os
import sys
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db, SessionLocal
from app.db.database_test import TestingSessionLocal, test_engine as engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# SQLite In-memory test DB URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables for the test DB at start
Base.metadata.create_all(bind=engine)

# Override get_db dependency in FastAPI app for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    trans = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    trans.rollback()
    connection.close()

# Override FastAPI's get_db to use test session
from app.db.database import get_db

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    """FastAPI test client."""
    yield TestClient(app)
