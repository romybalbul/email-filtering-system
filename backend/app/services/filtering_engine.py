from app.schemas.verdict import FilterResponse, MatchedRule
from app.services.rules.attachment_rule import AttachmentRule
from app.services.rules.blacklist_rule import BlacklistRule
from app.services.rules.keyword_rule import KeywordRule
from app.services.rules.trusted_domain_rule import TrustedDomainRule


class FilteringEngine:
    def __init__(self):
        self.rules = [
            TrustedDomainRule(trusted_domains={"company.com", "partner.com"}),
            KeywordRule(
                keywords={"urgent", "invoice", "password", "verify", "crypto"},
                score=30,
            ),
            AttachmentRule(
                blocked_extensions={".exe", ".bat", ".js", ".scr"},
                score=80,
            ),
            BlacklistRule(
                blocked_senders={"attacker@evil-example.com", "scam@bad.com"},
                score=100,
            ),
        ]

    def _score_to_verdict(self, score: int) -> str:
        if score >= 120:
            return "reject"
        if score >= 80:
            return "quarantine"
        if score >= 40:
            return "spam"
        return "allow"

    def evaluate(self, email) -> FilterResponse:
        total_score = 0
        reasons: list[str] = []
        matched_rules: list[MatchedRule] = []

        for rule in self.rules:
            result = rule.evaluate(email)
            if result.matched:
                total_score += result.score_delta
                if result.reason:
                    reasons.append(result.reason)
                matched_rules.append(
                    MatchedRule(rule=rule.name, score_delta=result.score_delta)
                )

        verdict = self._score_to_verdict(total_score)

        return FilterResponse(
            verdict=verdict,
            score=total_score,
            reasons=reasons,
            matched_rules=matched_rules,
        )
