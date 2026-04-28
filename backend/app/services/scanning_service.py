from sqlalchemy.orm import Session

from app.db.models.email import EmailRecord
from app.db.models.rule_hit import RuleHitRecord
from app.schemas.email import EmailInput
from app.services.filtering_engine import FilteringEngine


def scan_stored_email(db: Session, email: EmailRecord) -> EmailRecord:
    payload = EmailInput(
        sender=email.sender,
        recipient=email.recipient,
        subject=email.subject,
        body=email.body,
        attachments=[],
    )

    engine = FilteringEngine()
    result = engine.evaluate(payload, db)

    email.score = result.score
    email.verdict = result.verdict
    email.status = "scanned"

    db.query(RuleHitRecord).filter(RuleHitRecord.email_id == email.id).delete()

    for matched_rule in result.matched_rules:
        db.add(
            RuleHitRecord(
                email_id=email.id,
                rule_name=matched_rule.rule,
                score_delta=matched_rule.score_delta,
                reason=matched_rule.reason,
            )
        )

    db.commit()
    db.refresh(email)
    return email
