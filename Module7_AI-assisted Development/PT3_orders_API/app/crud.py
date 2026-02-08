# Implement CRUD functions:
# - create_order
# - get_orders with pagination and filtering:
#   filters: status, min_amount, max_amount, date_from, date_to

from sqlalchemy.orm import Session
from . import models, schemas   
from datetime import datetime

def create_order(db: Session, customer_name: str, status: str, amount: float) -> models.Order:
    db_order = models.Order(customer_name=customer_name, status=status, amount=amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(
    db: Session,
    page: int,
    limit: int,
    status: str | None,
    min_amount: float | None,
    max_amount: float | None,
    start_date: datetime | None,
    end_date: datetime | None
):
    query = db.query(models.Order)
    if status:
        query = query.filter(models.Order.status == status)
    if min_amount is not None:
        query = query.filter(models.Order.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Order.amount <= max_amount)
    if start_date:
        query = query.filter(models.Order.created_at >= start_date)
    if end_date:
        query = query.filter(models.Order.created_at <= end_date)
    return query.offset((page - 1) * limit).limit(limit).all() 
