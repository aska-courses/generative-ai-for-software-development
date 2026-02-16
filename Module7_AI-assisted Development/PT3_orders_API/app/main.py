# Initialize FastAPI app
# Include orders router
# Create database tables on startup

from fastapi import FastAPI
from .routes.orders import router
from . import database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    database.create_tables()
    print("✓ Database tables created!")
    yield

app = FastAPI(title="Orders API", version="2.0.0", lifespan=lifespan)
app.include_router(router)


# Create database tables automatically on startup
@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Orders API! Visit /docs for API documentation.",
        "docs": "/docs",
        "endpoints": {
            "create_order": "/orders (POST)",
            "list_orders": "/orders (GET)"
        }
    }