# Create Pydantic schemas for OrderCreate and OrderResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List 

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=200)
    status: str = Field(..., pattern="^(pending|completed|cancelled)$")
    amount: float = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "customer_name": "John Doe",
                "status": "pending",
                "amount": 150.0
            }]
        }
    }

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    amount: float
    created_at: datetime

    model_config = {"from_attributes": True}

class PaginationMeta(BaseModel):
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total pages")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")

class PaginatedOrderResponse(BaseModel):
    data: List[OrderResponse]
    pagination: PaginationMeta