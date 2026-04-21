from pydantic import BaseModel
from typing import List


class MatchedRule(BaseModel):
    rule: str
    score_delta: int
    reason: str | None = None


class FilterResponse(BaseModel):
    verdict: str
    score: int
    reasons: List[str]
    matched_rules: List[MatchedRule]
    email_id: int | None = None
