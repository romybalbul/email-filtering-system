from fastapi import FastAPI
from app.api.routes.emails import router as emails_router

app = FastAPI(title="Email Filtering System")

app.include_router(emails_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Email Filtering System API"}
