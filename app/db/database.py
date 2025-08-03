# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from typing import Generator
# from sqlalchemy.orm import Session
# # from .database import SessionLocal

# # Absolute path to project's root directory (two levels up from current file)
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# # Construct absolute path for SQLite DB file
# SQLITE_DB_PATH = os.path.join(BASE_DIR, "products.db")
# DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")

# # print(f"Using DB URL: {DB_URL}")

# engine = create_engine(
#     DB_URL,
#     connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {},
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db() -> Generator[Session, None, None]:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./products.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()