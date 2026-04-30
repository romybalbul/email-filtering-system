from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.models.email_queue import EmailQueueRecord
from app.db.session import get_db

router = APIRouter(prefix="/queue", tags=["queue"])


@router.get("")
def get_queue(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    items = (
        db.query(EmailQueueRecord)
        .order_by(EmailQueueRecord.created_at.desc())
        .limit(100)
        .all()
    )

    return [
        {
            "id": item.id,
            "email_id": item.email_id,
            "status": item.status,
            "attempts": item.attempts,
            "last_error": item.last_error,
            "created_at": item.created_at,
        }
        for item in items
    ]
