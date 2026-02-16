import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models

# Create test database
TEST_DATABASE_URL = "sqlite:///./test_orders.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Setup and teardown
@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def create_order(payload=None):
    """Helper function to create an order"""
    if payload is None:
        payload = {
            "customer_name": "John Doe",
            "status": "pending",
            "amount": 150.0
        }
    return client.post("/orders/", json=payload)

# ========== BASIC CRUD TESTS ==========

def test_create_order_success():
    """Test successful order creation"""
    r = create_order()
    assert r.status_code == 201
    data = r.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == "pending"
    assert data["amount"] == 150.0
    assert "id" in data
    assert "created_at" in data

def test_create_order_invalid_status():
    """Test order creation with invalid status"""
    r = create_order({
        "customer_name": "Test", 
        "status": "invalid_status", 
        "amount": 100
    })
    assert r.status_code == 422

def test_create_order_negative_amount():
    """Test order creation with negative amount"""
    r = create_order({
        "customer_name": "Test", 
        "status": "pending", 
        "amount": -50
    })
    assert r.status_code == 422

def test_create_order_empty_name():
    """Test order creation with empty name"""
    r = create_order({
        "customer_name": "", 
        "status": "pending", 
        "amount": 100
    })
    assert r.status_code == 422

# ========== PAGINATION METADATA TESTS ==========

def test_pagination_metadata_structure():
    """Test pagination metadata is included in response"""
    create_order()
    r = client.get("/orders/")
    assert r.status_code == 200
    data = r.json()
    
    # Check structure
    assert "data" in data
    assert "pagination" in data
    
    # Check pagination fields
    pagination = data["pagination"]
    assert "total" in pagination
    assert "page" in pagination
    assert "limit" in pagination
    assert "total_pages" in pagination
    assert "has_next" in pagination
    assert "has_previous" in pagination

def test_pagination_metadata_values():
    """Test pagination metadata calculates correctly"""
    # Create 25 orders
    for i in range(25):
        create_order({
            "customer_name": f"User{i}", 
            "status": "pending", 
            "amount": 100 + i
        })
    
    r = client.get("/orders/?page=1&limit=10")
    data = r.json()
    
    assert data["pagination"]["total"] == 25
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["limit"] == 10
    assert data["pagination"]["total_pages"] == 3
    assert data["pagination"]["has_next"] is True
    assert data["pagination"]["has_previous"] is False

def test_pagination_last_page():
    """Test pagination on last page"""
    for i in range(25):
        create_order({
            "customer_name": f"User{i}", 
            "status": "pending", 
            "amount": 100
        })
    
    r = client.get("/orders/?page=3&limit=10")
    data = r.json()
    
    assert data["pagination"]["page"] == 3
    assert data["pagination"]["has_next"] is False
    assert data["pagination"]["has_previous"] is True
    assert len(data["data"]) == 5  # 25 total, 10 per page, page 3 has 5

# ========== PAGINATION TESTS ==========

def test_default_pagination():
    """Test default pagination values"""
    for i in range(15):
        create_order({
            "customer_name": f"User{i}", 
            "status": "pending", 
            "amount": 100
        })
    
    r = client.get("/orders/")
    assert r.status_code == 200
    data = r.json()
    assert len(data["data"]) == 10  # default limit
    assert data["pagination"]["page"] == 1

def test_custom_pagination():
    """Test custom page and limit"""
    for i in range(30):
        create_order({
            "customer_name": f"User{i}", 
            "status": "pending", 
            "amount": 100
        })
    
    r = client.get("/orders/?page=2&limit=5")
    data = r.json()
    assert len(data["data"]) == 5
    assert data["pagination"]["page"] == 2

def test_max_limit_enforcement():
    """Test that limit cannot exceed 100"""
    r = client.get("/orders/?limit=150")
    assert r.status_code == 422

def test_invalid_page_zero():
    """Test that page 0 is invalid"""
    r = client.get("/orders/?page=0")
    assert r.status_code == 422

def test_empty_page_beyond_results():
    """Test requesting page beyond results"""
    create_order()
    r = client.get("/orders/?page=999")
    data = r.json()
    assert len(data["data"]) == 0
    assert data["pagination"]["total"] == 1

# ========== FILTERING TESTS ==========

def test_filter_by_status():
    """Test filtering by status"""
    create_order({"customer_name": "Alice", "status": "completed", "amount": 200})
    create_order({"customer_name": "Bob", "status": "pending", "amount": 150})
    create_order({"customer_name": "Carol", "status": "completed", "amount": 300})
    
    r = client.get("/orders/?status=completed&limit=100")
    data = r.json()
    assert data["pagination"]["total"] == 2
    assert all(order["status"] == "completed" for order in data["data"])

def test_filter_by_amount_range():
    """Test filtering by amount range"""
    create_order({"customer_name": "User1", "status": "pending", "amount": 50})
    create_order({"customer_name": "User2", "status": "pending", "amount": 150})
    create_order({"customer_name": "User3", "status": "pending", "amount": 250})
    
    r = client.get("/orders/?min_amount=100&max_amount=200")
    data = r.json()
    assert data["pagination"]["total"] == 1
    assert all(100 <= order["amount"] <= 200 for order in data["data"])

def test_filter_by_date_range():
    """Test filtering by date range"""
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)
    
    create_order()
    
    r = client.get(
        f"/orders/?start_date={yesterday.isoformat()}&end_date={tomorrow.isoformat()}"
    )
    assert r.status_code == 200
    assert r.json()["pagination"]["total"] >= 1

def test_combined_filters():
    """Test multiple filters together"""
    create_order({"customer_name": "Frank", "status": "completed", "amount": 250})
    create_order({"customer_name": "Grace", "status": "completed", "amount": 80})
    create_order({"customer_name": "Heidi", "status": "pending", "amount": 150})
    
    r = client.get("/orders/?status=completed&min_amount=100&limit=100")
    data = r.json()
    assert all(
        order["status"] == "completed" and order["amount"] >= 100 
        for order in data["data"]
    )

# ========== EDGE CASES ==========

def test_no_results():
    """Test response when no orders exist"""
    r = client.get("/orders/")
    data = r.json()
    assert len(data["data"]) == 0
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["total_pages"] == 0

def test_no_results_for_filter():
    """Test when filters match nothing"""
    create_order({"customer_name": "Test", "status": "pending", "amount": 100})
    
    r = client.get("/orders/?status=cancelled")
    data = r.json()
    assert len(data["data"]) == 0
    assert data["pagination"]["total"] == 0

def test_performance_large_dataset():
    """Test with large dataset"""
    for i in range(100):
        create_order({
            "customer_name": f"User{i}", 
            "status": "pending", 
            "amount": 100 + i
        })
    
    r = client.get("/orders/?page=5&limit=20")
    data = r.json()
    assert len(data["data"]) == 20
    assert data["pagination"]["total"] == 100


# Add these at the end of your test file

# ========== ADDITIONAL EDGE CASES ==========

def test_filter_by_max_amount_only():
    """Test filtering by maximum amount only"""
    create_order({"customer_name": "User1", "status": "pending", "amount": 50})
    create_order({"customer_name": "User2", "status": "pending", "amount": 150})
    create_order({"customer_name": "User3", "status": "pending", "amount": 250})
    
    r = client.get("/orders/?max_amount=100")
    data = r.json()
    assert all(order["amount"] <= 100 for order in data["data"])

def test_invalid_date_format():
    """Test that invalid date format returns validation error"""
    r = client.get("/orders/?start_date=not-a-valid-date")
    assert r.status_code == 422

def test_pagination_with_filters_empty_result():
    """Test pagination metadata when filters return no results"""
    create_order({"customer_name": "Test", "status": "pending", "amount": 100})
    
    r = client.get("/orders/?status=cancelled&page=1&limit=10")
    data = r.json()
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["total_pages"] == 0
    assert data["pagination"]["has_next"] is False
    assert data["pagination"]["has_previous"] is False
    assert len(data["data"]) == 0

def test_order_sorting_by_date():
    """Test that orders are returned in correct chronological order"""
    import time
    
    # Create orders with small time gaps
    create_order({"customer_name": "First", "status": "pending", "amount": 100})
    time.sleep(0.1)
    create_order({"customer_name": "Second", "status": "pending", "amount": 200})
    time.sleep(0.1)
    create_order({"customer_name": "Third", "status": "pending", "amount": 300})
    
    r = client.get("/orders/?limit=10")
    data = r.json()
    
    # Should be in descending order (newest first)
    assert data["data"][0]["customer_name"] == "Third"
    assert data["data"][1]["customer_name"] == "Second"
    assert data["data"][2]["customer_name"] == "First"


# ... existing tests ...

# ========== COVERAGE GAP FILLERS ==========

def test_filter_invalid_amount_range_logic():
    """
    Hits app/crud.py line 45: 
    Checks if min_amount > max_amount raises 400
    """
    r = client.get("/orders/?min_amount=100&max_amount=50")
    assert r.status_code == 400
    assert r.json()["detail"] == "min_amount cannot be greater than max_amount"

def test_filter_invalid_date_range_logic():
    """
    Hits app/crud.py line 47: 
    Checks if start_date > end_date raises 400
    """
    now = datetime.now()
    start = now + timedelta(days=1)
    end = now - timedelta(days=1)
    
    r = client.get(f"/orders/?start_date={start.isoformat()}&end_date={end.isoformat()}")
    assert r.status_code == 400
    assert r.json()["detail"] == "start_date cannot be greater than end_date"

def test_root_endpoint():
    """
    Hits app/main.py lines 27-33:
    Tests the welcome message
    """
    r = client.get("/")
    assert r.status_code == 200
    assert "Welcome to the Orders API" in r.json()["message"]

def test_model_repr():
    """Test the string representation of the Order model"""
    from app.models import Order
    order = Order(id=1, customer_name="Test", status="pending")
    # This triggers the __repr__ method in models.py
    assert repr(order) == "<Order(id=1, customer=Test, status=pending)>"