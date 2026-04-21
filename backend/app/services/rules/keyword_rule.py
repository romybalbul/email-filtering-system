from app.services.rules.base import BaseRule, RuleResult


class KeywordRule(BaseRule):
    name = "keyword_rule"

    def __init__(self, keywords: set[str], score: int = 30):
        self.keywords = {k.lower() for k in keywords}
        self.score = score

    def evaluate(self, email) -> RuleResult:
        text = f"{email.subject} {email.body}".lower()

        for keyword in self.keywords:
            if keyword in text:
                return RuleResult(
                    matched=True,
                    score_delta=self.score,
                    reason=f"suspicious keyword detected: {keyword}",
                )

        return RuleResult(matched=False)
