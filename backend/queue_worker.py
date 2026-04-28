import time

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.db.models.email import EmailRecord
from app.services.queue_service import (
    get_next_pending_item,
    mark_done,
    mark_failed,
    mark_processing,
)
from app.services.scanning_service import scan_stored_email
import app.db.models  # noqa: F401


POLL_INTERVAL_SECONDS = 2


def run_worker():
    Base.metadata.create_all(bind=engine)
    print("Email queue worker started")

    while True:
        db = SessionLocal()
        try:
            item = get_next_pending_item(db)

            if not item:
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            print(f"Processing queue item {item.id}, email_id={item.email_id}")
            mark_processing(db, item)

            email = db.query(EmailRecord).filter(EmailRecord.id == item.email_id).first()
            if not email:
                mark_failed(db, item, "Email record not found")
                continue

            scan_stored_email(db, email)
            mark_done(db, item)

            print(f"Done queue item {item.id}, email_id={item.email_id}")

        except Exception as exc:
            db.rollback()
            print(f"Worker error: {exc}")
        finally:
            db.close()


if __name__ == "__main__":
    run_worker()
