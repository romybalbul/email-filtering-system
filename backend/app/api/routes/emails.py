from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.email import EmailInput
from app.schemas.stored_email import EmailDetailsResponse, RuleHitResponse, StoredEmailResponse
from app.schemas.verdict import FilterResponse
from app.services.email_service import (
    get_email_by_id,
    list_emails,
    list_rule_hits_for_email,
    save_filtered_email,
)
from app.services.filtering_engine import FilteringEngine

router = APIRouter(prefix="/emails", tags=["emails"])
engine = FilteringEngine()


@router.post("/filter", response_model=FilterResponse)
def filter_email(payload: EmailInput, db: Session = Depends(get_db)) -> FilterResponse:
    result = engine.evaluate(payload)
    record = save_filtered_email(db, payload, result)
    return result.model_copy(update={"email_id": record.id})


@router.get("", response_model=list[StoredEmailResponse])
def get_emails(db: Session = Depends(get_db)) -> list[StoredEmailResponse]:
    return list_emails(db)


@router.get("/{email_id}", response_model=EmailDetailsResponse)
def get_email(email_id: int, db: Session = Depends(get_db)) -> EmailDetailsResponse:
    record = get_email_by_id(db, email_id)
    if not record:
        raise HTTPException(status_code=404, detail="Email not found")
    return record


@router.get("/{email_id}/rule-hits", response_model=list[RuleHitResponse])
def get_email_rule_hits(email_id: int, db: Session = Depends(get_db)) -> list[RuleHitResponse]:
    record = get_email_by_id(db, email_id)
    if not record:
        raise HTTPException(status_code=404, detail="Email not found")
    return list_rule_hits_for_email(db, email_id)
