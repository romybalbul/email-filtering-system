from sqlalchemy.orm import Session, selectinload

from app.db.models.email import EmailRecord
from app.db.models.rule_hit import RuleHitRecord
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
    db.flush()

    for matched_rule in result.matched_rules:
        hit = RuleHitRecord(
            email_id=record.id,
            rule_name=matched_rule.rule,
            score_delta=matched_rule.score_delta,
            reason=matched_rule.reason,
        )
        db.add(hit)

    db.commit()
    db.refresh(record)
    return record


def list_emails(db: Session) -> list[EmailRecord]:
    return db.query(EmailRecord).order_by(EmailRecord.created_at.desc()).all()


def get_email_by_id(db: Session, email_id: int) -> EmailRecord | None:
    return (
        db.query(EmailRecord)
        .options(selectinload(EmailRecord.rule_hits))
        .filter(EmailRecord.id == email_id)
        .first()
    )


def list_rule_hits_for_email(db: Session, email_id: int) -> list[RuleHitRecord]:
    return (
        db.query(RuleHitRecord)
        .filter(RuleHitRecord.email_id == email_id)
        .order_by(RuleHitRecord.id.asc())
        .all()
    )
