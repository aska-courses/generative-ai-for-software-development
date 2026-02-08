# Create Pydantic schemas for OrderCreate and OrderResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional 

class OrderCreate(BaseModel):
    customer_name: str
    status: str
    amount: float

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    amount: float
    created_at: datetime

    class Config:
        orm_mode = True