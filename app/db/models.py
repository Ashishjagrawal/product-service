from sqlalchemy import (
    Column, Integer, Float, String, Text, DateTime, Numeric, LargeBinary,
    ForeignKey, UniqueConstraint, Index, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False, index=True)
    rating = Column(Float, nullable=True, index=True)
    description = Column(Text, nullable=True)
    url = Column(String(512), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    availability = Column(String(100), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    embedding = relationship("Embedding", uselist=False, back_populates="product")

    marketing_summary = Column(Text, nullable=True)  # store cached summary
    summary_updated_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint('url', name='uq_product_url'),
    )

class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True, nullable=False)
    vector = Column(Text, nullable=False)  # Store as JSON-encoded string (portable for SQLite)
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="embedding")