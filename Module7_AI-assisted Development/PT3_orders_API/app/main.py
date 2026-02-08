# Initialize FastAPI app
# Include orders router
# Create database tables on startup

from fastapi import FastAPI
from .routes.orders import router
from . import database

app = FastAPI(title="Orders API")
app.include_router(router)


# Create database tables automatically on startup
@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)