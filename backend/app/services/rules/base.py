from pydantic import BaseModel


class RuleResult(BaseModel):
    matched: bool
    score_delta: int = 0
    reason: str | None = None


class BaseRule:
    name: str = "base_rule"

    def evaluate(self, email):
        raise NotImplementedError
