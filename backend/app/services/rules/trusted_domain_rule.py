from app.services.rules.base import BaseRule, RuleResult


class TrustedDomainRule(BaseRule):
    name = "trusted_domain_rule"

    def __init__(self, trusted_domains: set[str], score: int = -40):
        self.trusted_domains = {d.lower() for d in trusted_domains}
        self.score = score

    def evaluate(self, email) -> RuleResult:
        sender = email.sender.lower()

        if "@" not in sender:
            return RuleResult(matched=False)

        domain = sender.split("@", 1)[1]

        if domain in self.trusted_domains:
            return RuleResult(
                matched=True,
                score_delta=self.score,
                reason=f"trusted sender domain: {domain}",
            )

        return RuleResult(matched=False)
