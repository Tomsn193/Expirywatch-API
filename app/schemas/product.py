from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, description="Product display name")
    generic_name: Optional[str] = Field(None, max_length=150, description="Optional generic label")
    category: str = Field(..., min_length=1, max_length=80, description="Simple category lable")
    unit: str = Field(..., min_length=1, max_length=30, description="Counted unit (e.g. tablet)")
    reorder_level: int = Field(0, ge=0, description="Must be zero or greater")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    
    # This tells Pydantic to read data even if it is not a dictionary (SQLAlchemy objects)
    model_config = ConfigDict(from_attributes=True)