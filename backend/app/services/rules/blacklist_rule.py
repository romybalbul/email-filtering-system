from app.services.rules.base import BaseRule, RuleResult


class BlacklistRule(BaseRule):
    name = "blacklist_rule"

    def __init__(self, blocked_senders: set[str], score: int = 100):
        self.blocked_senders = {s.lower() for s in blocked_senders}
        self.score = score

    def evaluate(self, email) -> RuleResult:
        sender = email.sender.lower()

        if sender in self.blocked_senders:
            return RuleResult(
                matched=True,
                score_delta=self.score,
                reason=f"sender is blacklisted: {sender}",
            )

        return RuleResult(matched=False)
