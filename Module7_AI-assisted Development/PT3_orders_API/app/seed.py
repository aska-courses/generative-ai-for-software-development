# Seed database with 50 sample orders using Faker

from faker import Faker
from sqlalchemy.orm import Session
from .database import SessionLocal, create_tables
from . import models    

fake = Faker()

def seed_database(db: Session, num_orders: int):
    for _ in range(num_orders):
        order = models.Order(
            customer_name=fake.name(),
            status=fake.random_element(elements=("pending", "completed", "cancelled")),
            amount=fake.random_number(digits=5)
        )
        db.add(order)
    db.commit()

if __name__ == "__main__":
    create_tables()
    db = SessionLocal()
    try:
        seed_database(db, 50)
    finally:
        db.close()


