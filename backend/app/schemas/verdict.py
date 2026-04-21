from pydantic import BaseModel
from typing import List


class MatchedRule(BaseModel):
    rule: str
    score_delta: int


class FilterResponse(BaseModel):
    verdict: str
    score: int
    reasons: List[str]
    matched_rules: List[MatchedRule]
    email_id: int | None = None
