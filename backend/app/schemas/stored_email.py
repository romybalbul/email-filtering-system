from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StoredEmailResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    subject: str
    body: str
    score: int
    verdict: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
