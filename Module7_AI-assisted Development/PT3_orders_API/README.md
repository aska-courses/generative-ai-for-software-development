# Orders Management API

A RESTful Orders Management API built with **FastAPI** and **SQLAlchemy**, featuring
pagination, filtering, automated tests, and database seeding.  
This project demonstrates **AI-assisted development using GitHub Copilot**.

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest + pytest-cov

---

## Project Structure

```text
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── seed.py
│   └── routes/
│       └── orders.py
├── tests/
│   └── test_orders.py
├── orders.db
├── requirements.txt
├── pytest.ini
├── setup.py
└── README.md
```

---

## Setup Instructions

### 1. Create virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
```


### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 2.2 Setup
```bash
python setup.py                          # Create tables + seed data(10k)
python -m app.seed 100                   # OR Generate 100 fake orders
```
---

## Run the API

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Interactive docs:

```
http://127.0.0.1:8000/docs
```

---

## Database

* SQLite database (`orders.db`)
* Tables are created automatically on startup
* Optional seed script available

### Seed sample data (50 orders)

```bash
python app/seed.py
```

---

## API Endpoints

### 1. Create Order (POST /orders/)
code
```JSON
{
  "customer_name": "John Doe",
  "status": "pending",
  "amount": 150.0
}
```
### 2. List Orders (GET /orders/)
Supports pagination and filtering.

**Pagination Parameters:**
- ``page``: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

**Filter Parameters:**
- `status`: Filter by status (pending, completed, cancelled)
- `min_amount` / `max_amount`: Filter by price range
- `start_date` / `end_date`: Filter by creation date (ISO format)

#### Example Request:

```http
GET /orders/?page=1&limit=5&status=completed&min_amount=10
```
Example Response:
```JSON
{
  "data": [
    {
      "id": 1,
      "customer_name": "Jane Doe",
      "status": "completed",
      "amount": 150.0,
      "created_at": "2026-02-16T20:30:00"
    }
  ],
  "pagination": {
    "total": 45,
    "page": 1,
    "limit": 5,
    "total_pages": 9,
    "has_next": true,
    "has_previous": false
  }
}
```

---

## Testing

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

### Coverage

* ✅ 27 tests
* ✅ Pagination tested
* ✅ Filtering tested
* ✅ Edge cases tested
* ✅ **91% code coverage**
```bash
================================ tests coverage =================================
_______________ coverage: platform darwin, python 3.13.3-final-0 ________________

Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
app/__init__.py              0      0   100%
app/crud.py                 30      0   100%
app/database.py             15      6    60%   15-19, 22, 26
app/main.py                 15      4    73%   9-12
app/models.py               12      0   100%
app/routes/__init__.py       0      0   100%
app/routes/orders.py        16      0   100%
app/schemas.py              25      0   100%
------------------------------------------------------
TOTAL                      113     10    91%
============================== 27 passed in 1.37s ==============================
```
---

## Validation & Error Handling

* Invalid `page` or `limit` or their range → **422**
* Invalid date range → **422**
* Empty result sets → empty list (`[]`)

---

## GitHub Copilot Usage

* Used to scaffold FastAPI routes
* Generated SQLAlchemy models and CRUD functions
* Assisted in writing tests and pagination logic
* Manual review applied for:

  * Input validation
  * Edge cases
  * Database constraints

Detailed metrics available in **copilot_report.md**.