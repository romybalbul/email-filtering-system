from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RuleHitResponse(BaseModel):
    id: int
    email_id: int
    rule_name: str
    score_delta: int
    reason: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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


class EmailDetailsResponse(StoredEmailResponse):
    rule_hits: list[RuleHitResponse]
