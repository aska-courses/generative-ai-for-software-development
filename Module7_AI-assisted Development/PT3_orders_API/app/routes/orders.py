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

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderResponse, status_code=201)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order(db, order_in.customer_name, order_in.status, order_in.amount)

@router.get("/", response_model=list[schemas.OrderResponse])
def list_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(database.get_db)
):
    return crud.get_orders(db, page, limit, status, min_amount, max_amount, start_date, end_date)

