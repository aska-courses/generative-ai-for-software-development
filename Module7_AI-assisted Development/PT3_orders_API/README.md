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

### Create Order

**POST** `/orders`

```json
{
  "customer_name": "John Doe",
  "status": "pending",
  "amount": 150.0
}
```

Response:

```json
{
  "id": 1,
  "customer_name": "John Doe",
  "status": "pending",
  "amount": 150.0,
  "created_at": "2026-02-08T10:15:30"
}
```

---

### List Orders (Pagination + Filtering)

**GET** `/orders`

#### Pagination

| Param | Description            |
| ----- | ---------------------- |
| page  | Page number (>=1)      |
| limit | Items per page (1–100) |

Example:

```
/orders?page=1&limit=10
```

---

#### Filtering

| Param      | Description      |
| ---------- | ---------------- |
| status     | Filter by status |
| min_amount | Minimum amount   |
| max_amount | Maximum amount   |
| start_date | ISO datetime     |
| end_date   | ISO datetime     |

Example:

```
/orders?status=completed&min_amount=100&start_date=2026-02-01
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

* ✅ 15 tests
* ✅ Pagination tested
* ✅ Filtering tested
* ✅ Edge cases tested
* ✅ **98% code coverage**
```bash
===================================================== tests coverage ======================================================
____________________________________ coverage: platform darwin, python 3.13.3-final-0 _____________________________________

Name                     Stmts   Miss  Cover
--------------------------------------------
app/__init__.py              0      0   100%
app/crud.py                 22      0   100%
app/database.py             14      1    93%
app/main.py                  8      1    88%
app/models.py               10      0   100%
app/routes/__init__.py       0      0   100%
app/routes/orders.py        11      0   100%
app/schemas.py              15      0   100%
--------------------------------------------
TOTAL                       80      2    98%
============================================= 15 passed, 5 warnings in 0.49s ==============================================

```
---

## Validation & Error Handling

* Invalid `page` or `limit` → **422**
* Invalid date format → **422**
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




