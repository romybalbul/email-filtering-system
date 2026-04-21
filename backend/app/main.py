from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.emails import router as emails_router
from app.db.base import Base
from app.db.session import engine
import app.db.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Email Filtering System", lifespan=lifespan)

app.include_router(emails_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Email Filtering System API"}
