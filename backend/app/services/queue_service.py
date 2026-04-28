from sqlalchemy.orm import Session

from app.db.models.email import EmailRecord
from app.db.models.email_queue import EmailQueueRecord
from app.schemas.email import EmailInput


def enqueue_email(db: Session, payload: EmailInput) -> EmailRecord:
    record = EmailRecord(
        sender=payload.sender,
        recipient=payload.recipient,
        subject=payload.subject,
        body=payload.body,
        score=0,
        verdict="pending",
        status="pending",
    )
    db.add(record)
    db.flush()

    queue_item = EmailQueueRecord(
        email_id=record.id,
        status="pending",
    )
    db.add(queue_item)

    db.commit()
    db.refresh(record)
    return record


def get_next_pending_item(db: Session) -> EmailQueueRecord | None:
    return (
        db.query(EmailQueueRecord)
        .filter(EmailQueueRecord.status == "pending")
        .order_by(EmailQueueRecord.created_at.asc())
        .first()
    )


def mark_processing(db: Session, item: EmailQueueRecord) -> None:
    item.status = "processing"
    item.attempts += 1
    db.commit()


def mark_done(db: Session, item: EmailQueueRecord) -> None:
    item.status = "done"
    db.commit()


def mark_failed(db: Session, item: EmailQueueRecord, error: str) -> None:
    item.status = "failed"
    item.last_error = error
    db.commit()
