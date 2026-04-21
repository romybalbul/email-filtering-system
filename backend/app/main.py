from fastapi import FastAPI

app = FastAPI(title="Email Filtering System")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Email Filtering System API"}
