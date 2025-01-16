from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str


class ProductOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
