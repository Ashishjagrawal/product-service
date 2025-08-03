from pydantic import BaseModel, Field
from typing import Optional, List

class ProductOut(BaseModel):
    id: int
    name: str = Field(..., title="Product name", max_length=256)
    price: float = Field(..., ge=0.0, description="Price in GBP")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    description: Optional[str] = Field(None, max_length=50000)
    url: str = Field(..., max_length=512)
    category: Optional[str] = Field(None, max_length=100)
    availability: Optional[str] = Field(None, max_length=100)
    marketing_summary: Optional[str] = None

    model_config = {"from_attributes": True}  # for Pydantic v2; or use orm_mode=True for v1

class ProductListOut(BaseModel):
    items: List[ProductOut]
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=100)
    total: int = Field(..., ge=0)