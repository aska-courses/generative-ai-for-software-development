# POST /orders
# Create a new order and return it

# GET /orders
# Support pagination using page and limit query params
# Support filtering by:
# - status
# - amount range
# - created_at date range

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, crud, database  
import math

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderResponse, status_code=201)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order(db, order_in.customer_name, order_in.status, order_in.amount)

@router.get("/", response_model=schemas.PaginatedOrderResponse)
def list_orders(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status: str | None = Query(None, description="Filter by status"),
    min_amount: float | None = Query(None, ge=0, description="Min amount"),
    max_amount: float | None = Query(None, ge=0, description="Max amount"),
    start_date: datetime | None = Query(None, description="Start date"),
    end_date: datetime | None = Query(None, description="End date"),
    db: Session = Depends(database.get_db)
):
   # Get orders and total count
    orders, total = crud.get_orders(
        db, page, limit, status, min_amount, max_amount, start_date, end_date
    )
    
    # Calculate pagination metadata
    total_pages = math.ceil(total / limit) if total > 0 else 0
    has_next = page < total_pages
    has_previous = page > 1
    
    return schemas.PaginatedOrderResponse(
        data=orders,  # type: ignore
        pagination=schemas.PaginationMeta(
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous
        )
    )

