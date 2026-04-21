from sqlalchemy.orm import Session

from app.db.models.list_entry import ListEntryRecord

ALLOWED_LIST_TYPES = {
    "trusted_domains",
    "blocked_senders",
    "blocked_extensions",
}

DEFAULT_LISTS = {
    "trusted_domains": {"company.com", "partner.com"},
    "blocked_senders": {"attacker@evil-example.com", "scam@bad.com"},
    "blocked_extensions": {".exe", ".bat", ".js", ".scr"},
}


def normalize_value(value: str) -> str:
    return value.strip().lower()


def validate_list_type(list_type: str) -> None:
    if list_type not in ALLOWED_LIST_TYPES:
        raise ValueError(f"Unsupported list type: {list_type}")


def seed_default_lists(db: Session) -> None:
    for list_type, values in DEFAULT_LISTS.items():
        for value in values:
            normalized = normalize_value(value)
            exists = (
                db.query(ListEntryRecord)
                .filter(
                    ListEntryRecord.list_type == list_type,
                    ListEntryRecord.value == normalized,
                )
                .first()
            )
            if not exists:
                db.add(ListEntryRecord(list_type=list_type, value=normalized))
    db.commit()


def get_list_values(db: Session, list_type: str) -> set[str]:
    validate_list_type(list_type)
    rows = (
        db.query(ListEntryRecord)
        .filter(ListEntryRecord.list_type == list_type)
        .order_by(ListEntryRecord.id.asc())
        .all()
    )
    return {row.value for row in rows}


def list_entries_by_type(db: Session, list_type: str) -> list[ListEntryRecord]:
    validate_list_type(list_type)
    return (
        db.query(ListEntryRecord)
        .filter(ListEntryRecord.list_type == list_type)
        .order_by(ListEntryRecord.id.asc())
        .all()
    )


def create_list_entry(db: Session, list_type: str, value: str) -> ListEntryRecord:
    validate_list_type(list_type)
    normalized = normalize_value(value)

    existing = (
        db.query(ListEntryRecord)
        .filter(
            ListEntryRecord.list_type == list_type,
            ListEntryRecord.value == normalized,
        )
        .first()
    )
    if existing:
        return existing

    record = ListEntryRecord(list_type=list_type, value=normalized)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_list_entry(db: Session, list_type: str, entry_id: int) -> ListEntryRecord | None:
    validate_list_type(list_type)
    record = (
        db.query(ListEntryRecord)
        .filter(
            ListEntryRecord.id == entry_id,
            ListEntryRecord.list_type == list_type,
        )
        .first()
    )
    if not record:
        return None

    db.delete(record)
    db.commit()
    return record
