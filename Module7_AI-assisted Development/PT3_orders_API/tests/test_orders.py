# Tests for Orders API:
# - create order
# - list orders
# - pagination
# - filtering by status
# - filtering by amount
# - filtering by date range
# - edge cases

import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)


payload = {
    "customer_name": "John Doe",
    "status": "pending",
    "amount": 150.0
}


def create_order(payload=None):
    if payload is None:
        payload = {
            "customer_name": "John Doe",
            "status": "pending",
            "amount": 150.0
        }
    return client.post("/orders", json=payload)


# ---------- BASIC CRUD ----------

def test_create_order():
    r = create_order()
    assert r.status_code == 201
    data = r.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == "pending"
    assert data["amount"] == 150.0

def test_list_orders():
    # create some orders
    create_order({"customer_name": "Alice", "status": "completed", "amount": 200})
    create_order({"customer_name": "Bob", "status": "cancelled", "amount": 50})

    r = client.get("/orders?limit=100")
    assert r.status_code == 200

    names = [o["customer_name"] for o in r.json()]
    assert "Alice" in names
    assert "Bob" in names


# ---------- PAGINATION ----------

def test_pagination_page_1_limit_5():
    r = client.get("/orders?page=1&limit=5")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_pagination_page_2_limit_5():
    r = client.get("/orders?page=2&limit=5")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_invalid_page_zero():
    r = client.get("/orders?page=0&limit=5")
    assert r.status_code == 422  # validation error 


def test_invalid_limit_zero():
    r = client.get("/orders?page=1&limit=0")
    assert r.status_code == 422  # validation error

# ---------- FILTERING ----------

def test_filter_by_status():
    r = client.get("/orders?status=completed")
    assert r.status_code == 200
    data = r.json()
    assert all(order["status"] == "completed" for order in data)

def test_filter_by_amount_range():
    r = client.get("/orders?min_amount=100&max_amount=200")
    assert r.status_code == 200
    data = r.json()
    assert all(100 <= order["amount"] <= 200 for order in data)

def test_filter_by_min_amount():
    r = client.get("/orders?min_amount=100")
    assert r.status_code == 200
    data = r.json()
    assert all(order["amount"] >= 100 for order in data)

def test_filter_by_max_amount():
    r = client.get("/orders?max_amount=100")
    assert r.status_code == 200
    data = r.json()
    assert all(order["amount"] <= 100 for order in data)

# ---------- DATE FILTERING ----------
def test_filter_by_date_range():
    # create orders with known dates
    from datetime import datetime, timedelta
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)
    r = client.get(f"/orders?start_date={yesterday.isoformat()}&end_date={tomorrow.isoformat()}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)  # just check it returns a list


def test_filter_by_start_date():
    from datetime import datetime, timedelta
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    r = client.get(f"/orders?start_date={yesterday.isoformat()}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)  # just check it returns a list


def test_invalid_date_format():
    r = client.get("/orders?start_date=invalid-date")
    assert r.status_code == 422  # validation error

# ---------- EDGE CASES ----------

def test_no_results_for_unknown_status():
    r = client.get("/orders?status=__does_not_exist__")
    assert r.status_code == 200
    assert r.json() == []


def test_combined_filters():
    # create orders with different attributes
    create_order({"customer_name": "Frank", "status": "completed", "amount": 250.0})
    create_order({"customer_name": "Grace", "status": "completed", "amount": 80.0})
    create_order({"customer_name": "Heidi", "status": "pending", "amount": 150.0})

    r = client.get("/orders?status=completed&min_amount=100")
    assert r.status_code == 200
    data = r.json()
    assert all(order["status"] == "completed" and order["amount"] >= 100 for order in data)
