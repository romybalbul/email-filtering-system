from sqlalchemy.orm import Session

from app.schemas.verdict import FilterResponse, MatchedRule
from app.services.list_service import get_list_values
from app.services.rules.attachment_rule import AttachmentRule
from app.services.rules.blacklist_rule import BlacklistRule
from app.services.rules.keyword_rule import KeywordRule
from app.services.rules.trusted_domain_rule import TrustedDomainRule


class FilteringEngine:
    def __init__(self):
        self.keyword_rule = KeywordRule(
            keywords={"urgent", "invoice", "password", "verify", "crypto"},
            score=30,
        )

    def _score_to_verdict(self, score: int) -> str:
        if score >= 120:
            return "reject"
        if score >= 80:
            return "quarantine"
        if score >= 40:
            return "spam"
        return "allow"

    def _build_rules(self, db: Session):
        trusted_domains = get_list_values(db, "trusted_domains")
        blocked_extensions = get_list_values(db, "blocked_extensions")
        blocked_senders = get_list_values(db, "blocked_senders")

        return [
            TrustedDomainRule(trusted_domains=trusted_domains, score=-40),
            self.keyword_rule,
            AttachmentRule(blocked_extensions=blocked_extensions, score=80),
            BlacklistRule(blocked_senders=blocked_senders, score=100),
        ]

    def evaluate(self, email, db: Session) -> FilterResponse:
        total_score = 0
        reasons: list[str] = []
        matched_rules: list[MatchedRule] = []

        for rule in self._build_rules(db):
            result = rule.evaluate(email)
            if result.matched:
                total_score += result.score_delta
                if result.reason:
                    reasons.append(result.reason)
                matched_rules.append(
                    MatchedRule(
                        rule=rule.name,
                        score_delta=result.score_delta,
                        reason=result.reason,
                    )
                )

        verdict = self._score_to_verdict(total_score)

        return FilterResponse(
            verdict=verdict,
            score=total_score,
            reasons=reasons,
            matched_rules=matched_rules,
        )
