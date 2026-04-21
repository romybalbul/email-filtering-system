from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.list_entry import ListEntryCreate, ListEntryResponse
from app.services.list_service import (
    create_list_entry,
    delete_list_entry,
    list_entries_by_type,
    validate_list_type,
)

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("/{list_type}", response_model=list[ListEntryResponse])
def get_list_entries(list_type: str, db: Session = Depends(get_db)) -> list[ListEntryResponse]:
    try:
        validate_list_type(list_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return list_entries_by_type(db, list_type)


@router.post("/{list_type}", response_model=ListEntryResponse)
def add_list_entry(
    list_type: str,
    payload: ListEntryCreate,
    db: Session = Depends(get_db),
) -> ListEntryResponse:
    try:
        validate_list_type(list_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return create_list_entry(db, list_type, payload.value)


@router.delete("/{list_type}/{entry_id}", status_code=204)
def remove_list_entry(list_type: str, entry_id: int, db: Session = Depends(get_db)):
    try:
        validate_list_type(list_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    record = delete_list_entry(db, list_type, entry_id)
    if not record:
        raise HTTPException(status_code=404, detail="List entry not found")
