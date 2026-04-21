from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.emails import router as emails_router
from app.api.routes.lists import router as lists_router
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.services.list_service import seed_default_lists
import app.db.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_default_lists(db)
    finally:
        db.close()

    yield


app = FastAPI(title="Email Filtering System", lifespan=lifespan)

app.include_router(emails_router)
app.include_router(lists_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Email Filtering System API"}
