from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ListEntryCreate(BaseModel):
    value: str


class ListEntryResponse(BaseModel):
    id: int
    list_type: str
    value: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
