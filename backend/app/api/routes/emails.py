from fastapi import APIRouter
from app.schemas.email import EmailInput
from app.schemas.verdict import FilterResponse
from app.services.filtering_engine import FilteringEngine

router = APIRouter(prefix="/emails", tags=["emails"])
engine = FilteringEngine()


@router.post("/filter", response_model=FilterResponse)
def filter_email(payload: EmailInput) -> FilterResponse:
    return engine.evaluate(payload)
