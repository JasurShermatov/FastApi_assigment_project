from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int


class OrderCreateSchema(BaseModel):
    items: List[OrderItemSchema]


class OrderDetailOutSchema(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderOutSchema(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    order_details: List[OrderDetailOutSchema]

    model_config = ConfigDict(from_attributes=True)
