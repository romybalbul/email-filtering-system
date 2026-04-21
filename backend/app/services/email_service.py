from sqlalchemy.orm import Session

from app.db.models.email import EmailRecord
from app.schemas.email import EmailInput
from app.schemas.verdict import FilterResponse


def save_filtered_email(db: Session, payload: EmailInput, result: FilterResponse) -> EmailRecord:
    record = EmailRecord(
        sender=payload.sender,
        recipient=payload.recipient,
        subject=payload.subject,
        body=payload.body,
        score=result.score,
        verdict=result.verdict,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_emails(db: Session) -> list[EmailRecord]:
    return db.query(EmailRecord).order_by(EmailRecord.created_at.desc()).all()


def get_email_by_id(db: Session, email_id: int) -> EmailRecord | None:
    return db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
